# blackcart
# How to use
1- Add your woocomerce API and shopify API credentials to ``PLATFORMS_API_SETTINGS`` in global settings files

2- Make sure you have ``python3`` and ``virtualenv`` packages installed

3- browse to ``blackcart`` folder and navigate to ``venv`` folder

4- start the virtual environment by running ``source bin/activate``

5- run server by running: `python manage.py runserver`

6- Create Stores using the stores table created in SQLITE DATABASE using django admin ``http://127.0.0.1:8000/admin``
  6.a - Django admin credentials: username: admin | password: 12345
  
7- Run the following endpoint in the browser url to import product from the store ``<localhost_url>/store/<store id>/products/``
  7.a- <localhost> will be the url given to your when you ran the server in step 5
  7.b- <store id> will be the store id you created in the database in step 6
  7.c- url example ``http://127.0.0.1:8000/store/1561651/products/``
