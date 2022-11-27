from flask import render_template

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import add_classification_job
from config import Configuration

config = Configuration()


@app.route('/classifications', methods=['GET', 'POST'])
def classifications():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""
    form = ClassificationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data

        return add_classification_job(image_id, model_id)
    else:
        # otherwise, it is a get request and should return the
        # image and model selector
        return render_template('classification_select.html', form=form)
