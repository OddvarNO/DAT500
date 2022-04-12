thisset = set()
with open('profanitylist.txt', 'r') as f:
    for line in f:
        thisset.add(line.strip())

print(thisset)