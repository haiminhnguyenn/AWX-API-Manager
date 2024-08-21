from . import celery
from app.extensions import db
from app.models.kong_gateway_provision import KongGatewayProvision
import requests
import logging


logger = logging.getLogger(__name__)


@celery.task
def async_launch_workflow_template(consumer_id):
    try:
        provision_to_update = db.session.execute(
            db.select(KongGatewayProvision).where(KongGatewayProvision.consumer_id == consumer_id)
        ).scalar()

        if provision_to_update is None:
            logger.error(f"No Kong Gateway Provision found for consumer_id {consumer_id}.")
            return
    
        awx_url = f"https://awx-stg.apigw.fptcloud.com/api/v2/workflow_job_templates/11/launch/"
        response = requests.post(
            awx_url, 
            auth=("demo-kongservice-exe", "p8PWczX0C0AocWohR3ow"),
            timeout=30
        )
    
        if response.status_code == 201:
            provision_to_update.workflow_job = response.json().get('workflow_job')
            db.session.commit()
            logger.info(f"Workflow template launched successfully for consumer_id {consumer_id}.")
        else:
            logger.error(f"Failed to launch workflow template for consumer_id {consumer_id}. "
                         f"Status code: {response.status_code}, Response: {response.text}")
    
    except requests.RequestException as e:
        logger.error(f"Request to AWX failed for consumer_id {consumer_id}: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error occurred for consumer_id {consumer_id}: {str(e)}")