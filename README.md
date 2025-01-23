![banner](https://github.com/gabriellemosc/Ecommerce_Project/blob/main/Project%20Photos/png%20(1).png)

<h1 align="center"> Project "Reserva" Ecommerce </h1>

<span>My reference for creating the website was <a href="https://www.usereserva.com/?gad_source=1&gclid=Cj0KCQiA9667BhDoARIsANnamQYLynA7ewm7mCpcfk-0wf5uwTs3bRrLAI-t-mVEC5zaR2KSKUKTJO8aAlM7EALw_wcB">Reserva</a> 🛒 </span>

## 🚀 About

<p> This is a reference project used on a Brazilian website called <b>'Reserva'</b>. In this project, in addition to the mirrored look, I created an account management system, shopping cart, category and types of clothing, search filters by category, price, quantity sold, export of sales reports, payment system with integration with API paid market</p>

- This project was created using <b> Django a Python FrameWork</b>

:star:  If you liked it. Star me on GitHub !


![Homepage](https://github.com/gabriellemosc/Ecommerce_Project/blob/main/Project%20Photos/Captura%20de%20tela%20de%202024-12-25%2016-02-28.png)


## ✔️ Techniques and technologies used

- ``Python 3.12.3``
- ``Django``
- ``HTML``
- ``SQLite``
- ``OOP``
- ``Payment API Integration``
-  ``Virtual Enviroment``
-  ``JavaScript``


![appinterface](https://github.com/gabriellemosc/Ecommerce_Project/blob/main/Project%20Photos/Grava%C3%A7%C3%A3o%20de%20tela%20de%202024-12-25%2016-21-23.gif)


## 🛠️ Getting Started
1. **Clone the repository**  
  - Clone the repository to your local machine:

   ```bash
   git clone https://github.com/gabriellemosc/Ecommerce_Project
   ```
2. **Create and Activate the Virtual Environment**  
- To keep dependencies organized, create a Python virtual environment and activate it:
    ```bash
  python3 -m venv venv
  source venv/bin/activate  # No Windows, use 'venv\Scripts\activate'
  ```
3. **Database Config **  
- a) Modify the Database Settings in settings.py
Open the settings.py file and change the database settings for your own environment. By default, Django uses SQLite, but you can switch to another database, such as PostgreSQL or MySQL, if you prefer.:
  Exemplo para SQLite (sem alterações):
  ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
  }
  ```
- b) Create the Database and Migrations
    After configuring the database, create the necessary tables with the following commands:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. **Create a Django Superuser**
- To access the Django admin panel, you will need a superuser:
    ```bash
      python manage.py createsuperuser
      ```
Follow the instructions to set the username, email and password.

5. **Start the Local Server**
- Now run the development server to see the project running:
    ```bash
      python manage.py runserver
    ```
    
6. **Add Products,Type, Category to your store**
- Now that your application is running, acess localhost/admin, to add your products:
    ```bash
      URL: localhost/admin 
    ```


## 📸 Project Screenshots

Here are some screenshots of the  project, showing the main features and user interface.

| Shompping Cart  | Details of Product | LoginPage |
| --- | --- | --- |
| ![Sales Car](https://github.com/gabriellemosc/Ecommerce_Project/blob/main/Project%20Photos/Captura%20de%20tela%20de%202024-12-23%2019-26-23.png) | ![Product Details](https://github.com/gabriellemosc/Ecommerce_Project/blob/main/Project%20Photos/Captura%20de%20tela%20de%202024-12-22%2021-19-31.png) | ![Store](https://github.com/gabriellemosc/Ecommerce_Project/blob/main/Project%20Photos/Captura%20de%20tela%20de%202024-12-25%2014-16-46.png) |



## License

This project is licensed under the MIT License. See the file [LICENSE](./LICENSE) for more details.


- ## Author

[<img loading="lazy" src="https://github.com/gabriellemosc.png?size=115" width=115><br><sub>Gabriel Lemos</sub>](https://github.com/gabriellemosc) 


Description: Backend Developer
