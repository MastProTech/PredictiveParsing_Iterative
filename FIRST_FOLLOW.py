first_list=dict() # Global List of First
follow_list=dict() # Global List of Follow

def lookup_match(word, _list):
    match=False
    for key, val_list in _list.items():
        if key==word:
            result=val_list
            match=True
            return result
    return match

def FIRST(word, d):
    first=list()
    if not (word.isupper()):
        print(word, 'is terminal')
        first.append(word)
        first_list[word]=word
        return first
    result=lookup_match(word, first_list)
    if result:
        first=result
        return first
    result=list()
    for i in d[word]:
        if i[0].isupper():
            print(i[0], 'is non-terminal')
            l=FIRST(i[0], d)
            for j in l:
                first.append(j)
        else:
            print(i[0], 'is terminal')
            first.append(i[0])
    first_list[word]=first
    return first



def FOLLOW(word, d, start=False):
    follow=list()
    result=lookup_match(word, follow_list)
    if result:
        print('Result:',result)
        follow=result
        return follow
    if start:
        follow.append('$')
    key_list=list()
    for key, val_list in d.items():
        for val in val_list:
            print('Value:',val)
            loc=val.find(word)
            if loc!=-1:
                if loc+1==len(val):
                    if key==val[loc]:
                        pass
                    else:
                        f_returned=FOLLOW(key, d)
                        for index in f_returned:
                            if index!='$' or (index=='$' and '$' not in follow):
                                if index not in follow:
                                    follow.append(index)
                else:
                    if val[loc+1].isupper():
                        print('VAL:',val[loc+1])
                        print(val[loc+1], 'is non-terminal')
                        l=FIRST(val[loc+1], d)
                        for j in l:
                            if j not in follow:
                                if j!='@':
                                    follow.append(j)
                                else:
                                    l=FOLLOW(val[loc+1], d)
                                    for j in l:
                                        if j not in follow:
                                            follow.append(j)
                    else:
                        print(val, 'is terminal')
                        if val[loc+1] not in follow:
                            follow.append(val[loc+1])
                    print('Follow Found:',val[loc+1])
    follow_list[word]=follow
    return follow

'''
Grammar:
S  -> cAd|bd
A  -> ab|a
'''
g=dict()
# Grammar#1
g['S']=['cAd', 'bd']
g['A']=['ab', 'a']

FIRST('S', g)
FIRST('A', g)
FIRST('c', g)
FIRST('a', g)

FOLLOW('S', g, start=True)
FOLLOW('A', g)


# Grammar#2
# g['E']=['TD']
# g['D']=['+TD', '@']
# g['T']=['FS']
# g['S']=['*FS', '@']
# g['F']=['(E)', 'n']

# FIRST('E',g)
# FIRST('D',g)
# FIRST('T',g)
# FIRST('S',g)
# FIRST('F',g)

# FOLLOW('E',g, start=True)
# FOLLOW('D',g)
# FOLLOW('T',g)
# FOLLOW('S',g)
# FOLLOW('F',g)

print('Given Grammar:')
for item in g.keys():
    print(item,'->',g[item])

print('First List',first_list)
print('Follow List',follow_list)