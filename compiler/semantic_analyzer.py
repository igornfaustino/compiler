from symbol_table import SymbolTable
from colorpy import error, warning


class Analyzer():
    def __init__(self):
        self.symboltable = SymbolTable()
        self.success = True

    def __scan_tree(self, node):
        _continue, newcontex = self.__analyze(node)

        if (not _continue):
            return

        for child in node.children:
            self.__scan_tree(child)

        if (newcontex):
            self.symboltable.end_contex()

    # TODO: tratar expression
    def __analyze(self, node):
        if (node.value == "var_declaration"):
            children = node.children
            _type = children[0].value
            for var in children[1:]:
                dimension = 0
                if (len(var.children) > 1):
                    list_index = var.children[1]
                    for child in list_index.children:
                        if (child.value != "[" and child.value != "]"):
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

            return False, False
        elif (node.value == "var"):
            var = node  # var is always the first assignment son
            # first child: var name / second child? : index
            var_name = var.children[0].value
            table_line = self.symboltable.lookup(var_name)
            if (not table_line):
                self.success = False
                error("Variable " + var_name +
                      " not declared on line " + str(var.children[0].line))

            return False, False
        elif (node.value == "params_list"):
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
            return False, False
        elif (node.value == "func_declaration"):
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

            return True, True
        elif (node.value == "repita" or
                node.value == "se"):
            new_contex = self.symboltable.get_contex() + "_inner_" + node.value
            self.symboltable.add_contex(new_contex)
            return True, True
        elif (node.value == "function_call"):
            pass
        return True, False

    def verify_warnings(self):
        for line in self.symboltable.get_unused():
            if (line["name"] == "principal"):
                continue
            warning("Unused identifier \"" +
                    line["name"] + "\" on line: " + str(line["line"]))

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
