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

