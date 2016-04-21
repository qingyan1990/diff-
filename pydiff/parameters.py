#-------------------------------------------------------------
# global parameters
#-------------------------------------------------------------

DEBUG = False
# sys.setrecursionlimit(10000)


MOVE_RATIO     = 0.2
MOVE_SIZE      = 10
MOVE_ROUND     = 5

FRAME_DEPTH    = 1
FRAME_SIZE     = 20

allNodes1 = set()
allNodes2 = set()

CHANGETYPEDICT = {
    ('UFO', None): "",
    ('test', 'If'): "If condition change",
    ('test', 'While'): "While condition change",
    ('name_node', 'FunctionDef'): "Function rename",
    ('name_node', 'ClassDef'): "Class rename",
    ('args', 'arguments'): "Argument rename",
    ('value', 'Yield'): "Yield value change",
    ('value', 'Return'): "Return value change",
    ('decorator_list', 'FunctionDef'): "Decorator rename",
    ('values', 'Print'): 'Print value change',
    ('func', 'Call'): "Function name in call change",
    ('right', 'BinOp'): "Right part in BinOp change",
    ('left', 'BinOp'):  "Left part in BinOp change",
    ('args', 'Call'): "Args in Call rename",
    ('value', 'Assign'): "Value in Assignment change",
    ('elts', 'Tuple'): "Element in Tuple change",
    ('value', 'keyword'): "value of keyword change",
    ('targets', 'Assign'): "Target in Assignment rename",
    ('inst', 'Raise'): "inst in Raise change",
    ('type', 'Raise'): "Raise Type change",
    ('values', 'Dict'): "Value in Dict change",
    ('kwarg_name', 'FunctionDef'): "kwarg in FunctionDef rename",
    ('opsName', 'Compare'): "Operator in Compare stmt change",
    ('iter', 'For'): "iterator in For change"
}

