from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class ClassificationUploadForm(FlaskForm):
    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    image = FileField('Upload your image...', validators=[DataRequired()])
    submit = SubmitField('Submit')
