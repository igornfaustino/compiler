"""
inteiro principal()
	inteiro: digitado
	inteiro: i
	i := 1
	repita
		flutuante: f
		inteiro: int
		flutuante: resultado
		f := i/2.
		int := i/2
		resultado := f - int
		
		se  resultado > 0 então
			escreva(i)
		fim
		i := i+1
	até i <= digitado
fim
"""

from llvmlite import ir

mod = ir.Module('primo')

t_int = ir.IntType(32) # shortcut to int type
t_func = ir.FunctionType(t_int, ()) # second arg is a sequence describing the types of argument to the function.

#### principal function (main)

main = ir.Function(mod, t_func, name='main')
bb = main.append_basic_block('entry')
builder = ir.IRBuilder(bb)

digitado = builder.alloca(t_int, name="digitado")
i = builder.alloca(t_int, name="i")