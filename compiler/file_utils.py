from colorpy import error

def read_data_from_file(file_path):
    try:
        in_file = open(file_path, 'r')
        return in_file.read()
        in_file.close()
    except:
        error('An error occured trying to read the file.')
        exit(-1)

def save_data_into_file(file_path, data):
    try:
        out_file = open(file_path, 'w')
        out_file.write(str(data))
        out_file.close()
    except IOError:
        error('An error occured trying to read the file.')
        exit(-1)