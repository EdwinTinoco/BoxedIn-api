from flask import Flask, request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# MySQL database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'benjy2012!'
app.config['MYSQL_DB'] = 'boxedin_ecommerce_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


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
   products_stars_id = request.json['products_stars_id']

   cur = mysql.connection.cursor()

   cur.callproc("spUpdateProductById", [id, products_inventory, products_stars_id])

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
def add_user():   
      comments_comment = request.json['comments_comment']
      comments_products_id = request.json['comments_products_id']
      comments_users_id = request.json['comments_users_id']      

      cur = mysql.connection.cursor()
      
      cur.callproc("spInsertNewComment",
      [comments_comment, comments_products_id, comments_users_id])

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



if __name__ == '__main__':
    app.run(debug=True)