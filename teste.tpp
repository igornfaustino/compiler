inteiro: n, g 

inteiro fatorial(inteiro: n)
  flutuante: d
  d := 5.6 
  inteiro: fat
  se n > 10 então

    se n > 0 então
      fat := 1
      repita
        repita
          fat := fat * n
        até n = 0
        fat := fat * n
      até n = 0
    senão
      fat := 5
    fim
  fim
fim

inteiro principal()
  leia(n)
  escreva(fatorial(fatorial(1)))
fim