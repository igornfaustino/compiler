''' File manipulation '''

from colorpy import error


def read_data_from_file(file_path):
    ''' Read file data

    Args:
        file_path (str): path to the file
    Returns:
        str: file content
        None: invalid file path (print error msg)
    '''

    try:
        in_file = open(file_path, 'r')
        return in_file.read()
    except:
        error('An error occured trying to read the file.')
        return None


def save_data_into_file(file_path, data):
    ''' Save data into a file

    Args:
        file_path (str): path to the file
        data (str): Content to put on the file
    Returns:
        True: every thing goes ok
        False: Have an error (print error msg)
    '''

    try:
        out_file = open(file_path, 'w')
        out_file.write(str(data))
        out_file.close()
        return True
    except IOError:
        error('An error occured trying to read the file.')
        return False
