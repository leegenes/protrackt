from flask import request, make_response, abort, jsonify
from app import app, db, bcrypt
from app.models import Users, Organization, Project
from uuid import uuid4
import app.protrackt_lib as pl

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

@app.route('/api/v0/users/<uuid>/add_project', methods=['POST'])
def add_project(uuid):
    """Adds new project for given user.

    Receives
    - uuid: uuid4 [required - in URL]
    - start_date: date [required]
    - end_date: date [optional]
    - name: string [required]
    - description: text [optional]
    - tags: array [optional]

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
