from app.blueprints.api.v1 import bp
from app.models.kong_gateway_provision import KongGatewayProvision
from app.extensions import db
from flask import request, jsonify, abort
import logging


logger = logging.getLogger(__name__)


@bp.route("/webhooks/awx", methods=["PUT"])
def awx_webhook():
    data = request.get_json()
    if not data:
        logger.error("No JSON data received")
        abort(400, description="No JSON data received")
    
    workflow_job = data.get("id")
    update_status = data.get("status")
    
    if not workflow_job or not update_status:
        logger.error("Missing required data: 'id' or 'status'")
        abort(400, description="Missing required data: 'id' or 'status'")
    
    try:   
        provision_to_update = db.session.execute(
            db.select(KongGatewayProvision).where(KongGatewayProvision.workflow_job == workflow_job)
        ).scalar()
        
        if not provision_to_update:
            logger.error(f"No Kong Gateway Provision found for workflow_job {workflow_job} just received")
            abort(404, description=f"No record found for workflow_job {workflow_job}")
            
        provision_to_update.status = update_status
        db.session.commit()
        logger.info(f"Updated status for workflow_job {workflow_job} to {update_status}")
    
    except Exception as e:
        logger.error(f"Error processing webhook for workflow_job {workflow_job}: {str(e)}")
        abort(500, description="Internal Server Error")
    
    return jsonify({"msg": "Webhook received!", "workflow_job": workflow_job, "update_status": update_status})