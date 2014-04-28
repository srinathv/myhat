from app import remote
import json

params = dict()
params['pmmphr'] = 40
params['taucwepp'] = 6.2
params['tauc'] = 140
params['nbare'] = 0.02
params['mann'] = 0.05
params['immphr'] = 20
params['zparam1'] = 0.00008364
params['zparam2'] = -0.09355
params['zparam3'] = 1022.4
params['hcelev'] = 2.0
params['time'] = 10

remote.submit_remote_job('monte', 'rengers', json.dumps(params))


