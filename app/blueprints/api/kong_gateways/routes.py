from app.models.kong_gateway_provision import KongGatewayProvision
from app.models.login import User
from app.blueprints.api.kong_gateways import bp
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required
from app.tasks import async_launch_workflow_template
import uuid
import logging


logger = logging.getLogger(__name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        logger.error("No JSON data received")
        abort(400, description="No JSON data received")
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        logger.error("Missing required data: 'username' or 'password'")
        abort(400, description="Missing required data: 'username' or 'password'")
    
    user = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar()
    
    if user:
        logger.error("Username already exists")
        return jsonify({"msg": "This username is already registered. Please use a different username or log in."}), 409
    
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
    logger.info(f'Add new user with "username": {username}, "password": {hash_and_salted_password} into database.')
    
    return jsonify({"msg": "Register successfully!", "username": username, "password": password}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        logger.error("No JSON data received")
        abort(400, description="No JSON data received")
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        logger.error("Missing required data: 'username' or 'password'")
        abort(400, description="Missing required data: 'username' or 'password'")
    
    user = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar()
    
    if not user or not check_password_hash(user.password, password):
        logger.error("Bad username or password")
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
     

@bp.route("/", methods=["POST"])
@jwt_required()
def provision_kong_gw():
    try:
        consumer_id = str(uuid.uuid4())
        
        new_provision = KongGatewayProvision(consumer_id=consumer_id)
        db.session.add(new_provision)
        db.session.commit()
        logger.info(f"Add new Kong Gateway Provision with consumer_id {consumer_id} to database.")
        
        async_launch_workflow_template.delay(consumer_id)
        
        return jsonify({"id": consumer_id}), 202
    
    except Exception as e:
        logger.error(f"Error provisioning Kong Gateway: {str(e)}")
        return jsonify({"msg": "Internal Server Error"}), 500
    

@bp.route("/<consumer_id>", methods=["GET"])
@jwt_required()
def get_provision_status(consumer_id):
    try:
        kong_gw_provision = db.session.execute(
            db.select(KongGatewayProvision).where(KongGatewayProvision.consumer_id == consumer_id)
        ).scalar()
        
        if not kong_gw_provision:
            logger.error(f"No provision found for the provided consumer_id {consumer_id}.")
            return jsonify({"msg": f"No provision found for the provided consumer_id {consumer_id}."}), 404
    
        if kong_gw_provision.status is None:
            logger.error("Status is not yet available. Something went wrong while trying to request to AWX.")
            return jsonify({"msg": "Status is not yet available. Something went wrong while trying to request to AWX."}), 500

        return jsonify({"id": consumer_id, "status": kong_gw_provision.status}), 200
    
    except Exception as e:
        logger.error(f"Error retrieving provision status for consumer_id {consumer_id}: {str(e)}")
        return jsonify({"msg": "Internal Server Error. Unable to retrieve provision status."}), 500