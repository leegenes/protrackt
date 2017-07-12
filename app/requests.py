from flask import request, make_response, abort, jsonify, url_for
from app import app, db, bcrypt
from app.models import User, Organization, Project, UserDetail, Role, Skill
from uuid import uuid4
import app.protrackt_lib as pl

BASE_URL = '/api/v0'

### USER RELATED REQUESTS ###
@app.route(BASE_URL + '/users', methods=['POST'])
def new_user():
    """Add new user.

    Receives
    - username: string [required; unique]
    - email: string [required; unique]
    - password: string [required]

    Creates new user with login credentials.
    """
    content = request.json

    if not content['username'] or not content['password']:
        return abort(400)
    if User.query.filter_by(username=content['username']).first():
        abort(400)

    user = User(
        uuid=str(uuid4()),
        username=content['username'],
        email=content['email'])
    user.hash_password(content['password'])

    try:
        db.session.add(user)
        db.session.commit()
        return "New user, {}, added".format(user.username)
    except:
        abort(400, "User, {}, not added. Error on insert to db".format(user.username))

#TODO: add filters for dates, companies, jobs, skills, projects, etc.
@app.route(BASE_URL + '/users/<uuid>', methods=['GET'])
def get_user(uuid):
    """Returns user information.

    Receives
    - uuid: uuid4 [required - in URL]

    Outputs user information.
    """
    u = User.query.filter_by(uuid=uuid).first()
    return jsonify({'username': u.username}, 201)

@app.route(BASE_URL + '/users/<uuid>', methods=['POST'])
def update_user(uuid):
    """Updates a user's personal information.

    Receives
    - uuid: uuid4 [required - in URL]
    - first_name: string [optional]
    - last_name: string [optional]
    - preferred_name: string [optional]
    - address1: string [optional]
    - address2: string [optional]
    - city: string [optional]
    - state: two-char string [optional]
    - zipcode: five-char string [optional]

    Updates user information on account.
    """

    content = request.json
    if not content:
        abort(400)

    user_detail = UserDetail.query.filter_by(uuid=uuid).first()
    if not user_detail:
        user_detail = UserDetail(**content)
        user_detail.uuid = uuid
        try:
            db.session.add(user_detail)
            db.session.commit()
            return "Done!"
        except:
            abort(400)
    try:
        user_detail.update(**content)
        db.session.commit()
    except:
        abort(400)


### ORGANIZTION RELATED REQUESTS ###
@app.route(BASE_URL + '/users/<uuid>/org', methods=['POST'])
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
    if not content:
        abort(400)

    org = Organization(**content)
    pl.convert_to_date(org.start_date)
    pl.convert_to_date(org.end_date)
    org.uuid = uuid
    try:
        print("here3")
        db.session.add(org)
        db.session.commit()
        return "New org, {}, added for uuid: {}".format(
            org.name, uuid)
    except:
        print("here4")
        abort(400)

@app.route(BASE_URL + '/users/<uuid>/org/<org_id>', methods=['POST'])
def update_org(uuid, org_id):
    """Updates organization for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - org_id: integer [required - in URL]
    - start_date: date [optional - cannot be null]
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

    Updates organization for with foreign key uuid.
    """
    content = request.json
    # content['end_date'] = pl.convert_to_date(content['end_date']).date()
    print(content)
    org = Organization.query.filter_by(id=org_id).first()
    print(org.id)
    try:
        pl.write_requested_attributes(org, content)
        db.session.commit()
        return "Success"
    except:
        print("failed")
        abort(400)


@app.route(BASE_URL + '/users/<uuid>/role', methods=['POST'])
def add_role(uuid):
    """ Adds new role for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - start_date: date [required]
    - end_date: date [optional]
    - title: string [required]
    - description: text [optional]
    - org_id: integer [required]

    Create a new role within an organization for a user.
    """

    content = request.json
    if not content:
        abort(400)

    role = Role(**content)
    role.start_date = pl.convert_to_date(role.start_date).date()
    role.end_date = pl.convert_to_date(role.end_date).date()
    role.uuid = uuid

    try:
        db.session.add(role)
        db.session.commit()
        return "New role, {}, added to org, {}, for uuid: {}".format(
            role.title, role.org_id, role.uuid)
    except:
        abort(400)

@app.route(BASE_URL + '/users/<uuid>/role/<role_id>', methods=['POST'])
def update_role(uuid, role_id):
    content = request.json

    if not content:
        abort(400)

    role = Role.query.filter_by(id=role_id).first()
    role.id = role_id

    try:
        pl.write_requested_attributes(role, content)
        db.session.commit()
        return "Successful POST"
    except:
        abort(400)



@app.route(BASE_URL + 'users/<uuid>/project', methods=['POST'])
def add_project(uuid):
    """Adds new project for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - start_date: date [required]
    - end_date: date [optional]
    - name: string [required]
    - description: text [optional]
    - role_id: integer [required]

    Create a new project associated to uuid and position/role/degree
    """

    content = request.json
    if not content:
        abort(400)

    content['start_date'] = pl.convert_to_date(content['start_date'])

    project = Project(**content)
    pl.convert_to_date(project.start_date).date()
    pl.convert_to_date(project.end_date).date()
    try:
        db.session.add(project)
        db.session.commit()
    except:
        abort(400)

@app.route(BASE_URL + '/skill', methods=["POST"])
def add_skill():
    content = request.json

    if not content or 'name' not in content:
        abort(400)

    if not Skill.query.filter_by(name=content['name']).first():
        skill = Skill(**content)
        try:
            db.session.add(skill)
            db.session.commit()
            return "Skill added"
        except:
            abort(400)
    else:
        abort(400, "Skill already exists")

@app.route(BASE_URL + '/skill/<skill_id>', methods=["GET"])
def get_skill(skill_id):
    skill = Skill.query.filter_by(id=skill_id).first()
    return jsonify(skill_id=skill.id,
                    skill=skill.name)



if __name__ == '__main__':
    app.run(debug=True)
