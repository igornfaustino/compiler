from symbol_table import SymbolTable
from colorpy import error, warning

RELATIONAL_OP = ["=", "<>", ">", "<", ">=", "<=", "&&", "||"]

TYPE = ["inteiro", "flutuante"]

# TODO: If isFunction, check if return is correct
class Analyzer():
    def __init__(self):
        self.symboltable = SymbolTable()
        self.success = True

    def __scan_tree(self, node):
        flags = self.__analyze(node)

        if (not flags["goDeep"]):
            return

        for child in node.children:
            self.__scan_tree(child)

        if (flags["newContext"]):
            self.symboltable.end_contex()

    # TODO: Test index type
    def __analyze_var_declaration(self, node):
        children = node.children
        _type = children[0].value
        for var in children[1:]:
            dimension = 0
            if (len(var.children) > 1):
                list_index = var.children[1]
                for child in list_index.children:
                    if (child.value != "[" and child.value != "]"):
                        _type = self.__analyze_expression(child)
                        if(_type and _type != "inteiro"):
                            self.success = False
                            error("Index must be an Inteiro at line " + str(var.children[0].line))
                        dimension += 1
            status = self.symboltable.insert({
                "name": var.children[0].value,
                "type": _type,
                "used": False,
                "symbol_type": "var",
                "dimension": dimension,
                "line": var.children[0].line,
                "value": None
            })
            if (not status):
                self.success = False

    def __analyze_params_list(self, node):
        params = node.children
        for param in params:
            _type = param.children[0].value
            par_name = param.children[1].value
            self.symboltable.insert({
                "name": par_name,
                "type": _type,
                "used": False,
                "symbol_type": "par",
                "dimension": int(len(param.children[2:])/2),
                "line": param.children[0].line
            })

    def __analyze_function_declaration(self, node):
        # function header is global
        _type = node.children[0].value
        name = node.children[1].value
        par_list = node.children[2]
        params = []

        for par in par_list.children:
            params.append({
                "type": par.children[0].value,
                "vet": False if len(par.children) == 2 else True
            })
        status = self.symboltable.insert({
            "name": name,
            "type": _type,
            "used": False,
            "symbol_type": "func",
            "dimension": 0,
            "params": params,
            "line": node.children[0].line
        })
        if (not status):
            self.success = False

        self.symboltable.add_contex(name)
    
    def get_table_line_by_node_type(self, _type):
        aux = _type.children[0].value
        line = self.symboltable.lookup(aux)
        if (not line):
            self.success = False
            error(("Variable " if (_type.value == "var") else "Function ") + aux +
                " not declared on line " + str(_type.children[0].line))
            return None
        return line

    def __analyze_single_expression(self, node):
        children = node.children # factor and other variations
        if(len(children) == 1): # just factor
            _type = children[0].children[0] # if is function_call, num or var
        else:
            op = children[0].value
            _type = children[1].children[0] # if is function_call, num or var
            if (op == "!"):
                return "bool"
        if(_type.value == "num"):
            num = _type.children[0].value
            return "inteiro" if (type(num) is int) else "flutuante"
        else:
            line = self.get_table_line_by_node_type(_type)
            return line["type"] if line else None

    # TODO: check return types
    def __analyze_expression(self, node):
        # if is single_expression, just go all deep and return the type
        if (node.value == "expression"):
            return self.__analyze_expression(node.children[0])

        if (node.value == "single_expression"):
            return self.__analyze_single_expression(node)
        
        if (node.value in RELATIONAL_OP):
            return "bool"
        
        type1 = self.__analyze_expression(node.children[0])
        type2 = self.__analyze_expression(node.children[1])

        if (not type1 or not type2):
            return None

        if (type1 == type2):
            return type1
        elif (type1 in TYPE and type2 in TYPE): # one is inteiro other is fluatuante
            return "flutuante"
        elif (type1 == "bool" and type2 =="bool"):
            return "bool"
        else:
            self.success = False
            error("Invalid type at line", child.line)

    def __analyze_add_new_contex(self, node):
        new_contex = self.symboltable.get_contex() + "_inner_" + node.value
        self.symboltable.add_contex(new_contex)

    # TODO: tratar expression
    # TODO: tratar function_call
    # TODO: tratar assignment
    def __analyze(self, node):
        if (node.value == "var_declaration"):
            self.__analyze_var_declaration(node)
            return {
                "goDeep": False,
                "newContext": False,
                "isFunction": False,
            }  # dont go deep, dont change context
        elif (node.value == "params_list"):
            self.__analyze_params_list(node)
            return {
                "goDeep": False,
                "newContext": False,
                "isFunction": False,
            }
        # TODO: Remove this
        elif (node.value == "expression"):
            self.__analyze_expression(node)
            return {
                "goDeep": True,
                "newContext": False,
                "isFunction": False,
            } 
        elif (node.value == "func_declaration"):
            self.__analyze_function_declaration(node)
            return {
                "goDeep": True,
                "newContext": True,
                "isFunction": True,
            }   # go deep, and i change the context
        elif (node.value == "repita" or
                node.value == "se"):
            self.__analyze_add_new_contex(node)
            return {
                "goDeep": True,
                "newContext": True,
                "isFunction": False,
            } 
        elif (node.value == "function_call"):
            pass
        return {
                "goDeep": True,
                "newContext": False,
                "isFunction": False,
            } 

    def verify_warnings(self):
        for line in self.symboltable.get_unused():
            if (line["name"] == "principal"):
                continue
            warning("Unused identifier \"" +
                    line["name"] + "\" at line: " + str(line["line"]))

    def verify_principal(self):
        line = self.symboltable.has_principal()
        if(line and line["used"]):
            error("\"principal\" function shouldn't be called")
            self.success = False
        elif(not line):
            error("Program don't have a \"principal\" function")
            self.success = False

    def analyze(self, node):
        self.__scan_tree(node)


def analyze(tree):
    analyzer = Analyzer()
    analyzer.analyze(tree)
    analyzer.verify_principal()
    analyzer.verify_warnings()

    return analyzer.success
