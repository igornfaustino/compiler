''' Module to print colors outputs for error and warnings
'''

from Config import Config

def warning(text):
    ''' Print warnings

    - Only print warnings if Config.silence is false

    Args:
        text (str): Warning's text
    Output:
        "Warning: %s" % text
    '''
    if (not Config.silence):
        print('\033[93mWarning: ' + text + '\033[0m', end="\n\n")

def error(text):
    ''' Print errors

    Args:
        text (str): Error's text
    Output:
        "Error: %s" % text
    '''
    print('\033[91mError: ' + text + '\033[0m', end="\n\n")
