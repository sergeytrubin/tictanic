import json
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    session
)
from flask_login import login_user
from six.moves.urllib.parse import urlencode

from app.blueprints.user.models import User
from app.extensions import login_manager
from . import user
from .models import User
from app.database import db
from app.auth0 import (
    auth0,
    constants,
    AUTH0_CALLBACK_URL,
    AUTH0_AUDIENCE,
    AUTH0_CLIENT_ID
)



from app.lib.decorators import requires_auth



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


# @user.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         form.user.authenticated = True
#         db.session.add(form.user)
#         db.session.commit()
#         login_user(form.user)
#         return redirect(url_for('core.home'))
#     return render_template('user/login.html', form=form)


@user.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Check if user in database
    if not User.find_by_identity(userinfo['email']):
        print('why I am here????')
        print(f"\n\n\n{User.find_by_identity(userinfo['email'])}\n\n\n")
        print(f"\n\n\n{userinfo['email']}\n\n\n")
        User.create(
            username=userinfo['nickname'],
            name=userinfo['name'],
            email=userinfo['email'],
            image_link=userinfo['picture']
        )

    # Store the user information in flask session
    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')


@user.route('/login/')
def login():
    return auth0.authorize_redirect(
        redirect_uri=AUTH0_CALLBACK_URL,
        audience=AUTH0_AUDIENCE)


@user.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for(
        'user.login', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@user.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('layout/dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD],
                                                      indent=4))

