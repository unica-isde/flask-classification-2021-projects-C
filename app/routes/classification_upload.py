from flask import render_template, flash, request, redirect

from app import app
from app.forms.classification_upload_form import ClassificationUploadForm
from config import Configuration
from werkzeug.utils import secure_filename
from ml.classification_utils import add_classification_job
import os
from app.utils.allowed_file import allowed_file

config = Configuration()


@app.route('/classification_upload', methods=['GET', 'POST'])
def classification_upload():
    """API for selecting a model and uploading an image and running a
        classification job. Returns the output scores from the
        model."""
    form = ClassificationUploadForm()
    if form.validate_on_submit():  # POST
        image = form.image.data

        # The files that have no name are not saved
        if image.filename == '':
            flash('The file has no name')
            return redirect(request.url)

        # The uploaded image is saved
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(config.image_folder_path, filename))
            return add_classification_job(filename, form.model.data)
        else:
            flash('File format not supported. Pleas use png, jpg or jpeg')
            return redirect(request.url)

    return render_template('classification_select_upload.html', form=form)
