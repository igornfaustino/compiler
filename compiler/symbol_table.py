from anytree import PreOrderIter, Node
from colorpy import error

"""
each node in the tree have an table like this

[
    {
        name: x, 
        type: inteiro, 
        value: 10, 
        used: True, 
        dimension: [], 
        symbol_type: var,
        params: [{type: , vet: }] # if is a function 
    }
]
"""
class SymbolTable():
    def __init__(self):
        self.id = 1
        self.root = Node(0, contex="global", table=[])
        self.actual_contex = self.root
    
    def insert(self, line):
        line["contex"] = self.actual_contex.contex
        entry = self.lookup(line["name"], False)

        if (line["name"] == "principal" and line["contex"] != "global" and line["symbol_type"] != "func"):
            error('"Principal" must be a function at line: ' + str(line["line"]))
            return False

        if (entry and entry["contex"] == self.actual_contex.contex):
            error('Redeclaration of identifier "' + line["name"] + '" at line: ' + str(line["line"]))
            return False

        self.actual_contex.table.append(line)
        print(self.actual_contex.table)

        return True
    
    def __search_table(self, node, name):
        for line in node.table:
            if (line["name"] == name):
                return line


        if node.parent:
            return self.__search_table(node.parent, name)
        else:
            return False

    def lookup(self, name, used=True):
        line = self.__search_table(self.actual_contex, name)
        if (line and used):
            line["used"] = True
        return line
    
    def get_unused(self):
        unused_lines = []
        for contex in PreOrderIter(self.root):
            for line in contex.table:
                if(not line["used"]):
                    unused_lines.append(line)
        
        return unused_lines
    
    def has_principal(self):
        for line in self.root.table:
            if (line["name"] == "principal"):
                return line
        return False


    def get_contex(self):
        return self.actual_contex.contex

    def add_contex(self, contex):
        new_contex = Node(self.id, self.actual_contex, contex=contex, table=[])
        self.id += 1
        self.actual_contex = new_contex
    
    def end_contex(self):
        self.actual_contex = self.actual_contex.parent