ALLOWED_EXTENSIONS = ['csv']
UPLOADS_FOLDER = 'Userfiles/'
DOWNLOADS_FOLDER = 'PREDICTIONS/'
ERROR_FOLDER = 'invalid_file/'

def file_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS