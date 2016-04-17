from node import *
from utils import *
from htmlize import htmlize

class Texts:
    def __init__(self, origin_text, current_text, changes):
        self.origin_text = origin_text
        self.current_text = current_text
        self.changes = changes


# The difference between nodes are stored as a Change structure.
class Change:
    def __init__(self, orig, cur, cost, is_frame=False):
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
        self.is_frame = is_frame
    def __repr__(self):
        fr = "F" if self.is_frame else "-"
        def hole(x):
            return [] if x==None else x
        return ("(C:" + str(hole(self.orig)) + ":" + str(hole(self.cur))
                + ":" + str(self.cost) + ":" + str(self.similarity())
                + ":" + fr + ")")
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
str_dist_cache = {}


### string distance function
def str_dist(s1, s2):
    cached = str_dist_cache.get((s1, s2))
    if cached is not None:
        return cached

    if len(s1) > 100 or len(s2) > 100:
        if s1 != s2:
            return 2.0
        else:
            return 0

    table = create_table(len(s1), len(s2))
    d = dist1(s1, s2)
    ret = (1.0-d)*2

    str_dist_cache[(s1, s2)]=ret
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

    # try substructural diff
    def trysub(cc):
        (changes, cost) = cc
        if not move:
            return (changes, cost)
        elif can_move(node1, node2, cost):
            return (changes, cost)
        else:
            mc1 = diff_subnode(node1, node2, depth, move)
            if mc1 is not None:
                return mc1
            else:
                return (changes, cost)

    #pdb.set_trace()
    if isinstance(node1, list) and not isinstance(node2, list):
        node2 = [node2]

    if not isinstance(node1, list) and isinstance(node2, list):
        node1 = [node1]

    if isinstance(node1, list) and isinstance(node2, list):
        table = create_table(len(node1), len(node2))
        return diff_list(table, node1, node2, 0, move)


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

    if isinstance(node1, Op) and isinstance(node2, Op):
        if node1.name == node2.name:
            return ([mod_node(node1, node2, 0)], 0)
        else:
            return ([mod_node(node1, node2, 1)], 1)

    #if (isinstance(node1, Attribute) and isinstance(node2, Name) or
        #isinstance(node1, Name) and isinstance(node2, Attribute) or
        #isinstance(node1, Attribute) and isinstance(node2, Attribute)):
        #s1 = attr_to_str(node1)
        #s2 = attr_to_str(node2)
        #if s1 is not None and s2 is not None:
            #cost = str_dist(s1, s2)
            #return ([mod_node(node1, node2, cost)], cost)
        # else fall through for things like f(x).y vs x.y

    if isinstance(node1,Block) and isinstance(node2, Block):
        return diff_node(node1.stmts, node2.stmts, depth, move)

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

        # final all moves local to the node
        return find_moves((changes, cost))

    if (type(node1) == type(node2) and
             is_empty_container(node1) and is_empty_container(node2)):
        return ([mod_node(node1, node2, 0)], 0)

    # all unmatched types and unequal values
    return trysub(([del_node(node1), ins_node(node2)],
                   node_size(node1) + node_size(node2)))



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

        if ((is_frame(ls1[0]) and
             is_frame(ls2[0]) and
             not node_framed(ls1[0], m0) and
             not node_framed(ls2[0], m0))):
            frame_change = [mod_node(ls1[0], ls2[0], c0)]
        else:
            frame_change = []

        # short cut 1 (func and classes with same names)
        if can_move(ls1[0], ls2[0], c0):
            return (frame_change + m0 + m1, cost1)

        else:  # do more work
            (m2, c2) = diff_list(table, ls1[1:], ls2, depth, move)
            (m3, c3) = diff_list(table, ls1, ls2[1:], depth, move)
            cost2 = c2 + node_size(ls1[0])
            cost3 = c3 + node_size(ls2[0])

            if (not different_def(ls1[0], ls2[0]) and
                cost1 <= cost2 and cost1 <= cost3):
                return (frame_change + m0 + m1, cost1)
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




###################### diff into a subnode #######################

# Subnode diff is only used in the moving phase. There is no
# need to compare the substructure of two nodes in the first
# run, because they will be reconsidered if we just consider
# them to be complete deletion and insertions.

def diff_subnode(node1, node2, depth, move):

    if (depth >= FRAME_DEPTH or
        node_size(node1) < FRAME_SIZE or
        node_size(node2) < FRAME_SIZE):
        return None

    if isinstance(node1, AST) and isinstance(node2, AST):

        if node_size(node1) == node_size(node2):
            return None

        if isinstance(node1, Expr):
            node1 = node1.value

        if isinstance(node2, Expr):
            node2 = node2.value

        if node_size(node1) < node_size(node2):
            for f in node_fields(node2):
                (m0, c0) = diff_node(node1, f, depth+1, move)
                if can_move(node1, f, c0):
                    if not isinstance(f, list):
                        m1 = [mod_node(node1, f, c0)]
                    else:
                        m1 = []
                    framecost = node_size(node2) - node_size(node1)
                    m2 = [Change(None, node2, framecost, True)]
                    return (m2 + m1 + m0, c0 + framecost)

        if (node_size(node1) > node_size(node2)):
            for f in node_fields(node1):
                (m0, c0) = diff_node(f, node2, depth+1, move)
                if can_move(f, node2, c0):
                    framecost = node_size(node1) - node_size(node2)
                    if not isinstance(f, list):
                        m1 = [mod_node(f, node2, c0)]
                    else:
                        m1 = []
                    m2 = [Change(node1, None, framecost, True)]
                    return (m2 + m1 + m0, c0 + framecost)

    return None




##########################################################################
##                          move detection
##########################################################################
def move_candidate(node):
    return (is_def(node) or node_size(node) >= MOVE_SIZE)


def match_up(changes, round=0):

    deletions = lfilter(lambda p: (p.cur is None and
                                  move_candidate(p.orig) and
                                  not p.is_frame),
                       changes)

    insertions = lfilter(lambda p: (p.orig is None and
                                   move_candidate(p.cur) and
                                   not p.is_frame),
                        changes)

    matched = []
    new_changes = []
    total = 0

    # find definition with the same names first
    for d0 in deletions:
        for a0 in insertions:
            (node1, node2) = (d0.orig, a0.cur)
            if same_def(node1, node2):
                matched.append(d0)
                matched.append(a0)
                deletions.remove(d0)
                insertions.remove(a0)

                (changes, cost) = diff_node(node1, node2, 0, True)
                nterms = node_size(node1) + node_size(node2)
                new_changes.extend(changes)
                total += cost

                if (not node_framed(node1, changes) and
                    not node_framed(node2, changes) and
                    is_def(node1) and is_def(node2)):
                    new_changes.append(mod_node(node1, node2, cost))
                stat.add_moves(nterms)
                break


    # match the rest of the deltas
    for d0 in deletions:
        for a0 in insertions:
            (node1, node2) = (d0.orig, a0.cur)
            (changes, cost) = diff_node(node1, node2, 0, True)
            nterms = node_size(node1) + node_size(node2)

            if (cost <= (node_size(node1) + node_size(node2)) * MOVE_RATIO or
                node_framed(node1, changes) or
                node_framed(node2, changes)):

                matched.append(d0)
                matched.append(a0)
                insertions.remove(a0)
                new_changes.extend(changes)
                total += cost

                if (not node_framed(node1, changes) and
                    not node_framed(node2, changes) and
                    is_def(node1) and is_def(node2)):
                    new_changes.append(mod_node(node1, node2, cost))
                stat.add_moves(nterms)
                break

    return (matched, new_changes, total)



# Get moves repeatedly because new moves may introduce new
# deletions and insertions.

def find_moves(res):
    (changes, cost) = res
    matched = None
    move_round = 1

    while move_round <= MOVE_ROUND and matched != []:
        (matched, new_changes, c) = match_up(changes, move_round)
        move_round += 1
        changes = lfilter(lambda c: c not in matched, changes)
        changes.extend(new_changes)
        savings = sum(map(lambda p: node_size(p.orig) + node_size(p.cur), matched))
        cost = cost + c - savings
    return changes, cost


#-------------------------------------------------------------
#                     main diff command
#-------------------------------------------------------------



def generate_html(filename, changes, has_lineno=False):
    htmlize(filename, changes, has_lineno)


def cleanup():
    str_dist_cache.clear()

    global allNodes1, allNodes2
    allNodes1 = set()
    allNodes2 = set()


