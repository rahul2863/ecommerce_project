from flask import Flask, render_template, request, session, redirect,make_response, url_for
import mysql.connector
from datetime import datetime, timezone, timedelta
import datetime as dt
import random
import json

app = Flask(__name__)

app.secret_key = "vortexEcommerce"

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="ecommerce"
)

cart = []

session_timeout = 30
@app.before_request
def check_session_timeout():
    now = datetime.now(timezone.utc)  # Get the current UTC time (timezone-aware)
    if 'user_id' in session:
        if 'last_activity' in session:
            last_activity = session['last_activity'].astimezone(timezone.utc)  # Ensure both are timezone-aware

            if (now - last_activity > timedelta(minutes=30)):
                session.clear()
                return redirect(url_for('login'))

        session['last_activity'] = now

@app.route("/")
def home():
    category_id = random.randint(1,3)
    sql = "Select * from products where category_id = %s"
    value = (category_id,)
    cursor = con.cursor()
    cursor.execute(sql,value)
    products = cursor.fetchall()
    random.shuffle(products)
    try:
        if 'uname' in session and session['uname'] == "admin@gmail.com":
            return render_template("homePage.html", title="Ecommerce", name = request.args['name'], products = products)
        else:
            if request.args["number_of_cart_items"]:
                return render_template("homePage.html", title="Ecommerce", products=products,number_of_cart_items=request.args["number_of_cart_items"])
            else:
                return render_template("homePage.html", title="Ecommerce", products = products)
    except:
        return render_template("homePage.html", title="Ecommerce", products = products)


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about-me")
def about():    
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():    
    if request.method == "GET":
        try:
            if request.cookies:
                return render_template("login.html",title="Sign In",email=request.cookies['email'], password = request.cookies['password'])
            else:
                return render_template("login.html",title="Sign In")
        except:
            return render_template("login.html",title="Sign In")
        
    else:
        email = request.form["email"]
        password = request.form["password"]

        #Validate user from the database
        sql = "Select * from users;"
        cursor = con.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        
        for record in records:
            if email in record and password in record:
                name = record[3]
                session["uname"] = email
                session["user_id"] = record[0]

                if 'remember-me' in request.form:
                    resp = make_response(redirect(f"/?name={name}"))
                    resp.set_cookie("email",email,expires=dt.datetime.now()+dt.timedelta(days=1))
                    resp.set_cookie("password",password,expires=dt.datetime.now()+dt.timedelta(days=1))
                    return resp
                else:
                    return redirect(f"/?name={name}")
        else:
            return render_template("login.html",status="Failed")
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():    
    if request.method == "GET":
        return render_template("register.html",title="Register")
    else:
        #Store into database
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]
       
        try:
            sql = "Insert into users(email,password,name,mobile) values(%s,%s,%s,%s)"
            values = (email, password, name, mobile)
            cursor = con.cursor()
            cursor.execute(sql,values)
            con.commit() #DML commands needs a commit
            return render_template("register.html",status="Success",title="Register")
            # return f"Name: {name}, Email: {email}, Mobile: {mobile}, Password: {password}"
        except:
            return render_template("register.html",status="Failed",title="Register")
           

@app.route("/settings")
def settings():
    return f"Settings Page"

@app.route("/update_profile",methods=['GET','POST'])
def updateProfile():
    if request.method=='GET':
        cursor = con.cursor()
        sql = "select * from users where id = %s"
        values = (session['user_id'],)
        cursor.execute(sql,values)
        user = cursor.fetchone()
        return render_template("updateProfile.html",user=user)
    else:
        new_name = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('confirm_password')
        cursor = con.cursor()
        sql = "update users set name=%s,email=%s,password=%s where id=%s"
        values = (new_name,email,new_password,session['user_id'])
        cursor.execute(sql,values)
        con.commit()

        sql = "select * from users where id = %s"
        values = (session['user_id'],)
        cursor.execute(sql,values)
        user = cursor.fetchone()

        return render_template('updateProfile.html',user=user,message = 'Profile update Successfull')

@app.route("/profile")
def profile():
    return render_template("profile_page.html")

@app.route("/admin-page")
def adminPage():
    if "uname" in session:
        if session['uname'] == "admin@gmail.com":
            return render_template("AdminPage.html")
        else:
            return render_template("404_page.html", title="404 - Page Not Found")
    else:
        return render_template("404_page.html", title="404 - Page Not Found")


@app.route("/detail_category")
def detailCategory():
    category_id = request.args["id"]
    sql = "Select * from products where category_id = %s"
    value = (category_id,)
    cursor = con.cursor()
    cursor.execute(sql, value)
    products = cursor.fetchall()
    return render_template("detail_category.html", products=products)


@app.route("/view_customers")
def viewCustomers():
    sql = "select id,email,name,mobile,joining_date from users"
    cursor = con.cursor()
    cursor.execute(sql)
    customers = cursor.fetchall()
    return render_template("viewCustomers.html", customers=customers)

@app.route("/view_products")
def viewProducts():
    sql = "select pid,media,name,date_added,price,category_id,stock_quantity from products order by category_id"
    cursor = con.cursor()
    cursor.execute(sql)
    products = cursor.fetchall()
    return render_template("viewProducts.html", products=products)

@app.route("/addProduct",methods=["GET","POST"])
def addProducts():
    if request.method=="GET":
        return render_template("addProducts.html")
    else:
        name = request.form["product_name"]
        description = request.form["description"]
        price = request.form["price"]
        stocks = request.form["stock"]
        media = request.form["media"]
        category = request.form["category"].lower()
        if category == "watch":
            category = 1
        elif category == "shoes":
            category = 2
        elif category == "clothes":
            category = 3
        else:
            return render_template("addProducts.html", warning = "Enter Valid Category")
        
        sql = "Insert into products(name,description,price,stock_quantity,category_id,media) values(%s,%s,%s,%s,%s,%s)"
        values = (name, description, price, stocks, category, media)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()
        return redirect("/admin-page")

@app.route('/delete_customer')
def deleteCustomer():
    sid = request.args['sid']
    sql = "delete from users where id=%s"
    value = (sid,)
    cursor = con.cursor()
    cursor.execute(sql,value)
    con.commit()
    return redirect(request.referrer)

@app.route('/deleteProduct')
def deleteProduct():
    pid = request.args['pid']
    sql = "delete from products where pid=%s"
    value = (pid,)
    cursor = con.cursor()
    cursor.execute(sql,value)
    con.commit()
    return redirect(request.referrer)


@app.route('/editProduct',methods=['GET','POST'])
def editProduct():
    if request.method=='GET':
        pid = request.args['pid']
        cursor = con.cursor()
        sql = "select * from products where pid = %s"
        values = (pid,)
        cursor.execute(sql,values)
        product = cursor.fetchone()
        # return f"{product}"
        return render_template("updateProduct.html",product=product)
    else:
        pid = request.form.get('pid')
        product_name = request.form.get('product_name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category')
        stock = request.form.get('stock')
        media = request.form.get('media')
        cursor = con.cursor()
        sql = "update products set name=%s,description=%s,price=%s,category_id=%s,stock_quantity=%s,media=%s where pid=%s"
        values = (product_name,description,price,category_id,stock,media,pid,)
        cursor.execute(sql,values)
        con.commit()

        sql = "select pid,media,name,date_added,price,category_id,stock_quantity from products order by category_id"
        cursor = con.cursor()
        cursor.execute(sql)
        products = cursor.fetchall()
        return render_template("viewProducts.html", products=products)

@app.route('/admin_orders')
def adminOrders():
    sql = " select media,order_id, users.name, users.email,products.name, products.price, orders.status from orders inner join products on orders.pid = products.pid inner join users on orders.user_id = users.id;"
    cursor = con.cursor()
    cursor.execute(sql) 
    orders = cursor.fetchall()
    return render_template("adminOrders.html",orders = orders)

@app.route('/updateOrderStatus', methods = ['GET', 'POST'])
def updateOrderStatus():
    if request.method == 'GET':
       order_id = request.args['order_id']
       return render_template('updateOrderStatus.html',order_id = order_id)
    else:
        order_id = request.form['order_id']
        status = request.form['status']
        sql = "update orders set status = %s where order_id = %s"
        values = (status,order_id)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()
        return redirect('/admin_orders')
       

@app.route("/add_to_cart")
def addToCart():
    if "user_id" in session:
        user_id = session["user_id"]
        pid = request.args["pid"]
        sql = "insert into cart(user_id,product_id) values(%s,%s)"
        values = (user_id,pid)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()

        sql = "select * from cart where user_id=%s"
        cursor = con.cursor()
        values = (user_id,)
        cursor.execute(sql,values)
        cart_items = cursor.fetchall()

        cart=[]
        for item in cart_items:
            cart.append(item[2])

        #Calculate the total_quantity
        quantity = 0
        for items in cart_items:
            quantity = quantity + items[3]
        
        #serializing cart bcoz cookies stores data in string format only
        cart = json.dumps(cart)

        #Setting cart_count
        session["cart_count"] = quantity
        resp = make_response(redirect(request.referrer))
        resp.set_cookie("cart_items",cart,expires=dt.datetime.now()+dt.timedelta(days=1))
        resp.set_cookie("cart_count",str(session["cart_count"]),expires=dt.datetime.now()+dt.timedelta(days=1))
        return resp
    
    else:
        return redirect("/login")


@app.route("/viewCart")
def viewCart():
    if "user_id" in session:
        user_id = session["user_id"]
        sql = "select * from cart where user_id=%s"
        values = (user_id,)
        cursor = con.cursor()
        cursor.execute(sql, values)
        cart_items = cursor.fetchall()
        products = []
        for item in cart_items:
            sql = "Select * from products where pid = %s"
            value = (item[2],)
            cursor = con.cursor()
            cursor.execute(sql, value)
            products.append(cursor.fetchone())

        set_products = set(products)
        # return f"{set_products}"
        return render_template("viewCart.html",products=products,set_products=set_products)
    else:
        return redirect("/login")

@app.route("/removeFromCart",methods=["POST","GET"])
def removeFromCart():

    if "user_id" in session:
        user_id = session["user_id"]
        pid = request.args["pid"]
        sql = "delete from cart where user_id = %s and product_id = %s"
        values = (user_id,pid)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()


        sql = "select * from cart where user_id=%s"
        cursor = con.cursor()
        values = (user_id,)
        cursor.execute(sql,values)
        cart_items = cursor.fetchall()

        #Calculate the total_quantity
        quantity = 0
        for items in cart_items:
            quantity = quantity + items[3]

        #Setting cart_count
        session["cart_count"] = quantity
        resp = make_response(redirect(request.referrer))
        if request.cookies.get('cart_count'):
            resp.set_cookie("cart_count",str(session["cart_count"]),expires=dt.datetime.now()+dt.timedelta(days=1))
        return resp
    
    else:
        return redirect("/login")



@app.route("/productDetails")
def productDetails():
    if 'user_id' in session:
        pid = request.args['pid']
        sql = "select * from products where pid=%s"
        values = (pid,)
        cursor = con.cursor()
        cursor.execute(sql, values)
        product = cursor.fetchone()
        return render_template("productDetails.html",product=product)
    else:
        return redirect("/login")


@app.route("/add_to_fav")
def addToFav():

    if "user_id" in session:
        user_id = session["user_id"]
        pid = request.args["pid"]

        sql = "insert into favourites(user_id, pid) values(%s,%s)"
        values = (user_id,pid)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()

        sql = "select distinct pid from favourites where user_id=%s"
        cursor = con.cursor()
        values = (user_id,)
        cursor.execute(sql,values)
        #Count only unique vals
        fav_items = set(cursor.fetchall())
        
        #Setting fav_count
        session["fav_count"] = len(fav_items)
        resp = make_response(redirect(request.referrer))
        resp.set_cookie("fav_count",str(session["fav_count"]),expires=dt.datetime.now()+dt.timedelta(days=1))
        return resp  
    else:
        return redirect("/login")
    

@app.route("/viewFav")
def viewFav():

    if "user_id" in session:
        user_id = session["user_id"]
        sql = "select * from favourites where user_id=%s"
        values = (user_id,)
        cursor = con.cursor()
        cursor.execute(sql, values)
        fav_items = cursor.fetchall()
        products = []
        for item in fav_items:
            sql = "Select * from products where pid = %s"
            value = (item[2],)
            cursor = con.cursor()
            cursor.execute(sql, value)
            products.append(cursor.fetchone())

        set_products = set(products)
        return render_template("viewFav.html",products=products,set_products=set_products)
    else:
        return redirect("/login")
    

@app.route("/removeFromFav",methods=["POST"])
def removeFromFav():

    if "user_id" in session:
        user_id = session["user_id"]
        pid = request.form["product_id"]
        sql = "delete from favourites where user_id = %s and pid = %s"
        values = (user_id,pid)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()

        sql = "select * from favourites where user_id=%s"
        cursor = con.cursor()
        values = (user_id,)
        cursor.execute(sql,values)
        fav_items = cursor.fetchall()

       #Setting cart_count
        session["fav_count"] = len(fav_items)
        resp = make_response(redirect(request.referrer))
        if request.cookies.get('fav_count'):
            resp.set_cookie("fav_count",str(session["fav_count"]),expires=dt.datetime.now()+dt.timedelta(days=1))
        return resp
    
    else:
        return redirect("/login")
    

@app.route("/buy_product",methods=["GET","POST"])
def buyProduct():
    if request.method == "GET":
        pid = request.args["pid"]
        price = request.args['price']
        user_id = session["user_id"]
        quantity = request.args["quantity"]
        session["total_price"] = float(price) * float(quantity)

        sql = "select pid,name,price,description,stock_quantity,media from products where pid =%s"
        cursor = con.cursor()
        values = (pid,)
        cursor.execute(sql,values)
        cart_items = cursor.fetchall()

        cart_items2 = []
            # Extract quantity for each product based on the product ID
        for item in cart_items:
            item = list(item)
            product_id = str(item[0])  # The product ID
            item.append(int(quantity))
            cart_items2.append(tuple(item))

        session['quantities'] = quantity
        session['cart_items2'] = cart_items2
        resp = make_response(render_template("checkout.html", buy_type='cart_items', cart_items=cart_items2, quantities=quantity))
        resp.set_cookie("quantities",json.dumps(quantity),expires=dt.datetime.now()+dt.timedelta(days=1))
        return resp
    
    else:
        user_id = session["user_id"]
        # Get total price from the form
        total_price = float(request.form["total_price"])
        session["total_price"] = total_price

        # List to store cart item IDs and their quantities
        cart_item_ids = []
        quantities = []

        # Fetch cart items for the user
        sql = """
            SELECT pid, name, price, description, stock_quantity, media 
            FROM products 
            WHERE pid IN (
                SELECT product_id 
                FROM cart 
                WHERE user_id=%s
            );
        """
        cursor = con.cursor()
        values = (user_id,)
        cursor.execute(sql, values)
        cart_items = cursor.fetchall()

        cart_items2 = []
        # Extract quantity for each product based on the product ID
        for item in cart_items:
            item = list(item)
            product_id = str(item[0])  # The product ID
            quantity = request.form[f'quantity_'+product_id]  # Fetch quantity from the form
            cart_item_ids.append(item[0])
            quantities.append(quantity)
            item.append(int(quantity))
            cart_items2.append(tuple(item))
        
        session['quantities'] = quantities
        session['cart_items2'] = cart_items2
        resp = make_response(render_template("checkout.html", buy_type='cart_items', cart_items=cart_items2, cart_item_ids=cart_item_ids, quantities=quantities))
        resp.set_cookie("quantities",json.dumps(quantities),expires=dt.datetime.now()+dt.timedelta(days=1))
        return resp


@app.route("/process_payment",methods=["POST"])
def processPayment():

    # if request.form['buy_type'] == 'cart_items':
    total_amount = session["total_price"]+10
    user_id = session["user_id"]
    cart = session['cart_items2']
    for item in cart:
        pid = item[0]
        quantity = item[6]
        sql = "insert into orders(user_id,total_amount,pid,quantity) values(%s,%s,%s,%s)"
        values = (user_id,total_amount,pid,quantity)
        cursor = con.cursor()
        cursor.execute(sql,values)
        con.commit()


    #Empty the cart
    sql = "truncate cart"
    cursor = con.cursor()
    cursor.execute(sql)

    #Setting cart_count
    session["cart_count"] = 0
    resp = make_response(render_template('order_success.html'))
    if request.cookies.get('cart_count'):
        resp.set_cookie("cart_count",str(session["cart_count"]),expires=dt.datetime.now()+dt.timedelta(days=1))
    return resp
    
    # else:
    #     pid = request.form['pid']
    #     total_amount = session["total_price"] + 10
    #     user_id = session["user_id"]
    #     sql = "insert into orders(user_id,total_amount,pid) values(%s,%s,%s)"
    #     values = (user_id,total_amount,pid)
    #     cursor = con.cursor()
    #     cursor.execute(sql,values)
    #     con.commit()
    #     return render_template('order_success.html')

@app.route("/order_details", methods=["GET"])
def orderDetails():
    if "user_id" not in session:
        return redirect("/login")
    else:
        sql = "select distinct orders.pid,products.name,price,media,order_date,status,orders.quantity from products inner join orders on products.pid = orders.pid inner join users where orders.user_id = %s;"
        values = (session['user_id'],)
        cursor = con.cursor()
        cursor.execute(sql,values)
        orders = cursor.fetchall()

        return render_template("order_details.html", orders=orders)

@app.route("/delete_order", methods=["GET"])
def orderDelete():
    sql = "delete from orders where order_id = %s;"
    values = (request.args['order_id'],)
    cursor = con.cursor()
    cursor.execute(sql,values)
    con.commit()
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(debug=True)
