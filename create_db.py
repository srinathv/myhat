#!/usr/bin/env python
import os
import datetime
from app import db, models

from config import SQLALCHEMY_DATABASE_PATH
os.remove(SQLALCHEMY_DATABASE_PATH)
db.create_all()

# # add user
# user = models.User(name='molu8455', email='monte.lunacek@email.com')
# db.session.add(user)
# user = models.User.query.filter_by(name='molu8455').first()

# # # add models
# # mod = models.Model(name='rengers', 
# # 				   user_id=user.id)
# # db.session.add(mod)

# # print mod.name, mod.user_id

# # mod = models.Model(name='benchmarks', 
# # 				   user_id=user.id)
# # db.session.add(mod)

# # print mod.name, mod.user_id


# db.session.commit()	
# print models.User.query.all()
# print models.Model.query.all()
