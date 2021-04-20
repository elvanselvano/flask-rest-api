from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_mysqldb import MySQL

# Create an object (name it with "app"). This object will then be used as the main object to be able to run the API
app = Flask(__name__)

# mysql configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'flask_mysql'

# Create a config to get data from MySQL as list of dictionaries. (optional)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Create an object to connect to MySQL
mysql = MySQL(app)

# Create a route that connects to the table in the previously configured database. In this case what will be used is the "employee" table in the database "flask_mysql"

# membuat route untuk operasi create dan read terhadap database
# route hanya bsa diakses dgn get dan post
@app.route('/employee', methods=['GET', 'POST'])
def employee():
  if request.method == 'GET':
    # connect to db
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM employee''')
    results = cur.fetchall()
    return jsonify(results) #convert to json
  elif request.method == 'POST':
    # data yang dikirim pas request akan terdapat pada request.form
    # convert data menjadi dictionary
    form = dict(request.form)

    # menyimpan data ke bbrp variabel
    username = form['username']
    full_name = form['full_name']
    gender = form['gender']

    # data dikirim dalam string, convert ke boolean
    married = bool(form['married'])

    # create query
    sql = "INSERT INTO employee(username, full_name, gender, married) VALUES (%s,%s,%s,%s)"
    data = (username, full_name, gender, married)

    # connect to db and execute query
    cur = mysql.connection.cursor()
    cur.execute(sql, data)

    # close connection (for patch and delete)
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Insert Success"})

# Create a route that leads to the table in database that have configured before. In this case table namely “employee” in the “flask_mysql” database will be used. In addition to patching and deleting data, data delivery will go through the route path variable "id". Then, create the request method "PATCH" in this router.
@app.route('/employee/<id>', methods=['PATCH', 'DELETE'])
def employeeid(id):
  if request.method == 'PATCH':
    form = dict(request.form)
    username = form['username']
    full_name = form['full_name']
    gender = form['gender']
    married =form['married']

    # create update query
    sql = f"UPDATE employee SET username='{username}', full_name='{full_name}', gender='{gender}', married={married} WHERE ID={id}"

    # connect to db and exec query
    cur = mysql.connection.cursor()
    cur.execute(sql)

    # close connection
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Update Success", "user_id": id})
  elif request.method == 'DELETE':
    # create delete query
    sql = f"DELETE FROM employee WHERE id = {id}"

    # connect to db and exec query
    cur = mysql.connection.cursor()
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Delete Success", "user_id": id})

@app.route("/")
def home():
  return render_template("homepage.html") 

# running api
if __name__ == '__main__':
  app.run(debug=True)
