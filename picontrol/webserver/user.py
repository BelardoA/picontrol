#!/usr/bin/python 
#user.py

import jwt
import datetime

class User():
    username = ''
    password = ''

    def generate_auth_token(self, key, expiration=172800):
        # Set the expiration time
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        # Create the token
        token = jwt.encode({'id': self.username, 'exp': exp}, key, algorithm='HS256')
        return token

    @staticmethod
    def verify_auth_token(token, key):
        try:
            # Decode the token
            data = jwt.decode(token, key, algorithms=['HS256'])
            sessionUser = User()
            sessionUser.username = data['id']
            return sessionUser
        except jwt.ExpiredSignatureError:
            # The token is expired
            return None
        except jwt.InvalidTokenError:
            # The token is invalid
            return None
