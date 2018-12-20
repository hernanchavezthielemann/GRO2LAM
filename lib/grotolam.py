#!/usr/bin/python
#    -------------    runing   ----------------
from lib.misc.version import __version__
from lib.misc.file import write_file
from lib.gui.main_gui import launch_gui

class Grotolam(object):
    def __init__(self, master=None):
        
        self._data_ = []
    
    @property
    def content(self):
        return self._data_
    @content.setter
    def content(self, value):
        self._data_ = value
    
    def save_data(self):
        ' in beta.beta version'
        import pickle
        output = ''
        pickle.dump(self._data_ , output, pickle.HIGHEST_PROTOCOL)
        write_file('content.g2l', output)

def grotolam_launcher():
    ''' at this point this is just the name, quite deceptive ;) 
        maybe <run> can call directly the GUI in the future,
        but this handles the library'''
    print '\n'+' '*20+__version__+'\n'
    
    launch_gui()
    
def grotolam_launcher_test():
    
    print '-'*21+'  TESTING  '+'-'*21+'\n\n'
    print '\n'+' '*20+__version__+'\n'
    launch_gui( True)
    
    #conv_data, ckbuttons, solva_tags,_quit_flag_ = launch_gui()
    
    #if not _quit_flag_:
    #    sim_data = extract_gromacs_data(conv_data[1:], solva_tags, ckbuttons)
    #    config = conv_data[0], ckbuttons
    #    flag_done_ = write_lammps_data( sim_data, 'data.gro2lam', config)
    
# vim:tw=79
