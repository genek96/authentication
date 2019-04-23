from flask import Flask
from flask import request
import requests as http_request
from hashlib import sha256
import json

PERSISTANCE_API = "/innoreports/user"

app = Flask(__name__)

@app.route('/innoreports/login', methods=['POST', 'GET'])
def login():
    response = {'status': None, 'message': None, 'data': {}}   # answer to the client
    if request.method != 'POST':
        return 'Error request type'

    user_login = str(request.form['login'])
    password = str(request.form['password'])

#    user_login = request.args.get('login', '')
#    password = request.args.get('password', '')

    if len(user_login) < 3 or len(password) < 3:
        response['status'] = 'Error'
        response['message'] = 'Login or password is incorrect!'
        return json.dumps(response)

    user = __get_user_data(user_login)
    if user is None:
        response['status'] = 'Error'
        response['message'] = "The user with such email doesn't exists!"
        return json.dumps(response)
    if user['password'] != password:
        response['status'] = 'Error'
        response['message'] = "The password is incorrect!"
        return json.dumps(response)

    token = sha256(user_login.encode() + password.encode()).hexdigest()
    if not __update_token(user_login, token):
        response['status'] = 'Error'
        response['message'] = "Some problems occurred during the token obtaining"
        return json.dumps(response)

    response['status'] = "Success"
    response['message'] = "You have successfully logged in!"
    response['data']['token'] = token
    return json.dumps(response)


def __get_user_data(login):
    """
    requests the user data from persistence
    :param login: user login to be checked
    :return: user data in success case, else returns None
    """
    # mock start
    user = {'email': login, 'password': 'admin'}
    return user
    # mock end
    data = {'login': login}
    response = http_request.post(url=PERSISTANCE_API + '/getUser', data=data)
    user = response.json()
    if user['email'] == "":
        return None
    return user


def __update_token(email, token):
    # mock start
    return True
    # mock end
    data = {'email': email, 'token': token}
    response = http_request.put(url=PERSISTANCE_API + '/updateToken', data=data).json()
    if response is None:
        return False
    return True
