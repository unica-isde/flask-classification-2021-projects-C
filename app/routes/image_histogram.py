from flask import render_template

from app import app
from app.forms.image_histogram_form import HistogramForm
from config import Configuration

config = Configuration()


@app.route('/image_histogram_select', methods=['GET', 'POST'])
def image_histogram_select():
    """API for selecting an image. The histogram of the selected image is then calculated in the frontend"""
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data

        # returns the template that renders the image histogram
        return render_template("image_histogram_output.html", image_id=image_id)

    # otherwise, it is a get request and should return the
    # image selector
    return render_template('image_histogram_select.html', form=form)