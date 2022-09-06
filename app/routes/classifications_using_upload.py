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
    
    """API for selecting a model and an uploaded image and running a 
    classification job. Returns the output scores from the model."""
    classication_form = ClassificationForm()

    if request.method == "POST":

        model_id = classication_form.model.data

        uploaded_file = request.files['file']
        uploaded_filename = 'classifications_using_upload_' + uploaded_file.filename
        uploaded_file.save('app/static/imagenet_subset/' + uploaded_filename)

        image_id = uploaded_filename

        if uploaded_file.filename != '':
            redis_url = Configuration.REDIS_URL
            redis_conn = redis.from_url(redis_url)

            with Connection(redis_conn):
                q = Queue(name=Configuration.QUEUE)
                job = Job.create(classify_image, kwargs={
                    "model_id": model_id,
                    "img_id": image_id
                })
                task = q.enqueue_job(job)

            # returns the image classification output from the specified model
            return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())
            
    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_using_upload.html', classication_form=classication_form)
