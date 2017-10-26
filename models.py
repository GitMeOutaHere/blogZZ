from app import db

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __init__(self, title, body, writer):
        self.title = title
        self.body = body
        self.writer = writer

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='writer')

    def __init__(self, email, password):
        self.email= email
        self.password= password