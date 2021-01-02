first_list=dict() # Global List of First
follow_list=dict() # Global List of Follow
entries=list() # Each entry in 'entries' contains: [key, first, rule]

def lookup_match(word:str, _list:dict)->bool: # Check if 'word' is in dictionary
    for key, val_list in _list.items():
        if key==word:
            result=val_list
            return result
    return False

def FIRST(word:str, d:dict)->list:
    first=list()
    if not (word.isupper()): # Terminal Detected: FIRST(terminal)=terminal
        # print(word, 'is terminal')
        first.append(word)
        return first
    result=lookup_match(word, first_list) # Already exists?
    if result:
        first=result
        return first
    result=list()   
    for i in d[word]:
        if i[0].isupper():
            # Non-Terminal Detected: FIRST(Non-Terminal1)->Non-Terminal2 => FIRST(Non-Terminal1)<-FIRST(Non-Terminal2)->?
            # print(i[0], 'is non-terminal')
            first_returned=FIRST(i[0], d) # Recursion continues until FIRST is detected
            for j in first_returned:
                entries.append([word, j, word+'->'+i]) ##################################################
                first.append(j)
        else: # Terminal Detected: FIRST(Non-Terminal)->Terminal
            # print(i[0], 'is terminal')
            first.append(i[0])
            if i[0]=='@': # '@' -> epsilon
                follow_returned=FOLLOW(word, d)
                for j in follow_returned:
                    entries.append([word, j, word+'->'+i]) ##############################################
            else:
                entries.append([word, i[0], word+'->'+i]) ##############################################
                # terminals.add(i[0])
    first_list[word]=first
    return first

def FOLLOW(word:str, d:dict, start=False)->list:
    follow=list()
    result=lookup_match(word, follow_list) # Already exists?
    if result:
        # print('Result:',result)
        follow=result
        return follow
    
    if start: # Given word is start of grammar?
        follow.append('$')
    for key, val_list in d.items():
        for val in val_list: # Check each rule if it contains given key
            # print('Value:',val)
            loc=val.find(word)
            if loc!=-1: # Found given word
                if loc+1==len(val): # Reached at end of rule. E->TD reader reached at D
                    if key!=val[loc]: # Will not iterate on it's own rule. E->TE. That'll create a loop
                        f_returned=FOLLOW(key, d) # follow_returned
                        for index in f_returned:
                            if index not in follow:# and index!='$' or (index=='$' and '$' not in follow):
                                # index shouldn't create duplicates in follow
                                # if index contains '$' then append only if it's not already in follow
                                follow.append(index)
                else: # Haven't reached end of rule
                    if val[loc+1].isupper(): # If NEXT is Non-Terminal
                        # print(val[loc+1], 'is non-terminal')
                        f_returned=FIRST(val[loc+1], d) # first_returned
                        for j in f_returned: # Add each value in f_returned in follow
                            if j not in follow: # Preventing duplicates
                                if j!='@': 
                                    follow.append(j)
                                else: # if follow contains epsilon
                                    f_returned=FOLLOW(val[loc+1], d)
                                    for j in f_returned:
                                        if j not in follow:
                                            follow.append(j)
                    else: # NEXT is Terminal
                        # print(val, 'is terminal')
                        if val[loc+1] not in follow: # Preventing duplicates
                            follow.append(val[loc+1])
                    # print('Follow Found:',val[loc+1])
    follow_list[word]=follow
    return follow

def parsing_table(entries_list, non_terminals, terminals):
    d_t=dict()
    d_nt=dict()
    # Making and filling the table using 2D Dictionaries
    for i in terminals:
        d_t[i]='Error'
    for i in non_terminals:
        d_nt[i]=d_t.copy()

    # Entry in the table start now
    for entry in entries_list:
        d_nt[entry[0]][entry[1]]=entry[2]
    print('Table in RAW form:')
    for k in d_nt.keys():
        print(k, d_nt[k])
    formatted_table(d_nt, list(non_terminals), list(terminals))

def formatted_table(d:dict, non_terminals, terminals): # Prints the table in beautiful format
    t_spacing=10
    nt_spacing=10
    headers='NTs\\Ts'.center(nt_spacing)+'|'
    for i in terminals:
        headers+=i.center(10)+'|'
    print('*'*len(headers))
    print('|'+headers)
    print('*'*len(headers))
    
    for i in range(len(non_terminals)):
        row=''
        for j in terminals:
            row+=d[non_terminals[i]][j].center(t_spacing)+'|'
        print('|'+non_terminals[i].center(nt_spacing)+'|'+row)
        print('-'*len(headers))
    print('*'*len(headers))

g=dict()

# Grammar#1
# g['S']=['cAd', 'bd']
# g['A']=['ab', 'a']

# FOLLOW('S', g, start=True)
# FOLLOW('A', g)

# FIRST('S', g)
# FIRST('A', g)
# FIRST('c', g)
# FIRST('a', g)

# Grammar#2
g['E']=['TD']
g['D']=['+TD', '@']
g['T']=['FS']
g['S']=['*FS', '@']
g['F']=['(E)', 'n']

FOLLOW('E',g, start=True)
FOLLOW('D',g)
FOLLOW('T',g)
FOLLOW('S',g)
FOLLOW('F',g)

FIRST('E',g)
FIRST('D',g)
FIRST('T',g)
FIRST('S',g)
FIRST('F',g)

# Grammar#3
# g['S']=['F', '(ST)']
# g['T']=['+FT', '@']
# g['F']=['i', 'n']

# FOLLOW('S', g, start=True)
# FOLLOW('T', g)
# FOLLOW('F', g)

# FIRST('S', g)
# FIRST('T', g)
# FIRST('F', g)

print('Given Grammar:')
for item in g.keys():
    print(item,'->',g[item])

print('First List')
for key in first_list:
    print('FIRST({0})->{1}'.format(key, first_list[key]))
print('Follow List')
for key in follow_list:
    print('FOLLOW({0})->{1}'.format(key, follow_list[key]))

print('\nentries:\n',entries,'\n')

terminals=set()
for j in g:
    for i in g[j]:
        for k in i:
            if not str.isupper(k):
                terminals.add(k)
non_terminals=[i for i in g]
terminals.discard('@') # Replace '@' with '$' while making table
terminals.add('$')

parsing_table(entries, non_terminals, terminals)