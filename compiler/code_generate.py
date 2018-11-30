from llvmlite import ir
import llvm_utils

# TODO: Cast de tipos

# Initialize global vars when enters on main
class LLVMCodeGenerator():
    def __init__(self, module_name):
        self.module = ir.Module(module_name)
        self.actual_function = None
        self.builder = None
        self.global_var = {}
        self.f_vars = {}
        self.functions = {}
        # save nodes of initializations and call on main function
        self.globals_nodes_initialize = []
        self.loopId = 0;

    def __var_declaration(self, node):
        """ get var_declaration node and create the var
        """

        # children[0] = type
        # children[1:] = vars
        children = node.children
        llvm_type = llvm_utils.get_type(children[0].value)
        for var in children[1:]:
            var_name = var.children[0]
            line = var_name.table_pointer
            # print(line)
            if(not self.actual_function):
                self.global_var[line["name"]] = ir.GlobalVariable(
                    self.module, llvm_type, line["name"])
            else:
                self.f_vars[line["name"]] = self.builder.alloca(
                    llvm_type, name=line["name"])

    # TODO suport to arrays on params
    def __function_declaraion(self, node):
        """ get function declaration node and create a new function on LLVM
        the att actual_function gets the new function and the builder the functions entry block
        """

        # *** function can have no type
        # children[0] = name
        # children[1] = par_list
        children = node.children
        p_names = []
        p_types = []
        if(len(children) == 3):  # children without type
            return_type = "void"
            f_name = children[0].value

            for par in children[1].children:
                p_type.append(par.children[0].value)
                p_names.append(par.children[1].value)
        else:
            # children[0] = type
            # children[1] = name
            # children[2] = par_list
            return_type = children[0].value
            f_name = children[1].value

            for par in children[2].children:
                p_types.append(par.children[0].value)
                p_names.append(par.children[1].value)

        f_name = f_name if f_name != "principal" else "main"
        f_type = llvm_utils.get_function_type(return_type, p_types)

        self.actual_function = ir.Function(self.module, f_type, f_name)
        bb = self.actual_function.append_basic_block('entry')
        self.builder = ir.IRBuilder(bb)

        self.functions[f_name] = self.actual_function

        # put args on f_vars
        i = 0
        for name in p_names:
            self.f_vars[name] = self.actual_function.args[i]
            i += 1

        if f_name == "main":
            # print(self.globals_nodes_initialize)
            for global_init in self.globals_nodes_initialize:
                self.__assignment(global_init)

    def __get_var(self, var_name):
        var = self.f_vars[var_name] if var_name in self.f_vars.keys() else self.global_var[var_name]
        return var

    # TODO... finish this
    def __call_function(self, function_node):
        # f_name = function_node[0]
        # f_args = function_node[1].children
        print(function_node)

    # TODO... Handle complex expressions
    # TODO... Handle function call
    def __expression(self, node):
        """ expression... returns the value of the expression
        """

        # op or single exp
        child = node.children[0] if node.value == "expression" else node
        if (child.value == "single_expression"):
            factor = child.children[0]
            if (len(factor.children) == 1):
                n_type = factor.children[0]
                if (n_type.value == "num"):
                    num = n_type.children[0].value
                    t_num = "inteiro" if type(num) is int else "flutuante"
                    return llvm_utils.get_const(num, llvm_utils.get_type(t_num))
                elif (n_type.value == "var"):
                    var_name = n_type.children[0].value
                    return llvm_utils.load_value(self.builder, self.__get_var(var_name))
                elif (n_type.value == "function_call"):
                    return self.__call_function(node)
                else:
                    return self.__expression(n_type)
        else:  # operators
            op = child
            val1 = self.__expression(op.children[0])
            val2 = self.__expression(op.children[1])
            return llvm_utils.do_operation(self.builder, op.value, val1, val2)

    def __assignment(self, node):
        """ Get assignment node and create this lines on llvm code
        """

        # children[0] = var
        # children[1] = expression
        children = node.children
        var_node = children[0]
        var_name = var_node.children[0].value
        if(not self.actual_function):  # global contex
            self.globals_nodes_initialize.append(node)
        else:
            var = self.__get_var(var_name)
            res = self.__expression(children[1])
            print(type(res))
            res = llvm_utils.load_value(self.builder, res)
            self.builder.store(res, var)

    def __retorna(self, node):
        exp = node.children[0]
        res = self.__expression(exp)
        res = llvm_utils.load_value(self.builder, res)
        self.builder.ret(res)

    def __conditional(self, node):
        conditional_size = len(node.children)
        exp = node.children[0]
        pred = self.__expression(exp)
        if (conditional_size == 3):  # if function has if and ese block
            se = node.children[1]
            senao = node.children[2]

            with self.builder.if_else(pred) as (if_block, else_block):
                with if_block:
                    self.walk_on_tree(se)
                with else_block:
                    self.walk_on_tree(senao)
        else:  # if function just have if block
            se = node.children[1]

            with self.builder.if_then(pred):
                self.walk_on_tree(se)

    def __loops(self, node):
        body = node.children[0]
        exp = node.children[1]
        pred = self.__expression(exp)
        pred = self.builder.not_(pred)
        loopBlock = self.builder.append_basic_block("loop " + str(self.loopId))
        self.loopId += 1
        # self.builder = ir.IRBuilder(new_block)
        with self.builder.if_then(pred):
            self.walk_on_tree(body)
            with self.builder.if_then(pred):
                self.builder.branch(loopBlock)

    def walk_on_tree(self, node):
        enterFunction = False

        if (node.value == "var_declaration"):
            self.__var_declaration(node)
        elif (node.value == "assignment"):
            self.__assignment(node)
        elif (node.value == "func_declaration"):
            self.__function_declaraion(node)
            enterFunction = True
        elif (node.value == "retorna"):
            self.__retorna(node)
        elif (node.value == "conditional"):
            self.__conditional(node)
            return  # stop look deep in this node
        elif (node.value == "repita"):
            self.__loops(node)
            return

        for child in node.children:
            self.walk_on_tree(child)

        if (enterFunction):
            self.actual_function = None
            self.f_vars = {}


def generate_code(tree, module_name):
    LLVM_gem = LLVMCodeGenerator(module_name)
    LLVM_gem.walk_on_tree(tree)
    print(LLVM_gem.module)
