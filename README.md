# Compiler

A simple compiler made in python for my college class.
This is a compiler for a fictional language named t++

## t++ example

```
inteiro:n
    
inteiro fatorial(inteiro:n)
    inteiro:fat
    se n>0 então {não calcula se n>0}
        fat:=1
        repita
            fat:=fat∗n
            n:=n−1
        até n=0
        retorna(fat) {retorna o valor do fatorial de n}
    senão
        retorna(0)
    fim
fim

inteiro principal()
    leia(n)
    escreva(fatorial(n))
    retorna(0)
fim
```

## setup the environment

- Install pip-tools

``` bash
$ pip install pip-tools
```

- Install all the dependencies

``` bash
$ pip-sync requirements.txt
```