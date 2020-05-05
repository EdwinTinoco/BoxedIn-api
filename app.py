from flask import Flask, request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'benjy2012!'
app.config['MYSQL_DB'] = 'boxedin_ecommerce_db'

mysql = MySQL(app)


@app.route('/add-product', methods=['POST'])
def add_product():   
      products_name = request.json['products_name']
      products_description = request.json['products_description']
      products_inventory = request.json['products_inventory']
      products_image_url = request.json['products_image_url']
      products_category_id = request.json['products_category_id']
      products_stars_id = request.json['products_stars_id']

      cur = mysql.connection.cursor()

      cur.execute("""INSERT INTO products
      (products_name, products_description, products_inventory, products_image_url, products_category_id, products_stars_id) 
      VALUES (%s, %s, %s, %s, %s, %s)""", 
      (products_name, products_description, products_inventory, products_image_url, products_category_id, products_stars_id))

      mysql.connection.commit()
      cur.close()

      return 'Record inserted successfully'
   



if __name__ == '__main__':
    app.run(debug=True)