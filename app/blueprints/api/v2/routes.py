from app.blueprints.api.v2 import bp
from models.kong_gateway_provision import KongGatewayProvision
from app.extensions import db
from flask import request, jsonify

@bp.route("/awx-webhook", methods=["POST"])
def awx_webhook():
    data = request.get_json()
    workflow_job = data.get("id")
    update_status = data.get("status")
    
    provision_to_update = db.session.execute(db.select(KongGatewayProvision).where(KongGatewayProvision.workflow_job == workflow_job)).scalar()
    provision_to_update.status = update_status
    
    return jsonify({"message": "Webhook received!", "workflow_job": workflow_job, "update_status": update_status})
    