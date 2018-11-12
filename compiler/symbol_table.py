"""
each node in the tree have an table like this

[
    {
        "name": "x",
        "type": "inteiro",
        "used": False,
        "initialized": True,
        "symbol_type": "var",
        "dimension": 0,
        "params": params,
        "line": 10,
        "pos": 2
    }
]
"""

from anytree import PreOrderIter, Node
from colorpy import error


class SymbolTable():
    def __init__(self):
        self.id = 1
        self.root = Node(0, contex="global", table=[])
        self.actual_contex = self.root

    def insert(self, line):
        ''' insert line into table

        Args:
            line (Dict): line to inset on the table
        Returns:
            Bool: success
        '''

        line["contex"] = self.actual_contex.contex
        entry = self.lookup(line["name"], False)

        if (line["name"] == "principal" and line["contex"] != "global" and line["symbol_type"] != "func"):
            error('"Principal" must be a function at line: ' +
                  str(line["line"]) + "." + str(line["pos"]))
            return False

        if (entry and entry["contex"] == self.actual_contex.contex):
            error('Redeclaration of identifier "' +
                  line["name"] + '" at line: ' + str(line["line"]) + "." + str(line["pos"]))
            return False
        self.actual_contex.table.append(line)
        # print(self.actual_contex.table)

        return True

    def __search_table(self, node, name):
        for line in node.table:
            if (line["name"] == name):
                return line

        if node.parent:
            return self.__search_table(node.parent, name)
        else:
            return False

    def lookup(self, name, used=True, initialized=False):
        ''' get line from the table

        Args:
            name (str): line's name
            used=True (bool): set used field on the line to True
            initialized=False (bool): set initialized field on the line to True
        Returns:
            Dict: Line
            None: not found
        '''

        line = self.__search_table(self.actual_contex, name)
        if (line and used):
            line["used"] = True
        if (line and initialized):
            line["initialized"] = True
        return line

    def get_unused(self):
        ''' get line from the table that are set as unused

        Returns:
            List: unused_lines
        '''

        unused_lines = []
        for contex in PreOrderIter(self.root):
            for line in contex.table:
                if(not line["used"]):
                    unused_lines.append(line)

        return unused_lines

    def get_uninitialized(self):
        ''' get line from the table that are set as not initialized

        Returns:
            List: not initilized lines
        '''

        uninitialized_lines = []
        for contex in PreOrderIter(self.root):
            for line in contex.table:
                if(not line["initialized"]):
                    uninitialized_lines.append(line)

        return uninitialized_lines

    def set_return(self):
        ''' set that the actual contex has a return
        '''

        self.actual_contex._return = True

    def get_global_last_line(self):
        ''' get last line from global scope

        Return:
            Dict: last line
        '''

        return self.root.table[-1]

    def has_principal(self):
        ''' get principal line from global scope

        Returns:
            Dict: Principal's line
            False: not found
        '''

        for line in self.root.table:
            if (line["name"] == "principal"):
                return line
        return False

    def __look_down_return(self, contex):
        inners_contex = contex.children
        se_has_return = False
        _return = False
        for inner in inners_contex:
            inner_return = inner._return
            if not inner._return:
                inner_return = self.__look_down_return(inner)
            if inner.contex == "se":
                se_has_return = inner_return
            elif (se_has_return and inner.contex == "senão" and inner_return):
                _return = True
        return _return

    def check_return(self):
        ''' check if function has return

        Returns:
            Bool: if scope has return
        '''
        function_return = self.root.children[-1]._return
        if (function_return):
            return function_return
        return self.__look_down_return(self.root.children[-1])

    def get_contex(self):
        ''' get actual contex

        Return:
            Node: actual contex
        '''
        return self.actual_contex.contex

    def add_contex(self, contex):
        ''' add a new contex

        Args:
            contex (str): contex's name
        ''' 

        new_contex = Node(self.id, self.actual_contex,
                          contex=contex, table=[], _return=False)
        # print(contex)
        self.id += 1
        self.actual_contex = new_contex

    def end_contex(self):
        ''' end actual contex '''

        self.actual_contex = self.actual_contex.parent
