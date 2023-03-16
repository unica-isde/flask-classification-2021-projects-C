from flask import render_template, flash, request, redirect

from app import app
from app.forms.classification_upload_form import ClassificationUploadForm
from config import Configuration
from werkzeug.utils import secure_filename
from ml.classification_utils import add_classification_job
import os
from app.utils.allowed_file import allowed_file
import datetime
from datetime import datetime, timedelta
from dateutil import tz

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

        # The uploaded image is saved with time
        if image and allowed_file(image.filename):
            date_string = datetime.now().replace(tzinfo=tz.tzlocal()).strftime("%Y-%m-%d-%H-%M")
            name = 'uploaded_' + date_string + '_' + image.filename

            filename = secure_filename(name)
            image.save(os.path.join(config.image_folder_path, filename))
            return add_classification_job(filename, form.model.data)
        else:
            flash('File format not supported. Pleas use png, jpg or jpeg')
            return redirect(request.url)

    # Uploaded images get checked, if uploaded 10 minutes ago or earlier they get deleted
    uploaded_images = filter(lambda x: x.lower().startswith('uploaded'), os.listdir(config.image_folder_path))
    for i in uploaded_images:
        date = datetime.strptime(i.split("_")[1], '%Y-%m-%d-%H-%M')
        from_zone = tz.tzlocal()
        to_zone = tz.tzutc()
        date.replace(tzinfo=from_zone)

        if date.astimezone(to_zone) < datetime.utcnow().replace(tzinfo=to_zone) + timedelta(minutes=-10):
            try:
                os.remove(config.image_folder_path + '/' + i)
            except FileNotFoundError:
                pass

    return render_template('classification_select_upload.html', form=form)
