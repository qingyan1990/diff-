import json

f = open('json.txt')
content = f.read()
f.close()

h = json.loads(content)
print h.get('type')
