from llvmlite import ir
from llvmlite import binding as llvm
import llvm_utils
from ctypes import CFUNCTYPE, c_int
from enum import Enum
from Config import Config
from file_utils import save_data_into_file


class Terminator(Enum):
    retorna = 0
    loop = 1
    conditional = 2

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
        self.loopId = 0
        self.__declare_print_function()
        self.__declare_read_function()

    def declare_print_float_const(self):
        fmt = "%f \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(
            self.module, c_fmt.type, name="fstr_float")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        self.global_float = global_fmt

    def declare_print_int_const(self):
        fmt = "%d \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(
            self.module, c_fmt.type, name="fstr_int")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        self.global_int = global_fmt

    def declare_read_float_const(self):
        fmt = "%lf\00"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(
            self.module, c_fmt.type, name="fstr_float_r")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        self.global_float_read = global_fmt

    def declare_read_int_const(self):
        fmt = "%i\00"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(
            self.module, c_fmt.type, name="fstr_int_r")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        self.global_int_read = global_fmt

    def __declare_print_function(self):
        # declare an printf function (yes... this is the C funcition)
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

        self.declare_print_float_const()
        self.declare_print_int_const()

    def __declare_read_function(self):
        # declare an scanf function (yes... this is the C funcition)
        voidptr_ty = ir.IntType(8).as_pointer()
        scanf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        scanf = ir.Function(self.module, scanf_ty, name="scanf")
        self.scanf = scanf

        self.declare_read_float_const()
        self.declare_read_int_const()

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
            if(not self.actual_function):
                if(line["dimension"] == 0):
                    self.global_var[line["name"]] = ir.GlobalVariable(
                        self.module, llvm_type, line["name"])
                    self.global_var[line["name"]].linkage = 'internal'
                elif(line["dimension"] == 1):
                    index = var.children[1]
                    val = self.__expression(index.children[1])
                    array_type = ir.ArrayType(llvm_type, val.constant)
                    self.global_var[line["name"]] = ir.GlobalVariable(
                        self.module, array_type, line["name"])
                    self.global_var[line["name"]].linkage = 'internal'
                else:
                    index = var.children[1]
                    val1 = self.__expression(index.children[1])
                    val2 = self.__expression(index.children[4])
                    array_type_inner = ir.ArrayType(llvm_type, val2.constant)
                    array_type = ir.ArrayType(array_type_inner, val1.constant)
                    self.global_var[line["name"]] = ir.GlobalVariable(
                        self.module, array_type, line["name"])
                    self.global_var[line["name"]].linkage = 'internal'
            else:
                if(line["dimension"] == 0):
                    self.f_vars[line["name"]] = self.builder.alloca(
                        llvm_type, name=line["name"])
                elif(line["dimension"] == 1):
                    index = var.children[1]
                    val = self.__expression(index.children[1])
                    array_type = ir.ArrayType(llvm_type, val.constant)
                    self.f_vars[line["name"]] = self.builder.alloca(
                        array_type, name=line["name"])
                else:
                    index = var.children[1]
                    val1 = self.__expression(index.children[1])
                    val2 = self.__expression(index.children[4])
                    array_type_inner = ir.ArrayType(llvm_type, val2.constant)
                    array_type = ir.ArrayType(array_type_inner, val1.constant)
                    self.f_vars[line["name"]] = self.builder.alloca(
                        array_type, name=line["name"])

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
                p_types.append(par.children[0].value)
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
            val = self.actual_function.args[i]
            type_ = p_types[i]
            self.f_vars[name] = self.builder.alloca(
                llvm_utils.get_type(type_), name=name)
            self.builder.store(val, self.f_vars[name])
            i += 1

        if f_name == "main":
            # print(self.globals_nodes_initialize)
            for global_init in self.globals_nodes_initialize:
                self.__assignment(global_init)

    def __get_var(self, var_name):
        var = self.f_vars[var_name] if var_name in self.f_vars.keys(
        ) else self.global_var[var_name]
        return var

    def __call_function(self, function_node):
        f_name = function_node.children[0].value
        f_args = function_node.children[1].children
        params = function_node.table_pointer["params"]
        # print(function_node.table_pointer)
        param_pos = 0
        args = []
        for arg in f_args:
            exp = self.__expression(arg)
            if(params[param_pos]["type"] == "inteiro"):
                try:
                    exp = self.builder.fptosi(
                        exp, llvm_utils.get_type("inteiro"))
                except expression as identifier:
                    pass
            else:
                try:
                    exp = self.builder.sitofp(
                        exp, llvm_utils.get_type("flutuante"))
                except expression as identifier:
                    pass
            args.append(exp)
            param_pos += 1

        fn = self.functions[f_name]
        return self.builder.call(fn, args)

    def __expression(self, node):
        """ expression... returns the value of the expression
        """

        # op or single exp
        child = node.children[0] if node.value == "expression" else node
        if (child.value == "single_expression"):

            if (len(child.children) == 1):
                factor = child.children[0]
                n_type = factor.children[0]
                if (n_type.value == "num"):
                    num = n_type.children[0].value
                    t_num = "inteiro" if type(num) is int else "flutuante"
                    return llvm_utils.get_const(num, llvm_utils.get_type(t_num))
                elif (n_type.value == "var"):
                    var_name = n_type.children[0].value
                    var = llvm_utils.load_value(
                        self.builder, self.__get_var(var_name))
                    if len(n_type.children) == 2:
                        index = n_type.children[1]
                        for child in index.children:
                            if (child.value == "expression"):
                                exp = self.__expression(child)
                                var = self.builder.gep(self.__get_var(var_name), [
                                                       llvm_utils.get_const(0, llvm_utils.get_type("inteiro")), exp])
                                var = llvm_utils.load_value(self.builder, var)
                    return var
                elif (n_type.value == "function_call"):
                    return self.__call_function(n_type)
                else:
                    return self.__expression(n_type)
            else:
                factor = child.children[1]
                n_type = factor.children[0]
                if (n_type.value == "num"):
                    num = n_type.children[0].value
                    t_num = "inteiro" if type(num) is int else "flutuante"
                    return self.builder.not_(llvm_utils.get_const(num, llvm_utils.get_type(t_num)))
                elif (n_type.value == "var"):
                    var_name = n_type.children[0].value
                    var = llvm_utils.load_value(
                        self.builder, self.__get_var(var_name))
                    if len(n_type.children) == 2:
                        index = n_type.children[1]
                        for child in index.children:
                            if (child.value == "expression"):
                                exp = self.__expression(child)
                                var = self.builder.gep(self.__get_var(var_name), [
                                                       llvm_utils.get_const(0, llvm_utils.get_type("inteiro")), exp])
                                var = llvm_utils.load_value(self.builder, var)
                    return self.builder.not_(var)
                elif (n_type.value == "function_call"):
                    return self.builder.not_(self.__call_function(n_type))
                else:
                    return self.builder.not_(self.__expression(n_type))
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
        line = var_node.table_pointer

        if(not self.actual_function):  # global contex
            self.globals_nodes_initialize.append(node)
        else:
            var = self.__get_var(var_name)
            res = self.__expression(children[1])
            res = llvm_utils.load_value(self.builder, res)

            if(len(var_node.children) == 2):
                index = var_node.children[1]
                for child in index.children:
                    if (child.value == "expression"):
                        exp = self.__expression(child)
                        var = self.builder.gep(var, [llvm_utils.get_const(
                            0, llvm_utils.get_type("inteiro")), exp])

            try:
                self.builder.store(res, var)
            except TypeError:
                if (line["type"] == "inteiro"):
                    i_res = self.builder.fptosi(
                        res, llvm_utils.get_type("inteiro"))
                    self.builder.store(i_res, var)
                else:
                    f_res = self.builder.sitofp(
                        res, llvm_utils.get_type("flutuante"))
                    self.builder.store(f_res, var)
                # exit(0)

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

    def __get_pred(self, exp):
        pred = self.__expression(exp)
        pred = self.builder.not_(pred)
        return pred

    def __loops(self, node):
        body = node.children[0]
        exp = node.children[1]

        # create blocks
        loop_block = self.builder.append_basic_block(
            "loop_" + str(self.loopId))
        loop_end = self.builder.append_basic_block(
            "end_loop_" + str(self.loopId))
        self.loopId += 1

        self.builder.cbranch(self.__get_pred(exp), loop_block, loop_end)
        self.builder.position_at_end(loop_block)
        self.walk_on_tree(body)
        self.builder.cbranch(self.__get_pred(exp), loop_block, loop_end)
        self.builder.position_at_end(loop_end)

    def __print_function(self, node):
        value = self.__expression(node.children[0])

        if (str(value.type) == "i32"):
            fmt = self.global_int
        else:
            fmt = self.global_float
        # Declare argument list
        voidptr_ty = ir.IntType(8).as_pointer()

        fmt_arg = self.builder.bitcast(fmt, voidptr_ty)

        # Call Print Function
        self.builder.call(self.printf, [fmt_arg, value])

    def __read_function(self, node):
        var_node = node.children[0]
        var_name = var_node.children[0].value
        value = self.__get_var(var_name)

        line = var_node.children[0].table_pointer
        if (line["type"] == "inteiro"):
            fmt = self.global_int_read
        else:
            fmt = self.global_float_read
        # Declare argument list
        voidptr_ty = ir.IntType(8).as_pointer()

        fmt_arg = self.builder.bitcast(fmt, voidptr_ty)

        read_value = self.builder.call(self.scanf, [fmt_arg, value])

    def walk_on_tree(self, node):
        enterFunction = False
        hasTerminator = False
        return_value = None

        if (node.value == "var_declaration"):
            self.__var_declaration(node)
        elif (node.value == "assignment"):
            self.__assignment(node)
        elif (node.value == "func_declaration"):
            self.__function_declaraion(node)
            enterFunction = True
        elif (node.value == "retorna"):
            self.__retorna(node)
            return Terminator.retorna
        elif (node.value == "conditional"):
            self.__conditional(node)
            return Terminator.conditional  # stop look deep in this node
        elif (node.value == "repita"):
            self.__loops(node)
            return Terminator.loop
        elif (node.value == "escreva"):
            self.__print_function(node)
        elif (node.value == "leia"):
            self.__read_function(node)
        elif (node.value == "expression"):
            if (node.parent.value == "body"):
                self.__expression(node)

        for child in node.children:
            ret = self.walk_on_tree(child)
            if (enterFunction and ret == Terminator.conditional or ret == Terminator.loop):
                hasTerminator = False
            elif (enterFunction and ret == Terminator.retorna):
                hasTerminator = True
            elif (not enterFunction):
                return_value = ret if ret else return_value

        if (enterFunction):
            if not hasTerminator:
                return_type = self.actual_function.return_value.type
                i_type = llvm_utils.get_type("inteiro")
                f_type = llvm_utils.get_type("flutuante")
                if(return_type is i_type):
                    self.builder.ret(llvm_utils.get_const(0, i_type))
                elif(return_type is f_type):
                    self.builder.ret(llvm_utils.get_const(0, f_type))
                else:
                    self.builder.ret_void()

            self.actual_function = None
            self.f_vars = {}

        return return_value

    def compile_ir(self):
        """
        Execute generated code.
        """
        # initialize the LLVM machine
        # These are all required (apparently)
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create engine and attach the generated module
        # Create a target machine representing the host
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        # And an execution engine with an empty backing module
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

        # Parse our generated module
        mod = llvm.parse_assembly(str(self.module))
        mod.verify()
        # Now add the module and make sure it is ready for execution
        engine.add_module(mod)
        engine.finalize_object()

        # Look up the function pointer (a Python int)
        func_ptr = engine.get_function_address("main")

        # Run the function via ctypes
        c_fn = CFUNCTYPE(c_int)(func_ptr)
        c_fn()


def generate_code(tree, module_name):
    LLVM_gem = LLVMCodeGenerator(module_name)
    LLVM_gem.walk_on_tree(tree)
    save_data_into_file(Config.output, str(LLVM_gem.module))
    if (Config.show):
        print(LLVM_gem.module)
    if (Config.exec_):
        LLVM_gem.compile_ir()
    
