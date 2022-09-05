from flask import render_template, url_for, request

from app import app
from config import Configuration
from app.forms.histogram_form import HistogramForm
import base64

conf = Configuration()


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():

    """API for selecting a model and an uploaded image and running a 
    classification job. Returns the output scores from the model."""
    histogram_form = HistogramForm()
    if request.method == "POST":
        print(request.form)
        image_id = request.form.get('image_id')
        if image_id:
            image_url = url_for('static', filename='imagenet_subset/' + image_id)
            return str(image_url)

    # returns the histogram output from the specified model
    return render_template('histogram_output.html', histogram_form=histogram_form, image_id=None)
