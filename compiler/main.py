from sys import argv
import getopt
import lex
import parse
import file_utils


def print_help():
    print('\nUsage: python', argv[0], '[OPTIONS] file\n')
    print('\n')
    print('Options:')
    print('  -h, --help                            Print usage')
    print('  -d, --debug                           Debug code')
    print('      --tree                            Print tree')
    print('      --tree-output=                    Print tree to a file')
    print('      --tokens                          Show tokens founded')
    print('      --tokens-format                   Show tokens founded formated')
    print('      --tokens-output=                  Print tokens to a file')


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


def print_tokens_to_file(listToken, path):
    file_utils.save_data_into_file(path, listToken)


def main(argv):
    output_file_path_tokens = None
    output_file_path_tree = None
    format_print = False
    show_lex = False
    show_tree = False
    debug = False

    # Check for options
    optlist, args = getopt.getopt(
        argv[1:], "hd", ["tokens-format", "help", "tokens", "tokens-output=", "tree-output=", "tree", "debug"])
    for o, a in optlist:
        if (o == '--tokens-format'):
            format_print = True
            show_lex = True
        if (o == '-h' or o == '--help'):
            print_help()
            return
        if (o == '-d' or o == '--debug'):
            debug = True
        if(o == '--tokens'):
            show_lex = True
        if(o == '--tokens-output'):
            show_lex = True
            output_file_path_tokens = a
        if(o == '--tree-output'):
            output_file_path_tree = a
        if(o == '--tree'):
            show_tree = True
    if(len(args) == 0):
        print("Requires at least 1 argument.")
        print("Type '--help' for more informations")
        return

    # Read file
    data = file_utils.read_data_from_file(args[0])

    # Save data into file
    if (show_lex):
        if (output_file_path_tokens):
            print(output_file_path_tokens)
            print_tokens_to_file(lex.scan(data), output_file_path_tokens)
        else:
            print_tokens(lex.scan(data), format_print)
    parse.parse(data, output_file_path_tree, show_tree, debug)


main(argv)
