# from flask import (
#     Flask,
#     Blueprint,
#     render_template,
#     escape,
#     request,
#     abort,
#     jsonify,
#     flash,
#     redirect,
#     url_for,
#     session
# )
# from functools import wraps
# from flask_cors import CORS
# from os import environ as env
# from authlib.integrations.flask_client import OAuth
# from six.moves.urllib.parse import urlencode
# from lib.auth import AuthError, requires_auth, create_login_link
# import constants
# import json
# from dotenv import load_dotenv, find_dotenv
# import requests
# from datetime import datetime
# import tictanic.app


# user = Blueprint('user', __name__, template_folder='templates')

# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     print(ENV_FILE)
#     load_dotenv(ENV_FILE)

# AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
# AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
# AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
# AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
# AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
# AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

# oauth = tictanic.create_app().oauth

# auth0 = oauth.register(
#     'auth0',
#     client_id=AUTH0_CLIENT_ID,
#     client_secret=AUTH0_CLIENT_SECRET,
#     api_base_url=AUTH0_BASE_URL,
#     access_token_url=AUTH0_BASE_URL + '/oauth/token',
#     authorize_url=AUTH0_BASE_URL + '/authorize',
#     client_kwargs={
#         'scope': 'openid profile email',
#     },
# )



# # @user.route('/login')
# # def login():
# #     return render_template('login.html')

# @user.route('/callback')
# def callback_handling():
#     auth0.authorize_access_token()
#     resp = auth0.get('userinfo')
#     userinfo = resp.json()

#     session[constants.JWT_PAYLOAD] = userinfo
#     session[constants.PROFILE_KEY] = {
#         'user_id': userinfo['sub'],
#         'name': userinfo['name'],
#         'picture': userinfo['picture']
#     }
#     return redirect('/dashboard')

# @user.route('/login')
# def login():
#     return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

# @user.route('/logout')
# def logout():
#     session.clear()
#     params = {'returnTo': url_for(
#         'home', _external=True), 'client_id': AUTH0_CLIENT_ID}
#     return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# @user.route('/dashboard')
# @requires_auth
# def dashboard():
#     return render_template('dashboard.html',
#                             userinfo=session[constants.PROFILE_KEY],
#                             userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))
