# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# JANUS Web API

# <codecell>

from __future__ import print_function

import json
import requests

# <headingcell level=2>

# Query API database with `get` requests

# <codecell>

uri = 'http://localhost:5000/api/monte'

models = json.loads(requests.get(uri).text)
tmp = map(print, models['models'])

# <codecell>

uri = 'http://localhost:5000/api/monte/rengers'

jobs = json.loads(requests.get(uri).text)
tmp = map(print, jobs['jobs'])

# <headingcell level=2>

# Submit a job with `post`

# <codecell>

uri = 'http://localhost:5000/api/monte/rengers'

# <markdowncell>

# Define the model parameters

# <codecell>

params = dict()
params['pmmphr'] = 40
params['taucwepp'] = 6.2
params['hcelev'] = 2.0
params['time'] = 15

# <markdowncell>

# Call the model

# <codecell>

r = requests.post(uri, data=json.dumps(params))
print(r.text)

# <markdowncell>

# Print last 5 jobs

# <codecell>

jobs = json.loads(requests.get(uri).text)
ids = map(lambda x: x['id'], jobs['jobs'])
tmp = map(print, ids[-5:])

# <codecell>

ids[-1]

# <headingcell level=2>

# Check the output of a job

# <codecell>

uri = 'http://localhost:5000/api/monte/rengers/' + str(ids[-1])

r = requests.get(uri)
print(r.text)

# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt

x = map( lambda x: float(x.strip()), r.text.split(',')[1:-1])
plt.plot(x)
plt.ylim(990,1025)

# <codecell>


