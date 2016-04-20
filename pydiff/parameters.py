#-------------------------------------------------------------
# global parameters
#-------------------------------------------------------------
from ast import *

DEBUG = False
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
                  ('values', 'Print'): 'Print value change'}
