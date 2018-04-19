#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'
# checked ok 11/04/2018 

#------------------------------------------------------
#///    Packages and globals definitions are here   ///
#------------------------------------------------------

from Tkinter import Tk, Frame, Label, Button, Entry, Listbox, PhotoImage
from Tkinter import Checkbutton
from Tkinter import SUNKEN, TOP, LEFT, RIGHT, X, Y, TclError, VERTICAL
from Tkinter import END, IntVar, YES

from os import getcwd, system
from os.path import dirname, realpath
from sys import exc_info, exit

from popup import FilePopUp, PromptPopUp, AboutPopUp, PromptPopUp2
from tk_lib import bottom_hline_deco, generate_listbox, format_dec
from tk_lib import createmenubar, create_entry, get_entriesvalue
from lib.misc.warn import wrg_1, wrg_3, print_dec_g
from lib.misc.file import check_file, run_command
from lib.grotolam import __version__

from lib.handling.gromacs import extract_gromacs_data
from lib.handling.lammps import write_lammps_data, write_lammps_input

#------------------- GLOBALS  --------------------
global dir_path, lib_path

dir_path = dirname( realpath( __file__))
lib_path = dir_path




#------------------------------------------------------
'''///////////////        Class        /////////////'''
#------------------------------------------------------

class Gro2Lam_GUI(Frame):
    ''' Graphic User Interface '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        _ver= __version__.split()
        self.master.title(" "*25+"{}    {}".format(_ver[0],_ver[2]))#.master
        self.pack()
        
        self.im_file = PhotoImage( file= lib_path+"/img/file.ppm")
        self.im_logo = PhotoImage( file= lib_path+"/img/logo.ppm")
        self.im_gear = PhotoImage( file= lib_path+"/img/gear.ppm")
        
        self.prevailing_body = 1
        
        self.MAINVERTEX = [0, 0, 0, 0, 0, 0]
        # total data container
        self.data_c = []
        
        self.f_par_container = []
        
        self._bstatus = [1,1,0]
        self._ckvar = []
        self._ckbut_container=[]
        
        self._solvatedinfo_= None
        
        self._quit_flag_ = True # seems not used
        
        self.createWidgets()
        self.set_ckbuttonstate(self._bstatus)
        
        # Script part
        self.script_basicsetup = []
        self._convertdata_= None

    def createWidgets(self):
        ''' Self explanatory neated with subroutines to make it more readable'''
        
        row = Frame(self,bg = "white")
        Label(row,bg = "white", image= self.im_logo).pack(side= LEFT, padx=25)
        row.pack(side="top", fill=X, padx=1)
        
        self.body = Frame(self)
        # this part can be changed to make it more dynamic
        self.create_conversion_gui()
        self.body.pack( side=TOP, fill=X)

    def swapbody(self, _pbody_):# checked ok 16/09 -----------WF
        ''' Deletes and clean the last generated mol entry '''
        
        if self.prevailing_body <> _pbody_:
            self.body.destroy()
            self.body = Frame(self)
                
            if _pbody_==1:
                print 'Swapping to converter GUI'
                self.data_c = []
                self.f_par_container = []
                self._ckvar = []
                self._ckbut_container=[]
                self.create_conversion_gui()
                self.set_ckbuttonstate(self._bstatus)
            elif _pbody_==2:
                print 'Swapping to input generator GUI'
                self.create_script_gui()
                
            elif _pbody_==3:
                print 'Swapping to run cript GUI'
                self.create_run_gui()
                
            else:
                exit('Wuut...')
                
            self.prevailing_body = _pbody_
            self.body.pack(side=TOP, fill=X)

    def create_conversion_gui(self):
        
        #    first header row
        row = Frame(self.body)
        TEXT1= "\nSelect the parameters to perform the conversion: "
        Label(row, text=TEXT1, anchor='w').pack(side=TOP, padx=2, pady=10)
        row.pack( side=TOP, fill=X, padx=5)
        bottom_hline_deco(self.body)
        
        #Section for atom style
        bottom_hline_deco(self.body, self.atomstyle)

        # file section
        
        fi_txt=['Enter the gro file',
                'Enter the top file',
                'Enter the forcefield file',
                'Enter the non bonded file',
                'Enter the bonded file']
        for fi in range(len(ex_files)):
            self.f_par_container.append(self.createfileentry(self.body ,
                                                             fi_txt[fi],
                                                             ex_files[fi]))
        bottom_hline_deco(self.body)
        
        bottom_hline_deco(self.body, self.build_check_section)
        #    Final Buttons
        self.build_finalbuttons()

    def build_check_section(self):
        
        row = Frame(self.body)
        self.check_row( row, 'Solvated .gro file',['  Configuration -> '])
        self.solv_b = Button( row, image= self.im_gear,
                             command=(lambda: config_solvation(self)))
        self.solv_b.pack(side=RIGHT, padx=0)
        row.pack(side=TOP, fill=X, pady=3)
        
        #  Parametrization or Parameterization ???
        row = Frame(self.body)
        self.check_row( row, 'Parametrization in file',['.top','.itp'])
        row.pack(side=TOP, fill=X, pady=3)

    def atomstyle(self):
        ''' in this case just one, but could be modified 
        to be generic, accepting <row>, <text> and <options>'''
        a_mainrow= Frame(self.body)
        row_fst = Frame(a_mainrow)
        
        
        TEXT2=  'Choose an atom style'
        format_dec([row_fst, TEXT2])
        
        _options= ['Full','Angle','Atomic']
        row_fsep = Frame(row_fst)
        self.f_par_container.append(generate_listbox(row_fsep, _options))
        row_fsep.pack(side=LEFT, fill=X, pady=0)
        #labelc = Label(row_fst, width=1, anchor='w')
        #labelc.pack(side=LEFT, padx=0)
        
        # row packing
        row_fst.pack(side=LEFT, pady=0)
        
        a_mainrow.pack(side=TOP, fill=X, pady=3)

    def check_row(self, _s_row_, _text_, _desc_=['']):
        
        _f_labels = format_dec([_s_row_, _text_], _pack_=False)
        
        for d in range(len(_desc_)):
            cvar = IntVar()
            self._ckvar.append(cvar)
            label_ck = Checkbutton(_s_row_, width=0, text= _desc_[d]
                                   ,variable=cvar
                                   ,command=(lambda: self.checkbuttonstuff())
                                   , anchor='w')
            self._ckbut_container.append(label_ck)
        
        format_dec(_f_labels, _create_=False)
        
        for d in range(len(_desc_)):
            self._ckbut_container[-len(_desc_)+d].pack(side=LEFT, padx=6)

    def set_ckbuttonstate(self, __sel__):
        '''Button setter in charge of set on or off 
        the entries acordingly to the check button status'''
        self._bstatus=__sel__
        for bck in range(len(self._ckbut_container)):
            if __sel__[bck]:
                self._ckbut_container[bck].select()
            else:
                self._ckbut_container[bck].deselect()

    def checkbuttonstuff(self):
        '''If this point is reached, some checkbutton changed,
        so this impose the available states'''
        auxi=-1
        _ckvar_g_=[]
        # First detect wich one change, comparing the fresh value
        # <self._ckvar[v].get()> with the stored <_bstatus>
        for v in range(len(self._ckvar)):
            _ckvar_g_.append(self._ckvar[v].get())
            if self._bstatus[v]<>_ckvar_g_[v]:
                auxi=v# and self.ckvar_g[v]==1:
        # Now, what was the change, and react:
        if auxi==0:
            if _ckvar_g_[0]==0:
                print wrg_1('You are choosing to not consider solvation.'
                            +' If some ', 'solvent molecules are on the'
                            +' .gro file they will be ignored!')
                self.solv_b.configure(state='disabled')
                self._ckbut_container[0].configure( text= '')
            else:
                self.solv_b.configure(state='normal')
                self._ckbut_container[0].configure(text= ' Configuration -> ')
        elif auxi==1:
            if _ckvar_g_[1]==0:
                _ckvar_g_[2]=1
            elif _ckvar_g_[1]==1:
                _ckvar_g_[2]=0
            else:
                # there is no action yet to print '
                pass
        elif auxi==2:
            if _ckvar_g_[2]==0:
                _ckvar_g_[1]=1
            elif _ckvar_g_[2]==1:
                _ckvar_g_[1]=0
            else:
                # there is no action yet to print '
                pass
        
        self.set_ckbuttonstate(_ckvar_g_)

    def createfileentry(self, parent_frame, fi_text, _def_fi_):
        ''' '''
        file_row = Frame(parent_frame)
        f_ex = ((fi_text ,'.'+_def_fi_.split('.')[-1]),)
        
        _f_labels = format_dec([file_row, fi_text], _pack_=False)
        
        Efile = Entry(file_row, width=13)
        Efile.insert(END, _def_fi_)
        Bsearch = Button(file_row, image= self.im_file,
                         command=(lambda El=Efile: self.browsefile(El, f_ex)))
        
        
        # Just packing
        format_dec(_f_labels, _create_=False)
        
        Efile.pack(side=LEFT, expand=YES, fill=X)
        
        Bsearch.pack(side=RIGHT, padx=0, pady=0)
        file_row.pack(side=TOP, fill=X, pady=3)
        
        # For tracing purposes list appending
        return Efile

    def build_finalbuttons(self):
        
        _row_= self.body
        b1 = Button(_row_, text='Convert',
                    command=(lambda: self.getdata_and_convert()))
        b1.pack(side=RIGHT, padx=30, pady=20)
        b2 = Button(_row_, text='Quit', command=self.quit)
        b2.pack(side=RIGHT, padx=10, pady=4)

    def browsefile(self, entry, ext=None):
        '''Browse a file button'''
        
        pop = FilePopUp(master=self)
        if ext<>None and isinstance(ext, tuple):
            #print '--- ', ext, type(ext)
            pop.filetypes['filetypes']=ext #(("All","*"),) # 
        filepath= pop.getfilepath()
        try:
            fito = open(filepath,"r")
            fito.close()
            entry.delete(0, END)
            entry.insert(0, filepath)
            entry.xview_moveto(1)
        except:
            if filepath<>'':
                print "Could not open File: ", filepath
                print exc_info()[1]

    def getdata_and_convert(self):
        
        if ( self._bstatus[0] and self._solvatedinfo_ == None):
            print wrg_1('First perform the solvation configuration --'
                       ,'You can do it pressing the gears')
            
        elif self.get_entriesvalues():
            
            # conv_data, ckbuttons, solva_tags,_quit_flag_ = launch_gui()
            sim_data = extract_gromacs_data(self.data_c[1:],
                                            self._solvatedinfo_,
                                            self._bstatus[:2])
            config = [self.data_c[0]]+ self._bstatus[:2]# <-- config --[0,1,2]
            flag_done_ = write_lammps_data( sim_data, 'data.gro2lam', config)
            
            if flag_done_:
                print_dec_g( 'Data file generated as "data.gro2lam"' ) 
            self._convertdata_ = sim_data
            self._convertdata_['config'] = config
        else:
            print wrg_1('-- The setup needs some further improvements'
                        +'to be runed --','Please check your inputs')

    def get_entriesvalues(self):
        ''' ---   app entry getter   ----
        mainly to obtain values beside check buttons'''
        e_values=[]
        _flag_ = True
        Flistbox = self.f_par_container[0]
        if len(Flistbox.curselection())>0:
            e_values.append(Flistbox.get(Flistbox.curselection()[0]))
        else:
            print wrg_3(" Select an atom style --- (select/click on it)\n")
            _flag_ = False
        for ent in range(len(self.f_par_container))[1:]:
            e_values.append(self.f_par_container[ent].get())
            _flag_ *= check_file(e_values[-1])
        self.data_c = e_values
        return _flag_

    def create_script_gui(self):
        'create_script_gui'
        
        #    first header row
        row = Frame(self.body)
        TEXT1= "\nIn this section you can create scripts "
        Label(row, text=TEXT1, anchor='w').pack(side=TOP, padx=2, pady=1)
        row.pack( side=TOP, fill=X, padx=5)
        bottom_hline_deco(self.body)
        
        #Section for atom style
        #=====================================================================
        '''  Create script section '''
        row2fill = Frame(self.body)
        row2fill_l = Frame(row2fill)
        self.s_entry_c = []
        
        self.s_entry_c.append(self.createfileentry(row2fill_l,
                                                 'Lammps data file to work',
                                                 './data.gro2lam')
                           )
        
        _entries_=[ 'Timestep [fs]', '-','NVE steps  [#]','-',
                   'NVT steps  [#]','Temperature at start:end [K]', 'Temperature damping [fs]',
                   '-','NPT steps  [#]', 'Presure at start:end  [atm]', 'Presure damping [fs]',
                   'Temperature at start:end [K]', 'Temperature damping [fs]']
        _defvals_=[ '0.5', '100000',
                   '100000', '400:293', '100',
                   '100000','-5:1', '1000', '400:293', '100']
        
        
        entr_maxlen = int(len(max(_entries_, key=len))*2.5/3)
        c=0
        for e in range(len(_entries_)):
            if _entries_[e]=='-':
                bottom_hline_deco(row2fill_l)
                c+=1
            else:
                self.s_entry_c.append(create_entry(row2fill_l,
                                                 _entries_[e],
                                                 _defvals_[e-c],
                                                 entr_maxlen))
        row2fill_l.pack( side="left")
        
        #===========        RIGHT section   =================================
        row2fill_r = Frame(row2fill)
        if self.script_basicsetup == []:
            self.script_basicsetup = [ '100', 'array', 'lj/cut/coul/long',
                                      '8.5','10','1.75', 'ewald', '1e-4',
                                      '0.0:0.0:0.5','1','1', 'aniso',
                                     ]

        self.fcb = Button( row2fill_r, image= self.im_gear,
                    command=(lambda re= self :
                             further_config_script(re)))
        self.fcb.pack(side='top', padx=10, pady=10)
        Frame(row2fill_r).pack(side="top", padx=40, pady=20)# --------------------- OJO

        Frame(row2fill_r).pack(side="top", pady=94)# -------------------- OJO
        
        row2fill_r.pack(side="right")
        row2fill.pack(side="top", padx=1, pady=5)
        
        bottom_hline_deco(self.body)

        #=====================================================================
        #    Final Button
        row= Frame(self.body)
        #Frame(row).pack(side="top", pady=2)# ------------------------ OJO
        b1 = Button( row, text='Create',# height=8,
                    command=( lambda re= self : write_script(re))
                   )
        b1.pack(side='left', padx=2, pady=4)
        b2 = Button(row, text='Quit', command=self.quit)
        b2.pack(side=RIGHT, padx=20, pady=4)
        row.pack( side='right', fill='both', padx=5)

    def create_run_gui(self):
        
        #=====================================================================
        #    first header row
        row = Frame(self.body)
        TEXT1= "\nIn this section you can run scripts "
        Label(row, text=TEXT1, anchor='w').pack(side=TOP, padx=2, pady=10)
        row.pack( side=TOP, fill=X, padx=5)
        bottom_hline_deco(self.body)
        
        
        '''  RUN  section '''
        entr_maxlen = int(8*2.5)
        self.r_entry_c = []
        row2fill = Frame(self.body)
        row2fill_l = Frame(row2fill)
        self.r_entry_c.append(self.createfileentry(row2fill_l,
                                                   'Select the script to run',
                                                   './in.gro2lam')
                             )
        _entries_ = ['Machine', 'Cores']
        _defvals_=['lammps','1']
        for e in range(len(_entries_)):
            self.r_entry_c.append(create_entry(row2fill_l,
                                               _entries_[e],
                                               _defvals_[e],
                                               entr_maxlen))
        row2fill_l.pack(side="left")
        row2fill_r = Frame(row2fill)
        b2 = Button( row2fill_r, text='Run', height=4,
                    command=( lambda re= self.r_entry_c :
                             run_script(*get_entriesvalue(re)))
                   )
        b2.pack(side=RIGHT, padx=5, pady=4)
        row2fill_r.pack(side="right")
        row2fill.pack(side="top", padx=1, pady=5)
        
        bottom_hline_deco(self.body)
        #=====================================================================
        #    Final Button
        row= Frame(self.body)
        Frame(row).pack(side="top", pady=2)# ------------------------ OJO
        b2 = Button(row, text='Quit', command=self.quit)
        b2.pack(side=RIGHT, padx=20, pady=4)
        row.pack( side='bottom', fill='both', padx=5)

#------------------------------------------------------
'''///////////////     Sub routines     /////////////'''
#------------------------------------------------------
def swap2converter(_app_):
    print 'swap to converter'
    _app_.swapbody(1)
def swap2lammpsinput(_app_):
    print 'swap to lammps input'
    _app_.swapbody(2)
def swap2runscript(_app_):
    print 'swap to runs cript'
    _app_.swapbody(3)
    
def showlicence():
    
    print 'opening licence file'
    command = 'gedit ./lib/docs/COPYING'#
    run_command(command)

def launch_about( _master_window_):
    
    print 'launching about'
    
    title_txt = 'GROTOLAM'
    
    pop = AboutPopUp(master = _master_window_,
                     title = title_txt,
                     licence = showlicence
                    )

def showuserman():
                     
    print 'Opening readme file'
    command = 'gedit ./lib/docs/README.txt'#
    run_command(command)

def write_script( _app_):
    
    print 'Writing the lammps script'
    _script_setup_  = [ get_entriesvalue( _app_.s_entry_c)
                       , _app_.script_basicsetup ]
    
    flag_done_ = write_lammps_input( _script_setup_, _app_._convertdata_ )
    
    if flag_done_:
        print_dec_g( 'Lammps script done!')

def run_script( _file_, machine='lammps', _cores_=1):
    
    if check_file(_file_):
        print _file_
        command = ''
        if _cores_>1:
            command = 'mpirun -np {} {} -in {}'.format(_cores_,
                                                       machine,
                                                       _file_)
        else:
            command ='{} -in {}'.format( machine, _file_)
        run_command(command)

def launch_gui():
    ''' launcher '''
    
    print wrg_3('Before you start, make sure there are no comments',
                '(;) in the middle of a line of the input GROMACS files.',
                'Data after this symbol are not taken into account.')
    
    global ex_files
    ex_files=['./Examples/IONP/Original/SPIO_part-water-em.gro',
    './Examples/IONP/Original/SPIO_part.top',
    './Examples/IONP/Original/forcefield.itp',
    './Examples/IONP/Original/ffoplsaaSI_FE_WATnb.itp',
    './Examples/IONP/Original/ffoplsaaSI_FE_WATbon.itp']
    #ex_files=['conf.gro','topol.top','forcefield.itp','nb.itp','bon.itp']
    
    
    MasterWin = Tk()
    prompt = Gro2Lam_GUI( master= MasterWin)# xl_App
    
    help_icon = PhotoImage( file= lib_path+"/img/help.ppm")
    entry_list_of_dicts = [{ 'title' : 'File',
                            'cascade' : (('Quit' ,MasterWin.quit), ) },
                           { 'title' : 'Converter',
                            'title_com' : (prompt.swapbody , 1)},#swap2converter , prompt)},
                           { 'title' : 'Script',
                            'title_com' : (prompt.swapbody , 2)},#swap2lammpsinput , prompt)},
                           { 'title' : 'Run',
                            'title_com' : (prompt.swapbody , 3)},#swap2runscript , prompt)},
                           { 'titlei' : help_icon, 
                            'cascade' : (('User manual' , showuserman),
                                         ('About' , launch_about, MasterWin),)}
                          ]
    createmenubar(MasterWin, entry_list_of_dicts)
    
    w = 460
    h = 560
    # get screen width and height
    ws = MasterWin.winfo_screenwidth() # width of the screen
    hs = MasterWin.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws/6) - (w/2)
    if x <100:
        x = 100
    y = (hs/3) - (h/2)
    if y< 40:
        y = 40
        
    prompt.MAINVERTEX = [ws, hs, w, h, x, y]
    #print MAINVERTEX
    # set the dimensions of the screen 
    # and where it is placed
    MasterWin.geometry('{:d}x{:d}+{:d}+{:d}'.format(*prompt.MAINVERTEX[2:]))

    prompt.mainloop()
    
    #_ckb_data_ = prompt._bstatus[:2]
    #_data_ = prompt.data_c
    #_flag_ = prompt._quit_flag_
    #_slv_tags_ = prompt._solvatedinfo_
    try:
        MasterWin.destroy()
    except TclError:
        pass
    
    #return _data_, _ckb_data_, _slv_tags_, _flag_

def further_config_script( _app_ ):
    
    defvals = []
    title_txt = ' '*3+'+ Simulation Parameters'
    instructions = 'Input further simulation parameters'
    askfor = ['Thermo output every',
              'Atom mapping',
              'Pairwise interactions',
              'L-J/Buck rcutoff',
              'Coulomb rcutoff',
              'Neighbor distance',
              'Long-range solver',
              'Long-range relative error',
              'Interaction 1-2:1-3:1-4',
              'Neighbor delay', 
              'Neighbor update',
              'Pressure control'
              
             ]
    defaultanswer = _app_.script_basicsetup 
            
    _app_.fcb.config(bg = 'gray40', width = 45) #cyan')
    _app_._aux_ = []
    pop = PromptPopUp2(master = _app_,
                      title = title_txt,
                      briefing = instructions, 
                      entries_txt = askfor, 
                      entries_val = defaultanswer,
                      width = 350,
                      height = 480
                     )
    
    pop.wait_window()
    if _app_._aux_ <> []:
        _app_.script_basicsetup = _app_._aux_
    _app_.fcb.config(bg = 'lightgrey', width = 29)

def config_solvation( _app_):
        
    title_txt = ' '*15+'Input Water name'
    instructions = 'Enter the atom tag letters of:'
    askfor = ['O in the non bonded file',
              'H in the non bonded file',
              'O in the .gro file',
              'H in the .gro file',
              'H - O partial charge'
              #'Na+ in the .gro file (if are present)',
              #'Cl- in the .gro file (if are present)'
             ]
    if _app_._solvatedinfo_ ==  None:
        defaultanswer = ['opls_116','opls_117','OW','HW1, HW2','0.4238'
                        #,'Na','Cl'
                       ]
    else:
        defaultanswer = _app_._solvatedinfo_
        
    _app_.solv_b.config(bg = 'gray40', width = 45) #cyan')
    _app_._aux_ = []
    pop = PromptPopUp2(master = _app_,
                      title = title_txt,
                      briefing = instructions, 
                      entries_txt = askfor, 
                      entries_val = defaultanswer
                     )
    
    pop.wait_window()
    if _app_._aux_ <> []:
        _app_._solvatedinfo_ = _app_._aux_
    _app_.solv_b.config(bg = 'lightgrey', width = 29)

# vim:tw=80
