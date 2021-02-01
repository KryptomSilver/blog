from flask import Flask,flash,render_template,url_for,redirect,request
from flask_login import login_user, current_user, logout_user, login_required,LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
# Modulo para correo electrónico
from flask_mail import Mail
from flask_mail import Message

import time
app = Flask(__name__)
app.debug=True
Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ywgqkpgjcotosl:157a6bfef189382f11f9fdce2c70075d62cfa419882763af78e507c60cb2fabe@ec2-54-196-1-212.compute-1.amazonaws.com:5432/d28g0vq4ef4ovn'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:1234@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kryptomsilver@gmail.com'
app.config['MAIL_PASSWORD'] = '5068616E746F6C'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Usuario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(250)) 
    apellido1 = db.Column(db.String(250)) 
    apellido2 = db.Column(db.String(250)) 
    email = db.Column(db.String(250), index=True)
    password = db.Column(db.String(250))
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True,index=True)
    titulo = db.Column(db.String(255), index=True) 
    descripcion = db.Column(db.String(800)) 
    id_usuario =  db.Column(db.Integer, db.ForeignKey('usuario.id'))
@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Usuario.query.get(int(user_id))
'----------------------------------------------------------- My Posts -----------------------------------------------------------'
@app.route('/myposts')
@login_required
def myposts():
    datos =  Usuario.query\
    .join(Posts, Usuario.id==Posts.id_usuario)\
    .add_columns(Usuario.id, Usuario.nombre, Usuario.email, Posts.titulo,Posts.descripcion,Posts.id)\
    .filter(Usuario.id == current_user.id).all()
    #print(datos)
    return render_template('my-posts.html',variable=datos)
'-----------------------------------------------------------Post Ver-----------------------------------------------------------'
@app.route('/post/<id_post>')
@login_required
def post_ver(id_post):
    datos = Posts.query.filter_by(id=int(id_post)).first()
    print(datos)
    return render_template('post.html',variable=datos)
'-----------------------------------------------------------Post Editar-----------------------------------------------------------'
@app.route('/post-editar/<id_post>')
@login_required
def post_editar(id_post):
    datos = Posts.query.filter_by(id=int(id_post)).first()
    print(datos)
    return render_template('post-editar.html',variable=datos)

@app.route('/post-actualizar',methods=['GET','POST'])
@login_required
def post_actualizar():
    if request.method == "POST":
        consulta = Posts.query.get(request.form['id'])
        consulta.titulo = request.form['titulo']
        consulta.descripcion = request.form['descripcion']
        consulta.id_usuario = current_user.id
        db.session.commit()
        flash("Post Actualizado")
        return redirect(url_for("myposts"))
'-----------------------------------------------------------Post Eliminar-----------------------------------------------------------'
@app.route('/eliminar/<post_id>')
@login_required
def post_eliminar(post_id): 
    consulta = Posts.query.filter_by(id=int(post_id)).delete()
    db.session.commit()
    flash("Post Eliminado")
    return redirect(url_for("myposts"))
'-----------------------------------------------------------Index-----------------------------------------------------------'
@app.route('/')
def index(): 
    datos =  Usuario.query\
    .join(Posts, Usuario.id==Posts.id_usuario)\
    .add_columns(Usuario.id, Usuario.nombre, Usuario.email, Posts.titulo,Posts.descripcion).all()
    #print(datos)
    return render_template('index.html',variable=datos)
'-----------------------------------------------------------Registrar Post-----------------------------------------------------------'
@app.route('/post-registrar', methods=['GET','POST'])
@login_required
def post_registrar():
    if request.method == "POST":
        vtitulo = request.form['titulo']
        vdescripcion = request.form['descripcion']
        post = Posts.query.filter_by(titulo=vtitulo).first()
        if post:
            flash('Post Existente')
            return redirect(url_for("post_registrar"))
            print(post)
        else:
            post = Posts(
            titulo=vtitulo,
            descripcion=vdescripcion,
            id_usuario=current_user.id
            )
            msg = Message("Registro de Post",sender="kryptomsilver@gmail.com",recipients=['abelromeror763@gmail.com'])
            msg.html = "<h1>" + vtitulo + "</h1>" + "<br>" + "<p>"+ vdescripcion + "</p>"
            mail.send(msg)
            db.session.add(post)
            db.session.commit()
            flash('Post Registrado')
            return redirect(url_for("index"))
    return render_template('post-registrar.html')
'-----------------------------------------------------------Login-----------------------------------------------------------'
@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == "POST":
        vemail = request.form['correo']
        vpassword = request.form['password']
        #vremember = True
        user = Usuario.query.filter_by(email=vemail).first()
        if user != None:
            print(user)
            if bcrypt.check_password_hash(user.password, vpassword):
                print("Ingresa aquí")
                login_user(user)
                return redirect(url_for("index"))
                #next_page = request.args.get('next')
                #return redirect(next_page) if next_page else redirect(url_for('blog'))  
            else:
                flash('Usuario o Contraseña incorrecta')
        else:
            flash('Ingresa valores!!')
    return render_template('login.html')

'-----------------------------------------------------------Cerrar sesión-----------------------------------------------------------'
@app.route("/logout")
@login_required
def logout():
    logout_user()
    
    return redirect(url_for("login"))

'-----------------------------------------------------------Perfil-----------------------------------------------------------'
@app.route("/profile/<id_usuario>")
def profile(id_usuario):
    datos = Usuario.query.filter_by(id=int(id_usuario)).first()
    return render_template("profile.html",variable=datos)

'-----------------------------------------------------------Usuario registrar-----------------------------------------------------------'
@app.route("/usuario-registrar",methods=['GET','POST'])
def usuario_registrar():
    if request.method == "POST":
        vnombre = request.form['nombre']
        vapellido1 = request.form['apellido1']
        vapellido2 = request.form['apellido2']
        vpassword = request.form['password']
        correo = request.form['correo']
        user = Usuario.query.filter_by(email=correo).first() 
        if user:
            flash('Correo existente')
            return redirect(url_for('usuario_registrar'))
        pw_hash = bcrypt.generate_password_hash(vpassword).decode('utf-8')
        usuario = Usuario(
            nombre=vnombre,
            apellido1=vapellido1,
            apellido2=vapellido2,
            password=pw_hash,
            email=correo
            )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario Registrado')
        return redirect(url_for('usuario_registrar'))
    return render_template('signup.html')
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)