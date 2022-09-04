from app import app
from flask import render_template, request
from config import Configuration
from ml.classification_utils import classify_image
from app.forms.classification_form import ClassificationForm
from rq.job import Job
import redis
from rq import Connection, Queue

config = Configuration()

@app.route('/classifications_using_upload', methods=['GET', 'POST'])
def classificationsUsingUpload():
    pass