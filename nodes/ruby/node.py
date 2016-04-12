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

class RbInt(Node):
    def __init__(self, value, start, end):
        Node.__init__(self, start, end)
        self.value = int(value)

class Op(Node):
    def __init__(self, name, start, end):
        Node.__init__(self, start, end)
        self.name = name

class BinOp(Node):
    def __init__(self, op, left, right, start, end):
        Node.__init__(self, start, end)
        self.op = op
        self.right = right
        self.left = left
        self.addChildren(left, right)

class Str(Node):
    def __init__(self, value, start, end):
        Node.__init__(self, start, end)
        self.value = value

class Module(Node):
    def __init__(self, name, body, docstring, start, end):
        Node.__init__(self, start, end)
        self.name = name
        self.body = body
        self.docstring = docstring
        self.addChildren(name, body)

class Void(Node):
    def __init__(self, start, end):
        Node.__init__(self, start, end)

class For(Node):
    def __init__(self, target, iterator, body, orelse, start, end):
        Node.__init__(self, start, end)
        self.target = target
        self.iterator = iterator
        self.body = body
        self.orelse = orelse
        self.addChildren(target, iterator, body, orelse)

class Call(Node):
    def __init__(self, func, args, keywords, kwargs, starargs, blockarg, start, end):
        Node.__init__(self, start, end)
        self.func = func
        self.args = args
        self.keywords = keywords
        self.kwargs = kwargs
        self.starargs = starargs
        self.blockarg = blockarg
        self.addChildren(func, kwargs, starargs, blockarg)
        self.addChildren(args)
        self.addChildren(keywords)

class Return(Node):
    def __init__(self, value, start, end):
        Node.__init__(self, start, end)
        self.value = value
        self.addChildren(value)

class Array(Node):
    def __init__(self, elts, start, end):
        Node.__init__(self, start, end)
        self.elts = elts
        for e in elts:
            self.addChildren(e)

class If(Node):
    def __init__(self,test, body,orelse, start, end):
        Node.__init__(self, start, end)
        self.test = test
        self.body = body
        self.orelse = orelse
        self.addChildren(test, body, orelse)

class Symbol(Node):
    def __init__(self, value, start, end):
        Node.__init__(self, start, end)
        self.value = value

class Dict(Node):
    def __init__(self, entries, start, end):
        Node.__init__(self, start, end)
        self.entries = entries
        for entry in entries:
            self.addChildren(entry)

class Assoc(Node):
    def __init__(self, key, value, start, end):
        Node.__init__(self, start, end)
        self.key = key
        self.value = value
        self.addChildren(key, value)

class While(Node):
    def __init__(self, test, body, orelse, start, end):
        Node.__init__(self, start, end)
        self.test = test
        self.body = body
        self.orelse = orelse
        self.addChildren(test, body, orelse)











