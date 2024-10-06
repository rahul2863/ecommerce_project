# Vortex E-commerce Website

An eCommerce platform built using Flask, MySQL, JavaScript, HTML, and CSS, allowing users to shop across various categories, manage their profiles, and track orders while giving admin control over product listings, user management, and order status updates.
## Features

- **User Authentication**: Register, log in, and log out.
- **Product Browsing**: Navigate through product categories like Shoes, Watches, and Clothes.
- **Shopping Cart & Wishlist**: Add items to the cart or mark them as favorites.
- **Order Management**: Place orders and view order history.
- **Profile Management**: Update and manage profile details.
- **Sessions and Cookies**: Used for login status, cart items, and favorites.

### Admin Functionalities

- **User Management**: View all registered users.
- **Product Management**: View, add, and update product listings.
- **Order Management**: View all orders and update their statuses (Pending, Shipped, Delivered).


### Technologies Used
- **Backend**: Flask.
- **Database**: MySQL.
- **Frontend**: HTML, CSS, JavaScript.
- **Session Management**: Flask sessions and cookies

## Installation
#### 1. Clone the repository:
```bash
git clone https://github.com/rahul2863/ecommerce_project.git
```
#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```
#### 3. Database Setup
- Run the SQL scripts provided in the ecommerce_sql.sql file to set up the required tables.
#### 4. Run the Application:
```bash
python app.py
```
#### 4. Access the Application:
- Open a browser and go to http://127.0.0.1:5000


## Usage
### User Guide
 1. Register and log in to access the site.
 2. Browse through product categories and add desired items to the cart or favorites.
 3. Place orders through the cart and check the order status in your profile.
 4. Update profile details as needed.

### Admin Guide
 1. Access the admin panel to manage users, products, and orders.
 2. Update the order status, with real-time updates reflected on the user’s order history.

### Future Enhancements
- Payment Gateway Integration
- Enhanced Filtering and Sorting for Products
- Product Recommendations Based on User History

## Contributing
Contributions are welcome! Feel free to submit a pull request for bug fixes, improvements, or new features.

## License

[MIT](https://choosealicense.com/licenses/mit/)
