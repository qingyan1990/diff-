from parser import Parser
from json import loads

s = open('json.txt').read()
h = loads(s)

node = Parser().convert(h)
print node

