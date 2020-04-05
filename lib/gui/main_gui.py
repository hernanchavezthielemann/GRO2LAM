#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'
# checked ok 30/04/2018 

#------------------------------------------------------
#///    Packages and globals definitions are here   ///
#------------------------------------------------------
from os.path import dirname, realpath
from sys import exit

from Tkinter import Tk, Frame, Label, TclError, PhotoImage

from conversion_gui import Conversion
from script_gui import Script_GUI
from run_gui import Run_GUI

from popup import AboutPopUp
from tk_lib import createmenubar

from lib.misc.warn import wrg_3
from lib.misc.file import run_command
from lib.misc.version import __version__

#------------------------------------------------------
'''///////////////        Class        /////////////'''
#------------------------------------------------------

class Gro2Lam_GUI(Frame):
    ''' Graphic User Interface '''
    def __init__(self, master=None, test = False):
        Frame.__init__(self, master)
        _ver= __version__.split()
        self.master.title(" "*5+"{}    {}".format(_ver[0],_ver[2]))#.master
        
        self.pack() # ... why I'm packing here?? coords?
        self.test = test
        
        # images storaging
        dir_path = dirname( realpath( __file__))
        self.img = dict()
        self.img['logo']    = PhotoImage( file = dir_path + "/img/logo.ppm")
        self.img['help']    = PhotoImage( file = dir_path + "/img/help.ppm")
        self.img['file']    = PhotoImage( file = dir_path + "/img/file.ppm")
        self.img['gear']    = PhotoImage( file = dir_path + "/img/gear.ppm")
        
        # body init
        self.prevailing_body = 0
        self.body = None
        self.MAINVERTEX = [ 0, 0, 0, 0, 0, 0]
        
        # Conversion gathered data container
        self._convert_ = {'setup' : [], 'solvation': []}
        self._convertdata_= None
        # Script part
        self._script_ = {'mainpage' : [], 'advanced': [], 'restrain': []}
        
        self.createmainPennon()
        

    def createmainPennon(self):
        '''Self explanatory neated with subroutines to make it more readable'''
        
        row = Frame(self,bg = "white")
        Label( row, bg = "white",
              image = self.img['logo']).pack( side= 'left', padx=25)
        row.pack(side="top", fill='x', padx=1)
        
        self.swapbody(1)

    def swapbody(self, _pbody_):# checked ok 16/09 -----------WF
        ''' Deletes and clean the last generated body
            maybe lacks a real body destroyer?? but works fine with
            this, because it is just a "small" overlapping I gess
        '''
        
        if self.prevailing_body <> _pbody_:
            if self.body == None:
                self.body = self.create_conversion_gui()
                
            else:
                self.body.destroy()
                    
                if _pbody_==1:
                    print 'Swapping to gro2lam converter GUI'
                    self.body = self.create_conversion_gui()
                    
                elif _pbody_==2:
                    print 'Swapping to input script generator GUI'
                    self.body = self.create_script_gui()
                    
                elif _pbody_==3:
                    print 'Swapping to run script GUI'
                    self.body = self.create_run_gui()
                    
                else:
                    exit('Wuut...')
                
            self.prevailing_body = _pbody_
            
            self.body.createWidgets()
            self.body.b1.focus()
            self.master.bind('<Return>', self.b1_hook )
            self.master.bind('<Escape>', self.quit_hook )
            self.body.pack(side='top', fill='x')

    def b1_hook(self, event=None):
        self.body.b1.invoke()
            
    def quit_hook(self, event=None):
        self.body.quit()
        
    def swap_hook(self):
        _l_ = [1,2,3]
        b = _l_[_l_.index(self.prevailing_body)-2]
        self.swapbody(b)
        
    def create_conversion_gui(self):
        'Hook to create conversion gui'
        return Conversion(self)# Hook
    
    def create_script_gui(self):
        'Hook to create script gui'
        return Script_GUI(self)# Hook
    
    def create_run_gui(self):
        'Hook to create run gui'
        return Run_GUI(self)# Hook

#------------------------------------------------------
'''///////////////     Sub routines     /////////////'''
#------------------------------------------------------

def launch_gui( started = False):
    ''' launcher 
        Main GUI constructor
    '''
    
    print wrg_3('Before you start, make sure there are no comments',
                '(;) in the middle of a line of the input GROMACS files.',
                'Data after this symbol are not taken into account.')
    
    MasterWin = Tk()
    prompt = Gro2Lam_GUI( master= MasterWin, test = started)# xl_App
    
    # Top main pennon menu bar definition
    
    entry_list_of_dicts = [{ 'title' : 'File',
                            'cascade' : (('Quit' ,MasterWin.quit), ) },
                           { 'title' : 'Data File Creation',
                            'title_com' : (prompt.swapbody , 1)},
                           { 'title' : 'Input File Creation',
                            'title_com' : (prompt.swapbody , 2)},
                           { 'title' : 'Run',
                            'title_com' : (prompt.swapbody , 3)},
                           { 'titlei' : prompt.img['help'], 
                            'cascade' : (('User manual' , showuserman),
                                         ('About' , launch_about, prompt),)}
                          ]
    createmenubar(MasterWin, entry_list_of_dicts)
    
    w = 460
    h = 570
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
    MasterWin.geometry('{:d}x{:d}+{:d}+{:d}'.format( *prompt.MAINVERTEX[2:]))
    
    
    prompt.mainloop()
    
    try:
        MasterWin.destroy()
    except TclError:
        pass

def showlicence():
    
    print 'Opening licence file'
    command = 'gedit ./lib/docs/COPYING'#
    run_command(command)

def launch_about( _master_window_):
    
    print 'Launching about'
    
    title_txt = ' '*17+'ABOUT GROTOLAM'
    
    pop = AboutPopUp(master = _master_window_,
                     title = title_txt,
                     licence = showlicence
                    )

def showuserman():
                     
    print 'Opening readme file'
    command = 'gedit ./lib/docs/README.md'#
    run_command(command)

# vim:tw=80
