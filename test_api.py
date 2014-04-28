#!/usr/bin/env python

from __future__ import print_function

import requests
import json

headers = {'content-type': 'application/json'}

print(requests.get('http://localhost:5000/api/monte/rengers').text)







