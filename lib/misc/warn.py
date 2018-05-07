#!/usr/bin/python
#    By Hernan Chavez Thielemann

from lib.gui.popup import message_box

def ye_deco(func):
    def func_wrapper(name):
        return "\033[93m{0}\033[0m".format(func(name))
    return func_wrapper

#@ye_deco
def wrg_3(*text):
    '''  yellow warning scheme'''
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
    
def green(_text_):
    return '\033[92m'+_text_+'\033[0m '

def pop_wrg_1(*_text_, **kwargs):
    
    if '_i_' in kwargs.keys():
        _i_ = kwargs['_i_']
    else:
        _i_ = -1
        
    print wrg_1(*_text_)
    message_box(_text_[_i_], 'Warning', icon='warning')
    
def pop_err_1(*_text_, **kwargs):
    
    if '_i_' in kwargs.keys():
        _i_ = kwargs['_i_']
    else:
        _i_ = -1
        
    print wrg_1(*_text_)
    message_box(_text_[_i_], 'Error', icon='error')
## test

#print wrg_1('')
#print wrg_2('')
#print wrg_3('')
#print dec_g('deco')
