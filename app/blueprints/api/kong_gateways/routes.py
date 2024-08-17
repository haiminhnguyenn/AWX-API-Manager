from app.models.kong_gateway_provision import KongGatewayProvision
from app.blueprints.api.kong_gateways import bp
from app.extensions import db
from flask import jsonify
from app.awx_service.tasks import async_launch_workflow_template
import uuid

@bp.route("/", methods=["POST"])
def provision_kong_gw():
    consumer_id = str(uuid.uuid4())
    new_provision = KongGatewayProvision(consumer_id=consumer_id)
    db.session.add(new_provision)
    db.session.commit()
    async_launch_workflow_template.delay(consumer_id)
    return jsonify({"id": consumer_id}), 202
    

@bp.route("/<consumer_id>", methods=["GET"])
def get_provision_status(consumer_id):
    kong_gw_provision = db.get_or_404(KongGatewayProvision, consumer_id)
    
    if kong_gw_provision.status is None:
        return jsonify({"message": "Something went wrong while trying to request to AWX."}), 500
    else:
        return jsonify({"id": consumer_id, "status": kong_gw_provision.status}), 200
        
