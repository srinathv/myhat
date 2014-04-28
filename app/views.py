from flask import render_template
from flask import flash
from flask import redirect

from flask import Flask
from flask import jsonify 
from flask import abort
from flask import request
from flask import make_response
from flask import url_for
from flask import g

from flask.ext.restful import Api, Resource, reqparse

from app import app, db, models, remote
import json
import re
import os

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
api = Api(app)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True


@app.route('/api/users/<int:id>')
def get_user(id):
    user = models.User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/')
@app.route('/index')
def index():
    users = models.User.query.all()
    return render_template("index.html",
        title = 'API',
        users = users)

@app.route('/<username>')
@auth.login_required
def user_view(username):
    if username != g.user.username:
        abort(400)
    user = models.User.query.filter_by(name=username).first()
    mods = models.Model.query.all()
    return render_template("user.html",
        user = user,
        mods = mods)

@app.route('/<username>/<mod>')
@auth.login_required
def model_view(username, mod):
    if username != g.user.username:
        abort(400)
    user = models.User.query.filter_by(name=username).first()
    mod = models.Model.query.filter_by(name=mod).first()
    return render_template("models.html",
        user = user,
        mod = mod)


def database_add(x):
    try:
        db.session.add(x)     
        db.session.commit() 
        return jsonify( {'success': 'True'} )
    except:
        return jsonify( {'success': 'False'} )


def get_user_or_return(username):
    user_ = models.User.query.filter_by(name=username).first()
    if user_ is None:
        abort(404)
    return user_


def get_model_or_return(user, modelname):
    mod_ = models.Model.query.filter_by(user_id=user.id).first()
    if mod_ is None:
        abort(404)
    return mod_


def get_jobs_or_return(user, mod):
    #jobs_ = models.Job.query.filter_by(user_id=user.id, model_id=mod.id).all()
    jobs_ = models.Job.query.all()
    if jobs_ is None:
        abort(404)
    return jobs_


def get_job_or_return(user, mod, job):
    #jobs_ = models.Job.query.filter_by(user_id=user.id, model_id=mod.id).all()
    job_ = models.Job.query.filter_by(id=job).first()
    if job_ is None:
        abort(404)
    return job_


"""
Instead of using Flask-RESTful, the API could be approached in the manner below.
Any arbitrary response data can be jsonified and returned to the user with the
proper headers. Doing so allows a relatively straightforawrd API key process
to be utilized.
"""
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})




class UserListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('email', type = str, location = 'json')
        super(UserListAPI, self).__init__()

    def get(self):
        users_q = models.User.query.all()
        return jsonify( { 'users': map( lambda t: {'name': t.name }, users_q) } )

    # Add a user
    def post(self):
        args = self.reqparse.parse_args()
        user_ = models.User(name=args['name'], 
                            email=args['email'])
        return database_add(user_)


class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('cmd', type = str, location = 'json')
        super(UserAPI, self).__init__()

    def get(self, username):
        user_ = get_user_or_return(username)
        model_q = models.Model.query.filter_by(user_id=user_.id).all()
        return jsonify( { 'models': map( lambda t: {'name': t.name }, model_q) })

    # Add a model
    def post(self, username):
        user_ = get_user_or_return(username)
        args = self.reqparse.parse_args()
        mod_ = models.Model(name=args['name'],
                            cmd=args['cmd'], 
                            user_id=user_.id)

        return database_add(mod_)


class ModelAPI(Resource):

    def get(self, username, modelname):
        user_ = get_user_or_return(username)
        model_ = get_model_or_return(user_, modelname)
        jobs_ = get_jobs_or_return(user_, model_)
        return jsonify( { 'jobs': map( lambda t: {'id': t.id }, jobs_) } )

    def post(self, username, modelname):
        user_ = get_user_or_return(username)
        model_ = get_model_or_return(user_, modelname)

        params = request.data
        jid, jout, jerr = remote.submit_remote_job(model_, params)

        job_ = models.Job(id=jid,
                          model_id=model_.id, 
                          user_id=user_.id,
                          output=jout,
                          error=jerr)

        return database_add(job_)

class JobAPI(Resource):
    def get(self, username, modelname, job):
        user_ = get_user_or_return(username)
        model_ = get_model_or_return(user_, modelname)
        job_ = get_job_or_return(user_, model_, job)
        output_ = remote.get_job_ouput(job_)

        return output_


api.add_resource(UserListAPI, '/api/')
api.add_resource(UserAPI, '/api/<string:username>')
api.add_resource(ModelAPI, '/api/<string:username>/<string:modelname>')
api.add_resource(JobAPI, '/api/<string:username>/<string:modelname>/<int:job>')






