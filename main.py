
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import cursor

app = Flask(__name__)

#establecer una conexion con la basedata
mysqlConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="project_bd"
)
#crea una instancia y crea una conexion, tunel entre basedata y project
cursor = mysqlConnection.cursor(dictionary=True)

'''ENDPOINTS O SERVICIOS'''

@app.route('/', methods=['GET'])
def helloWorld():
    response = {
        "message": "Hello World!"
    }
    return jsonify(response)

@app.route('/felipe', methods=['GET'])
def helloFelipe():
    response = {
        "message": "Hello Felipe!"
    }
    return jsonify(response)

#ruta para listar o buscar los usuarios
#pide a la basedata una consulta sql
@app.route('/users', methods=['GET'])
def getUsers():
    cursor.execute("SELECT * FROM users") #seleccione todos los datos de la tabla users
    users = cursor.fetchall() # convierte la info de la tabla en un vector/lista
    return jsonify(users) #si hay una lista de diccionarios en un texto (JSON)

@app.route('/users', methods=['POST']) #el POST crea
def createUser():
    data = request.get_json() #.getjson trae el json con la informacion de la peticion y la transforma en un dicc de py
    name = data['name']
    password = data['password']
    email = data['email']
    nickname = data['nickname']
    cursor.execute("INSERT INTO users (name, password, email, nickname) VALUES (%s, %s, %s, %s)",
                   (name, password, email, nickname))
    mysqlConnection.commit() #la basedata inserta los datos
    return jsonify({"message": "User created successfully"})

@app.route('/users/<int:userId>', methods=['GET']) # <int:userId> se define que va a llegar una variable dentro de la ruta
def getUser(userId):
    cursor.execute("SELECT * FROM users WHERE id = %s", (userId,)) # la basedata busca cual tiene este id
    user = cursor.fetchone()
    return jsonify(user) # lo retorna

@app.route('/users/<int:userId>', methods=['PUT'])
def updateUser(userId): #para actualizar necesitamos saber qué se actualizará (body)
    data = request.get_json()
    name = data['name']
    password = data['password']
    email = data['email']
    nickname = data['nickname']
    cursor.execute("UPDATE users SET name = %s, password = %s, email =%s, nickname = %s WHERE id = %s",
    (name, password, email, nickname, userId))

    mysqlConnection.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    cursor.execute("DELETE FROM users WHERE id = %s", (userId,))
    mysqlConnection.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    print("hello world")
    app.run(debug=True)