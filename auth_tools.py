#!/usr/bin/env python
import os
import sys
import argparse

import hashlib
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



ONE_YEAR = 365*24*60*60

parser = argparse.ArgumentParser(
    description='Simple utility for generating and signing API keys.'
    )
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '--generate-secret',
    help='Generate the server secret.',
    action='store_true'
    )
group.add_argument(
    '--generate-user-token',
    help='Generate the user key. You must also use --username to supply necessary information.',
    action='store_true'
    )
parser.add_argument(
    '--username',
    help='Username to sign into user token. Must be specified if generating user token.'
    )

args = parser.parse_args()

if args.generate_secret:
    pe_dir = os.path.dirname(__file__)
    sec_path = os.path.join(pe_dir,'api.sec')
    if os.path.isfile(sec_path):
        sys.stdout.write('Deleting old secret.\n')
        os.remove(sec_path)
    with open(sec_path, 'w+') as sec_file:
        secret = hashlib.sha256( str( random.getrandbits(256) ) ).hexdigest()
        sec_file.write( secret )
        sys.stdout.write( 'Server-secret generated at {}.\n'.format(sec_path) )
    sys.exit(0)
    
if args.generate_user_token:
    pe_dir = os.path.dirname(__file__)
    sec_path = os.path.join(pe_dir,'api.sec')
    if not os.path.isfile(sec_path):
        sys.stdout.write('No secret found! You must generate a secret before signing a token.\n')
        sys.exit(1)
    if not args.username:
        sys.stdout.write('No username specified! You must specify a username to sign a token.\n')
        sys.exit(1)
    with open(sec_path, 'r') as sec_file:
        secret = sec_file.readline()
        serializer = Serializer(secret, expires_in=ONE_YEAR)
        token = serializer.dumps({
                'username': args.username
            })
        sys.stdout.write( 'User token generated for {} (token will expire in one year):\n\n{}\n\n\n'.format(args.username,token) )
    sys.exit(0)
        
