class Usuarios(db.Model,UserMixin):
    Id_Usuario = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(30)) 
    apellido1 = db.Column(db.String(30)) 
    apellido2 = db.Column(db.String(30)) 
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
class Posts(db.Model):
    Id_Post = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String()) 
    descripcion = db.Column(db.String()) 
    seccion1 = db.Column(db.String()) 
    seccion2 = db.Column(db.String())