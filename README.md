Phimart - E-commerce API
Phimart is a RESTful e-commerce API built using Django REST Framework (DRF). It provides endpoints for managing products, categories, orders, and carts. The project also implements JWT authentication using Djoser and includes API documentation with Swagger.

Features
Product and category management
Cart and order functionality
JWT authentication using Djoser
API documentation using Swagger (drf_yasg)
Technologies Used
Django - Backend framework
Django REST Framework (DRF) - API development
Djoser - Authentication
Simple JWT - JWT authentication
drf-yasg - API documentation (Swagger)
PostgreSQL (or SQLite) - Database
Installation
Clone the repository:

git clone https://github.com/yourusername/phimart.git
cd phimart
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

pip install -r requirements.txt
Apply migrations:

python manage.py migrate
Create a superuser:

python manage.py createsuperuser
Run the development server:

python manage.py runserver
```    |
API Documentation
Swagger documentation is available at:

http://127.0.0.1:8000/swagger/
ReDoc documentation is available at:

http://127.0.0.1:8000/redoc/
Environment Variables
Create a .env file in the root directory and add the following:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=*
EMIL_HOST=your_email_host
License
This project is licensed under the MIT License.

Author
Your Name