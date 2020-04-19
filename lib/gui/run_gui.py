#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'
# checked ok 04/04/2018 

#------------------------------------------------------
#///    Packages and globals definitions are here   ///
#------------------------------------------------------

from Tkinter import Frame, Button, Label

from tk_lib import create_entry, get_entriesvalue, bottom_hline_deco
from custom_row import createfileentry
from lib.misc.data import check_vars
from lib.misc.file import check_file, run_command

#------------------------------------------------------
'''///////////////        Class       /////////////'''
#------------------------------------------------------
class Run_GUI(Frame):
    ''' Script creation graphical user interface.
        Since script gui  was crowding the main
        in order to neat
        this is a better place for them
    '''
    def __init__(self, master=None, **options):
        self.master  = master
        Frame.__init__(self, master)
        self.img = self.master.img

    def createWidgets(self):
        'create the script gui'
        #    first header row
        row = Frame(self)
        TEXT1= "\nIn this section you can run scripts "
        Label(row, text=TEXT1, anchor='w').pack(side='top', padx=2, pady=10)
        row.pack( side='top', fill='x', padx=5)
        bottom_hline_deco(self)
        
        
        '''  RUN  section '''
        entr_maxlen = int(8*2.5)
        self.r_entry_c = []
        row2fill = Frame(self)
        row2fill_l = Frame( row2fill)
        
        _def_inname_ = 'in.gro2lam'
        if self.master._convertdata_ not in [[], None] :
            _def_dataname_ = self.master._convertdata_['filename']
            _folder_ = '/'.join( _def_dataname_.split('/')[:-1]+[''])
            _def_inname_ =  _folder_ + _def_inname_
        else:
            _def_inname_ = './' + 'in.gro2lam'
        b_enb = ( self.master._convertdata_ == None)
        self.r_entry_c.append( createfileentry( self,
                                               'Select the script to run',
                                               _def_inname_,
                                               ['.in', 'in.*'],
                                               ['lammps input',]*2,
                                               b_enb
                                              )
                            )
        _entries_ = ['Machine', 'Cores']
        _defvals_=[['lammps-daily',
                    [ 'lammps', 'lmp_mpi', 'lmp_ubuntu' ,'lammps-daily']],
                    [ 1, {1}|set(range(3*3*3+1)[::2][1:])|{27,28}] # should be enough
                  ]
        for e in range(len(_entries_)):
            self.r_entry_c.append(create_entry(row2fill_l,
                                               _entries_[e],
                                               _defvals_[e],
                                               entr_maxlen))
            
        row2fill_l.pack(side="left")
        row2fill_r = Frame(row2fill)
        
        row2fill_r.pack(side="right")
        row2fill.pack(side="top", padx=1, pady=5)
        
        bottom_hline_deco(self, bottom_hline_deco(self))
        
        self.build_finalbuttons()
        
        if self.master.test:
            self.after(2000, self.master.master.destroy )
            print '\n'+'-'*20 + '  Test ended  ' + '-'*20
    
    def build_finalbuttons(self):
        '''    Final Buttons    '''
        row = Frame(self)#.body)
        #    Final Button
        Frame(row).pack(side='top', pady=4)# ------------------------ OJO
        row.pack(fill='x')
        
        row= Frame(self)#.body)
        self.b1 = Button( row, text='Run',
                    command=( lambda re= self.r_entry_c :
                             run_script(*get_entriesvalue(re)))
                   )
        self.b1.pack(side='right', padx=15, pady= 5)
        
        b2 = Button(row, text='Quit', command= self.quit )
        b2.pack(side='right', padx=5, pady= 4)
        row.pack( side='right', fill='both', padx=5)
        

def run_script( _file_, machine='lammps', _cores_='1'):
    
    core_flag = min(check_vars([_cores_],['int'],'Run aborted!'))
    if check_file(_file_) and core_flag:
        print _file_
        command = '{} -echo both -in {}'.format( machine, _file_)
        if int(_cores_)>1:
            command = 'mpirun -np {} '.format( _cores_) + command
            
        run_command(command)
        

