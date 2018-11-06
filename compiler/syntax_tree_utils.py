from anytree import Node, RenderTree

nodes_visited = []


def prune_tree(syntax_tree):
    __scan_tree(syntax_tree)


def __scan_tree(tree):
    global nodes_visited
    nodes_visited.append(tree)
    tree = __check_node(tree)

    if(not tree and tree not in nodes_visited):
        return
    for child in tree.children:
        __scan_tree(child)


def __check_node(node):
    if (node.value == "program"):
        return __prune_program(node)
    elif (
            node.value == "type" or
            node.value == "fim" or
            node.value == "(" or
            node.value == ")" or
            node.value == ":" or
            node.value == ":=" or
            node.value == ","):
        return __prune(node)
    elif (node.value == "header"):
        return __prune_header(node)
    elif (node.value == "body"):
        return __prune_body(node)
    elif (node.value == "var_list"):
        return __prune_var_list(node)
    elif (node.value == "var_init"):
        return __prune_var_init(node)
    elif (node.value == "params_list"):
        return __prune_params_list(node)
    elif (node.value == "arguments_list"):
        return __prune_arguments_list(node)
    elif (node.value == "param"):
        return __prune_param(node)
    elif (node.value == "index"):
        return __prune_index(node)
    elif (node.value == "se" or
            node.value == "então" or
            node.value == "até" or
            node.value == "leia" or
            node.value == "repita" or
            node.value == "escreva" or
            node.value == "retorna"):
        return __prune_actions(node)
    elif (node.value == "simple_expression" or
            node.value == "additive_expression" or
            node.value == "multiply_expression" or
            node.value == "logic_expression"):
        return __prune_general_expression(node)
    elif (node.value == "sum_operator" or
            node.value == "operator_relational" or
            node.value == "logic_operator" or
            node.value == "multiply_operator"):
        return __prune_operator(node)
    elif (node.value == "expression"):
        return __prune_expression(node)
    return node


def __prune(node):
    for child in node.children:
        node.parent.children = [child] + list(node.parent.children)
    node.parent = None

    return None


def __prune_header(node):
    for child in node.children:
        node.parent.children = list(node.parent.children) + [child]
    new_node = node.parent
    node.parent = None

    return new_node


def __prune_program(tree):
    program = tree
    children = list(program.children)
    while (len(children) > 0):
        if (children[0].value != "declaration"):
            node = children[0]
            node.parent = None
            children = children[1:]  # remove first element
            children = list(node.children) + children
        else:
            node = children[0]
            children = children[1:]  # remove first element
            node.parent = None
            node.children[0].parent = program

    return program


def __prune_body(tree):
    first_body = tree
    children = list(first_body.children)
    while (len(children) > 0):
        if (children[0].value != "action"):
            node = children[0]
            node.parent = None
            children = children[1:]  # remove first element
            if len(node.children) > 0:
                children = list(node.children) + children
        else:
            node = children[0]
            children = children[1:]  # remove first element
            node.parent = None
            node.children[0].parent = first_body

    return first_body


def __prune_var_list(tree):
    parent = tree.parent
    children = list(tree.children)
    while (len(children) > 0):
        if (children[0].value != "var"):
            node = children[0]
            node.parent = None
            children = children[1:]  # remove first element
            children = list(node.children) + children
        else:
            node = children[0]  # var
            children = children[1:]  # remove first element
            node.parent = parent

    tree.parent = None
    return parent


def __prune_var_init(tree):
    node = tree
    node.value = "assignment"
    aux = node.children[0]
    aux.parent = None
    for child in aux.children:
        child.parent = node

    return node


def __prune_params_list(tree):
    first_params_list = tree
    children = list(first_params_list.children)
    while (len(children) > 0):
        if (children[0].value != "param"):
            node = children[0]
            node.parent = None
            children = children[1:]  # remove first element
            if len(node.children) > 0:
                children = list(node.children) + children
        else:
            node = children[0]
            children = children[1:]  # remove first element
            if(node.parent != first_params_list):
                node.parent = None
                first_params_list.children = [
                    node] + list(first_params_list.children)

    return first_params_list

def __prune_arguments_list(tree):
    first_argument_list = tree
    children = list(first_argument_list.children)
    while (len(children) > 0):
        if (children[0].value != "expression"):
            node = children[0]
            node.parent = None
            children = children[1:]  # remove first element
            if len(node.children) > 0:
                children = list(node.children) + children
        else:
            node = children[0]
            children = children[1:]  # remove first element
            if(node.parent != first_argument_list):
                node.parent = None
                first_argument_list.children = [
                    node] + list(first_argument_list.children)

    return first_argument_list


def __prune_param(tree):
    first_param = tree
    children = list(first_param.children)
    while (len(children) > 0):
        if (children[0].value == "param"):
            node = children[0]
            node.parent = None
            children = children[1:]  # remove first element
            if len(node.children) > 0:
                children = list(node.children) + children
        else:
            node = children[0]
            children = children[1:]  # remove first element
            if (node.parent != first_param):
                first_param.children = [node] + list(first_param.children)

    return first_param


def __prune_actions(tree):
    first_se = tree
    children = list(first_se.children)
    while(len(children) > 0):
        if (children[0].value == "se" or
            children[0].value == "então" or
            children[0].value == "até" or
            children[0].value == "leia" or
            children[0].value == "repita" or
            children[0].value == "escreva" or
                children[0].value == "retorna"):
            children[0].parent = None
        children = children[1:]  # remove first element

    return first_se


def __prune_general_expression(tree):
    root = tree
    children = list(root.children)
    if (len(children) == 3):
        root.value = children[1].children[0].value  # move the op up
        new_children = list(root.children)
        new_children.pop(1)
        root.children = new_children
    elif(len(children) == 1):
        root.value = children[0].value
        children[0].parent = None
        for child in children[0].children:
            child.parent = root

        root = root.parent
    return root

def __prune_expression(tree):
    root = tree
    child = list(root.children)[0]
    if(child.value == "assignment"):
        child.parent = None
        root.value = child.value
        root.children = child.children
    return root

def __prune_operator(tree):
    root = tree
    child = root.children[0]

    child.parent = None
    root.value = child.value

    return root


def __prune_index(tree):
    first_index = tree
    children = list(first_index.children)
    while (len(children) > 0):
        if (children[0].value == "index"):
            node = children[0]
            children = children[1:]  # remove first element
            node.parent = None
            new_children = []
            for child in node.children:
                child.parent = None
                new_children.append(child)
            children = new_children + children
            first_index.children = new_children + list(first_index.children)
        else:
            children = children[1:]

    return first_index
            
