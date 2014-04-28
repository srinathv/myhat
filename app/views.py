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
from db_utils import *
import json
import re
import os

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()



def validate_alphanumeric(s):
    return re.search('\W+', s) == None
    
def validate_alphanumeric_with_allowed(s):
    return re.search("[;=[\\]^_`|]",s) == None

@auth.verify_password
def verify_password(username_or_token, password):
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True


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


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/api/job/<string:modelname>', methods=['GET'])
@auth.login_required
def read_jobs(modelname):
    if username != g.user.username:
        abort(400)
    user = get_user_or_return(username)
    model = get_model_or_return(user, modelname)
    jobs = get_jobs_or_return(user, model)
    return jsonify( { 'jobs': map( lambda t: {'id': t.id }, jobs) } )

@app.route('/api/job/<string:modelname>/<int:job_id>', methods=['GET'])
@auth.login_required
def read_job(modelname,job_id):
    if username != g.user.username:
        abort(400)
    user = db_utils.get_user_or_return(username)
    model = db_utils.get_model_or_return(user, modelname)
    job = db_utils.get_job_or_return(user, model, job_id)
    output = remote.get_job_ouput(job)

    return output

@app.route('/api/job/<string:modelname>', methods=['POST'])
@auth.login_required
def create_job(modelname):
    if username != g.user.username:
        abort(400)
    user = db_utils.get_user_or_return(username)
    model = db_utils.get_model_or_return(user, modelname)

    # Make sure there's no funny business
    for k,v in request.data.iteritems():
        if validate_alphanumeric_with_allowed(k) and validate_alphanumeric_with_allowed(v):
            continue
        else:
            abort(400)

    params = request.data
    jid, jout, jerr = remote.submit_remote_job(model, username, params)

    job = models.Job(id=jid,
                      model_id=model.id, 
                      user_id=user.id,
                      output=jout,
                      error=jerr)

    return db_utils.database_add(job)


# class UserListAPI(Resource):

#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('name', type = str, location = 'json')
#         self.reqparse.add_argument('email', type = str, location = 'json')
#         super(UserListAPI, self).__init__()

#     def get(self):
#         users_q = models.User.query.all()
#         return jsonify( { 'users': map( lambda t: {'name': t.name }, users_q) } )

#     # Add a user
#     def post(self):
#         args = self.reqparse.parse_args()
#         user_ = models.User(name=args['name'], 
#                             email=args['email'])
#         return database_add(user_)


# class UserAPI(Resource):

#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('name', type = str, location = 'json')
#         self.reqparse.add_argument('cmd', type = str, location = 'json')
#         super(UserAPI, self).__init__()

#     def get(self, username):
#         user_ = get_user_or_return(username)
#         model_q = models.Model.query.filter_by(user_id=user_.id).all()
#         return jsonify( { 'models': map( lambda t: {'name': t.name }, model_q) })

#     # Add a model
#     def post(self, username):
#         user_ = get_user_or_return(username)
#         args = self.reqparse.parse_args()
#         mod_ = models.Model(name=args['name'],
#                             cmd=args['cmd'], 
#                             user_id=user_.id)

#         return database_add(mod_)


# class ModelAPI(Resource):

#     def get(self, username, modelname):
#         user_ = get_user_or_return(username)
#         model_ = get_model_or_return(user_, modelname)
#         jobs_ = get_jobs_or_return(user_, model_)
#         return jsonify( { 'jobs': map( lambda t: {'id': t.id }, jobs_) } )

#     def post(self, username, modelname):
#         user_ = get_user_or_return(username)
#         model_ = get_model_or_return(user_, modelname)

#         params = request.data
#         jid, jout, jerr = remote.submit_remote_job(model_, params)

#         job_ = models.Job(id=jid,
#                           model_id=model_.id, 
#                           user_id=user_.id,
#                           output=jout,
#                           error=jerr)

#         return database_add(job_)

# class JobAPI(Resource):
#     def get(self, username, modelname, job):
#         user_ = get_user_or_return(username)
#         model_ = get_model_or_return(user_, modelname)
#         job_ = get_job_or_return(user_, model_, job)
#         output_ = remote.get_job_ouput(job_)

#         return output_


# api.add_resource(UserListAPI, '/api/')
# api.add_resource(UserAPI, '/api/<string:username>')
# api.add_resource(ModelAPI, '/api/<string:username>/<string:modelname>')
# api.add_resource(JobAPI, '/api/<string:username>/<string:modelname>/<int:job>')






