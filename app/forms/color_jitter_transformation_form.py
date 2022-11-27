from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


# Style the form
style1 = {'class': 'ColorJitterTransformationForm',
          'style': 'width: 34%; border-radius: 10px; background-color: #d7dbdd; margin-top: 10px; margin-left: 2px;'}
style2 = {'class': 'ColorJitterTransformationForm',
          'style': 'width: 34%; border-radius: 10px; background-color: #d7dbdd; margin-top: 10px; margin-left: 15px;'}
style3 = {'class': 'ColorJitterTransformationForm',
          'style': 'width: 34%; border-radius: 10px; background-color: #d7dbdd; margin-top: 10px; margin-left: 5px;'}
style4 = {'class': 'ColorJitterTransformationForm',
          'style': 'width: 34%; border-radius: 10px; background-color: #d7dbdd; margin-top: 10px; margin-left: 43px;'}


class ColorJitterTransformationForm(FlaskForm):
    brightness = FloatField('brightness', validators=[NumberRange(min=0)], render_kw=style1)
    contrast = FloatField('contrast', validators=[NumberRange(min=0)], render_kw=style2)
    saturation = FloatField('saturation', validators=[NumberRange(min=0)], render_kw=style3)
    hue = FloatField('hue', validators=[NumberRange(min=0, max=0.5)], render_kw=style4)
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
