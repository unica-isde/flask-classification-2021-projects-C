import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()


@app.route('/classification_upload', methods=['GET', 'POST'])
def classification_upload():
    """API for selecting a model and uploading an image and running a
        classification job. Returns the output scores from the
        model."""
    return