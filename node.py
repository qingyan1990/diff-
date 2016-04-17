class Node:
    def __init__(self, node_start, node_end):
        self.node_start = node_start
        self.node_end = node_end

    def addChildren(self, *nodes):
      if nodes:
          for node in nodes:
              if node:
                  node.parent = self

class Block(Node):
    def __init__(self, stmts, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.stmts = stmts
        self._fields = ["stmts"]

class Assign(Node):
    def __init__(self, target, value, node_start, node_end):
        Node.__init__(self,node_start, node_end)
        self.target = target
        self.value = value
        self.addChildren(target)
        self.addChildren(value)
        self._fields = ["target", "value"]

class Name(Node):
    def __init__(self, name, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.name = name
        self._fields = ["name"]


class RbFloat(Node):
    def __init__(self, value, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.value = float(value)

class RbInt(Node):
    def __init__(self, value, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.value = int(value)
        self._fields = ["value"]

class Op(Node):
    def __init__(self, name, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.name = name

class BinOp(Node):
    def __init__(self, op, left, right, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.op = op
        self.right = right
        self.left = left
        self.addChildren(left, right)

class Str(Node):
    def __init__(self, value, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.value = value

class Module(Node):
    def __init__(self, name, body, docstring, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.name = name
        self.body = body
        self.docstring = docstring
        self.addChildren(name, body)

class Void(Node):
    def __init__(self, node_start, node_end):
        Node.__init__(self, node_start, node_end)

class For(Node):
    def __init__(self, target, iterator, body, orelse, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.target = target
        self.iterator = iterator
        self.body = body
        self.orelse = orelse
        self.addChildren(target, iterator, body, orelse)

class Call(Node):
    def __init__(self, func, args, keywords, kwargs, starargs, blockarg, node_start, node_end):
        Node.__init__(self, node_start, node_end)
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
    def __init__(self, value, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.value = value
        self.addChildren(value)

class Array(Node):
    def __init__(self, elts, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.elts = elts
        for e in elts:
            self.addChildren(e)

class If(Node):
    def __init__(self,test, body,orelse, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.test = test
        self.body = body
        self.orelse = orelse
        self.addChildren(test, body, orelse)

class Symbol(Node):
    def __init__(self, value, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.value = value

class Dict(Node):
    def __init__(self, entries, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.entries = entries
        for entry in entries:
            self.addChildren(entry)

class Assoc(Node):
    def __init__(self, key, value, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.key = key
        self.value = value
        self.addChildren(key, value)

class While(Node):
    def __init__(self, test, body, orelse, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.test = test
        self.body = body
        self.orelse = orelse
        self.addChildren(test, body, orelse)

class Class(Node):
    def __init__(self, name, base, body, docstring, isStatic, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.name = name
        self.base = base
        self.body = body
        self.docstring = docstring
        self.isStatic = isStatic
        self.addChildren(name, base, body, docstring)

class Function(Node):
    def __init__(self, name, args, body, defaults, vararg, kwarg, afterRest, blockarg, docstring, node_start, node_end):
        Node.__init__(self, node_start, node_end)
        self.name = name
        self.args = args
        self.body = body
        self.defaults = defaults
        self.vararg = vararg
        self.kwarg = kwarg
        self.afterRest = afterRest
        self.blockarg = blockarg
        self.docstring = docstring
        self.addChildren(args)
        self.addChildren(defaults)
        self.addChildren(afterRest)
        self.addChildren(name, body, vararg, kwarg, blockarg)







