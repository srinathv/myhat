#!/usr/bin/env python
import os
import datetime
from app import db, models

from config import SQLALCHEMY_DATABASE_PATH
os.remove(SQLALCHEMY_DATABASE_PATH)
db.create_all()

# Add user
user = models.User(username='molu8455', name='monte', email='monte.lunacek@email.com')
db.session.add(user)
db.session.commit()

# Add models for monte
user = models.User.query.filter_by(username='molu8455').first()
mod = models.Model(name='rengers',
                   cmd='$HOME/projects/rengers/webapi_wrapper/execute.py',
				   user_id=user.id)
db.session.add(mod)
db.session.commit()

mod = models.Model(name='showq',
                   cmd='showq',
                   user_id=user.id)
db.session.add(mod)
db.session.commit()
#
#
# print mod.name, mod.user_id

# # mod = models.Model(name='benchmarks',
# # 				   user_id=user.id)
# # db.session.add(mod)

# # print mod.name, mod.user_id


print 'users'
print '-'*80
for user in models.User.query.all():
    print user.id,
    print user.username,
    print user.name,
    print user.email
    print ''

print 'models'
print '-'*80
for model in models.Model.query.all():
    print model.name,
    print model.user_id,
    print model.cmd,
    print model.id
    print ''
