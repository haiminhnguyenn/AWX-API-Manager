from dotenv import load_dotenv
import requests

from pathlib import Path
import logging
import os

from . import celery
from app.extensions import db
from app.models.kong_gateway_provision import KongGatewayProvision


env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


@celery.task
def async_launch_workflow_template(consumer_id):
    try:
        provision_to_update = db.session.execute(
            db.select(KongGatewayProvision).where(KongGatewayProvision.consumer_id == consumer_id)
        ).scalar()

        if provision_to_update is None:
            logging.error(f"No Kong Gateway Provision found for consumer_id {consumer_id}.")
            return
    
        awx_url = os.environ.get("AWX_URL")
        response = requests.post(
            awx_url, 
            auth=(os.environ.get("AWX_USER"), os.environ.get("AWX_PASSWORD")),
            timeout=900
        )
    
        if response.status_code == 201:
            provision_to_update.workflow_job = response.json().get('workflow_job')
            db.session.commit()
            logging.info(f"Workflow template launched successfully for consumer_id {consumer_id}.")
        else:
            logging.error(f"Failed to launch workflow template for consumer_id {consumer_id}. "
                         f"Status code: {response.status_code}, Response: {response.text}")
    
    except requests.RequestException as e:
        logging.error(f"Request to AWX failed for consumer_id {consumer_id}: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected error occurred for consumer_id {consumer_id}: {str(e)}")