#!/usr/bin/python
#    By Hernan Chavez Thielemann


def ye_deco(func):
    def func_wrapper(name):
        return "\033[93m{0}\033[0m".format(func(name))
    return func_wrapper

#@ye_deco
def wrg_3(*text):
    '''  warning scheme'''
    n_text = ''
    if text <>None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    return '\033[93mWarning!!\033[0m -- '+ n_text
    
def wrg_2(*text):
    '''  warning scheme'''
    n_text = ''
    if text <>None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    return '\033[92m'+'Warning!!'+'\033[0m -- ' + n_text
    
def wrg_1(*text):
    '''  warning scheme'''
    n_text = ''
    if text <>None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    return '\033[91m'+'Warning!!'+'\033[0m -- ' + n_text

def print_dec_g(*text):
    '''  warning scheme'''
    n_text = ''
    if text <>None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    print '\033[92m'+n_text+'\033[0m '
    
## test

#print wrg_1('')
#print wrg_2('')
#print wrg_3('')
#print dec_g('deco')
