from flask import Response

from app import app
from config import Configuration
from .classifications_id import classifications_id

import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg

config = Configuration()

def create_plot_from_results(labels, scores):

    """Returns the plot associated with the results of a
    classification as a horizontal bar chart."""

    # Create a list containing all labels to construct the y-axis
    y = list(labels)

    # Create a list containing all the scores to construct the x-axis
    x = list(scores)

    fig, ax = plt.subplots(facecolor='#e3e3e3')

    # Construct bar chart reflecting the characteristics of the interface plot
    ax.grid(b=True, color='grey', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.barh(y, x, align='center', color=['#1A4A04', '#750014', '#795703', '#06216C', '#3F0355'],
            edgecolor=['#1A4A04', '#750014', '#795703', '#06216C', '#3F0355'], linewidth=1)

    # Set the facecolor of the axes
    ax.set_facecolor('#e3e3e3')

    # Set ticks for the x-axis
    ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

    # Show labels read top-to-bottom
    ax.invert_yaxis()

    # Set legend
    plt.legend(['Output scores'], loc='upper center', bbox_to_anchor=(0.5, 1.2), facecolor='#e3e3e3')

    # Fit the plot within the figure cleanly through automatic parameters' adjustment
    fig.tight_layout()

    return fig


@app.route('/download_plot/<string:job_id>', methods=['GET'])
def download_plot(job_id):

    """API for downloading the plot of the results associated with the
        classification job identified by the id specified in the path.
        Returns a bar chart of the top-5 classification output from
        the model as a PNG image."""

    # Retain bytes of data in a memory buffer
    with io.BytesIO() as output_image:
        response = classifications_id(job_id)
        result = dict()

        # Convert the result of the classification into a dictionary to facilitate the recovery of labels and scores
        if response['data'] != None:
            for i in response['data']:
                result[i[0]] = i[1]

        # Create the plot based on the classification output labels and scores
        plot = create_plot_from_results(result.keys(), result.values())

        # Write the figure to a PNG file object rendered by the memory buffer
        FigureCanvasAgg(plot).print_png(output_image)

        return Response(output_image.getvalue(),
                    mimetype='image/png',
                    headers={'Content-Disposition':'attachment;filename=Plot'})