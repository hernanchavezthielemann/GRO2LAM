#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>' 


from lib.misc.warn import wrg_1, wrg_3 #
from os import getcwd, walk, system 
from os.path import join
from subprocess import Popen, PIPE

def check_file(_in_file_):
    '''Check the correctness of the given input file address'''
    try:
        _auxf = open(_in_file_,"r")
        _auxf.close()
        return True
    except IOError:
        print wrg_3(' File {} not found -- '.format(_in_file_))
        return False

def check_file_list(files_list, extensions=['*']):
    '''Check for input files integrity'''
    finam=''
    try:
        for x in range(len(files_list)):
            finam= files_list[x].split('/')[-1]
            fi= open (files_list[x],'r')
            fi.close()
            ext= finam.split('.')[-1]
            if extensions<>'*' and not ext in extensions:
                print extensions
                print wrg_3(' Invalid format: < '+ext+' >')
                return False
        return True
    except IOError:
        if finam== '':
            print wrg_3(" Select a file --- ")
        else: 
            print wrg_3(' No such file or directory: '+ finam)
        return False

def write_xfile(filename='test.txt',  content=''):
    
    write_file( filename, content)
    system('chmod +x '+filename)

def write_file( filename='test.txt', content=''):
        '''classic file maker'''
        out_file = open( filename, "w")
        out_file.write( content)
        out_file.close()

def write_list2file( filename, listofstrings):
        '''datafile maker'''
        plaintext=""
        
        if type(listofstrings)==type([]):
            for strings in listofstrings:
                plaintext+= strings+"\n"
            write_file( filename, plaintext)
        else:
            print wrg_3(" Wrong format list --- "), listofstrings

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
            print wrg_3(" Wrong format list --- ")

def debugger_file( char_str,  container ):
    ''' debugger'''
    print char_str
    write_listoflist2file( char_str+'.txt', container )

def run_command(__command__):
    ''' Runs the command'''    
    return Popen(__command__,stdout=PIPE, shell=True )

def fileseeker(path=getcwd(),word='data'):
    '''seek data & destroy, returns a list of posible files,
    filtered by "word" criterion'''
    list_of_files=[]
    if path==getcwd():
        DIR='.'
    else:
        DIR=path
    for (root, folder, filenames) in walk(DIR, topdown=True):
        for name in filenames:
            list_of_files.append(join(root, name))
    files=[]
    for fs in range(len(list_of_files)):
        # Could implement "while not" and use the same list_of_files
        # with remove(list_of_files[fs])
        _file_=list_of_files[fs]
        if '/' in _file_ and word in _file_.split('/')[-1]:
            files.append(_file_)
    if files==[]:
        print wrg_3(" No file(s) found with "+word+" criterion---")
    return files;

