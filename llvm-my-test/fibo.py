"""
def fibonacci( n ):
  if n <= 1:
    return 1;
  return fibonacci( n - 1 ) + fibonacci( n - 2)
"""

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int

# Defines the int type
int_type = ir.IntType(32)

# Defines a function return type as int and the arg as int
fn_int_to_int_type = ir.FunctionType( int_type, [int_type] )

module = ir.Module(name="fibo")

fibonacci = ir.Function(module, fn_int_to_int_type, "fibonacci")
fib_bloc = fibonacci.append_basic_block(name="fib_entry")

builder = ir.IRBuilder( fib_bloc )

# Get the function arg
fib_arg_n, = fibonacci.args # unwrap the tuple

# Const values
const_1 = ir.Constant(int_type, 1)
const_2 = ir.Constant(int_type, 2)

fib_n_less_eq_2 = builder.icmp_signed("<=", fib_arg_n, const_1)

# if (n <= 1) the
with builder.if_then(fib_n_less_eq_2):
    builder.ret(const_1)

fib_n_minus_1 = builder.sub(fib_arg_n, const_1)
fib_n_minus_2 = builder.sub(fib_arg_n, const_2)

call_fib_n_minus_1 = builder.call(fibonacci, [fib_n_minus_1])
call_fib_n_minus_2 = builder.call(fibonacci, [fib_n_minus_2])

fib_res = builder.add(call_fib_n_minus_1, call_fib_n_minus_2)

builder.ret(fib_res)

# print(module)

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
mod = llvm.parse_assembly( str( module ) )
mod.verify()
# Now add the module and make sure it is ready for execution
engine.add_module(mod)
engine.finalize_object()

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("main")

# Run the function via ctypes
c_fn = CFUNCTYPE(c_int)(func_ptr)
c_fn()

# Test our function for n in 0..50
# for n in range(0,50+1):
#   result = c_fn_fib(n)
#   print( "c_fn_fib({0}) = {1}".format(n, result) )

print(mod)