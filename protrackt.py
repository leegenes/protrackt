from flask import Flask, request, make_response, abort, jsonify
from app import app
from app.models import Base, Users, UserDetail, Organization, \
    OrganizationDetail
from uuid import uuid4

### USER RELATED REQUESTS ###
@app.route('/api/v0/users/add_user', methods=['POST'])
def add_user():
    """Add new user.

    Receives
    - username: string [required; unique]
    - email: string [required; unique]
    - password: string [required]

    Creates new user with login credentials.
    """
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

@app.route('/api/v0/users/get_user/<id>', methods=['GET']):
def get_user(id):
    # TODO: return object of all
    # {user: {organizations:
    #   [{org:
    #       {name:
    #       projects:
    #           [{name:,
    #           start_date:,
    #           end_date:,
    #           skills: [],
    #           desctiption:}]
    #       start_date:
    #       end_date:
    #       type: ed/volunteer/work
    #       address1:
    #       ...}}]}}
    pass

### ORGANIZTION RELATED REQUESTS ###
@app.route('/api/v0/users/<id>/add_org', methods=['POST'])
def add_org(id):
    """Adds new organization for given user.

    Receives
    - uuid: uuid4 [required]
    - organization: string [required]
    - type: string [required from education, work, volunteer]}
    Creates new organization for user to build projects to.
    """
    content = request.json
    if not content:
        abort(400)
    org = Organization()
    org.name = content['name']
    org.type = content['org_type']

    try:
        db.session.add(org)
        return "New org, {}, added for uuid: {}".format(
            org.name, content['uuid'])
    except:
        abort(400, )

if __name__ == '__main__':
    app.run()
