from symbol_table import SymbolTable
from colorpy import error, warning

RELATIONAL_OP = ["=", "<>", ">", "<", ">=", "<=", "&&", "||"]

TYPE = ["inteiro", "flutuante"]


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

        if (flags["isFunction"]):
            line = self.symboltable.get_global_last_line()
            _type = line["type"]
            if(_type != "" and not self.symboltable.check_return()):
                error("Function " + line["name"] + " must have a retorno")

    def __analyze_var(self, var):
        dimension = 0
        if (len(var.children) > 1):
            list_index = var.children[1]
            for child in list_index.children:
                if (child.value != "[" and child.value != "]"):
                    _type = self.__analyze_expression(child)
                    if(_type and _type != "inteiro"):
                        self.success = False
                        error("Index must be an Inteiro at line " +
                              str(var.children[0].line) + "." + str(var.children[0].pos))
                    dimension += 1
        return dimension

    def __crete_var(self, var, _type):
        dimension = self.__analyze_var(var)
        status = self.symboltable.insert({
            "name": var.children[0].value,
            "type": _type,
            "used": False,
            "symbol_type": "var",
            "initialized": False,
            "dimension": dimension,
            "line": var.children[0].line,
            "pos": var.children[0].pos,
            "value": None
        })
        if (not status):
            self.success = False

    def __analyze_var_declaration(self, node):
        children = node.children
        _type = children[0].value
        for var in children[1:]:
            self.__crete_var(var, _type)

    def __analyze_params_list(self, node):
        params = node.children
        for param in params:
            _type = param.children[0].value
            par_name = param.children[1].value
            self.symboltable.insert({
                "name": par_name,
                "type": _type,
                "used": False,
                "initialized": True,
                "symbol_type": "par",
                "dimension": int(len(param.children[2:])/2),
                "line": param.children[0].line,
                "pos": param.children[0].pos
            })

    def __analyze_function_declaration(self, node):
        # function header is global

        params = []
        _type = None
        if(len(node.children) == 4):
            _type = node.children[0].value
            name = node.children[1].value
            par_list = node.children[2]
        else:
            name = node.children[0].value
            par_list = node.children[1]

        for par in par_list.children:
            params.append({
                "type": par.children[0].value,
                "vet": 0 if len(par.children) == 2 else int((len(par.children) - 2)/2)
            })
        status = self.symboltable.insert({
            "name": name,
            "type": _type if _type else "",
            "used": False,
            "initialized": True,
            "symbol_type": "func",
            "dimension": 0,
            "params": params,
            "line": node.children[0].line,
            "pos": node.children[0].pos
        })
        if (not status):
            self.success = False

        self.symboltable.add_contex(name)

    def __analyze_function_call(self, node):
        funtion_line = self.get_table_line_by_node_type(node, False)
        if funtion_line:
            arg_list = node.children[-1]
            par = funtion_line["params"]
            given_args = []
            for exp in arg_list.children:
                arg = {}
                _type = self.__analyze_expression(exp)
                _type_tok = _type.split(" ")
                arg["type"] = _type_tok[0]
                arg["vet"] = int(_type_tok[1]) if len(_type_tok) == 2 else 0
                given_args.append(arg)
            if (len(par) != len(given_args)):
                self.success = False
                error("Function \"" + funtion_line["name"] + "\" takes " + str(len(par)) + " argments but " + str(
                    len(given_args)) + " were given at line " + str(node.line) + "." + str(node.pos))
            elif (par != given_args):
                warning("Implicit type conversion at line " +
                        str(node.line) + "." + str(node.pos))

    def get_table_line_by_node_type(self, _type, show_error=True, used=True, initialized=False):
        aux = _type.children[0].value
        line = self.symboltable.lookup(aux, used=used, initialized=initialized)
        if (not line):
            self.success = False
            if (show_error):
                error(("Variable " if (_type.value == "var") else "Function ") + aux +
                      " not declared on line " + str(_type.children[0].line) + "." + str(_type.children[0].pos))
        return line if line else None

    def __analyze_single_expression(self, node):
        """
        Return type:
            "bool"
            "inteiro"
            "flutuante"
            "inteiro dim"
            "flutuante dim"
        """
        children = node.children  # factor and other variations
        if(len(children) == 1):  # just factor
            _type = children[0].children[0]  # if is function_call, num or var
        else:  # factor and some other op
            op = children[0].value
            _type = children[1].children[0]  # if is function_call, num or var
            if (op == "!"):  # if op is ! then is a bool..
                if (_type != num):  # just search for the line for mark as used
                    line = self.get_table_line_by_node_type(_type)
                return "bool"

        # if not a bool... just do the regular verification
        if(_type.value == "num"):
            num = _type.children[0].value
            return "inteiro" if (type(num) is int) else "flutuante"
        else:
            line = self.get_table_line_by_node_type(_type)
            if(line and (line["symbol_type"] == "var" or line["symbol_type"] == "par")):
                dimension = line["dimension"]
                if (dimension != 0):
                    real_dimension = len(_type.children) - 1
                    if (dimension - real_dimension != 0):
                        return line["type"] + " " + str(dimension - real_dimension)
            return line["type"] if line else None

    def __analyze_expression(self, node):
        # if is single_expression, just go all deep and return the type
        if (node.value == "expression"):
            return self.__analyze_expression(node.children[0])

        if (node.value == "single_expression"):
            return self.__analyze_single_expression(node)

        type1 = self.__analyze_expression(node.children[0])
        type2 = self.__analyze_expression(node.children[1])

        if (node.value in RELATIONAL_OP):
            if(not type1 or not type2 or (len(type1.split(" ")) == 2 or len(type2.split(" ")) == 2)):
                self.success = False
                error("Invalid type at line " +
                      str(node.line) + "." + str(node.pos))
            return "bool"

        if (type1 == type2):
            return type1
        elif (type1 in TYPE and type2 in TYPE):  # one is inteiro other is fluatuante
            return "flutuante"

        return None

    def __analyze_add_new_contex(self, node):
        new_contex = node.value
        self.symboltable.add_contex(new_contex)

    def __analyze_assignment(self, node):
        var = node.children[0]
        exp = node.children[1]
        self.__analyze_var(var)
        line = self.get_table_line_by_node_type(
            var, initialized=True, used=False)
        _type = "inteiro"
        if(line):
            _type = line["type"]

        exp_type = self.__analyze_expression(exp)
        if (exp_type == "bool"):
            error("Invalid type association at line " +
                  str(var.line) + "." + str(var.pos))
            self.success = False
        elif (_type != exp_type):
            warning("Implicit type conversion at line " +
                    str(var.line) + "." + str(var.pos))

    def __analyze_return(self, node):
        exp = node.children[0]
        self.symboltable.set_return()
        _type = self.__analyze_expression(exp)
        line = self.symboltable.get_global_last_line()
        if(line["type"] not in TYPE or _type not in TYPE):
            error("Invalid return at line " +
                  str(node.line) + "." + str(node.pos))
        elif(line["type"] != _type):
            warning("Implicit type conversion at line " +
                    str(node.line) + "." + str(node.pos))

    def __analyze_body(self, node):
        for child in node.children:
            if (child.value == "expression"):
                self.__analyze_expression(child)

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
        elif (node.value == "assignment"):
            self.__analyze_assignment(node)
            return {
                "goDeep": True,
                "newContext": False,
                "isFunction": False,
            }
        elif (node.value == "body"):
            self.__analyze_body(node)
            return {
                "goDeep": True,
                "newContext": False,
                "isFunction": False,
            }
        elif (node.value == "retorna"):
            self.__analyze_return(node)
            return {
                "goDeep": False,
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
                node.value == "se" or
                node.value == "senão"):
            self.__analyze_add_new_contex(node)

            return {
                "goDeep": True,
                "newContext": True,
                "isFunction": False,
            }
        elif (node.value == "function_call"):
            self.__analyze_function_call(node)
        elif (node.value == "escreva" or
              node.value == "escreva"):
            self.__analyze_expression(node.children[0])
            return {
                "goDeep": False,
                "newContext": False,
                "isFunction": False,
            }
        return {
            "goDeep": True,
            "newContext": False,
            "isFunction": False,
        }

    def verify_warnings(self):
        for line in self.symboltable.get_uninitialized():
            warning("Identifier \"" +
                    line["name"] + "\" not initialized at line: " + str(line["line"]) + "." + str(line["pos"]))

        for line in self.symboltable.get_unused():
            if (line["name"] == "principal"):
                continue
            warning("Unused identifier \"" +
                    line["name"] + "\" at line: " + str(line["line"]) + "." + str(line["pos"]))

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
