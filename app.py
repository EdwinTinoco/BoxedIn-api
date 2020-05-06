from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)

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

      cur = mysql.connection.cursor()

      # cur.execute("""INSERT INTO products
      # (products_name, products_description, products_inventory, products_image_url, products_categories_id, products_stars_id) 
      # VALUES (%s, %s, %s, %s, %s, %s)""", 
      # (products_name, products_description, products_inventory, products_image_url, products_categories_id, products_stars_id))

      cur.callproc("spInsertaNewProduct",
      [products_name, products_description, products_inventory, products_image_url, products_categories, products_stars])

      mysql.connection.commit()
      cur.close()

      return jsonify('Product inserted successfully')

# GET ALL
@app.route('/products', methods=["GET"])
def get_products():    
   cur = mysql.connection.cursor()

   #cur.execute("""SELECT * FROM products""")
   cur.callproc("spGetAllProducts", ())
   all_products = cur.fetchall()

   cur.close()

   return jsonify(all_products)

# GET ONE
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
   cur = mysql.connection.cursor()

   #cur.execute("""SELECT * FROM products WHERE products_id = %s""", (id))
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

   cur = mysql.connection.cursor()

   cur.callproc("spUpdateProductById", [id, products_inventory, products_stars])

   mysql.connection.commit()
   cur.close()

   return jsonify('Product updated successfully')

# DELETE
@app.route('/delete-product/<id>', methods=['DELETE'])
def delete_product(id):
   cur = mysql.connection.cursor()

   #cur.execute(""" DELETE FROM products WHERE products_id = %s""", (id))
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

      return jsonify('Comment inserted successfully')

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

# I DONT NEED PATCH

# DELETE
@app.route('/delete-comment/<id>', methods=['DELETE'])
def delete_comment(id):
   cur = mysql.connection.cursor()
   
   cur.callproc("spDeleteCommentById", [id])
   mysql.connection.commit()

   cur.close()    

   return jsonify('Comment deleted')


# Endpoints for Sales Table-------------------------------------------------------------------------------------
# POST
@app.route('/add-sale', methods=['POST'])
def add_sale():   
      sales_products_id = request.json['sales_products_id']
      sales_users_id = request.json['sales_users_id']     
      sales_tax = request.json['sales_tax']     
      sales_total = request.json['sales_total']     

      cur = mysql.connection.cursor()
      
      cur.callproc("spInsertNewSale",
      [sales_products_id, sales_users_id, sales_tax, sales_total])

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