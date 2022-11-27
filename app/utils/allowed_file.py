from config import Configuration

config = Configuration()

def allowed_file(filename):
    """Function that checks if the uploaded image's extension is among the allowed ones"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
