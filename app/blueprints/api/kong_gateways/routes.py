from app.models.kong_gateway_provision import KongGatewayProvision
from app.models.login import User
from app.blueprints.api.kong_gateways import bp
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from app.awx_service.tasks import async_launch_workflow_template
import uuid

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if user:
        return jsonify({"msg": "This username is already registered. Please use a different username or log in."}), 409
    
    password = data.get("password")
    hash_and_salted_password = generate_password_hash(
        password,
        method="pbkdf2:sha256",
        salt_length=8
    )
    
    new_user = User(
        username = username,
        password = hash_and_salted_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Register successfully!", "username": username, "password": password}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
     

@bp.route("/", methods=["POST"])
@jwt_required()
def provision_kong_gw():
    consumer_id = str(uuid.uuid4())
    new_provision = KongGatewayProvision(consumer_id=consumer_id)
    db.session.add(new_provision)
    db.session.commit()
    async_launch_workflow_template.delay(consumer_id)
    return jsonify({"id": consumer_id}), 202
    

@bp.route("/<consumer_id>", methods=["GET"])
@jwt_required()
def get_provision_status(consumer_id):
    kong_gw_provision = db.get_or_404(KongGatewayProvision, consumer_id)
    
    if kong_gw_provision.status is None:
        return jsonify({"msg": "Something went wrong while trying to request to AWX."}), 500
    else:
        return jsonify({"id": consumer_id, "status": kong_gw_provision.status}), 200