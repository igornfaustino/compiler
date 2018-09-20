from anytree import AnyNode
from anytree.exporter import DotExporter

root = AnyNode(name="root", value="teste")
s1 = AnyNode(name="1", parent=root, value=2.3)
s2 = AnyNode(name="2", parent=root, value="teste3")


print(s1.value == 2.3)
DotExporter(root).to_dotfile('teste.txt')
