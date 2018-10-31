inteiro: T 
pedro := 4

inteiro: V1[T][10]

inteiro somavet(inteiro: vet[], inteiro: tam)
	inteiro: result, teste 
	result := 0
	$
	inteiro: i 
	i := -1
	i := !result

	repita
		inteiro: inner
		result := result + vet[i]
		i := i + 1
	até i = tam - 1

	retorna(result)	
fim

inteiro principal()
	inteiro: x
	x := somavet(V1,T)
	retorna(0)
fim
