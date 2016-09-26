
#====== Django Admin app: Views of "CRUD" ======

## To see how how django admin app works and the logic behind the views of "CRUD", we will get some idea on how we should build our own custom view of "CRUD": 

#1. model registration
- In order for your model to show up in the admin app, you have to import and register the model
- the default field used to display in the admin is the one define in the "__str__" or "__unicode__"
- in order to customize how your model show up in the admin,e.g. what fields to show on the list view,  you have to define another class for that model and define customizing fields, and register that class too!
- Note: when the model registered is "product", the django admin site will show up "prudcts", which the 's' is automatically added. So don't define model with the name of "products".

##2. BLANK vs NULL 
BLANK: 
The blank option actually doesn’t have to do with the database.  It has to do with validation of your web forms.  When blank is set to True it tells your form to allow the form to return with that field being empty.  In other words, blank=true tells django that this field is NOT required for your form to get submitted.
Another way of thinking about the blank option is to understand that since blank is set to False by default, this means that any field added to a model is going to be considered required for any web form in which django validates this field.  So you want to set blank=true when you don’t want this field to be required when validating a form.
NULL: 
The null option does concern your database.  Setting null=True is the option that tells the database to allow empty (null) values to be stored for that field.  Again, the default for this field is False, therefore, django will not allow null values for any field unless you set null equal to true.

##3. django admin app 
It has a common set of things the web application has to do: Authentication and **CRUD**
- Create
- Retrive
- Update
- Delete
    
    
#===== Make our own app: Views for each aspect of "CRUD" =====

##---- Retrive View -----

##1.. http request
- Each click of user on the web will make a http request
    
##2. URL.py
- url.py functions to recognize each url of http request and route it to a proper view function to render a web page
    - note, if you have include function to include app specific url in app folder, make sure not to use "$" sign at the end in the main url pattern.
    - the named pattern in the regular expression will be passed as a keyword argument to the view function
    
##3. view.py fucntions for controling each view of web pages. Each function/class in view.py take three argumetns and  render it and return a http response. 
- request
- html template,
- context variables

##4. Template
- template loading:
    - file system loader: define template DIR in settings.py: os.path.join(BASE_DIR,'template')
    - app directory loader:
- template tags and inheritance
    
##5. use slug field in stead of id field in the url
- add slug field in the model
- define a new patten in url with slug parameter
- in the view function to accept the slug parameter
    
##6.singal
- pre-save signal before saving to database
- define functions in model.py to automatically generate slug field, 

##---- Create View and django Form-----

##1. form 
form is the way to collect user input data from the web
    - create a form class and define form fields in form.py
    - Each instance of the form class represents each user input. 
    - Create an instance of the form class in the view.py by passing arguments:  request.POST (user post data) or None (blank form)
    
##2. Form Validation:
- whole form validation by method: is_valid(). we can directly use it in the view.py
- after validation, form data will be saved in the dict: form.cleaned_data
- specific field validation by defining and overiding instance method: clean_field() in the form.py

##3. Form Widgets:
 A widget is Django’s representation of an HTML input element. The widget handles the rendering of the HTML, and the extraction of data from a GET/POST dictionary that corresponds to the widget.
- Form Widgets vs HTML input elements
     - form.Textarea
     - form.RadioSelect
     - ...
- choices
- Form widgets attrs dict to customize vs HTML input eletments attribuites
    - class
    - placeholder
    - some-attr
- third-party app, like crispy form, to customize the form much easier

##4.Model Form: 
Just like django ModelAdmin class, take use of existing models, to display fields of the model on the admin, we have django ModelForm class that can take use of the model fields in our own view 
- just like ModelAdmin class, we just need to specify the model and the fields in a meta class to be used in the form 
- save form as an instance before saving to database can allow us to customize the instance 
    - instance = form.save(commit=False)
    - do some customization here
    - instance.save()
- you can still define regular form fields in the modleform and define form attributes. If the regular form fields name already exists in the model, it will override the model fields.
- to customize the model form fields, you can define a widget dict in the meta class for each field,
  
##---- Update View -----

##1. Update View
 The update view is similar like create view and detail view, except that we can edit the item. So in the update view, 
 - we will also need a form for updating item. What's different from create view is that we need to pass an instance of data model to the form for editing. 
 - ModelForm has a special attribute, instance, which can be used to access the model instance for updating data of the model
 
 
# =========== Class Based View (CBV) ==============

##1.CBV Overview:

 - CBV allow you to structure your views and reuse code by harnessing inheritance and mixins.
 - Django has built-in **class-based generic views**. 
    - inherit from **base classes** and different **mixins**.
    - when we build our own class based view inherited from django class-based generic views, and as such we have many hooks in the form of default **method**implementations and **attributes** that we are unlikely to be concerned with in the simplest use cases. 
    - However, we can override the default method or attribute for maximum flexibility. NOTE: after override, in the end you need to do **supercall** to return the value back to the parent class.
    
##2. Use custome Mixins for CBV: 

Mixins are a form of multiple inheritance where behaviors and attributes of multiple parent classes can be combined. Mixins are an excellent way of reusing code across multiple classes, but they come with some cost. The more your code is scattered among mixins, the harder it will be to read a child class and know what exactly it is doing. 

- **Inside Out mechnism** for more drying code: 
    Define Mixin class that contains methods that needs to be used and overrided in multiple class-base views. Separate them out in a Mixin.py files. Put the mixin class as the parent class of the class-based view. e.g. LoginRequiredMixin, MultiSlugMixin, SubmitBtnMixin etc.

##3. CBV - List View

##4. CBV - Detail View
- Unique snug

##5. CBV - Create View and update view
 
 
    
#  ====== Relating data with Foreign Keys and User Editing and Creating Permission ====

##1. Define relationship: Relate Product Model to admin user model
- product and user (one-to-many): associate product to user(product owner/creator): `user = models.ForeignKey(settings.AUTH_USER_MODEL)`
- product and managers (many-to-many): if you want to associate mulitple user to the product(e.g. allow multiple users/manager to edit items), we can create a many-to-many field:  `managers = models.ManyToMnayField(settings.AUTH_USER_MODEL)` 

## 2. Editing and creating permission
- access the user by self.request.user.
- Django uses sessions and middleware to hook the authentication system into request objects. These provide a request.user attribute on every request which represents the current user. If the current user has not logged in, this attribute will be set to an instance of AnonymousUser, otherwise it will be an instance of User.
- in the updateview override get_object() method: look for self.request.user and verified with user saved in model. If matches, then return object, if not, return 404.
- Modify the CreateView by overriding form_valid(self,form) method, because we want to add the login user(creator/owner of the product) to the database. Remember ModelForm has a special attribute, instance, which can be use to access/modify the model field.
```
user = self.request.user     
form.instance.user =user    
form.instance.managers.add(user)
```

##3. Login and staff required mixin
    
    
# ===== Statics and Media Files  =========
##1. static files

##2. media files
- media file download
    - return **httpresponse object** with no html format;
    - create a header to tell browser: Content-Disposition; X-SendFile
    - django FileWrapper for downloading big files
- product download permission

##3. ImageField


# ============ Template and view/function improvement  =======
##1. Simple Search
-  simple queryset filter using Q and order_by()
-  third party app for advance search, ref eCommence.

##2. Template improvement Tags & Filter
- give the list of content a dive class and define a CSS for it
- get_absolute_url for the product in the list in the template
- template tags and filter: eg. truncate descriptions to make it look better

##3. Tabular Inlines (like the portable table in filemaker)
- one products may have different thumnails. So make a seperate thumnail model and relate it to the products.
- first need a relation for tabular inline 
- make tabular inlines in the admin view

##4. Custome template tags
- much like a function, take an instance and variable and return new value
- register the function as template tags
- create folder called, templatetags, and __init__.py file. Put the template tag inside the folder.
- the custome tag is then available to use in the template in the format of "instance|tags: variable"

# ==================database logic and post-signal=======================

##1. Auto Generate Thumbnail
- product_post_save_receiver in the model
- create_new_thumb() function to make code more dry

# ================== Tags app ==============
 Tag products for use of recommendations, look products under the same tag ...etc
## 1. Create tag model,understand relationship and know how to query through relationship
- Create a tag model that has many to many relationship with product: 
    - one tag can be given to many different products; 
    - one products can have multiple tags
- Product and thumnail have one-to-many relationship
- Know how to query via relationships
 
##2. Create records in tag table from the product table(many-to-many relation)
- First, you need to create a tag field in the product form view(updateview and createview). This tag field can be regular form field not from the product model, just for collect user input and will be saved into tag model by querying through relations.
- Second, override the form_valid() method in the CBVs. get the tag data from cleaned_data and save them to the tag table. Note, in order for tags to be updated, clear previous values before setting new values.
```
def form_valid(self, form):
    valid_data = super(ProductUpdateView,self).form_valid(form)
    tags = form.cleaned_data.get('tags')
    obj =self.get_object()
    obj.tag_set.clear()  # clear previous values if there are, before set new values
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            new_tag = Tag.objects.get_or_create(title=str(tag).split()[0]  # add tag title to tag table by model manager
            new_tag.products.add(self.get_object())  # add product data to tag table through relations
     return valid_data
```
- In the product UpdateView, we need to get intial tag values from the tag table so that we can update the tags.
```
def get_initial(self):
    initial = super(ProductUpdateview,self).get_initial()
    tags = self.get_object().tag_set.all()
    initial['tag'] = ';'.join(x.title for x in tags)
    return initial
  
```
  
- model manager and queryset in the CBV view
    - override the get_queryset() method by returning different queryset you need

# ==============Analytics App=================
We are going to build a model for doing some analytics for the tag usage for simple recommendation purposes. As this analytic model are potential useful for doing other analytics. We separate it out as a new App.
  
##1. Create TagView model with user, tag and count fields

##2. Count tags 
in view everytime when called:
- in TagDetailView, override get_context_data() method, everytime it is called, use **get_or_create() method** of the TagView model manager to get an instance of TagView if there is or create new one, and increase count by one
-  Do the same to the product detailview
in the model:
- instead of count tags in view, we can also define a custom manager in TagView model and method to do the count. 

#========= Build a dashboard view for recommendations=========

Dashboard view can be considered as a place for landing multiple views. we need to build a seperate app for it.

##1. Create a class based DashBoardView.py from standard generic view. First, thinking about what data you want to display on the view. and then build the view class
- tags in the reverse order of counts
- products associated with those tags (main things for recommendations)
- simulate some randomness on the products recommended

##2. User Interface on the dashboard: 
- creating a **nav bar**
    - add it in the base.html, which make it to show up on every page.
    - creating a nav bar with CSS formatting
- add **suggested product list**
    - create a **product_list_snippet.html** from product list, so that it can be included into different views
    - include the product_list_snippet.htm in the dashboard view.html
- Add **top tags** into the dashboard view
- using CSS for clearing the dashboard
- logic for showing download, preview and purchase button 

##3. url template tag: {% url %}
two ways of using dynamic url in the template:
- href = "{{instance.get_absolute_url}}", need to define get_absolute_url function in the model
- href = '{% url "namespace:urlname" %}'
Note: {{request.build_absolute_uri}} could be used to build the whole url address, but not necessary, because once you build the relative link, the browser will be able to figure out the whole address.


# ====== Build Purchase Functions with jQuery UI and Ajax ====

Purchase Dialog is different from shopping cart(refer to ecommerce) 
##1. jQuery user interface(UI) library: Dialog Modal
- copy jQuery CDN and UI CDN into the base.html
- copy jQuery CSS into base.html
- add a script block right after jQuery CDN, and in the product detail view, write the block of code.
- create a confirm purchase div with style='display:none'; use the jquery to load in the dialog once the button is clicked

##2.Overview of Ajax: 
AJAX stands for Asynchronous JavaScript and XML. In a nutshell, it is the use of the XMLHttpRequest object to communicate with server-side scripts. It can send as well as receive information in a variety of formats, including JSON, XML, HTML, and even text files. AJAX’s most appealing characteristic, however, is its "asynchronous" nature, which means it can do all of this without having to refresh the page. This lets you update portions of a page based upon user events.

The two major features of AJAX allow you to do the following:

- Make requests to the server without reloading the page
- Receive and work with data from the server

##3. Setting up Ajax to make purchase function: jQuery Ajax() and django
- Create a new app, checkout
    - write CheckoutTestView using the base view from django. This is going to handle the ajax() stuff
    - create a checkout test.html template extend from base.html. Put a test Ajax link there.
    - write ajax code for the block

##4.Create a js folder in the static folder and separate the django crsf ajax javascripts out as a file and save it in the js folder


# ====== Seller App ====

## 1. Create seller app
Steps: 
    - model.py
    - view.py
    - urls.py
    - admin.py to register app
    - setting.py to add app
## 2. user apply for account
- create a regular form for agreeing to term (no need modelform to save data)
- use FormMixin for the generic base view (formveiw = baseview + formMixin ).Note that both get() and post() are both needed. 
    - get() is to display empty data. check user exists and active status and add the value to the context 
    - post() is to process data when user submit form.
    - form_valid() method