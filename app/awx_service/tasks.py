from flask import current_app
from celery import Celery
from app.extensions import db
from app.models.kong_gateway_provision import KongGatewayProvision
import requests
import logging

celery = Celery("tasks", broker="amqp://localhost") #amqp://guest:guest@localhost:5672//
logger = logging.getLogger(__name__)

@celery.task
def async_launch_workflow_template(consumer_id):
    with current_app.app_context():
        provision_to_update = db.get_or_404(KongGatewayProvision, consumer_id)
    
        awx_url = f"https://awx-stg.apigw.fptcloud.com/api/v2/workflow_job_templates/11/launch/"
        response = requests.post(awx_url, auth=("demo-kongservice-exe", "p8PWczX0C0AocWohR3ow"))
    
        if response.status_code == 201:
            provision_to_update.workflow_job = response.json().get('workflow_job')
        else:
            logger.error(f"Failed to launch workflow template for consumer_id {consumer_id}. "
                         f"Status code: {response.status_code}, Response: {response.text}")

        db.session.commit()