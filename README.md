myhat
=====

RESTful job submission


# Setting up API tokens
There are two components to successful authentication: the server secret, and the consumer token. The server secret is generated first, and has no expiration date. The server secret is then used to sign an API user's information, generating a consumer key valid for one year by default. To submit a request, the user need only to pass the token as a request parameter.

Generating a server secret and consumer key with auth_tools.py:
```
$ python auth_tools.py --generate-server-secret
>> Server-secret generated at api.sec.
$ python auth_tools.py --generate-user-token --username exampleuser
>> User token generated for exampleuser (token will expire in one year):
>> r34llY/l0nG.3x4mple.t0k3n
```

To submit an API request:
```
$ curl -u r34llY/l0nG.3x4mple.t0k3n:unused -i -X GET https://your-myhat-server.com/api/resource
>> HTTP/1.0 200 OK
>> Content-Type: application/json
>> Content-Length: 29
>> Server: Werkzeug/0.9.4 Python/2.7.3
>> Date: Mon, 28 Apr 2014 22:31:56 GMT

>> {
>>   "data": "Hello, exampleuser!"
>> }
```

