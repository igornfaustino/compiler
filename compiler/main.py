from sys import argv
import getopt
import lex
import parse
import file_utils
import semantic_analyzer
from syntax_tree_utils import prune_tree
from anytree.exporter import DotExporter


def print_help():
    print('\nUsage: python', argv[0], '[OPTIONS] file\n')
    print('\n')
    print('Options:')
    print('  -h, --help                            Print usage')
    print('  -d, --debug                           Debug code')
    print('      --prune                           Print prune tree')
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


def print_tokens_to_file(listToken, path):
    file_utils.save_data_into_file(path, listToken)


def check_options(argv):
    options = {
        "output_file_path_tokens": None,
        "output_file_path_tree": None,
        "output_file_path_prune_tree": None,
        "format_print": False,
        "show_lex": False,
        "show_tree": False,
        "debug": False,
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
                                   "prune",
                                   "debug"])
    for o, a in optlist:
        if (o == '--tokens-format'):
            options["format_print"] = True
            options["show_lex"] = True
        if (o == '-h' or o == '--help'):
            print_help()
            return
        if (o == '-d' or o == '--debug'):
            options["debug"] = True
        if(o == '--tokens'):
            options["show_lex"] = True
        if(o == '--tokens-output'):
            options["show_lex"] = True
            options["output_file_path_tokens"] = a
        if(o == '--tree-output'):
            options["show_tree"] = True
            options["output_file_path_tree"] = a
        if(o == '--tree-prune-output'):
            options["output_file_path_prune_tree"] = a
        if(o == '--tree'):
            options["show_tree"] = True
        if(o == '--prune'):
            options["show_prune"] = True
    if(len(args) == 0):
        print("Requires at least 1 argument.")
        print("Type '--help' for more informations")
        exit(0)

    return optlist, args, options


def main(argv):
    optlist, args, options = check_options(argv)

    # Read file
    data = file_utils.read_data_from_file(args[0])

    ################# LEX ####################
    tokens, lex_success = lex.scan(data)
    
    # Show tokens
    if (lex_success and options["show_lex"]):
        if (options["output_file_path_tokens"]):
            print_tokens_to_file(tokens,
                                 options["output_file_path_tokens"])
        else:
            print_tokens(tokens)


    ################ SYNTAX ######################
    syntax_tree, parser_success = parse.parse(data,
                                              options["debug"])

    # Show tokens
    if (parser_success and lex_success and options["show_tree"]):
        if(options["output_file_path_tree"]):
            DotExporter(syntax_tree,
                        nodeattrfunc=lambda node: 'label="{}"'.format(node.value)).to_dotfile(options["output_file_path_tree"])
        else:
            for pre, fill, node in RenderTree(syntax_tree):
                print("%s%s" % (pre, node.value))

    ##################### PRUNE ###############################

    prune_tree(syntax_tree)

    # show prune
    if(lex_success and parser_success and options["show_prune"]):
        if(options["output_file_path_prune_tree"]):
            DotExporter(syntax_tree,
                        nodeattrfunc=lambda node: 'label="{}"'.format(node.value)).to_dotfile(options["output_file_path_prune_tree"])
        else:
            for pre, fill, node in RenderTree(syntax_tree):
                print("%s%s" % (pre, node.value))
    
    ########################### SEMANTIC #########################

    semantic_success = semantic_analyzer.analyze(syntax_tree)

    ########################### CODE GENERATOR #####################

    if(lex_success and parser_success and semantic_success):
        # generate code
        pass


main(argv)
