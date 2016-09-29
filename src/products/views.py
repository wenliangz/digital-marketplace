import os

from mimetypes import guess_type

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

# Create your views here.
from analytics.models import TagView
from digitalmarket.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin, 
			SubmitBtnMixin,
			AjaxRequiredMixin
			)

from sellers.models import SellerAccount
from sellers.mixins import SellerAccountMixin
from tags.models import Tag

from .forms import ProductAddForm, ProductModelForm
from .mixins import ProductManagerMixin
from .models import Product, ProductRating, MyProducts



class ProductRatingAjaxView(AjaxRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return JsonResponse({}, status=401)
		# credit card required ** 
		
		user = request.user
		product_id = request.POST.get("product_id")
		rating_value = request.POST.get("rating_value")
		exists = Product.objects.filter(id=product_id).exists()
		if not exists:
			return JsonResponse({}, status=404)

		try:
			product_obj = Product.object.get(id=product_id)
		except:
			product_obj = Product.objects.filter(id=product_id).first()

		rating_obj, rating_obj_created = ProductRating.objects.get_or_create(
				user=user, 
				product=product_obj
				)
		try:
			rating_obj = ProductRating.objects.get(user=user, product=product_obj)
		except ProductRating.MultipleObjectsReturned:
			rating_obj = ProductRating.objects.filter(user=user, product=product_obj).first()
		except:
			#rating_obj = ProductRating.objects.create(user=user, product=product_obj)
			rating_obj = ProductRating()
			rating_obj.user = user
			rating_obj.product = product_obj
		rating_obj.rating = int(rating_value)
		myproducts = user.myproducts.products.all()

		if product_obj in myproducts:
			rating_obj.verified = True
		# verify ownership
		rating_obj.save()

		data = {
			"success": True
		}
		return JsonResponse(data)




class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Add Product"

	def form_valid(self, form):
		seller = self.get_account()
		form.instance.seller = seller
		valid_data = super(ProductCreateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		if tags:
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(form.instance)
		return valid_data


class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Update Product"

	def get_initial(self):
		initial = super(ProductUpdateView,self).get_initial()
		print initial
		tags = self.get_object().tag_set.all()
		initial["tags"] = ", ".join([x.title for x in tags])
		"""
		tag_list = []
		for x in tags:
			tag_list.append(x.title)
		"""
		return initial

	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			tags_list = tags.split(",")
			
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(self.get_object())
		return valid_data




class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		tags = obj.tag_set.all()
		rating_avg = obj.productrating_set.aggregate(Avg("rating"), Count("rating"))
		context["rating_avg"] = rating_avg
		if self.request.user.is_authenticated():
			rating_obj = ProductRating.objects.filter(user=self.request.user, product=obj)
			if rating_obj.exists():
				context['my_rating'] = rating_obj.first().rating
			for tag in tags:
				new_view = TagView.objects.add_count(self.request.user, tag)
		return context


class ProductDownloadView(MultiSlugMixin, DetailView):
	model = Product

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if not request.user.is_authenticated():
			raise Http404
		if obj in request.user.myproducts.products.all():
			filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
			guessed_type = guess_type(filepath)[0]
			wrapper = FileWrapper(file(filepath))
			mimetype = 'application/force-download'
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)
			
			if not request.GET.get("preview"):
				response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)
			
			response["X-SendFile"] = str(obj.media.name)
			return response
		else:
			raise Http404



class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "sellers/product_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(seller=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs




class VendorListView(ListView):
	model = Product
	template_name = "products/product_list.html"

	def get_object(self):
		username= self.kwargs.get("vendor_name")
		seller = get_object_or_404(SellerAccount, user__username=username)
		return seller

	def get_context_data(self, *args, **kwargs):
		context = super(VendorListView, self).get_context_data(*args, **kwargs)
		context["vendor_name"] = str(self.get_object().user.username)
		return context

	def get_queryset(self, *args, **kwargs):
		seller = self.get_object()
		qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs



class ProductListView(ListView):
	model = Product

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs


class UserLibraryListView(LoginRequiredMixin, ListView):
	model = MyProducts
	template_name = "products/library_list.html"

	def get_queryset(self, *args, **kwargs):
		obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
		qs = obj.products.all()
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs




def create_view(request): 
	form = ProductModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		print form.cleaned_data.get("publish")
		instance = form.save(commit=False)
		instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
			"form": form,
			"submit_btn": "Create Product"
		}
	return render(request, template, context)


def update_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	form = ProductModelForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		#instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
		"object": product,
		"form": form,
		"submit_btn": "Update Product"
		}
	return render(request, template, context)



def detail_slug_view(request, slug=None):
	product = Product.objects.get(slug=slug)
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()
	# print slug
	# product = 1
	template = "detail_view.html"
	context = {
		"object": product
		}
	return render(request, template, context)


def detail_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	template = "detail_view.html"
	context = {
		"object": product
		}
	return render(request, template, context)

	# if object_id is not None:
	# 	product = get_object_or_404(Product, id=object_id)
	# 	# product = Product.objects.get(id=object_id)
	# 	# try:
	# 	# 	product = Product.objects.get(id=object_id)
	# 	# except Product.DoesNotExist:
	# 	# 	product = None

		
	# else:
	# 	raise Http404


def list_view(request):
	# list of items
	print request
	queryset = Product.objects.all()
	template = "list_view.html"
	context = {
		"queryset": queryset
	}
	return render(request, template, context)




