from utils import *
from htmlize import htmlize
import sys
from improve_ast import *

class Texts:
    def __init__(self, origin_text, current_text, changes):
        self.origin_text = origin_text
        self.current_text = current_text
        self.changes = changes


# The difference between nodes are stored as a Change structure.
class Change:
    def __init__(self, orig, cur, cost, is_move=False):
        self.orig = orig
        self.cur = cur
        if orig is None:
            self.cost = node_size(cur)
        elif cur is None:
            self.cost = node_size(orig)
        elif cost == 'all':
            self.cost = node_size(orig) + node_size(cur)
        else:
            self.cost = cost
        self.is_move = is_move
    def __repr__(self):
        move = "M" if self.is_move else "-"
        def hole(x):
            return [] if x==None else x
        return ("(C:" + str(hole(self.orig)) + ":" + str(hole(self.cur))
                + ":" + str(self.cost) + ":" + str(self.similarity())
                + ":" + move + ")")
    def similarity(self):
        total = node_size(self.orig) + node_size(self.cur)
        return 1 - div(self.cost, total)



# Three major kinds of changes:
# * modification
# * deletion
# * insertion
def mod_node(node1, node2, cost):
    return Change(node1, node2, cost)

def del_node(node):
    return Change(node, None, node_size(node))

def ins_node(node):
    return Change(None, node, node_size(node))


# 2-D array table for memoization of dynamic programming
def create_table(x, y):
    table = []
    for i in range(x+1):
        table.append([None] * (y+1))
    return table

def table_lookup(t, x, y):
    return t[x][y]

def table_put(t, x, y, v):
    t[x][y] = v





#-------------------------------------------------------------
#                  string distance function
#-------------------------------------------------------------

### diff cache for AST nodes

### string distance function
def str_dist(s1, s2):
    if len(s1) > 100 or len(s2) > 100:
        if s1 != s2:
            return 2.0
        else:
            return 0

    d = dist1(s1, s2)
    ret = (1.0-d)*2

    return ret


# the main dynamic programming part
# similar to the structure of diff_list
def dist1(s1, s2):
    if s1 == s2:
        return 1.0
    if s1 == '' or s2 == '':
        return 0

    s = set()
    for i in range(len(s1)-1):
        s.add(s1[i:i+2])
    count = 0
    for j in range(len(s2)-1):
        if s2[j:j+2] in s:
            count += 1
    return div(2*count, len(s1)+len(s2)-2)



#-------------------------------------------------------------
#                        diff of nodes
#-------------------------------------------------------------

def diff_node(node1, node2, depth=0, move=False):

    #pdb.set_trace()
    if isinstance(node1, list) and not isinstance(node2, list):
        node2 = [node2]

    if not isinstance(node1, list) and isinstance(node2, list):
        node1 = [node1]

    if isinstance(node1, list) and isinstance(node2, list):
        table = create_table(len(node1), len(node2))
        (changes,cost) = diff_list(table, node1, node2, 0, move)
        if move:
            matched, new_changes = find_move(changes)
            if matched:
                changes = lfilter(lambda p: p not in matched, changes)
                changes.extend(new_changes)
                #for change in new_changes:
                    #print change
        return (changes,cost)


    if node1 == node2:
        return ([mod_node(node1, node2, 0)], 0)

    if isinstance(node1, Num) and isinstance(node2, Num):
        if node1.n == node2.n:
            return ([mod_node(node1, node2, 0)], 0)
        else:
            return ([mod_node(node1, node2, 1)], 1)

    if isinstance(node1, Str) and isinstance(node2, Str):
        cost = str_dist(node1.s, node2.s)
        return ([mod_node(node1, node2, cost)], cost)

    if isinstance(node1, Name) and isinstance(node2, Name):
        cost = str_dist(node1.id, node2.id)
        return ([mod_node(node1, node2, cost)], cost)


    if (isinstance(node1, Attribute) and isinstance(node2, Name) or
        isinstance(node1, Name) and isinstance(node2, Attribute) or
        isinstance(node1, Attribute) and isinstance(node2, Attribute)):
        s1 = attr_to_str(node1)
        s2 = attr_to_str(node2)
        if s1 is not None and s2 is not None:
            cost = str_dist(s1, s2)
            return ([mod_node(node1, node2, cost)], cost)
        # else fall through for things like f(x).y vs x.y

    if isinstance(node1,Module) and isinstance(node2, Module):
        return diff_node(node1.body, node2.body, depth, move)

    # same type of other AST nodes
    if (isinstance(node1, AST) and isinstance(node2, AST) and
        type(node1) == type(node2)):
        fs1 = node_fields(node1)
        fs2 = node_fields(node2)
        changes, cost = [], 0
        min_len = min(len(fs1), len(fs2))

        for i in range(min_len):
            (m, c) = diff_node(fs1[i], fs2[i], depth, move)
            changes = m + changes
            cost += c

        return (changes, cost)

    if (type(node1) == type(node2) and
             is_empty_container(node1) and is_empty_container(node2)):
        return ([mod_node(node1, node2, 0)], 0)

    # all unmatched types and unequal values
    return ([del_node(node1), ins_node(node2)],
                   node_size(node1) + node_size(node2))



########################## diff of a list ##########################

# diff_list is the main part of dynamic programming

def diff_list(table, ls1, ls2, depth, move):

    def memo(v):
        table_put(table, len(ls1), len(ls2), v)
        return v

    def guess(table, ls1, ls2):
        (m0, c0) = diff_node(ls1[0], ls2[0], depth, move)
        (m1, c1) = diff_list(table, ls1[1:], ls2[1:], depth, move)
        cost1 = c1 + c0
        # short cut 1 (func and classes with same names)
        if can_move(ls1[0], ls2[0], c0):
            return (m0 + m1, cost1)

        else:  # do more work
            (m2, c2) = diff_list(table, ls1[1:], ls2, depth, move)
            (m3, c3) = diff_list(table, ls1, ls2[1:], depth, move)
            cost2 = c2 + node_size(ls1[0])
            cost3 = c3 + node_size(ls2[0])

            if (not different_def(ls1[0], ls2[0]) and
                cost1 <= cost2 and cost1 <= cost3):
                return (m0 + m1, cost1)
            elif (cost2 <= cost3):
                return ([del_node(ls1[0])] + m2, cost2)
            else:
                return ([ins_node(ls2[0])] + m3, cost3)

    # cache look up
    cached = table_lookup(table, len(ls1), len(ls2))
    if cached is not None:
        return cached

    if (ls1 == [] and ls2 == []):
        return memo(([], 0))

    elif (ls1 != [] and ls2 != []):
        return memo(guess(table, ls1, ls2))

    elif ls1 == []:
        d = []
        for n in ls2:
            d = [ins_node(n)] + d
        return memo((d, node_size(ls2)))

    else: # ls2 == []:
        d = []
        for n in ls1:
            d = [del_node(n)] + d
        return memo((d, node_size(ls1)))


def find_move(changes):
    matched = []
    new_changes = []
    deletions = lfilter(lambda p: (p.cur is None and p.orig is not None), changes)
    insertions = lfilter(lambda p: (p.cur is not None and p.orig is None), changes)

    if deletions and insertions:
        for d0 in deletions:
            for a0 in insertions:
                node1, node2 = d0.orig, a0.cur
                changes, cost = diff_node(node1, node2, 0)
                if cost == 0:
                    matched.append(d0)
                    matched.append(a0)
                    deletions.remove(d0)
                    insertions.remove(a0)
                    for change in changes:
                        change.is_move = True
                    new_changes.extend(changes)
                    break;
    return matched, new_changes


#-------------------------------------------------------------
#                     main diff command
#-------------------------------------------------------------

def diff(file1, file2, move=False, parent=False):

    # get AST of file1
    f1 = open(file1, 'r')
    lines1 = f1.read()
    f1.close()

    try:
        node1 = parse(lines1)
    except (SyntaxError, Exception):
        print('file %s cannot be parsed' % file1)
        raise
    improve_ast(node1, lines1, file1, 'left', parent)

    # get AST of file2
    f2 = open(file2, 'r');
    lines2 = f2.read()
    f2.close()

    try:
        node2 = parse(lines2)
    except (SyntaxError, Exception):
        print('file %s cannot be parsed' % file2)
        raise

    improve_ast(node2, lines2, file2, 'right', parent)

    # get the changes
    (changes, cost) = diff_node(node1, node2, 0, move)
    return changes


def diffstring(str1, str2, move=False, parent=False):

    try:
        node1 = parse(str1)
    except (SyntaxError, Exception):
        print('string -- %s -- cannot be parsed' % str1)
        raise

    improve_ast(node1, str1, None, 'left', parent)

    try:
        node2 = parse(str2)
    except (SyntaxError, Exception):
        print('string -- %s -- cannot be parsed' % str2)
        raise

    improve_ast(node2, str2, None, 'right', parent)

    # get the changes
    (changes, cost) = diff_node(node1, node2, 0, move)
    return changes, cost

def generate_html(filename, changes, has_lineno=False):
    htmlize(filename, changes, has_lineno)


def change_type(change):
    origin = change.orig
    current = change.cur
    if origin is None and current is not None:
        if isinstance(current, stmt):
            if isinstance(current, Expr):
                print type(current.value).__name__ + " statement insert"
            else:
                print type(current).__name__ + " statement insert"
        if isinstance(current, expr):
            print current.subtype + " insert"
    if current is None and origin is not None:
        if isinstance(origin, stmt):
            if isinstance(origin, Expr):
                print type(origin.value).__name__ + " statement delete"
            else:
                print type(origin).__name__ + " statement delete"
        if isinstance(origin, expr):
            print origin.subtype + " delete"
    if current is not None and origin is not None and change.cost > 0 and \
        not isinstance(current, stmt):
        element = detail_change(current)
        print element
        if element in CHANGETYPEDICT:
            print CHANGETYPEDICT[element]
        else:
            print element[0] + " in " + element[1] + " change"

def detail_change(node):
    role = "UFO"
    parent = None
    while not isinstance(node, Module):
        if isinstance(node, expr):
            role = node.subtype
            parent = node.parent
            return role, type(parent).__name__
        node = node.parent
    return role, type(parent).__name__

def main():
    if len(sys.argv) == 3:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        content1 = open(file1).read()
        content2 = open(file2).read()
        changes = diff(file1, file2, parent=True, move=True)
        #for change in changes:
            #change_type(change)
            #if change.cost != 0:
                #print change
        generate_html('tmp.html', Texts(content1, content2, changes))


if __name__ == '__main__':
    main()
