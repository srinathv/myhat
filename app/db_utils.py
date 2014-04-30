from flask import jsonify
from flask import abort
from app import app, db, models, remote



def database_add(x):
    try:
        db.session.add(x)     
        db.session.commit() 
        return jsonify( {'success': 'True'} )
    except:
        return jsonify( {'success': 'False'} )


def get_user_or_return(username):
    user_ = models.User.query.filter_by(username=username).first()
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

