from sys import argv
import getopt
import lex
import file_utils


def print_help():
    print('\nUsage: python', argv[0], '[OPTIONS] file\n')
    print('Return an list of tokens\n')
    print('OPTIONS:')
    print('  -h, --help                            Print usage')
    print('  -o, --output file                     Place the output into file')


def main(argv):
    output_file_path = None
    optlist, args = getopt.getopt(argv[1:], "ho:", ["help", "output="])
    for o, a in optlist:
        if (o == '-h' or o == '--help'):
            print_help()
            return
        if (o == '-o' or o == '--output'):
            output_file_path = a
    if(len(args) == 0):
        print("Requires at least 1 argument.")
        print("Type '--help' for more informations")
        return 

    # Read file
    data = file_utils.read_data_from_file(args[0])

    # Save data into file
    if (output_file_path):
        file_utils.save_data_into_file(output_file_path, lex.scan(data))
    else:
        print(lex.scan(data))


main(argv)
