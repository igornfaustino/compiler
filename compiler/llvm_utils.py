from llvmlite import ir

t_int = ir.IntType(32)
t_float = ir.DoubleType()
t_void = ir.VoidType()


def get_type(_type):
    ''' get type from str

    raises error if not a valid type

    Args:
        _type (str): [inteiro|flutuante|void]

    Return:
        IntType(64): if inteiro
        FloatType: if flutuante
        VoidType: if void
    '''

    if (_type.lower() == "inteiro"):
        return t_int
    if (_type.lower() == "flutuante"):
        return t_float
    if (_type.lower() == "void"):
        return t_void

    raise(TypeError("Type " + _type + " is invalid"))


def get_const(value, _type):
    ''' get const value

    Args:
        value: const value
        _type: llvm type
    Return
        ir.Constant: constant value
    '''

    return ir.Constant(_type, value)


def get_function_type(return_type, args_type):
    ''''get function type

    Args
        return_type (str): [inteiro|flutuante|void]
        args_type (list): function args type

    Return
        FunctionType: return type and args
    '''
    llvm_return_type = get_type(return_type)
    llvm_args_type = []
    for _type in args_type:
        llvm_args_type.append(get_type(_type))

    return ir.FunctionType(llvm_return_type, llvm_args_type)

def do_int_operations(builder, op, val1, val2):
    if (op == "+"):
        return builder.add(val1, val2)
    elif (op == "-"):
        return builder.sub(val1, val2)
    elif (op == "*"):
        return builder.mul(val1, val2)
    elif (op == "/"):
        return builder.sdiv(val1, val2)
    elif (op == "="):
        return builder.icmp_signed("==", val1, val2)
    elif (op == "<"):
        return builder.icmp_signed("<", val1, val2)
    elif (op == ">"):
        return builder.icmp_signed(">", val1, val2)
    elif (op == "<="):
        return builder.icmp_signed("<=", val1, val2)
    elif (op == ">="):
        return builder.icmp_signed(">=", val1, val2)
    elif (op == "<>"):
        return builder.icmp_signed("!=", val1, val2)
    elif (op == "&&"):
        return builder.and_(val1, val2)
    elif (op == "||"):
        return builder.or_(val1, val2)

def do_float_operations(builder, op, val1, val2):
    if (val1.type is t_int):
        val1 = builder.sitofp(val1, t_float)
    if (val2.type is t_int):
        val2 = builder.sitofp(val2, t_float)

    if (op == "+"):
        return builder.fadd(val1, val2)
    elif (op == "-"):
        return builder.fsub(val1, val2)
    elif (op == "*"):
        return builder.fmul(val1, val2)
    elif (op == "/"):
        return builder.fdiv(val1, val2)
    elif (op == "="):
        return builder.icmp_signed("==", val1, val2)
    elif (op == "<"):
        return builder.icmp_signed("<", val1, val2)
    elif (op == ">"):
        return builder.icmp_signed(">", val1, val2)
    elif (op == "<="):
        return builder.icmp_signed("<=", val1, val2)
    elif (op == ">="):
        return builder.icmp_signed(">=", val1, val2)
    elif (op == "<>"):
        return builder.icmp_signed("!=", val1, val2)
    elif (op == "&&"):
        return builder.and_(val1, val2)
    elif (op == "||"):
        return builder.or_(val1, val2)

def do_operation(builder, op, val1, val2):
    if(val1.type is get_type("inteiro") and val2.type is get_type("inteiro")):
        return do_int_operations(builder, op, val1, val2)
    return do_float_operations(builder, op, val1, val2)



def load_value(builder, val):
    # print(type(val))
    return val if (
        type(val) is not ir.values.GlobalVariable and
        type(val) is not ir.instructions.AllocaInstr and
        type(val) is not ir.instructions.GEPInstr) else builder.load(val, align=4)


if __name__ == "__main__":
    print(get_type("inteiro"))
    print(get_type("flutuante"))
