from flask import jsonify
from app import app
from app.extensions import db
from app.awx_service.celery import celery
from app.models.kong_gateway_provision import KongGatewayProvision
import requests

@celery.task
def async_launch_workflow_template(consumer_id):
    provision_to_update = db.get_or_404(KongGatewayProvision, consumer_id)
    
    awx_url = f"http://{app.config["AWX_HOST"]}:{app.config["AWX_PORT"]}/api/v2/workflow_job_templates/{app.config["AWX_TEMPLATE_ID"]}/launch/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "limit": "testnodes",
    }
    
    response = requests.post(
        awx_url, headers=headers, 
        json=payload, 
        auth=(app.config["AWX_USERNAME"], app.config["AWX_PASSWORD"])
    )
    
    if response.status_code == 201:
        provision_to_update.workflow_job = response.json().get('workflow_job')
    else:
        app.logger.error(f"Failed to launch workflow template for consumer_id {consumer_id}. "
                         f"Status code: {response.status_code}, Response: {response.text}")

    db.session.commit()