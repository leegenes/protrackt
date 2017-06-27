from flask import Flask, request, make_response, abort, jsonify
from app import app
from app.models import Base, Users, UserDetail, Organization, \
    OrganizationDetail
from uuid import uuid4

@pt.route('/api/v0/users/add_user', methods=['POST'])
def add_user():
    content = request.json
    if not content:
        abort(400)
    user = Users()
    user.uuid = uuid.uuid4()
    user.username = content['username']
    user.email = content['email']
    user.password = content['password']
    try:
        db.session.add(user)
        return "New user, {}, added".format(user.username)
    except:
        abort(400, "User, {}, not added. Error on insert to db".format(user.username))

if __name__ == '__main__':
    app.run()
