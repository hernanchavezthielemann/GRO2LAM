#!/usr/bin/python
#    -------------    runing simulations   ----------------
__version__ = 'GROTOLAM version 2.0 (07 May 2018)'#.split()[2]

__old_ver__ = ['version 1.0 (13 Apr 2018)']

__url__ = 'https://github.com/hernanchavezthielemann/GRO2LAM'

#from lib.misc.file import write_file
from gui.main_gui import launch_gui


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
        ' in beta version'
        import pickle
        output = ''
        pickle.dump(self._data_ , output, pickle.HIGHEST_PROTOCOL)
        write_file('content.g2l', output)

def grotolam_launcher():
    ''' at tis point this is just the name, quite deceptive ;) 
        maybe <run> can call directly the GUI'''
    print '\n'+' '*20+__version__+'\n'
    
    launch_gui()
    
def grotolam_launcher_test():
    
    print '\n'+' '*20+__version__+'\n'
    launch_gui( True)
    
    #conv_data, ckbuttons, solva_tags,_quit_flag_ = launch_gui()
    
    #if not _quit_flag_:
    #    sim_data = extract_gromacs_data(conv_data[1:], solva_tags, ckbuttons)
    #    config = conv_data[0], ckbuttons
    #    flag_done_ = write_lammps_data( sim_data, 'data.gro2lam', config)
# vim:tw=79
