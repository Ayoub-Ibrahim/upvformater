===================
upvformat-converter
===================

django-convert is a Django app to convert UPV markup language format to Moodle format.

------------
Installation
------------

1. Install using pip:

   pip install django-convert

2. Add "convert" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
       ...
       'convert',
   ]

3. Include the convert URLconf in your project urls.py like this::

   path('convert/', include('convert.urls')),

4. Run `python manage.py migrate` to create the convert models.

5. Start the development server and visit http://127.0.0.1:8000/admin/ to use the app.
