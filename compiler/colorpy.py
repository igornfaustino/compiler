def warning(text):
    print('\033[93mWarning: ' + text + '\033[0m', end="\n\n")

def error(text):
    print('\033[91mError: ' + text + '\033[0m', end="\n\n")