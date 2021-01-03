#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>' 


from lib.misc.warn import wrg_1, wrg_3, pop_wrg_1
from lib.misc.display import show #
from os import getcwd, walk, system, stat
from os.path import join, sep
from subprocess import Popen, PIPE


p_sep = sep

def check_file(_in_file_, content = True, string2chk = '', size = 0):
    '''Check the correctness of the given input file address'''
    
    ok_flag = False
    show( _in_file_, v = 4)
    try:
        with open( _in_file_, "r") as _auxf:
            su = 0
            strcheck = False
            if content:
                if string2chk == '':
                    try:
                        prev_line = ''
                        for line in _auxf:
                            su += len( line.rstrip('\n'))
                            prev_line = line
                    except UnicodeDecodeError:
                        show( prev_line, line, sep = '\n', v = 3)
                else:
                    for line in _auxf:
                        line = line.rstrip('\n')
                        if string2chk in line:
                            strcheck = True
        
        if content and su < 2 and string2chk == '':
            pop_wrg_1(' File {} is empty -- '.format(_in_file_))
        elif content and string2chk != '' and not strcheck:
            aux_txt = ' Section {} not found in file {} -- '
            pop_wrg_1( aux_txt.format( string2chk, _in_file_))
        else:
            act_size = stat( _in_file_).st_size
            if size:
                if act_size == size:
                    ok_flag = True
                else:
                    show( '<{}:{}-{}>'.format(_in_file_, act_size, size),
                         sep='', v =3)
            else:
                show( "{ '", _in_file_, "': ", act_size, '}', sep='', v = 3)
                ok_flag = True
            
    except IOError:
        pop_wrg_1(' File {} not found -- '.format( _in_file_))
        
    return ok_flag

def check_file_list(files_list, extensions=['*']):
    '''Check for input files integrity and extension'''
    finam = ''
    _flag = True
    try:
        for x in range(len(files_list)):
            finam = files_list[x].split('/')[-1]
            fi = open (files_list[x],'r')
            fi.close()
            ext = finam.split('.')[-1]
            if extensions != ['*'] and not ext in extensions:
                show( extensions)
                show( wrg_3( ' Invalid format: < ' + ext + ' >') )
                _flag = False
                break
    except IOError:
        if finam == '':
            show( wrg_3( " Select a file --- "))
        else: 
            show( wrg_3(' No such file or directory: ' + finam))
        _flag = False
    return _flag
def check_in_file( _file_, *args, **kwargs):
    ''' Checks if some args are in a file or not '''
    
    _flags_ = [0 for x in args]
    
    with open( _file_, 'r')  as indata:
        if 'slce' in kwargs.keys():
            
            _min, _max = [ int(x) for x in kwargs['slce'].split(':')]
            for k_line in indata:
                for a in range( len( args)):
                    #show( args[a]
                    line_c = k_line[ _min: _max].strip(' ')
                    #show( line_c
                    if args[a] == line_c:
                        _flags_[a] = 1
                        if min(_flags_):
                            break
                            
        elif 'pstn' in kwargs.keys():
            position = int(kwargs['pstn'])
            for k_line in indata:
                for a in range( len( args)):
                    line_c = k_line.split()
                    if len(line_c) > position:
                        if args[a] == line_c[position]:
                            _flags_[a] = 1
                            if min(_flags_):
                                break
                            
        else:
            for k_line in indata:
                for a in range(len(args)):
                    #show( args[a]
                    line_c = k_line.split(args[a])
                    if len(line_c)>1:
                        _flags_[a] = 1
                        if min(_flags_):
                            break
    return _flags_

def make_dir( _path_, _name_):
    
    if _path_[-1] == '/':
        path_dir = _path_ + _name_
    else:
        path_dir = _path_ + '/' + _name_
    show( 'Creating folder {}'.format( path_dir))
    # TODO: hadle the case in which the folder already exists
    #try:
    #    write_file( 'test.txt', content=' ', path_dir):
    #    out_file = open( path_dir + '/' + 'test.txt', "r")
    #    out_file.close()
    #    
    #except IOError:
    if len(path_dir.split(' ')) > 1:
        path_dir = '"' + path_dir + '"'
    system( 'mkdir ' + path_dir)
    return path_dir + '/'

def write_xfile(filename='test.txt',  content=''):
    
    write_file( filename, content)
    system('chmod +x '+filename)

def move_file( _file_, _folder_):
    system('mv ' + _file_ + ' ' + _folder_)

def write_file( filename='test.txt', content='', _folder_ = None):
    '''classic file maker'''
    out_file = open( filename, "w")
    out_file.write( content)
    out_file.close()
    
    if _folder_ != None:
        move_file( filename, _folder_)
    
    

def write_list2file( filename, listofstrings):
        '''datafile maker'''
        plaintext=""
        
        if type(listofstrings)==type([]):
            for strings in listofstrings:
                plaintext+= strings+"\n"
            write_file( filename, plaintext)
        else:
            show( wrg_3(" Wrong format list --- "), listofstrings)

def write_listoflist2file( filename, listoflistsofstrings):
        '''datafile maker'''
        
        listofstrings=[]
        if type(listoflistsofstrings)==type([]):
            for rw in range(len(listoflistsofstrings)):
                row_text=""
                for st in range(len(listoflistsofstrings[rw])):
                    row_text+=listoflistsofstrings[rw][st]+' '
                row_text=row_text[:-1]
                listofstrings.append(row_text)
            write_list2file( filename, listofstrings)
        else:
            show( wrg_3(" Wrong format list --- ") )

def debugger_file( char_str,  container ):
    ''' debugger'''
    show( char_str)
    write_listoflist2file( char_str+'.txt', container )

def run_command(__command__):
    ''' Runs the command'''    
    system(__command__)
    #return Popen(__command__,stdout=PIPE,stdin=PIPE, shell=True )

def fileseeker( path = getcwd(), word = 'data', notw = None):
    '''seek data & destroy, returns a list of posible files,
    filtered by "word" criterion
    '''
    list_of_files = []
    if path == getcwd():
        DIR = '.'
    else:
        DIR = path 
    for (root, folder, filenames) in walk( DIR, topdown = True):
        for name in filenames:
            list_of_files.append( join( root, name))
    files = []
    for fs in range( len( list_of_files)):
        # Could implement "while not" and use the same list_of_files
        # with remove(list_of_files[fs])
        _file_ = list_of_files[fs]
        if '/' in _file_ and word in _file_.split('/')[-1]:
            if notw != None and notw in _file_.split('/')[-1]:
                pass
            else:
                files.append( _file_)
    if files == []:
        show( wrg_3( " No file(s) found with " + word + " criterion---"))
        
    return files
 
# vim:tw=80
