from app.blueprints.api.v1 import bp
from app.models.kong_gateway_provision import KongGatewayProvision
from app.extensions import db
from flask import request, jsonify

@bp.route("/webhooks/awx", methods=["PUT"])
def awx_webhook():
    data = request.get_json()
    workflow_job = data.get("id")
    update_status = data.get("status")
    
    provision_to_update = db.session.execute(db.select(KongGatewayProvision).where(KongGatewayProvision.workflow_job == workflow_job)).scalar()
    provision_to_update.status = update_status
    db.session.commit()
    
    return jsonify({"msg": "Webhook received!", "workflow_job": workflow_job, "update_status": update_status})