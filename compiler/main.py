from sys import argv
import lex

def main(argv):
    data = open(argv[1], 'r').read()
    print(lex.scan(data))

main(argv)