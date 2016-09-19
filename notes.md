
#====== Django Admin app: Views of "CRUD" ======


#1. model registration
- In order for your model to show up in the admin app, you have to import and register the model
- the default field used to display in the admin is the one define in the "__str__" or "__unicode__"
- in order to customize how your model show up in the admin,e.g. what fields to show on the list view,  you have to define another class for that model and define customizing fields, and register that class too!
- Note: when the model registered is "product", the django admin site will show up "prudcts", which the 's' is automatically added. So don't define model with the name of "products".
    
#2. BLANK vs NULL 
BLANK

The blank option actually doesn’t have to do with the database.  It has to do with validation of your web forms.  When blank is set to True it tells your form to allow the form to return with that field being empty.  In other words, blank=true tells django that this field is NOT required for your form to get submitted.

Another way of thinking about the blank option is to understand that since blank is set to False by default, this means that any field added to a model is going to be considered required for any web form in which django validates this field.  So you want to set blank=true when you don’t want this field to be required when validating a form.

NULL

The null option does concern your database.  Setting null=True is the option that tells the database to allow empty (null) values to be stored for that field.  Again, the default for this field is False, therefore, django will not allow null values for any field unless you set null equal to true.

#3. django admin app 
It has a common set of things the web application has to do: Authentication and **CRUD**
- Create
- Retrive
- Update
- Delete
    
#===== Make our own app: Views for each aspect of "CRUD" =====

#---- Retrive View -----

#4. http request
- Each click of user on the web will make a http request
    
#5. URL.py
- url.py functions to recognize each url of http request and route it to a proper view function to render a web page
    - note, if you have include function to include app specific url in app folder, make sure not to use "$" sign at the end in the main url pattern.
    - the named pattern in the regular expression will be passed as a keyword argument to the view function
    
#6. view.py fucntions for controling each view of web pages. Each function/class in view.py take three argumetns and  render it and return a http response. 
- request
- html template,
- context variables
#7. Template
- template loading:
    - file system loader: define template DIR in settings.py: os.path.join(BASE_DIR,'template')
    - app directory loader:
- template tags and inheritance
    
#8. use slug field in stead of id field in the url
- add slug field in the model
- define a new patten in url with slug parameter
- in the view function to accept the slug parameter
    
#9. singal
- pre-save signal before saving to database
- define functions in model.py to automatically generate slug field, 

#---- Create View -----

#10. form 
form is the way to collect user input data from the web
    - create a form class and define form fields in form.py
    - Each instance of the form class represents each user input. 
    - Create an instance of the form class in the view.py by passing arguments:  request.POST (user post data) or None (blank form)
    
#11. Form Validation:
- whole form validation by method: is_valid(). we can directly use it in the view.py
- after validation, form data will be saved in the dict: form.cleaned_data
- specific field validation by defining and overiding instance method: clean_field() in the form.py

#12. Form Widgets:
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

# 13.Model Form: 
Just like django ModelAdmin class, take use of existing models, to display fields of the model on the admin, we have django ModelForm class that can take use of the model fields in our own view 
- just like ModelAdmin class, we just need to specify the model and the fields in a meta class to be used in the form 
- save form as an instance before saving to database can allow us to customize the instance 
    instance = form.save(commit=False)
    ##### do some customization here
    instance.save()
- you can still define regular form fields in the modleform and define form attributes. If the regular form fields name already exists in the model, it will override the model fields.
- to customize the model form fields, you can define a widget dict in the meta class for each field,
 
 
#---- Update View -----
 The update view is similar like create view and detail view, except that we can edit the item. So in the update view, 
 - we will also need a form for updating item. What's different from create view is that we need to pass an instance of data model to the form for editing. 
 
 
# =========== Class Based View (CBV) ==============
 # 14 . CBV Overview:
 - CBV allow you to structure your views and reuse code by harnessing inheritance and mixins.
 - Django has built-in **class-based generic views**. 
    - inherit from **base classes** and different **mixins**.
    - when we build our own class based view inherited from django class-based generic views, and as such we have many hooks in the form of default **method**implementations and **attributes** that we are unlikely to be concerned with in the simplest use cases. 
    - However, we can override the default method or attribute for maximum flexibility.
 - Use custome Mixins: 
    - Mixins are a form of multiple inheritance where behaviors and attributes of multiple parent classes can be combined. 
    - Mixins are an excellent way of reusing code across multiple classes, but they come with some cost. The more your code is scattered among mixins, the harder it will be to read a child class and know what exactly it is doing. 
    
# 15. Relating data with Foreign Keys
- Type of Relationship:
    - One-to-One
    - One-to-Many (ForeignKey)
    - Many-to-Many
- Define relationship: Relate Product Model to admin user model
    - product and user (one-to-many)
    - product and managers (many-to-many)
- Applications of the relationship:
    - Editing and creating permission
    - Login and staff required mixin
 
 