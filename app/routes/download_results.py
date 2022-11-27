import json
from flask import Response

from app import app
from config import Configuration
from .classifications_id import classifications_id

config = Configuration()


@app.route('/download_results/<string:job_id>', methods=['GET'])
def download_results(job_id):

    """API for downloading the results associated with the classification
    job identified by the id specified in the path. Returns the output
    labels and scores from the model as a JSON file."""

    response = classifications_id(job_id)
    result = dict()

    # Convert the result of the classification into a dictionary to facilitate its conversion to JSON
    if response['data'] != None:
        for i in response['data']:
            result[i[0]] = i[1]

    # Convert the result of the classification to JSON format
    json_results = json.dumps(result)

    return Response(json_results,
                    mimetype='application/json',
                    headers={'Content-Disposition':'attachment;filename=Results'})
