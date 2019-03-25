import time
from .ms_auth import get_token_from_code, get_token_from_refresh_token
from .ms_graph import get_me 

class MSlogin():
    status = {}
    redirect = {'login':'', 'logout':''}
    urls = {'login':'', 'logout':''}
    users = {}

    @staticmethod
    def check(user_id):
        for user in MSlogin.users.keys():
            if user == user_id:
                MSlogin.renew_if_expired(user_id)
                return {'status':'login', 'user':user, 'urls':MSlogin.urls}
        return {'status':'logout', 'user':'', 'urls':MSlogin.urls}
    
    @staticmethod
    def sign_in(auth_code):
        # Get tokens
        redirect_uri = MSlogin.redirect['login']
        token = get_token_from_code(auth_code, redirect_uri)
        access_token = token['access_token']
        refresh_token = token['refresh_token']
        expires_in = token['expires_in']
            # expires_in is in seconds
            # Get current timestamp (seconds since Unix Epoch) and
            # add expires_in to get expiration time
            # Subtract 5 minutes to allow for clock differences
        expiration = int(time.time()) + expires_in - 300
        # User id & tokens
        user = get_me(access_token)
        user_id= user['mail']
        tokens = {'access': access_token, 'refresh':refresh_token, 'expire':expiration}
        MSlogin.users.update({user_id:tokens})
        return user_id
    
    @staticmethod
    def renew_if_expired(user_id):
        current_token = MSlogin.users[user_id]['access']
        expiration = MSlogin.users[user_id]['expire']
        now = int(time.time())
        if (current_token and now < expiration):
            # Token still valid
            return current_token
        else:
            # Token expired
            refresh_token = MSlogin.users[user_id]['refresh']
            redirect_uri = MSlogin.redirect['login']
            new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)
            expiration = int(time.time()) + new_tokens['expires_in'] - 300

            MSlogin.users[user_id]['access'] = new_tokens['access_token']
            MSlogin.users[user_id]['refresh'] = new_tokens['refresh_token']
            MSlogin.users[user_id]['expire'] = expiration
            return new_tokens['access_token']


            

