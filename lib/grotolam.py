#!/usr/bin/python
#    -------------    runing simulations   ----------------
__version__ = 'GROTOLAM version 1.0 (13 Apr 2018)'#.split()[2]

#from os import getcwd, walk, chdir, makedirs, system
#from os.path import join
#from sys import exit, argv

from lib.misc.file import write_file
from gui.main_gui import launch_gui
#from handling.gromacs import extract_gromacs_data
#from handling.lammps import write_lammps_data

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
    
    print '\n'+' '*20+__version__+'\n'
    
    
    
    launch_gui()
    #conv_data, ckbuttons, solva_tags,_quit_flag_ = launch_gui()
    
    #if not _quit_flag_:
    #    sim_data = extract_gromacs_data(conv_data[1:], solva_tags, ckbuttons)
    #    config = conv_data[0], ckbuttons
    #    flag_done_ = write_lammps_data( sim_data, 'data.gro2lam', config)
# vim:tw=79
