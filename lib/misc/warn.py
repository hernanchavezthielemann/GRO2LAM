#!/usr/bin/python
#    By Hernan Chavez Thielemann
#    this came from a blend of warn and verbose 

from lib.gui.popup import message_box
from display import show

def wrg_3(*text):
    '''  Yellow warning scheme'''
    n_text = ''
    if text != None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    return '\033[93mWarning!!\033[0m -- '+ n_text
    
def wrg_2(*text):
    '''  Green warning scheme'''
    n_text = ''
    if text != None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    return '\033[92m'+'Warning!!'+'\033[0m -- ' + n_text
    
def wrg_1(*text):
    '''  Red!! warning scheme'''
    n_text = ''
    if text != None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text +=text[-1]
    return '\033[91m'+'Warning!!'+'\033[0m -- ' + n_text

def pop_wrg_1(*_text_, **kwargs):
    ''' Warning pop-up'''
    if '_i_' in kwargs.keys():
        _i_ = kwargs['_i_']
    else:
        _i_ = -1
        
    show( wrg_1(*_text_) )
    message_box(_text_[_i_], 'Warning', icon='warning')
    
def pop_err_1(*_text_, **kwargs):
    ''' error pop-up'''
    if '_i_' in kwargs.keys():
        _i_ = kwargs['_i_']
    else:
        _i_ = -1
        
    show( wrg_1(*_text_) )
    message_box(_text_[_i_], 'Error', icon='error')
    