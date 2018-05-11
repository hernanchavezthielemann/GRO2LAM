#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'
# checked ok 04/05/2018 

#------------------------------------------------------
#///    Packages and globals definitions are here   ///
#------------------------------------------------------

from Tkinter import Frame, Label, IntVar, Radiobutton, StringVar
from Tkinter import Widget, Button

from popup import PromptPopUp, PromptPopUp_wck
from tk_lib import bottom_hline_deco, format_dec, Drop_Down_List
from tk_lib import createmenubar, create_entry, get_entriesvalue

from lib.misc.data import check_vars
from lib.misc.warn import print_dec_g, pop_wrg_1, pop_err_1
from lib.misc.file import check_file, check_in_file

from lib.handling.gromacs import extract_gromacs_data
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
    def __init__(self, master=None, **options):
        
        #if not master and options.get('parent'):
        #    master = options['parent']
        self.master  = master
        Frame.__init__(self, master)
        
        self.im_gear = self.master.im_gear
        
        # inner class object container
        self.objt_c = []
        

    def create_conversion_gui(self):
        
        #    first header row
        row = Frame(self)
        TEXT1= "\nSelect the parameters to perform the conversion: "
        Label(row, text=TEXT1, anchor='w').pack(side='top', padx=2, pady=10)
        row.pack( side='top', fill='x', padx=5)
        bottom_hline_deco(self)
        
        # file section
        #=======================       DEFAULTS       =========================
        ex_files=['./Examples/IONP/Original/SPIO_part-water-em.gro',
                  './Examples/IONP/Original/SPIO_part.top',
                  './Examples/IONP/Original/forcefield.itp',
                  './Examples/IONP/Original/ffoplsaaSI_FE_WATnb.itp',
                  './Examples/IONP/Original/ffoplsaaSI_FE_WATbon.itp'
                 ]
        #ex_files=['conf.gro','topol.top','forcefield.itp','nb.itp','bon.itp']
        _atomstyle_ = 'full'
        _radio_ = 1
        
        data_cont = self.master._convert_['setup']
        if data_cont <> []:
            ex_files = data_cont[:-2]
            _atomstyle_ = data_cont[-2]
            _radio_ = data_cont[-1]
        
        fi_txt=['Enter the gro file',
                'Enter the top file',
                'Enter the forcefield file',
                'Enter the non bonded file',
                'Enter the bonded file'
               ]
        
        for fi in range( len( ex_files)):
            self.objt_c.append( 
               self.master.createfileentry(
                   self, fi_txt[fi], ex_files[fi],
               )
            )
        bottom_hline_deco( self)
        
        bottom_hline_deco( self, self.atomstyle)
        self.objt_c[-1].set( _atomstyle_)
        
        self.sol_buffer = _radio_
        bottom_hline_deco( self, self.build_solvation_section)
        self.objt_c[-1].set( _radio_)
        
        #    Final Buttons
        self.build_finalbuttons()
        
        if self.master.test:
            print 'Seeing main gro2lam converter GUI'
            self.after(2000, self.master.swap_hook  )

    def build_solvation_section( self):
        
        row = Frame(self)
        
        self.radio_part( row, 'Solvation atoms', [' yes',' no'])
        
        self.solv_b = Button( row, image= self.im_gear,
                             width = 25, height=23,
                             command= self.config_solvation
                            )
        self.solv_b.pack( side='right', padx=0)
        row.pack( side='top', fill='x', pady=3)

    def radio_part(self, _s_row_, _text_, _desc_=[''], _vals_=[]):
        
        _f_labels = format_dec([_s_row_, _text_])#, _pack_=False)
        
        radio_var = IntVar()
        for d in range( len( _desc_)):
            
            label_rb = Radiobutton(_s_row_, width=0, text= _desc_[d]
                                   ,variable = radio_var
                                   , value= len( _desc_)-1-d
                                   ,command = self.solvastuff
                                   , anchor='w'
                                  )
            label_rb.pack(side='left', padx=6)
        self.objt_c.append( radio_var)
        
    
    def solvastuff(self):
        '''If this point is reached, some button changed '''
        
        _solvation_ = self.objt_c[-1].get()
        if self.sol_buffer <> _solvation_:
            self.sol_buffer = _solvation_
            
            if _solvation_:
                self.solv_b.configure( state = 'normal')
            else:
                pop_wrg_1('You are choosing to not consider solvation.'
                                ,' If some solvent molecules are in the'
                                +' .gro file they will be ignored!', _i_=0)
                self.solv_b.configure( state = 'disabled')


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

    def build_finalbuttons(self):
        
        Frame(self).pack(side="top", fill='x', pady=20) # Space
        
        _row_= self
        self.b1 = Button(_row_, text='Convert',
                         command = self.getdata_and_convert)
        self.b1.pack( side = 'right', padx=30, pady=15)
        
        b2 = Button(_row_, text = 'Quit', command = self.quit)
        b2.pack( side = 'right', padx=10, pady=4)

    def getdata_and_convert(self):
        _solvatedinfo_ = self.master._convert_['solvation']
        
        if ( self.objt_c[-1].get() and _solvatedinfo_ == []):
            pop_wrg_1( 'First perform the solvation configuration.'
                      + ' You can do it pressing the solvation settings gears',
                      _i_=0
                     )
            self.solv_b.invoke()
            
        elif self.get_entriesvalues():
            
            data_cont = self.master._convert_['setup']
            config = data_cont[-2:]+[0]
            
            sim_data, flag_done_ = extract_gromacs_data(data_cont[:-2],
                                                        _solvatedinfo_,
                                                        config[1:])
            if flag_done_:
                try:
                    flag_done_ = write_lammps_data( sim_data, 'data.gro2lam',
                                                   config )
                except:
                    pop_err_1('There are inconsistencies in your input files')
                    flag_done_ = False
                    
            if flag_done_:
                print_dec_g( 'Data file generated as "data.gro2lam"' )
                
                self._convertdata_ = sim_data
                self._convertdata_['config'] = config
                
                # Returning the values
                self.master._convertdata_ = self._convertdata_
                self.master.swapbody(2)
                
        else:
            pop_wrg_1('The setup needs some further improvements'
                        +'to be runed. Please check your inputs')

    def get_entriesvalues(self):
        ''' ---   app entry getter   ----
        mainly to obtain values beside check buttons'''
        e_values=[]
        _flag_ = True
        ent_rang  =  range(len(self.objt_c))
        
        for ent in ent_rang:#[1:]:
            e_values.append(self.objt_c[ent].get())
            if ent <= 4:
                _flag_ *= check_file(e_values[-1])
            
        self.master._convert_['setup'] = e_values
        return _flag_

    def createWidgets(self):
        self.create_conversion_gui()

    def config_solvation( self):
            
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
        _solvatedinfo_ = self.master._convert_['solvation']
        
        if _solvatedinfo_ ==  []:
            defaultanswer = ['opls_116','opls_117','OW','HW1, HW2','0.4238'
                            #,'Na','Cl'
                           ]
        else:
            defaultanswer = _solvatedinfo_
            
        self.solv_b.config(bg = 'gray40', width = 45) #cyan')
        self.master._aux_ = []
        
        pop = PromptPopUp(master = self.master,
                          title = title_txt,
                          briefing = instructions, 
                          entries_txt = askfor, 
                          entries_val = defaultanswer
                         )
        
        pop.wait_window()
        
        if self.master._aux_ <> [] and self.get_entriesvalues():
            _app_aux_ = self.master._aux_
            
            _flag_ = self.check_solvation_inputs( _app_aux_, True)
            if _flag_:
                self.master._convert_['solvation'] = _app_aux_
                print_dec_g('Solvation setup saved!')
                #self.solv_b.focus()
        self.solv_b.config(bg = 'lightgrey', width = 28)

    def check_solvation_inputs( self, _app_aux_, _vbs_ = False):
        ''' ================    Check inputs    ================= '''
        _flag_ = 1
        nb_Ox, nbHy, gro_Oxs, gro_Hys, pch= _app_aux_
        _gro_f, _, _, _nbn_f, _, _, _= self.master._convert_['setup']
        _flags = check_in_file( _nbn_f, nb_Ox, nbHy, pstn = 0)
        print ([nb_Ox, nbHy])
        
        if min(_flags)==0:
            print nb_Ox, nbHy
            
        list_aux = [Ox.strip(' ') for Ox in gro_Oxs.split(',')]
        list_aux += [Ox.strip(' ') for Ox in gro_Hys.split(',')]
        _flags += check_in_file( _gro_f, *list_aux, slce = '10:15')
        print (list_aux)
        
        if min(_flags[2:])==0:
            print list_aux
            
        try:
            x = float(pch)
            if -10<x<10:
                _flags += [1]
                partial_charges = 'Partial charges for H: {} and for O: {}'
                print partial_charges.format( x, x*-2)
            else:
                _flags += [0]
        except:
            _flags += [0]
        list_aux = [nb_Ox, nbHy] + list_aux
        
        # ================= Now check the flags =====================
        for v in range(len(_flags)):
            err_txt = ''
            if not _flags[v] and v <> (len(_flags)-1):
                filename = _nbn_f
                if v>1:
                    filename = _gro_f
                err_txt = 'Atom tag {} not found in {}'
                if '/' in filename:
                    filename = filename.split('/')[-1]
                err_txt = err_txt.format( list_aux[v], filename)
                _flag_*=0
            
            elif not _flags[v]:
                err_txt = 'Non valid partial charge {}'.format( pch)
                _flag_*=0
                
            if err_txt<>'':
                pop_err_1(err_txt+'\nSetup not saved')
        #============       Done!  ==================================
        return _flag_
    
