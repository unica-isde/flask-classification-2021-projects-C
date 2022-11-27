from flask import render_template

import torchvision.transforms as T
import torchvision.transforms.functional as TF
import os

from app import app
from app.forms.color_jitter_transformation_form import ColorJitterTransformationForm
from ml.classification_utils import fetch_image
from config import Configuration
import torchvision.utils

config = Configuration()


@app.route('/color_jitter_transformation', methods=['GET', 'POST'])
def color_jitter_transformation():

    """API for setting up the values of the parameters
    for the color jitter transformation to be applied
    to the selected image. Returns the transformed
    image."""

    form = ColorJitterTransformationForm(brightness=1, saturation=1, contrast=1, hue=0)
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        brightness_value = form.brightness.data
        contrast_value = form.contrast.data
        saturation_value = form.saturation.data
        hue_value = form.hue.data

        # Get the image associated with the specified ID
        image = fetch_image(image_id)

        # Convert PIL Image into tensor
        tensor_transform = T.ToTensor()

        # Apply the transform to the image according to the selected transformation parameters
        image = image.convert('RGB')
        transformed_image = tensor_transform(image)
        transformed_image = TF.adjust_brightness(transformed_image, brightness_value)
        transformed_image = TF.adjust_contrast(transformed_image, contrast_value)
        transformed_image = TF.adjust_saturation(transformed_image, saturation_value)
        transformed_image = TF.adjust_hue(transformed_image, hue_value)

        # Close the image
        image.close()

        # Check whether the specified path is in an existing directory or not
        if not os.path.isdir(config.transformed_image_folder_path):

            # Create the directory in the specified path if it does not exist
            os.mkdir(config.transformed_image_folder_path)

        # Setup explicitly the image format to avoid format misunderstanding
        id = image_id.replace('.JPEG', '.JPEG')

        # Create the new name for the image according to the applied transformation parameters
        img_name = "transform__" + "{}_{}_{}_{}".format(str(brightness_value), str(contrast_value),
                                                        str(saturation_value), str(hue_value)) + "__" + id

        # Create the path where to save the new image
        new_path = os.path.join(config.transformed_image_folder_path, img_name)

        # Save the given tensor into an image file
        torchvision.utils.save_image(transformed_image, new_path)

        # returns the transformed image
        return render_template("color_jitter_transformation_output.html", img_name=img_name)

    # otherwise, it is a get request and should return the
    # image and color jitter transformation selector
    return render_template('image_and_color_jitter_transformation_select.html', form=form)
