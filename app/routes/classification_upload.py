from flask import render_template, flash, request, redirect

from app import app
from app.forms.classification_upload_form import ClassificationUploadForm
from config import Configuration
from werkzeug.utils import secure_filename
from .classifications import classification
import os

config = Configuration()


@app.route('/classification_upload', methods=['GET', 'POST'])
def classification_upload():
    """API for selecting a model and uploading an image and running a
        classification job. Returns the output scores from the
        model."""
    form = ClassificationUploadForm()
    if form.validate_on_submit():  # POST
        # check if the form has the image data part
        if form.image.data is None:
            flash('No image submitted')
            return redirect(request.url)

        image = form.image.data

        # The files that have no name are not saved
        if image.filename == '':
            flash('The file has no name')
            return redirect(request.url)

        # The uploaded image is saved
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(config.image_folder_path, filename))
            return classification(filename, form.model.data)

    return render_template('classification_select_upload.html', form=form)


def allowed_file(filename):
    """Function that checks if the uploaded image's extension is among the allowed ones"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
