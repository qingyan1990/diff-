#-------------------------------------------------------------
#                        HTML generation
#-------------------------------------------------------------

import os

from parameters import *
from ast import *
from utils import *


#-------------------- types and utilities ----------------------

class Tag:
    def __init__(self, tag, idx, start=-1):
        self.tag = tag
        self.idx = idx
        self.start = start
    def __repr__(self):
        return "tag:" + str(self.tag) + ":" + str(self.idx)



# escape for HTML
def escape(s):
    s = s.replace('"', '&quot;')
    s = s.replace("'", '&#39;')
    s = s.replace("<", '&lt;')
    s = s.replace(">", '&gt;')
    return s



uid_count = -1
uid_hash = {}
def clear_uid():
    global uid_count, uid_hash
    uid_count = -1
    uid_hash = {}


def uid(node):
    if node in uid_hash:
        return uid_hash[node]

    global uid_count
    uid_count += 1
    uid_hash[node] = str(uid_count)
    return str(uid_count)


def html_header():

    install_path = get_install_path()

    js_filename = ''.join([install_path, 'nav.js'])
    js_file = open(js_filename, 'r')
    js_text = js_file.read()
    js_file.close()

    css_filename = ''.join([install_path, 'diff.css'])
    css_file = open(css_filename, 'r')
    css_text = css_file.read()
    css_file.close()

    out = []
    out.append('<html>\n')
    out.append('<head>\n')
    out.append('<META http-equiv="Content-Type" content="text/html; charset=utf-8">\n')

    out.append('<style>\n')
    out.append(css_text)
    out.append('\n</style>\n')

    out.append('<script type="text/javascript">\n')
    out.append(js_text)
    out.append('\n</script>\n')

    out.append('</head>\n')
    out.append('<body>\n')
    return ''.join(out)


def html_footer():
    out = []
    out.append('</body>\n')
    out.append('</html>\n')
    return ''.join(out)


def write_html(text, side):
    out = []
    out.append('<div id="' + side + '" class="src">')
    out.append('<pre>')
    if side == 'left':
        out.append('<a id="leftstart" tid="rightstart"></a>')
    else:
        out.append('<a id="rightstart" tid="leftstart"></a>')

    out.append(text)
    out.append('</pre>')
    out.append('</div>')
    return ''.join(out)


def htmlize(outname, changes, has_lineno=False):
    if not isinstance(changes, list):
        changes = [changes]
    outfile = open(outname, 'w')
    outfile.write(html_header())
    for c in changes:
        if c.changes is None:
            outfile.write(write_html(c.origin_text, 'left'))
            outfile.write(write_html(c.current_text, 'right'))
        else:
            tags1 = change_tags(c.changes, 'left')
            tags2 = change_tags(c.changes, 'right')
            tagged_text1 = apply_tags(c.origin_text, tags1, has_lineno)
            tagged_text2 = apply_tags(c.current_text, tags2, has_lineno)
            outfile.write(write_html(tagged_text1, 'left'))
            outfile.write(write_html(tagged_text2, 'right'))
        outfile.write('<hr/>')

    outfile.write(html_footer())
    outfile.close()


# put the tags generated by change_tags into the text and create HTML
def apply_tags(s, tags, has_lineno=False):
    tags = sorted(tags, key = lambda t: (t.idx, -t.start))
    curr = 0
    lineno = 1
    out = []
    for t in tags:
        while curr < t.idx and curr < len(s):
            if curr == 0:
                if has_lineno:
                    out.append('<strong>' + fix_width(str(lineno)) + '</strong>')
                    lineno += 1
            out.append(escape(s[curr]))
            if s[curr] == '\n':
                if has_lineno:
                    out.append('<strong>' + fix_width(str(lineno)) + '</strong>')
                    lineno += 1
            curr += 1
        out.append(t.tag)

    while curr < len(s):
        out.append(escape(s[curr]))
        if s[curr] == '\n':
            if has_lineno:
                out.append('<strong>' + fix_width(str(lineno)) + '</strong>')
                lineno += 1
        curr += 1
    return ''.join(out)




#--------------------- tag generation functions ----------------------

def change_tags(changes, side):
    tags = []
    for c in changes:
        key = c.orig if side == 'left' else c.cur
        if hasattr(key, 'lineno'):
            start = node_start(key)
            end = node_end(key)

            if start and end:
                if c.orig != None and c.cur != None:
                    # <a ...> for change and move
                    tags.append(Tag(link_start(c, side), start))
                    tags.append(Tag("</a>", end, start))
                else:
                    # <span ...> for deletion and insertion
                    tags.append(Tag(span_start(c), start))
                    tags.append(Tag('</span>', end, start))

    return tags


def change_class(change):
    if (change.cur == None):
        return 'd'
    elif (change.orig == None):
        return 'i'
    elif (change.cost > 0):
        return 'c'
    else:
        return 'u'


def span_start(change):
    return '<span class=' + qs(change_class(change)) + ' title=' + qs(change_detail(change)) + '>'


def link_start(change, side):
    cls = change_class(change)

    if side == 'left':
        me, other = change.orig, change.cur
    else:
        me, other = change.cur, change.orig
    if cls == 'c':
        return ('<a id=' + qs(uid(me)) +
            ' tid=' + qs(uid(other)) +
            ' class=' + qs(cls) + ' title=' + qs(change_detail(change)) +
            '>')
    else:
        return ('<a id=' + qs(uid(me)) +
            ' tid=' + qs(uid(other)) +
            ' class=' + qs(cls) +
            '>')


def qs(s):
    return "'" + s + "'"


def fix_width(s, number=5):
    need_length = number - len(s)
    spaces = " " * need_length
    return s+spaces

def change_detail(change):
    cla = change_class(change)
    if cla == 'd':
        return type(change.orig).__name__ + " statement delete"
    if cla == 'i':
        return type(change.cur).__name__ + " statement insert"
    if cla == 'c':
        return change.cur.subtype
    return ''

#def type_of_node(node):
    #if isinstance(node,Assign):
        #return 'Assign expression'
    #if isinstance(node,Name):
        #if node.subtype == "name_node":
            #if isinstance(node.parent,FunctionDef):
                #return "function name " + node.id

#def locate_node(node):
    #location = ""
    #line = str(node.lineno)
    #column = str(node.col_offset)
    #location = "(line " + line +",column " + column + ")"
    #return location

#def parent_location(node):
    #node = node.parent
    #if isinstance(node,Module):
        #return " in global context"

#def detail_report(changes):
    #result = ""
    #for change in changes:
        #if change.orig is None and change.cur is None:
            #continue
        #elif is_atom(change.orig) or is_atom(change.cur):
            #continue
        #elif change.cur is None:
            #result += "delete the " + type_of_node(change.orig) + locate_node(change.orig) + parent_location(change.orig) + "\n"
        #elif change.orig is None:
            #result += "insert the " + type_of_node(change.cur) + locate_node(change.cur) + parent_location(change.cur) + "\n"
        #elif type(change.orig) == type(change.cur):
            #if type(change.orig) in (ClassDef,FunctionDef):
                #continue
            #elif change.cost == 0:
                #continue
            #else:
                #result += "change the " + type_of_node(change.orig) + locate_node(change.orig) + " to " + type_of_node(change.cur) + locate_node(change.cur)
        #print result
