from app import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)



class User(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(32), index=True)

    name = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    models = db.relationship('Model', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.name)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.filter_by(username=data['username']).first()
        return user

class Model(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(140), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    cmd = db.Column(db.String(180))

    def __repr__(self):
        return '<Model %r>' % (self.name)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    output = db.Column(db.String(250))
    error = db.Column(db.String(250))
