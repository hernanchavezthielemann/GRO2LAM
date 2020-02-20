#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'
# checked ok 27/01/2019

#------------------------------------------------------
#///    Packages and globals definitions are here   ///
#------------------------------------------------------

from Tkinter import Frame, Label, StringVar, Button # , IntVar

from tk_lib import bottom_hline_deco, format_dec, Drop_Down_List
from tk_lib import createmenubar, create_entry, get_entriesvalue
from custom_row import File_Entry

from lib.misc.warn import print_dec_g, pop_wrg_1, pop_err_1
from lib.misc.file import check_file, check_in_file

from lib.handling.gromacs import extract_gromacs_data, get_ffldfiles
from lib.handling.lammps import write_lammps_data

#------------------------------------------------------
'''///////////////        Class       /////////////'''
#------------------------------------------------------

class Conversion(Frame):
    ''' Script creation graphical user interface.
        Since this page was crowding the main
        in order to neat
        this is a better place for it
    '''
    def __init__(self, master=None, **kwargs):
        
        #if not master and options.get('parent'):
        #    master = options['parent']
        self.master  = master
        Frame.__init__(self, master)
        
        self.img = self.master.img
        # inner class object container
        self.objt_c = []
        self.file_e = []

    def create_conversion_gui(self):
        
        # file section
        #=======================       DEFAULTS       =========================
        
        _autoload_ = 0
        
        eg_files=['./Examples/IONP/gromacs/SPIO_em.gro',
                  './Examples/IONP/gromacs/SPIO_part.top',
                  './Examples/IONP/gromacs/forcefield.itp',
                  './Examples/IONP/gromacs/ffoplsaaSI_FE_WATnb.itp',
                  './Examples/IONP/gromacs/ffoplsaaSI_FE_WATbon.itp'
                 ]
        
        #eg_files=['conf.gro','topol.top','forcefield.itp','nb.itp','bon.itp']
        _atomstyle_ = 'full'
        
        data_cont = self.master._convert_['setup']
        if data_cont <> []:
            _autoload_ = data_cont[0]
            eg_files = data_cont[1:-1]
            _atomstyle_ = data_cont[-1]

            
        if _autoload_:
            enabled = [ 1, 1, 0, 0, 0]
        else:
            enabled = [ 1, 1, 1, 1, 1]
            
        fi_txt=['Enter the gro file',
                'Enter the top file',
                'Enter the forcefield file',
                'Enter the non bonded file',
                'Enter the bonded file'
                 ]
        
        ######            CONSTRUCTION SITE      ###############
        ## CS   first header row
        row = Frame(self)
        TEXT1= "\nSelect the parameters to perform the conversion: "
        Label(row, text=TEXT1, anchor='w').pack(side='top', padx=2, pady=10)
        row.pack( side='top', fill='x', padx=5)
        bottom_hline_deco(self)
        
        ## CS   files                              ------------------------- :@
        # appends file entries capturing button also 
        self.objt_c.append( _autoload_) # allocating space for autoload in [0]
        for fi in range( len( eg_files)):
            
            self.file_e.append( File_Entry( self,
                                            e_txt = fi_txt[fi],
                                            e_val = eg_files[fi])
                              )
            self.file_e[-1].setter( enabled[fi])
            self.objt_c.append( self.file_e[-1]._entry)
            self.file_e[-1].pack(fill='x')
            
            if fi == 1:
                self.file_e[-1]._strvar.trace( 'w', self.load_top_file)
                #sv = self.file_e[-1]._strvar
                #sv.trace('w', lambda name, index, mode, sv=sv: self.load_top_file(sv) )
                #"w"
                bottom_hline_deco( self)
                ## CS   autoload                   ------------------------- :@
                # self.objt_c.append inside 
                self.autoload_buffer = ''
                self.autoloadff()
                
            
            
        bottom_hline_deco( self)
        
        ## CS   atom style                         ------------------------- :@
        # self.objt_c.append inside 
        bottom_hline_deco( self, self.atomstyle)
        self.objt_c[-1].set( _atomstyle_)
        
        
        #    Final Buttons                         ------------------------- :@
        self.build_finalbuttons()
        
        ######     END CONSTRUCTION SITE  -> PACK OUTSIDE #########
        
        if self.master.test:
            print 'Seeing main gro2lam converter GUI'
            self.after(2000, self.test_hook  )

    def atomstyle( self):
        ''' in this case just one, but could be modified 
        to be generic, accepting <row>, <text> and <options>'''
        a_mainrow= Frame( self)
        row_fst = Frame( a_mainrow)
        
        #from self-ttk import Combobox
        TEXT2=  'Choose an atom style'
        format_dec([row_fst, TEXT2])

        row_fsep = Frame(row_fst)
        
        atom_var = StringVar()
        atom_style_ddl = Drop_Down_List(row_fsep,
                                        textvariable = atom_var,
                                        #state="readonly"
                                       )
        atom_style_ddl['values'] = ('full', 'charge', 'molecular',
                                    'angle', 'bond','atomic')
        atom_style_ddl.bind("<Key>", lambda e: "break") # Magic
        atom_style_ddl.pack()
        self.objt_c.append( atom_var)
        
        row_fsep.pack(side='left', fill='x', pady=0)
        
        # row packing
        row_fst.pack(side='left', pady=0)
        
        a_mainrow.pack(side='top', fill='x', pady=3)

    def autoloadff(self):
        '''
        function that enables the autoload of the forcefield files as
        stated in the top file, also as a logic side effect disables the 
        file load option for forcefields
        '''
        _a_row_ = Frame(self)
        
        _text_ =  'Autoload forcefield files'
        
        bt_txt_ = 'Press to autoload'
        
        _f_labels = format_dec([_a_row_, _text_])
        
        self.autol_b = Button( _a_row_, text = bt_txt_,
                             #width = 25, height=23,
                             command= self.autoloadstuff
                            )
        self.autol_b.pack(  padx=0)#side='center',
        _a_row_.pack( side='top', fill='x', pady=3)

    def autoloadstuff(self):
        
        nonerr_flag = True
        
        #_autoload_ = self.objt_c[0].get()
        main_top_file = self.objt_c[2].get()

        if self.autoload_buffer <> main_top_file:
        #    self.autoload_buffer = _autoload_
            self.autoload_buffer = main_top_file
            aux_cont, nonerr_flag = get_ffldfiles( main_top_file )
            if nonerr_flag:
                for i in [2, 3, 4]:
                    nonerr_flag *= check_file( aux_cont[i-2])
                    self.file_e[i]._entry.delete(0, 'end')
                    self.file_e[i]._entry.insert(0, aux_cont[i-2])
                    self.file_e[i]._entry.xview_moveto(1)
                    
                    self.file_e[i].setter( 0)
                    
                self.objt_c[0] = ( 1)
            else:
                self.objt_c[0] = ( 0)
        elif self.objt_c[0] and self.autoload_buffer == main_top_file:
            pop_wrg_1('Autoload already performed for selected top file.', _i_=0)
                        
                    
                    
        if not self.objt_c[0]:
            pop_err_1('Autoload failed!')
            self.autoload_buffer = ''
            self.autol_b.configure( state = 'disabled')
            for i in [2, 3, 4]:
                    self.file_e[i].setter( 1)
    
    def load_top_file( self, *args ):#event=None, 
        ''' function to capture the change in the top load button.
        in order to avoid the the waving experienced with a first "''"
        in the entry an if is inside 
        '''
        #print args
        if self.objt_c[2].get() <> '':
            #print ( self.objt_c[2].get())
            
            self.autol_b.configure( state = 'normal')
            for i in [2, 3, 4]:
                    self.file_e[i].setter( 1)
        
    def build_finalbuttons(self):
        
        _ypadhere_ = 1
        Frame(self).pack(side="top", fill='x', pady=35) # Space
        
        _row_= self
        self.b1 = Button(_row_, text='Convert',
                         command = self.getdata_and_convert)
        self.b1.pack( side = 'right', padx=30, pady= _ypadhere_)
        
        b2 = Button(_row_, text = 'Quit', command = self.quit)
        b2.pack( side = 'right', padx=10, pady= _ypadhere_)

    def getdata_and_convert(self):
        
        
        _autoload_ = self.objt_c[0]
        if not _autoload_:
            pop_wrg_1('Proceeding without autoload.\nThis means that any '
                      + 'internal address to files that are not specified '
                      + 'as GUI input are going to be ignored.')
        if self.get_entriesvalues():
            
            data_cont = self.master._convert_['setup']
            root_folder = '/'.join(data_cont[1].split('/')[:-1]+[''])
            print( 'Root folder: {}'.format( root_folder) )
            
            sim_data, _flags_ = extract_gromacs_data( data_cont[1:-1],
                                                     _autoload_)
            flag_done_, _sidemol_ = _flags_
            
            config = [data_cont[-1], _sidemol_, _autoload_, root_folder]
            if flag_done_:
                try:
                    flag_done_, data_fnam = write_lammps_data( sim_data,
                                                               'data.gro2lam',
                                                              config )
                    
                except KeyError as Err:
                    err_str = ''
                    for er in Err.args:
                        err_str += er + ' '
                    pop_err_1('There are missing or incomplete coefficients in'
                              + ' your input files related to: ' + err_str)
                    flag_done_ = False
                except Exception as Exc:
                    pop_err_1('There are inconsistencies in your input files\n'
                             + Exc.args[0]
                             )
                    flag_done_ = False
                    
            if flag_done_:
                print_dec_g( 'Data file generated as "data.gro2lam"' )
                
                self._convertdata_ = sim_data
                self._convertdata_['filename'] = data_fnam
                self._convertdata_['config'] = config
                
                # Returning the values
                self.master._convertdata_ = self._convertdata_
                
                # to ensure freshness of our dependant values
                self.master._script_['advanced'] = []
                self.master._script_['restrain'] = []
                
                self.master.swapbody(2)
                
        else:
            pop_wrg_1('The setup needs some further improvements'
                        +'to be runed. Please check your inputs')

    def get_entriesvalues(self):
        ''' ---   app entry getter   ----
        mainly to obtain values beside check buttons
        ... which check buttons?
        '''
        e_values=[]
        _flag_ = True
        ent_rang  =  range(len(self.objt_c))
        
        for ent in ent_rang:#[1:]:
            if ent == 0:
                e_values.append( self.objt_c[ent])
            else:
                e_values.append(self.objt_c[ent].get())
                if ent and ent <= 5:
                    _flag_ *= check_file(e_values[-1])
            
        self.master._convert_['setup'] = e_values
        return _flag_

    def test_hook(self, event=None):
        self.autol_b.invoke()
        self.b1.invoke()

    def createWidgets(self):
        ''' unified name hook'''
        self.create_conversion_gui()

# vim:tw=80
