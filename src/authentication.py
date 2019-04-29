from flask import Flask, request, Response
from flask import request
import requests as http_request
from hashlib import sha256
import json
import os

ip_adress = os.environ.get("USER_PERSISTENCE_URL") # "http://10.240.20.108:5001"
PERSISTANCE_API = "/innoreports/user"

app = Flask(__name__)

@app.route('/innoreports/login', methods=['POST', 'GET'])
def login():
    response = {'status': " ", 'message': " ", 'token': " " }   # answer to the client
    if request.method != 'POST':
        return Response (json.dumps(response), status=401)

    user_login = str(request.form['login'])
    password = str(request.form['password'])

#    user_login = request.args.get('login', '')
#    password = request.args.get('password', '')

    if len(user_login) < 3 or len(password) < 3:
        response['status'] = 'Error'
        response['message'] = 'Login or password is incorrect!'
        return Response (json.dumps(response), status=401)

    user = __get_user_data(user_login)
    if user is None:
        response['status'] = 'Error'
        response['message'] = "The user with such email doesn't exists!"
        return Response (json.dumps(response), status=401)
    if user['password'] != password:
        response['status'] = 'Error'
        response['message'] = "The password is incorrect!"
        return Response (json.dumps(response), status=401)

    token = sha256(user_login.encode() + password.encode()).hexdigest()
    if not __update_token(user_login, token):
        response['status'] = 'Error'
        response['message'] = "Some problems occurred during the token obtaining"
        return Response (json.dumps(response), status=409)

    response['status'] = "Success"
    response['message'] = "You have successfully logged in!"
    response['token'] = token
    response['email'] = user_login
    return Response (json.dumps(response), status=200)


def __get_user_data(login):
    """
    requests the user data from persistence
    :param login: user login to be checked
    :return: user data in success case, else returns None
    """
    data = {'email': login}
    response = http_request.post(url=ip_adress + PERSISTANCE_API + '/getUser', data=data)
    print (response)
    if response.status_code != 200:
    	return None
    user_t = response.text.replace("'",'"')
    user = json.loads(user_t)
    return user


def __update_token(email, token):
    # mock start
    # return True
    # mock end
    data = {'email': email, 'token': token}
    response = http_request.put(url=ip_adress + PERSISTANCE_API + '/updateToken', json=data)
    if response.status_code != 200:
    	return False
    return True
