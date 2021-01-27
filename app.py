from flask import Flask,flash,render_template,url_for,redirect,request
from flask_login import login_user, current_user, logout_user, login_required,LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.debug=True
Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:1234@localhost:5432/blog'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:1234@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
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
    Id_Post = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String(30)) 
    descripcion = db.Column(db.String(30)) 
    seccion1 = db.Column(db.String(30)) 
    seccion2 = db.Column(db.String(30))

@app.route('/')
@login_required
def index():
    datos = Posts.query.all()
    return render_template('index.html',variable=datos)
@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Usuario.query.get(int(user_id))

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
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
   

@app.route("/usuario-registrar",methods=['GET','POST'])
def usuario_registrar():
    if request.method == "POST":
        vnombre = request.form['nombre']
        vapellido1 = request.form['apellido1']
        vapellido2 = request.form['apellido2']
        vpassword = request.form['password']
        vemail = request.form['correo']
        print("vnombre:", vnombre)
        print("vapellido1:", vapellido1)
        print("vapellido2:", vapellido2)
        print("vpassword:", vpassword)
        print("vemail:", vemail)
        user = Usuario.query.filter_by(email=vemail).first() 
        if user:
            flash('Correo existente')
            return redirect(url_for('usuario_registrar'))
        pw_hash = bcrypt.generate_password_hash(vpassword).decode('utf-8')
        usuario = Usuario(
            nombre=vnombre,
            apellido1=vapellido1,
            apellido2=vapellido2,
            password=pw_hash,
            email=vemail
            )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario Registrado')
        return redirect(url_for('usuario_registrar'))

    return render_template('usuario-registrar.html')
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)