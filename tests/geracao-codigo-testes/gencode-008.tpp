inteiro: A[1024]
inteiro: B[1024]

inteiro principal()
    inteiro: a, i, v[10]
    i := 0

    repita
        { leia(a) }
        A[i] := i
        i := i + 1
    até i = 1024

    i := 0
    repita
        B[1023 - i] := A[i]
        i := i + 1
    até i = 1024

    i := 0
    repita
        escreva(B[i])
        i := i + 1
    até i = 1024    

    retorna(0)
fim
