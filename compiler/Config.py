''' Configurations '''

class Config():
    ''' Static class to control options
    
    Options:
        silence (False): Hide warnings
        debug (False): Enable PLY debug
        format_print (False): Format print tokens
        show_lex (False): Print tokens
        output_file_path_tokens (None): Path to save tokens
        show_tree (False): Print tree
        output_file_path_tree (None): Path to save tree
        show_prune (False): Show prune tree
        output_file_path_prune_tree (None): Path to save prune tree   

    '''

    # General
    silence = False
    debug = False

    # Tokens
    format_print = False
    show_lex = False
    output_file_path_tokens = None
    
    # Parser
    show_tree = False
    output_file_path_tree = None
    
    # Prune
    show_prune = False
    output_file_path_prune_tree = None

    # gen
    show = False
    output = "a.ll"
    exec_ = False