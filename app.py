from flask import Flask, request, jsonify, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
import requests
import uuid

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend-server.db'

db = SQLAlchemy(app)

class Provision(db.Model):
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    workflow_job: Mapped[int] = mapped_column(Integer, unique=True)


with app.app_context():
    db.create_all()

users = {
    "user": generate_password_hash("password")
}

AWX_HOST = '10.240.224.64'
AWX_PORT = '32375'
AWX_USERNAME = 'admin'
AWX_PASSWORD = 'HO8djiFzRHNdN40alSzvCrpYlE0GEB5p'
AWX_TEMPLATE_ID = '15'

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@app.route('/api/kong_gateways', methods=['POST'])
@auth.login_required
def provision_kong_gw():
    provision_id = str(uuid.uuid4())
    
    awx_url = f"http://{AWX_HOST}:{AWX_PORT}/api/v2/workflow_job_templates/{AWX_TEMPLATE_ID}/launch/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "limit": "testnodes",
    }
    
    response = requests.post(awx_url, headers=headers, json=payload, auth=(AWX_USERNAME, AWX_PASSWORD))
    
    if response.status_code == 201:
        workflow_job = response.json().get('workflow_job')
        provision = Provision(id=provision_id, workflow_job=workflow_job)
        db.session.add(provision)
        db.session.commit()
        return jsonify({"id": provision_id}), 201
    else:
        abort(response.status_code)


@app.route('/api/kong_gateways/<provision_id>/', methods=['GET'])
@auth.login_required
def get_provision_status(provision_id):
    provision = Provision.query.get(provision_id)
    if not provision:
        abort(404)
    
    awx_url = f"http://{AWX_HOST}:{AWX_PORT}/api/v2/workflow_jobs/{provision.workflow_job}/"
    response = requests.get(awx_url, auth=(AWX_USERNAME, AWX_PASSWORD))
    
    if response.status_code == 200:
        status = response.json().get('status')
        return jsonify({"id": provision_id, "status": status}), 200
    else:
        abort(response.status_code)


if __name__ == '__main__':
    app.run(debug=True)