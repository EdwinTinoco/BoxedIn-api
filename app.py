from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_heroku import Heroku


app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b2d18267c8be21'
app.config['MYSQL_PASSWORD'] = '4f896c41'
app.config['MYSQL_DB'] = 'heroku_6db9d1407cd6160'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



mysql = MySQL(app)

@app.route('/', methods=["GET"])
def home():    
    return "<h1>BoxedIn home</h1>"


# Enpoints for Products table------------------------------------------------------------------------
# POST
@app.route('/add-product', methods=['POST'])
def add_product():   
      products_name = request.json['products_name']
      products_description = request.json['products_description']
      products_inventory = request.json['products_inventory']
      products_image_url = request.json['products_image_url']
      products_categories = request.json['products_categories']
      products_stars = request.json['products_stars']
      products_price = request.json['products_price']

      cur = mysql.connection.cursor()

      cur.callproc("spInsertaNewProduct",
      [products_name, products_description, products_inventory, products_image_url, products_categories, products_stars, products_price])

      mysql.connection.commit()
      cur.close()

      return jsonify('Product inserted successfully')

# GET ALL
@app.route('/products', methods=["GET"])
def get_products():    
   cur = mysql.connection.cursor()

   cur.callproc("spGetAllProducts", ())
   all_products = cur.fetchall()

   cur.close()

   return jsonify(all_products)

# GET ONE
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
   cur = mysql.connection.cursor()

   cur.callproc("spGetProdById", [id])
   product = cur.fetchall()

   cur.close()

   if product:
      return jsonify(product)
   else:
      return jsonify("That product doesnt exist")  

# PATCH
@app.route('/product/<id>', methods=['PATCH'])
def update_product(id):
   products_inventory = request.json['products_inventory']
   products_stars = request.json['products_stars']
   products_price = request.json['products_price']

   cur = mysql.connection.cursor()

   cur.callproc("spUpdateProductById", [id, products_inventory, products_stars, products_price])

   mysql.connection.commit()
   cur.close()

   return jsonify('Product updated successfully')

# DELETE
@app.route('/delete-product/<id>', methods=['DELETE'])
def delete_product(id):
   cur = mysql.connection.cursor()

   cur.callproc("spDeleteProductById", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('Product deleted')


# Endpoints for Users Table-------------------------------------------------------------------------------------
# POST
@app.route('/add-user', methods=['POST'])
def add_user():   
      users_first_name = request.json['users_first_name']
      users_last_name = request.json['users_last_name']
      users_email = request.json['users_email']
      users_address = request.json['users_address']
      users_zip_code = request.json['users_zip_code']
      users_password = request.json['users_password']
      users_role = request.json['users_role']

      cur = mysql.connection.cursor()
      
      cur.callproc("spInsertNewUser",
      [users_first_name, users_last_name, users_email, users_address, users_zip_code, users_password, users_role])

      mysql.connection.commit()
      cur.close()

      return jsonify('User inserted successfully')

# @app.route('/user-credentials', methods=['GET'])
# def get_user_credentials():   
#    users_email = request.json['users_email']
#    users_password = request.json['users_password']

#    cur = mysql.connection.cursor()

#    cur.callproc("spGetUserCredentials", [users_email, users_password])
#    user = cur.fetchall()

#    mysql.connection.commit()
#    cur.close()

#    return jsonify(user)

# GET ALL
@app.route('/users', methods=["GET"])
def get_users():    
   cur = mysql.connection.cursor()
   
   cur.callproc("spGetAllUsers", ())
   all_users = cur.fetchall()

   cur.close()

   return jsonify(all_users)

# GET ONE
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
   cur = mysql.connection.cursor()
  
   cur.callproc("spGetUserById", [id])
   user = cur.fetchall()

   cur.close()

   if user:
      return jsonify(user)
   else:
      return jsonify("That user doesnt exist")  

# PATCH
@app.route('/user/<id>', methods=['PATCH'])
def update_user(id):
   users_email = request.json['users_email']
   users_password = request.json['users_password']
   users_role = request.json['users_role']

   cur = mysql.connection.cursor()

   cur.callproc("spUpdateUserById", [id, users_email, users_password, users_role])

   mysql.connection.commit()
   cur.close()

   return jsonify('User updated successfully')

# DELETE
@app.route('/delete-user/<id>', methods=['DELETE'])
def delete_user(id):
   cur = mysql.connection.cursor()
   
   cur.callproc("spDeleteUserById", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('User deleted')


# Endpoints for Comments Table-------------------------------------------------------------------------------------
# POST
@app.route('/add-comment', methods=['POST'])
def add_comment():        
      comments_comment = request.json['comments_comment']
      comments_date = request.json['comments_date']
      comments_products_id = request.json['comments_products_id']
      comments_users_id = request.json['comments_users_id']      

      cur = mysql.connection.cursor()
      
      cur.callproc("spInsertNewComment",
      [comments_comment, comments_date, comments_products_id, comments_users_id])
      
      mysql.connection.commit()
      cur.close()

      return jsonify("Comment inserted succesfully")

# GET ALL
@app.route('/comments', methods=["GET"])
def get_comments():    
   cur = mysql.connection.cursor()
   
   cur.callproc("spGetAllComments", ())
   all_comments = cur.fetchall()

   cur.close()

   return jsonify(all_comments)

# GET ONE
@app.route('/comment/<id>', methods=['GET'])
def get_comment(id):
   cur = mysql.connection.cursor()
  
   cur.callproc("spGetCommentById", [id])
   comment = cur.fetchall()

   cur.close()

   if comment:
      return jsonify(comment)
   else:
      return jsonify("That comment doesnt exist")  

# GET COMMENTS BY PRODUCT_ID
@app.route('/comments-by-product/<id>', methods=['GET'])
def get_commentsByProduct(id):
   cur = mysql.connection.cursor()
  
   cur.callproc("spGetCommentsByProduc", [id])
   comments = cur.fetchall()

   cur.close()
   
   return jsonify(comments)  

# I DONT NEED PATCH

# DELETE
@app.route('/delete-comment/<id>', methods=['DELETE'])
def delete_comment(id):
   cur = mysql.connection.cursor()
   
   cur.callproc("spDeleteCommentById", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('Comment deleted')

# Endpoints for Cart Table-------------------------------------------------------------------------------------
# POST
@app.route('/add-item-cart', methods=['POST'])
def add_item_cart():   
      cart_products_id = request.json['cart_products_id']
      cart_products_name = request.json['cart_products_name']
      cart_products_image_url = request.json['cart_products_image_url']
      cart_users_id = request.json['cart_users_id']
      cart_users_first_name = request.json['cart_users_first_name']
      cart_date = request.json['cart_date']
      cart_quantity_items = request.json['cart_quantity_items']
      cart_products_price = request.json['cart_products_price']

      cur = mysql.connection.cursor()
      
      cur.callproc("spInsertItemsCart",
      [cart_products_id, cart_products_name, cart_products_image_url, cart_users_id, cart_users_first_name, cart_date, cart_quantity_items, cart_products_price])

      mysql.connection.commit()
      cur.close()

      return jsonify('Item inserted to the Cart successfully')

#GET ALL
@app.route('/carts', methods=["GET"])
def get_carts():    
   cur = mysql.connection.cursor()
   
   cur.callproc("spGetAllCarts", ())
   all_carts = cur.fetchall()

   cur.close()

   return jsonify(all_carts)

#GET ALL ITMES BY USER_ID
@app.route('/carts-items-by-user/<id>', methods=["GET"])
def get_carts_items_by_user(id):    
   cur = mysql.connection.cursor()
   
   cur.callproc("spGetItemCartsByUser", [id])
   all_carts = cur.fetchall()

   cur.close()

   return jsonify(all_carts)

# PATCH
@app.route('/cart/<id>', methods=['PATCH'])
def update_item_cart(id):
   cart_quantity_items = request.json['cart_quantity_items']

   cur = mysql.connection.cursor()

   cur.callproc("spUpdateItemCartById", [id, cart_quantity_items])

   mysql.connection.commit()
   cur.close()

   return jsonify('Item Cart updated successfully')

# DELETE
@app.route('/delete-item-cart/<id>', methods=['DELETE'])
def delete_item_cart(id):
   cur = mysql.connection.cursor()
   
   cur.callproc("spDeleteItemCartById", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('Item Cart deleted')

# DELETE ITEMS BY USER_ID
@app.route('/delete-item-cart-by-user/<id>', methods=['DELETE'])
def delete_item_cart_by_user(id):
   cur = mysql.connection.cursor()
   
   cur.callproc("spDeleteItemCartByUser", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('Item Cart deleted by User')


# Endpoints for Sales Table-------------------------------------------------------------------------------------
# POST
@app.route('/add-sale', methods=['POST'])
def add_sale():   
      sales_products_id = request.json['sales_products_id']
      sales_users_id = request.json['sales_users_id']     
      sales_date = request.json['sales_date']     
      sales_tax = request.json['sales_tax']     
      sales_total = request.json['sales_total']     

      cur = mysql.connection.cursor()
      
      cur.callproc("spInsertNewSale",
      [sales_products_id, sales_users_id, sales_date, sales_tax, sales_total])

      mysql.connection.commit()
      cur.close()

      return jsonify('Sale inserted successfully')

# GET ALL
@app.route('/sales', methods=["GET"])
def get_sales():    
   cur = mysql.connection.cursor()
   
   cur.callproc("spGetAllSales", ())
   all_sales = cur.fetchall()

   cur.close()

   return jsonify(all_sales)

# GET ONE
@app.route('/sale/<id>', methods=['GET'])
def get_sale(id):
   cur = mysql.connection.cursor()
  
   cur.callproc("spGetSaleById", [id])
   sale = cur.fetchall()

   cur.close()

   if sale:
      return jsonify(sale)
   else:
      return jsonify("That sale doesnt exist")  

# I DONT NEED PATCH

# DELETE
@app.route('/delete-sale/<id>', methods=['DELETE'])
def delete_sale(id):
   cur = mysql.connection.cursor()
   
   cur.callproc("spDeleteSaleById", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('Sale deleted')



if __name__ == '__main__':
    app.run(debug=True)