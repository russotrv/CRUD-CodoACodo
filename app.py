#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------
#para agregar los productos a la bbdd
import json

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255) NOT NULL,
            categoria VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL
            )CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    #----------------------------------------------------------------
    def agregar_producto(self, nombre, descripcion, categoria, cantidad, precio):
        # Verificamos si ya existe un producto con el mismo nombre, dado que el codigo es auto incremental
        self.cursor.execute("SELECT * FROM productos WHERE nombre = %s AND descripcion = %s AND categoria = %s", (nombre, descripcion, categoria))
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO productos (nombre, descripcion, categoria, cantidad, precio) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, descripcion, categoria, cantidad, precio)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def consultar_producto(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute("SELECT * FROM productos WHERE codigo = %s",(codigo,))
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_producto(self, codigo, nuevo_nombre, nueva_descripcion, nueva_categoria, nueva_cantidad, nuevo_precio):
        sql = "UPDATE productos SET nombre = %s, descripcion = %s, categoria = %s, cantidad = %s, precio = %s WHERE codigo = %s"
        valores = (nuevo_nombre, nueva_descripcion, nueva_categoria, nueva_cantidad, nuevo_precio, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos

    def listar_productosCat(self, categoria, ):
        self.cursor.execute("SELECT * FROM productos WHERE categoria = %s", (categoria,))
        productos = self.cursor.fetchall()
        return productos

    #----------------------------------------------------------------
    def eliminar_producto(self, codigo):
        try:
            # Eliminamos un producto de la tabla a partir de su código
            self.cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
            self.conn.commit()

            #eliminacion_exitosa = self.cursor.rowcount > 0
            # Reorganizamos los valores AUTO_INCREMENT después de la eliminación
            #if eliminacion_exitosa:
            #    self.cursor.execute("ALTER TABLE productos AUTO_INCREMENT = 1;")
            #    self.conn.commit()

            #return eliminacion_exitosa
        except Exception as e:
            print("Error al eliminar el producto:", e)
            # Manejar otros errores según sea necesario
            return False

    #----------------------------------------------------------------
    def mostrar_producto(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        producto = self.consultar_producto(codigo)
        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['codigo']}")
            print(f"Nombre.....: {producto['nombre']}")
            print(f"Descripción: {producto['descripcion']}")
            print(f"Categori.....: {producto['categoria']}")
            print(f"Cantidad...: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
        else:
            print("Producto no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------

@app.route("/productos/<string:categoria>", methods=["GET"])
def consultar_productos(categoria):
    productos = catalogo.listar_productosCat(categoria)
    return jsonify(productos)

@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = catalogo.listar_productos()
    return jsonify(productos)


#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["GET"])
def mostrar_producto(codigo):
    producto = catalogo.consultar_producto(codigo)
    if producto:
        return jsonify(producto), 201
    else:
        return "Producto no encontrado", 404

#--------------------------------------------------------------------
@app.route("/productos", methods=["POST"])
def agregar_producto():
    #Recojo los datos del form
    #codigo = request.form['codigo']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    if catalogo.agregar_producto(nombre, descripcion, categoria, cantidad, precio):
        #imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        return jsonify({"mensaje": "Producto agregado"}), 201
    else:
        return jsonify({"mensaje": "Producto ya existe"}), 400

#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["PUT"])
def modificar_producto(codigo):
    #Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nueva_descripcion = request.form.get("descripcion")
    nueva_categoria = request.form.get("categoria")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    
    if catalogo.modificar_producto(codigo, nuevo_nombre, nueva_descripcion, nueva_categoria, nueva_cantidad, nuevo_precio):
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 403


#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["DELETE"])
def eliminar_producto(codigo):

    if catalogo.eliminar_producto(codigo):
        return jsonify({"mensaje": "Producto eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    

#--------------------------------------------------------------------
if __name__ == "__main__":
    catalogo = Catalogo(host='localhost', user='root', password='', database='miapp')

    with open('catalogo.json', 'r', encoding='utf-8') as file:
        productos = json.load(file)

    for producto in productos:
        catalogo.agregar_producto(  producto["nombre"], 
                                    producto["descripcion"], 
                                    producto["categoria"], 
                                    producto["cantidad"], 
                                    producto["precio"] 
                                )

    app.run(debug=True)