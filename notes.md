1. model registration
    - In order for your model to show up in the admin app, you have to import and register the model
    - the default field used to display in the admin is the one define in the "__str__" or "__unicode__"
    - in order to customize how your model show up in the admin,e.g. what fields to show on the list view,  you have to define another class for that model and define customizing fields, and register that class too!
    - Note: when the model registered is "product", the django admin site will show up "prudcts", which the 's' is automatically added. So don't define model with the name of "products".
    
2. BLANK vs NULL 
BLANK

The blank option actually doesn’t have to do with the database.  It has to do with validation of your web forms.  When blank is set to True it tells your form to allow the form to return with that field being empty.  In other words, blank=true tells django that this field is NOT required for your form to get submitted.

Another way of thinking about the blank option is to understand that since blank is set to False by default, this means that any field added to a model is going to be considered required for any web form in which django validates this field.  So you want to set blank=true when you don’t want this field to be required when validating a form.

NULL

The null option does concern your database.  Setting null=True is the option that tells the database to allow empty (null) values to be stored for that field.  Again, the default for this field is False, therefore, django will not allow null values for any field unless you set null equal to true.

3. django admin app 
   It has a common set of things the web application has to do: Authentication and CRUD