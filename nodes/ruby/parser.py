from node import *
class Parser:
    def convert(self, h):
        if (not isinstance(h, dict)) or len(h) == 0:
            return None

        t = h.get("type")
        start = h.get("start")
        end = h.get("end")

        if t == "program":
            return self.convert(h.get("body"))

        if t == "block":
            stmts = self.convertList(h.get("stmts"))
            return Block(stmts, start, end)

        if t == "assign":
            target = self.convert(h.get("target"))
            value = self.convert(h.get("value"))
            return Assign(target, value, start, end)

        if t == "name":
            s = h.get("id")
            return Name(s, start, end)

        if t == "float":
            value = h.get("value")
            return RbFloat(value, start, end)

        if t == "int":
            value = h.get("value")
            return RbInt(value, start, end)

        if t == "binary":
            left = self.convert(h.get("left"))
            right = self.convert(h.get("right"))
            op = self.convert(h.get("op"))
            return BinOp(op, left, right, start, end)

        if t == "op":
            name = h.get("name")
            return Op(name, start, end)

        if t == "string":
            value = h.get("id")
            return Str(value, start, end)

        if t == "module":
            name = self.convert(h.get("name"))
            body = self.convert(h.get("body"))
            docstring = self.convert(h.get("doc"))
            return Module(name, body, docstring, start, end)

        if t == "void":
            return Void(start, end)

        if t == "for":
            target = self.convert(h.get("target"))
            iterator = self.convert(h.get("iter"))
            body = self.convert(h.get("body"))
            return For(target, iterator, body, None,start, end)

        if t == "call":
            func = self.convert(h.get("func"))
            args = h.get("args")
            blockarg = None
            stararg = None

            if args:
                pass
            else:
                return Call(func, None, None, None, stararg, blockarg, start, end)


        if t == "return":
            value = self.convert(h.get("value"))
            return Return(value, start, end)

        if t == "array":
            elts = self.convertList(h.get("elts"))
            if elts is None:
                elts = []
            return Array(elts, start, end)

        if t == "if":
            test = self.convert(h.get("test"))
            body = self.convert(h.get("body"))
            orelse = self.convert(h.get("else"))
            return If(test, body, orelse, start, end)

        if t == "symbol":
            value = h.get("id")
            return Symbol(value, start, end)

        if t == "hash":
            entries = self.convertList(h.get("entries"))
            return Dict(entries, start, end)

        if t == "assoc":
            key = self.convert(h.get("key"))
            value = self.convert(h.get("value"))
            return Assoc(key, value, start, end)

        if t == "while":
            test = self.convert(h.get("test"))
            body = self.convert(h.get("body"))
            return While(test, body, None, start, end)




        print "error occus,type is ", t

    def convertList(self, array):
        if array is None:
            return None
        out = []
        for m in array:
            node = self.convert(m)
            if node:
                out.append(node)
        return out

