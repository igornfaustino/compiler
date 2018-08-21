def read_data_from_file(file_path):
    try:
        in_file = open(file_path, 'r')
        return in_file.read()
    except IOError:
        return print('An error occured trying to read the file.')
    finally:
        in_file.close()


def save_data_into_file(file_path, data):
    try:
        out_file = open(file_path, 'w')
        out_file.write(str(data))
    except IOError:
        return print('An error occured trying to read the file.')
    finally:
        out_file.close()
