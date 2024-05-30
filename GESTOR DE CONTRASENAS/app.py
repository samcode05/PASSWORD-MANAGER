from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
import os
import json
import random
import string

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'      
bcrypt = Bcrypt(app)

# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    contrasena = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150))

# Formularios
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Rutas de autenticación
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rutas de gestión de productos
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/crear_producto', methods=['POST'])
@login_required
def crear_producto():
    data = request.json
    new_product = Product(nombre=data['nombre'], contrasena=data['contrasena'], correo=data.get('correo'))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Producto creado correctamente"})

@app.route('/ver_productos')
@login_required
def ver_productos():
    productos = Product.query.all()
    productos_list = [{"id": p.id, "nombre": p.nombre, "contrasena": p.contrasena, "correo": p.correo} for p in productos]
    return jsonify({"productos": productos_list})

@app.route('/editar_producto', methods=['POST'])
@login_required
def editar_producto():
    data = request.json
    print("Datos recibidos para editar:", data)  # Agregar mensaje de depuración
    product = db.session.get(Product, data['id'])  # Usar db.session.get en lugar de Product.query.get
    print("Producto encontrado:", product)  # Agregar mensaje de depuración
    if product:
        product.nombre = data['nombre']
        product.contrasena = data['contrasena']
        product.correo = data['correo']
        db.session.commit()
        return jsonify({"message": "Producto editado correctamente"})
    return jsonify({"message": "Producto no encontrado"}), 400

@app.route('/eliminar_producto', methods=['POST'])
@login_required
def eliminar_producto():
    data = request.json
    print("Datos recibidos para eliminar:", data)  # Agregar mensaje de depuración
    product = db.session.get(Product, data['id'])  # Usar db.session.get en lugar de Product.query.get
    print("Producto encontrado:", product)  # Agregar mensaje de depuración
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Producto eliminado correctamente"})
    return jsonify({"message": "Producto no encontrado"}), 400

@app.route('/generar_contrasena_random', methods=['GET'])
@login_required
def generar_contrasena_random():
    length = int(request.args.get('length', 12))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return jsonify({"contrasena": password})

@app.route('/exportar_contrasenas', methods=['GET'])
@login_required
def exportar_contrasenas():
    productos = Product.query.all()
    csv_data = "Nombre,Contraseña,Correo\n"
    for product in productos:
        csv_data += f"{product.nombre},{product.contrasena},{product.correo}\n"

    with open('passwords.csv', 'w') as file:
        file.write(csv_data)

    return send_file('passwords.csv', as_attachment=True)

# Función para importar desde un archivo CSV
def importar_desde_csv(archivo):
    import csv
    decoded_file = archivo.read().decode('latin1')  # Reemplaza 'tu_codificacion' con la codificación correcta
    csv_reader = csv.DictReader(decoded_file.splitlines())

    for row in csv_reader:
        nombre = row['Nombre']
        contrasena = row['Contraseña']
        correo = row['Correo']

        nuevo_producto = Product(nombre=nombre, contrasena=contrasena, correo=correo)
        db.session.add(nuevo_producto)

    db.session.commit()

# Ruta para importar contraseñas desde un archivo CSV
@app.route('/importar_contrasenas', methods=['POST'])
@login_required
def importar_contrasenas():
    if 'file' not in request.files:
        return jsonify({'message': 'No se encontró ningún archivo'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Nombre de archivo no válido'}), 400

    if file and file.filename.endswith('.csv'):
        importar_desde_csv(file)
        return jsonify({'message': 'Contraseñas importadas correctamente'})
    else:
        return jsonify({'message': 'El archivo debe estar en formato CSV'}), 400

# Gestión de usuarios
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Creación de base de datos
def create_database():
    if not os.path.exists('instance/database.db'):
        with app.app_context():
            db.create_all()

# Plantillas HTML
@app.route('/register.html')
def register_template():
    return render_template('register.html')

@app.route('/login.html')
def login_template():
    return render_template('login.html')

@app.route('/index.html')
def index_template():
    return render_template('index.html')

# Archivos estáticos
@app.route('/static/styles.css')
def styles():
    return send_file('static/styles.css')

@app.route('/static/script.js')
def script():
    return send_file('static/script.js')

# Inicialización de la base de datos
create_database()

if __name__ == '__main__':
    app.run(debug=True)



# tu puedes ! c:
