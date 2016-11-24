import codecs
import json
f = codecs.open('result.txt', encoding='utf-8')
for line in f:
    line_obj = json.loads(line)
    print(line_obj['summary'])
