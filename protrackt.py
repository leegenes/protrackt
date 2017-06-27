from flask import Flask, request, make_response, abort, jsonify
from app import pt
from app.models import Base, User
from sqlalchemy import create_engine, update

@pt.route('/api/v0/users/add_user', methods=['POST'])
def add_user():
    content = request.json
    if not content:
        abort(400)
    user = User()
    user.username = content['username']
    user.email = content['email']
    user.password = content['password']

    return "New user, {}, added".format(user.username)

if __name__ == '__main__':
    pt.run()
