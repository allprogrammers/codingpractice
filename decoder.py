import json
encoded = input()
letters = {}
letters['a'] = 'f'
letters['b'] = 'i'
letters['c'] = 'l'
letters['d'] = 'o'
letters['e'] = 'r'
letters['f'] = 'u'
letters['g'] = 'x'
letters['h'] = 'a'
letters['i'] = 'm'
letters['j'] = 'g'
letters['k'] = 'j'
letters['l'] = 'd'
letters['m'] = 'p'
letters['n'] = 's'
letters['o'] = 'v'
letters['p'] = 'y'
letters['q'] = 'b'
letters['r'] = 'e'
letters['s'] = 'h'
letters['t'] = 'k'
letters['u'] = 'n'
letters['v'] = 'q'
letters['w'] = 't'
letters['x'] = 'w'
letters['y'] = 'z'
letters['z'] = 'c'
letters[' '] = ' '

for i in encoded:
    print(letters[i],end="")
