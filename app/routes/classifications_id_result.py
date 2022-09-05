from app import app
from flask import render_template, Response
from .classifications_id import classifications_id
import json


@app.route('/classifications/result/<string:job_id>/<string:filename>/', methods=['GET'])
def classifications_id_result_to_json(job_id, filename):

    """API for selecting a model and an uploaded image and running a 
    classification job. Returns the output scores from the model."""
    response = classifications_id(job_id)

    result = {}
    for key, value in response['data']:
        result[key] = value

    # returns the json output of classification scores
    return Response(json.dumps(result, indent=4), mimetype='application/json', headers={"Content-disposition": f"attachment; filename={'_'.join(filename.split('.')[:-1])}_result.json"})
