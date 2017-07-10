from flask import request, make_response, abort, jsonify
from app import app, db, bcrypt
from app.models import Users, Organization, Project
from uuid import uuid4
import app.protrackt_lib as pl

BASE_URL = '/api/v0'
CREATE_URL = BASE_URL + '/users/<uuid>/create'

### USER RELATED REQUESTS ###
@app.route(BASE_URL + '/create_user', methods=['POST'])
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

#TODO: add filters for dates, companies, jobs, skills, projects, etc.
@app.route(BASE_URL + '/users/<uuid>', methods=['GET'])
def get_user(uuid):
    """Returns user information.

    Receives
    - uuid: uuid4 [required - in URL]

    Outputs user information.
    """

    return User.query.filter_by(uuid).first()

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

    try:
        user_detail = UserDetail.query.filter_by(uuid).first()
        user_detail.update(**content)
    except:
        abort(400)


### ORGANIZTION RELATED REQUESTS ###
@app.route(CREATE_URL + '/org', methods=['POST'])
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

    content['start_date'] = pl.convert_to_date(content['start_date'])
    content['end_date'] = pl.convert_to_date(content['end_date'])

    org = Organization(**content)

    try:
        db.session.add(org)
        db.session.commit()
        return "New org, {}, added for uuid: {}".format(
            org.name, uuid)
    except:
        abort(400)

@app.route(CREATE_URL + '/role', methods=['POST'])
def add_role(uuid):
    """ Adds new role for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - start_date: date [required]
    - end_date: date [optional]
    - name: string [required]
    - description: text [optional]
    - org_id: integer [required]

    Create a new role within an organization for a user.
    """

    content = request.json
    if not content or not content['']


@app.route(CREATE_URL + '/project', methods=['POST'])
def add_project(uuid):
    """Adds new project for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - start_date: date [required]
    - end_date: date [optional]
    - name: string [required]
    - description: text [optional]
    - tags: array [optional]
    - role_id: integer [required]

    Create a new project associated to uuid and position/role/degree
    """

    content = request.json
    if not content or not content['name']:
        abort(400)

    content['start_date'] = pl.convert_to_date(content['start_date'])

    project = Project({
        'name': content['name'],
        'start_date': pl.convert_to_date(content['start_date']),
        'end_date': pl.convert_to_date(content['start_date']),
        'description': content['description']
        })

    skills = []
    for s in content['skills']:
        skill = Skill({'name': s})

        project_skill = ProjectSkill({
            'project_id': project.id,
            'skill_id': skill.id
            })

        skills.append({'skill': skill, 'project_skill': project_skill})

    try:
        db.session.add(project)
        for skill in skills:
            db.session.add(skill['skill'])
            db.session.add(skill['project_skill'])
        db.session.commit()
        return "New project {} added for uuid {}".format(
            project.name, uuid)
    except:
        abort(400)



if __name__ == '__main__':
    app.run(debug=True)
