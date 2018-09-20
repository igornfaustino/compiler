from sys import argv
import getopt
import lex
import parse
import file_utils


def print_help():
    print('\nUsage: python', argv[0], '[OPTIONS] file\n')
    print('Return an list of tokens\n')
    print('Options:')
    print('  -f, --format                          Format output print')
    print('  -h, --help                            Print usage')
    print('  -o, --output file                     Place the output into file')
    print('      --tokens                          Show tokens founded')


def print_tokens(listToken, format_print=False):
    current_lineno = 1
    for token in listToken:
        if format_print:
            if token.lineno != current_lineno:
                print("")
                current_lineno = token.lineno
            print("<" + str(token.type) + ", '" +
                  str(token.value) + "'>", end=" ")
        else:
            print("<" + str(token.type) + ", '" + str(token.value) + "'>")


def main(argv):
    output_file_path = None
    format_print = False
    show_lex = False

    # Check for options
    optlist, args = getopt.getopt(
        argv[1:], "fho:", ["format", "help", "output=", "tokens"])
    for o, a in optlist:
        if (o == '-f' or o == '--format'):
            format_print = True
        if (o == '-h' or o == '--help'):
            print_help()
            return
        if (o == '-o' or o == '--output'):
            output_file_path = a
        if(o == '--tokens'):
            show_lex = True
    if(len(args) == 0):
        print("Requires at least 1 argument.")
        print("Type '--help' for more informations")
        return

    # Read file
    data = file_utils.read_data_from_file(args[0])

    # Save data into file
    if (show_lex):
        print_tokens(lex.scan(data), format_print)
    parse.parse(data)


main(argv)
