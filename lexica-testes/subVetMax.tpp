inteiro somaMax(inteiro: v[], inteiro: t)
    inteiro: i, sAtual, sMax
    i := 1
    sAtual := v[0]
    sMax := v[0]

    repita
        sAtual := sAtual + v[i]
        se v[i] > sAtual então
            sAtual := v[i]
        fim
        se sAtual > somaMax então
            somaMax := sAtual
        fim
        i := i + 1
    até i < t

    retorna(somaMax)
fim

inteiro principal()
    inteiro: V[100]
    inteiro: i, res
	i := 0
    { Inicia vetor }
	repita
		V[i] := i+1
		i := i + 1
	até i = 100

	{ Soma maxima }
    res := somaMax(V, 100)
    escreva(res)
fim