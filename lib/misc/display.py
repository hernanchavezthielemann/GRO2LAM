#!/usr/bin/python
#    By Hernan Chavez Thielemann
#    this came out of a blend of warn and verbose 

from sys import stdout

__verbose__ = [True,0,0,0]

def in_red_(_text_):
    return '\033[91m' + _text_ + '\033[0m'

def in_green_(_text_):
    return '\033[92m' + _text_ + '\033[0m'

def in_yellow_(_text_):
    return '\033[93m' + _text_ + '\033[0m'

def yellow_deco(func):
    def func_wrapper(name):
        return "\033[93m{0}\033[0m".format(func(name))
    return func_wrapper
#@yellow_deco

def show_in_green(*text):
    '''  this should be replaced with a colour_show with sep = "\n"
        now this looks like nonsense ;)
    '''
    n_text = ''
    if text != None:
        for line in text[:-1]:
            n_text += line +'\n'
        n_text += text[-1]
    show(  in_green_( n_text ))
    
    
def show( *multi_print, **kargs):
    ''' show in terminal function
        to handle basically two things:
            verbose levels (under development)
            print under py2 and py3 with the same behaviour
                e.g. to avoid : print( var1, var2) >< print var1, var2
    '''
    # verbose level set in each show command, else is printed
    try:
        v = kargs['v'] - 1
    except KeyError:
        v = 0
    
    if __verbose__[ v]:
        
        try:
            end = kargs['end']
        except KeyError:
            end = '\n'
        try:
            sep = kargs['sep']
        except KeyError:
            sep = ' '
        try:
            deep = kargs['deep']
        except KeyError:
            deep = 0
        #ln = len( multi_print)
        try:
            string = sep.join( multi_print)
        except TypeError:
            #if not deep:
            #    for item in multi_print:
            #        show( item, str(type(item)), deep = 1 )
            #    show( 'other', type(multi_print), deep = 1 )
            multi_print = [ str( item ) for item in multi_print]
            string = sep.join( multi_print)
        #string = '{}'.format( elem)
        
        stdout.write( string + end)
        stdout.flush()
        
        
def set_verbose( degrees ):
    ''' four degrees of verbose deep should be more than enough'''
    global __verbose__
    
    def_max = 4
    if degrees < 1:
        degrees = 1
    elif degrees > def_max:
        def_max = degrees
    
    __verbose__ = [ True]*degrees + [ False]*( def_max - degrees)
    
def test_show():
    set_verbose( 2)
    a = 'misc txt here\n oops new line in the same var'
    b = "another var\n with\n multiple\n lines"
    c = 'last var'
    show( )
    show( a)
    show( a , b, c)
    show( a , b, c, sep = '')
    show( a , b, c, sep = '\n')
    show( a , b, c, end = ' - ')
    show( a , b, c, sep = ' - ', end = '\n')
    show('-------------------')
    
    _in_file_ = './lib/./gui/main_gui.py'
    act_size = 7074
    show( ["{ '", _in_file_, "':", act_size, '}'])
    show('-------------------')
    show( "{ '", _in_file_, "':", act_size, '}', v = 2)
    show('-------------------')
    show( "{ '", _in_file_, "':", act_size, '}',sep='', v = 2)
    
    aux_dict = {'./lib/./gui/main_gui.py':7074,'./lib/i.py':7,'./lib/mobi.dic':1010}
    show( aux_dict)
    show( a , b, c, sep = ' & ', end = '\n', v = 3)
    show('-------------------')

## test
if __name__ == '__main__':
    #print wrg_1('')
    #print wrg_2('')
    #print wrg_3('')
    #print dec_g('deco')
    test_show()
    pass

# vim:tw=80