from collections import Counter

def readwords( filename ):
    f = open(filename)
    words = [ line.rstrip() for line in f.readlines()]
    return words

positive = readwords('positive.txt')
negative = readwords('negetive.txt')

paragraph = 'this is really bad and in fact awesome. really awesome.'

count = Counter(paragraph.split())
print(count)
pos = 0
neg = 0
for key, val in count.items():
    key = key.rstrip('.,?!\n') # removing possible punctuation signs
    if key in positive:
        pos += val
    if key in negative:
        neg += val

print(pos)
print(neg)