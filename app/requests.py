from flask import request, make_response, abort, jsonify
from app import app, db, bcrypt
from app.models import Users, Organization
from uuid import uuid4
from datetime import datetime

### USER RELATED REQUESTS ###
@app.route('/')
def hello():
    return 'hello, world'

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
    print(content)
    if not content:
        abort(400)

    user = Users(
        uuid=str(uuid4()),
        username=content['username'],
        email=content['email'],
        password=bcrypt.generate_password_hash(content['password']).decode('utf-8')
        )

    try:
        db.session.add(user)
        db.session.commit()
        return "New user, {}, added".format(user.username)
    except:
        abort(400, "User, {}, not added. Error on insert to db".format(user.username))

### ORGANIZTION RELATED REQUESTS ###
@app.route('/api/v0/users/<uuid>/add_org', methods=['POST'])
def add_org(uuid):
    """Adds new organization for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - start_date: date [required]
    - end_date: date [optional]
    - description: text [optional]
    - name: string [required]
    - address1: string [optional]
    - address2: string [optional]
    - city: string [optional]
    - state: string(2) [optional]
    - zipcode: string(5) [optional]
    - phone: string(10) [optional]
    - website: string(50) [optional]
    
    Creates new organization for with foreign key uuid.
    """

    content = request.json
    if not content or not content['name']:
        abort(400)
    content['start_date'] = datetime.strptime(content['start_date'], '%Y-%m-%d')
    content['uuid'] = uuid
    org = Organization(**content)
    print(org)

    try:
        db.session.add(org)
        db.session.commit()
        return "New org, {}, added for uuid: {}".format(
            org.name, content['uuid'])
    except:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
