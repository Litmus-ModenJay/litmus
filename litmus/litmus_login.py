import time
from .ms_auth import get_token_from_code, get_token_from_refresh_token
from .ms_graph import get_me 

class MSlogin():
    status = {}
    redirect = {'login':'a', 'logout':''}
    urls = {'login':'x', 'logout':''}
    users = {}

    @staticmethod
    def check(id):
        for user in MSlogin.users.keys():
            if user == id:
                MSlogin.renew_if_expired(id)
                return {'status':'login', 'user':user, 'urls':MSlogin.urls}
        return {'status':'logout', 'user':'', 'urls':MSlogin.urls}
    
    @staticmethod
    def renew_if_expired(id):
        current_token = MSlogin.users[id]['access']
        expiration = MSlogin.users[id]['expire']
        now = int(time.time())
        if (current_token and now < expiration):
            # Token still valid
            return current_token
        else:
            # Token expired
            refresh_token = MSlogin.users[id]['refresh']
            redirect_uri = MSlogin.redirect['login']
            new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)
            expiration = int(time.time()) + new_tokens['expires_in'] - 300

            MSlogin.users[id]['access'] = new_tokens['access_token']
            MSlogin.users[id]['refresh'] = new_tokens['refresh_token']
            MSlogin.users[id]['expire'] = expiration
            return new_tokens['access_token']

