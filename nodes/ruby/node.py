class Node:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def addChildren(self, *nodes):
      if nodes:
          for node in nodes:
              if node:
                  node.parent = self

class Block(Node):
    def __init__(self, stmts, start, end):
        Node.__init__(self, start, end)
        self.stmts = stmts

class Assign(Node):
    def __init__(self, target, value, start, end):
        Node.__init__(self,start, end)
        self.target = target
        self.value = value
        self.addChildren(target)
        self.addChildren(value)

class Name(Node):
    def __init__(self, name, start, end):
        Node.__init__(self, start, end)
        self.name = name


class RbFloat(Node):
    def __init__(self, value, start, end):
        Node.__init__(self, start, end)
        self.value = float(value)
