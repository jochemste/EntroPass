#!/usr/bin/env python3
import sys
import time
from threading import Thread
import itertools

def permutations(keywords, fixed_len=None):
    perms = itertools.permutations(keywords)
    if fixed_len==None:
        perms = itertools.permutations(keywords)
    else:
        perms = itertools.permutations(keywords, fixed_len)

    perms_as_list=[]

    for perm in perms:
        word=''
        for char in perm:
            word+=char
        perms_as_list.append(word)

    return perms_as_list
        
def invert_string(string):
    return string[::-1]

def thread_func1(keywords, ctr, results):
    cat = cat_keywords(keywords, ctr)
    if not(cat in results[ctr]):
        results[ctr].append(cat)

    cat = invert_string(cat)
    if not(cat in results[ctr]):
        results[ctr].append(cat)

def thread_func2(keywords, ctr, results):
    pass

def remove_duplicates_list(dlist):
    dlist = list(dict.fromkeys(dlist))
    return dlist

def replace_chars(string, char, rep_char, count=None, occurrence=None):
    ctr=0
    if occurrence:
        
    elif count==None:
        new_string=''
        for c in string:
            new_char = c
            if c==char:
                new_char = rep_char
            new_string += new_char
    elif occurrence==None:
        new_string=''
        for c in string:
            new_char = c
            if c==char and ctr<count:
                new_char = rep_char
                ctr+=1
            new_string += new_char
    return new_string

def architecture():
    results=[]
    threads=[]
    keywords=[]
    for i in range(1, len(sys.argv)):
        keywords.append(sys.argv[i])

    perms = permutations(keywords)

    for i in range(len(keywords)):
        results.append([])
        threads.append(Thread(target=thread_func2, args=(keywords, i, results,)))
        threads[-1].start()

    [t.join() for t in threads]

    full_list = perms
    for r in results:
        full_list+=r
    for i in range(1,len(keywords)):
        full_list += permutations(keywords, i)
    full_list = remove_duplicates_list(full_list)

    mod_list=[]
    for string in full_list:
        s = replace_chars(string=string, char='a', rep_char='@')
        mod_list.append(s)
    full_list+= mod_list


    mod_list=[]
    for string in full_list:
        if 'a' in string:
            s = replace_chars(string=string, char='a', rep_char='@', count=1)
            mod_list.append(s)
    full_list+= mod_list

    print('Results:')
    [print(k) for k in full_list]


def main():
    start = time.time()

    architecture()
    
    stop = time.time()

    print('Time needed: ', str(int(stop-start))+'s', '('+str(stop-start)+')')

if __name__=='__main__':
    main()
