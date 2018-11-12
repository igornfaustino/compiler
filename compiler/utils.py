from Config import Config
import getopt
from anytree.exporter import DotExporter
from anytree import RenderTree
from Config import Config


def print_help():
    print('\nUsage: python', argv[0], '[OPTIONS] file\n')
    print('\n')
    print('Options:')
    print('  -d, --debug                           Debug code')
    print('  -h, --help                            Print usage')
    print('      --prune                           Print prune tree')
    print('      --quiet                           Don\'t show warnings')
    print('      --tree                            Print tree')
    print('      --tree-output=                    Print tree to a file')
    print('      --tree-prune-output=              Print prune tree to a file')
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
    print("\n")


def print_tokens_to_file(listToken, path):
    status = file_utils.save_data_into_file(path, listToken)
    if (not status):
        exit(-1)


def check_options(argv):
    options = {
        "output_file_path_tokens": None,
        "output_file_path_tree": None,
        "output_file_path_prune_tree": None,
        "format_print": False,
        "show_lex": False,
        "show_tree": False,
        "debug": False,
        "show_prune": False,
    }

    # Check for options
    optlist, args = getopt.getopt(argv[1:],
                                  "hd",
                                  ["tokens-format",
                                   "help",
                                   "tokens",
                                   "tokens-output=",
                                   "tree-output=",
                                   "tree-prune-output=",
                                   "tree",
                                   "quiet",
                                   "prune",
                                   "debug"])
    for o, a in optlist:
        if (o == '--tokens-format'):
            Config.format_print = True
            Config.show_lex = True
        if (o == '-h' or o == '--help'):
            print_help()
            return
        if (o == '-d' or o == '--debug'):
            Config.debug = True
        if (o == '--quiet'):
            Config.silence = True
        if(o == '--tokens'):
            Config.show_lex = True
        if(o == '--tokens-output'):
            Config.show_lex = True
            Config.output_file_path_tokens = a
        if(o == '--tree-output'):
            Config.show_tree = True
            Config.output_file_path_tree = a
        if(o == '--tree-prune-output'):
            Config.show_prune = True
            Config.output_file_path_prune_tree = a
        if(o == '--tree'):
            Config.show_tree = True
        if(o == '--prune'):
            Config.show_prune = True
    if(len(args) == 0):
        print("Requires at least 1 argument.")
        print("Type '--help' for more informations")
        exit(0)

    return args


def show_tree(tree, path=None):
    if(path):
        DotExporter(tree,
                    nodeattrfunc=lambda node: 'label="{}"'.format(node.value)).to_dotfile(path)
    else:
        for pre, fill, node in RenderTree(tree):
            print("%s%s" % (pre, node.value))


def show_tokens(tokens, path=None):
    if (path):
        print_tokens_to_file(tokens, path)
    else:
        print_tokens(tokens, Config.format_print)
