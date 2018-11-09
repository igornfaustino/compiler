from sys import argv
import lex
import parse
import file_utils
import semantic_analyzer
from syntax_tree_utils import prune_tree
from utils import *


def main(argv):
    args = check_options(argv)

    # Read file
    data = file_utils.read_data_from_file(args[0])

    ################# LEX ####################
    tokens, lex_success = lex.scan(data)

    # Show tokens
    if (lex_success and Config.show_lex):
        show_tokens(tokens, Config.output_file_path_tokens)

    ################ SYNTAX ######################
    syntax_tree, parser_success = parse.parse(data,
                                              Config.debug)

    # Show tokens
    if (parser_success and lex_success and Config.show_tree):
        show_tree(syntax_tree, Config.output_file_path_tree)
        ##################### PRUNE ###############################

    prune_tree(syntax_tree)

    # show prune
    if(lex_success and parser_success and Config.show_prune):
        show_tree(syntax_tree, Config.output_file_path_prune_tree)

    ########################### SEMANTIC #########################

    semantic_success = semantic_analyzer.analyze(syntax_tree)

    ########################### CODE GENERATOR #####################

    if(lex_success and parser_success and semantic_success):
        # generate code
        pass


main(argv)
