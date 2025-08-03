# Ameaozon - Pet Shop E-commerce Platform

![Ameaozon Logo](static/images/logo2.png)

A comprehensive e-commerce platform designed for pet shops, built with Django. Ameaozon offers a complete solution for managing pet products, customer orders, and inventory.

## Features

### Customer Features
- User registration and authentication
- Browse products by categories and subcategories
- Advanced product search functionality
- Product reviews and ratings system
- Wishlist management
- Shopping cart functionality
- Order placement and tracking
- Multiple payment options (Cash on Delivery, bKash, Nagad, Rocket, Card)

### Admin Features
- Comprehensive admin dashboard
- Product management (add, edit, delete)
- Category and subcategory management
- Order processing and status updates
- Stock management
- Carousel management for homepage
- User management

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository
```bash
git clone https://github.com/RahatGithub/ameaozon-local.git
cd ameaozon-local
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your_secret_key
DEBUG=True
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

5. Run migrations
```bash
python manage.py migrate
```

6. Set up initial data
```bash
python manage.py setup_initial_data
python manage.py setup_demo_products
```

7. Create a superuser
```bash
python manage.py createsuperuser
```

8. Run the development server
```bash
python manage.py runserver
```

9. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

```
ameaozon/
├── accounts/            # User authentication and profiles
├── dashboard/           # Admin dashboard functionality
├── media/               # User-uploaded files (development only)
├── orders/              # Order processing and cart functionality
├── payment/             # Payment processing
├── static/              # Static files (CSS, JS, images)
├── store/               # Main store functionality, products, categories
├── templates/           # HTML templates
├── ameaozon/            # Project settings
├── manage.py            # Django management script
├── requirements.txt     # Project dependencies
└── README.md            # This file
```

## Screenshots

### Home Page
![Home Page](https://via.placeholder.com/800x400?text=Home+Page)

### Product Listing
![Product Listing](https://via.placeholder.com/800x400?text=Product+Listing)

### Product Detail
![Product Detail](https://via.placeholder.com/800x400?text=Product+Detail)

### Shopping Cart
![Shopping Cart](https://via.placeholder.com/800x400?text=Shopping+Cart)

### Admin Dashboard
![Admin Dashboard](https://via.placeholder.com/800x400?text=Admin+Dashboard)

## Usage

### Customer Use
1. Browse products by navigating categories or using the search function
2. Add products to your cart or wishlist
3. Proceed to checkout when ready to purchase
4. Fill in shipping and payment details
5. Complete the order and receive a tracking number
6. Track your order status using the tracking number

### Admin Use
1. Log in with admin credentials
2. Access the admin dashboard
3. Manage products, categories, and orders
4. Update order statuses as they progress
5. Monitor inventory levels
6. Manage carousel images for the homepage



---

Developed with ❤️ for pet lovers everywhere.