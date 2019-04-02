#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'
# checked ok 30/04/2018 

#------------------------------------------------------
#///    Packages and globals definitions are here   ///
#------------------------------------------------------

from Tkinter import Frame, Button, Label

from popup import PromptPopUp, PromptPopUp_wck

from tk_lib import bottom_hline_deco, format_dec, Drop_Down_List
from tk_lib import createmenubar, create_entry, get_entriesvalue

from custom_row import File_Entry, createfileentry

from lib.handling.lammps import write_lammps_input

from lib.misc.data import check_vars
from lib.misc.warn import print_dec_g, pop_wrg_1

#------------------------------------------------------
'''///////////////        Class       /////////////'''
#------------------------------------------------------
class Script_GUI(Frame):
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
        
        # Just as an extension
        self._convertdata_ = self.master._convertdata_
        self.img = self.master.img
        
        self._container_ = self.master._script_
        
        
    def createWidgets(self):
        'create the script gui'
        
        #    first header row
        row = Frame(self)
        TEXT1= "\nIn this section you can create input Lammps scripts "
        Label(row, text=TEXT1, anchor='w').pack(side='top', padx=2, pady=1)
        row.pack( side='top', fill='x', padx=5)
        bottom_hline_deco(self)
        
        bottom_hline_deco(self, self.create_main_section)
        
        self.build_finalbuttons()
        
        if self.master.test:
            self.after(2000, self.test_hook)
    
    def createWidgets_n_pack(self):
        self.createWidgets()
        self.pack()
    
    def create_main_section(self):
        '''Section for main input values    '''
        #=====================================================================
        '''  Create script section '''
        row2fill = Frame(self)
        row2fill_l = Frame(row2fill)
        self.s_entry_c = []
        _mainpage_ = self._container_['mainpage']
        _defvals_ = [ '0.1', '1000',
                     '1000', '300:299', '100',
                     '1000','10:1', '1000', '299:300', '100']
        _def_dataname_ = './data.gro2lam'
        
        if self._convertdata_ <> None:
            _def_dataname_ = self._convertdata_['filename']
        elif _mainpage_ <> []:
            _def_dataname_ = _mainpage_[0]
            _defvals_ = _mainpage_[1:] 
        
        
        
        self.s_entry_c.append( createfileentry( self,
                                               'Lammps data file to work',
                                               _def_dataname_,
                                               ['.data', 'data.*'],
                                               ['lammps data', 'lammps data'],
                                               (self._convertdata_ == None)
                                              )
                            )

        _entries_=  [ 'Timestep [fs]', '-','NVE steps  [#ts]','-',
                     'NVT steps  [#ts]','Temperature at start:end [K]',
                     'Temperature damping [fs]',
                     '-','NPT steps  [#ts]', 'Pressure at start:end  [atm]',
                     'Pressure damping [fs]',
                     'Temperature at start:end [K]', 'Temperature damping [fs]'
                    ]
        
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
        # ====================
        row2fill.pack(side="top", padx=1, pady=5)

    def build_finalbuttons(self):
        '''    Final Buttons    '''
        row = Frame(self)
        ########          ADVANCED OPTIONS #################
        
        if self._container_['advanced'] == []: # advanced _init_
            
            _pair_style_ = 'lj/cut/coul/cut'
            _comb_rl_ = 'No'
            lj_12_13_14_ = '0.0:0.0:0.0'
            co_12_13_14_ = '0.0:0.0:0.0'
            if self._convertdata_ <> None:
                _aux_here_ = self._convertdata_['defaults']
                buckorlj, comb_rule, _flg_, f14_LJ, f14_Co = _aux_here_
                if int( buckorlj) == 2:
                    _pair_style_ = 'buck/coul/long'
                    
                mix_val = {'1':'geometric', '2':'arithmetic', '3':'geometric'}
                _comb_rl_ = mix_val[comb_rule]
                if _flg_ == 'yes':
                    lj_12_13_14_ = '0.0:0.0:'+f14_LJ
                    co_12_13_14_ = '0.0:0.0:'+f14_Co
                    
            self._container_['advanced'] = [[],[]]
            self._container_['advanced'][0] = [ '10', 
                                               'array', 
                                               _pair_style_,
                                               '8.5','10','1.9', 
                                               'pppm',
                                               '1e-4',
                                               lj_12_13_14_, co_12_13_14_,
                                               '1','1',
                                               'aniso',
                                               _comb_rl_,
                                               
                                               '300',
                                               '1e-10',
                                               'NVE-NVT-NPT-NVT-R',
                                               '0.0001','0','0'
                                              ]
        
        self.fcb = Button( row, text = 'Advanced settings', compound='left',
                          image = self.img['gear'], bg='gray86',
                          height = 15, width = 145,
                          command = self.further_config_script
                         )
        self.fcb.pack(side='left', padx=10, pady=0)
        
        ######           RESTRAIN GROUP         ##############
        
        self.resb = Button( row, text = 'Restrain',
                          command = self.config_restrain
                          )
        self.resb.pack(side='left', padx=10, pady=0)
        
        self.b1 = Button( row, text='Create',# height=8,
                    command= self.write_script
                   )
        self.b1.pack(side='right', padx=2, pady=4)
        
        
        b2 = Button(row, text='Quit', command=self.quit)
        b2.pack(side='right', padx=20, pady=4)
        row.pack( side='top', fill='both', padx=5)
        
        
    def write_script(self):
    
        print 'Writing the lammps script'
        _mainpage_ = get_entriesvalue( self.s_entry_c)
        
        _flag_ = True # data ok flag
        
        _entries_ = [ 'float', 'int', 'int', 'float:', 'float', 'int',
                     'float:', 'float', 'float:', 'float']
        _flag_ *= self.check_datafile( bool)
        _flag_ *= min( check_vars( _mainpage_[1:], _entries_))
        
        if _flag_:
            self._container_['mainpage'] = _mainpage_
            _script_setup_  = [ _mainpage_, self._container_['advanced'][0]
                           , self._container_['restrain']]
            self.master._script_ = self._container_
            
            _flag_ = write_lammps_input( _script_setup_, self._convertdata_)
            
            if _flag_:
                print_dec_g( 'Lammps script done!')
                self.master.swapbody(3)
    
    def further_config_script( self ):
        ''' Section for advaced settings
        
        '''
        pop_wrg_1('Advanced settings!\nChanging these parameters could result'
                  +' in a different simulation than the base one')
        defvals = []
        title_txt = ' '*3+'+ Simulation Parameters'
        instructions = 'Input further simulation parameters'
        askfor = ['Thermo output every  [#ts]',
                  'Atom mapping',
                  'Pairwise interactions',
                  "L-J/Buck rcutoff  ["+u'\u00c5'+"]",
                  "Coulomb rcutoff  ["+u'\u00c5'+"]",
                  "Neighbor skin distance  ["+u'\u00c5'+"]",
                  'Long-range solver',
                  'Long-range relative error',
                  'L-J interaction 1-2:1-3:1-4',
                  'Coul interaction 1-2:1-3:1-4',
                  'Neighbor delay  [#ts]', 
                  'Neighbor update  [#ts]',
                  'Pressure control',
                  'Force mixing rule',
                  
                  'Velocity creation Temp  [K]',
                  
                  'Energy minimization tolerance',
                  'Simulation order',
                  '---',
                  'Shake tolerance',
                  'Shake bonds [b#]',
                  'Shake angles [a#]',
                  
                 ]
                        
        _pair_style_ = ['lj/cut/coul/long','lj/cut/coul/cut', 'lj/cut',
                        'lj/charmm/coul/long',
                        'buck/coul/long', 'buck', 'buck/coul/cut',
                        #'lj/cut/tip4p/cut', 'lj/cut/tip4p/long',
                        #'lj/gromacs', 'lj/gromacs/coul/gromacs',
                        #, 'none',
                        'zero']
        
        if self._convertdata_ <> None:
            buckorlj = int( self._convertdata_['defaults'][0])
            if buckorlj == 1:
                _pair_style_ = _pair_style_[ :3] + [_pair_style_[ -1]]
            else:
                _pair_style_ = _pair_style_[ 3:]
                
        _kspace_ = ['pppm', 'pppm/cg', 'ewald', 'pppm/disp', 'ewald/disp',
                  #'pppm/tip4p', 'pppm/disp/tip4p'
                   ]
        
        _comb_rule_ = ['No','geometric', 'arithmetic', 'sixthpower']
        
        #  ['advanced'][1] in case of drop down lists, to show the other cases 
        self._container_['advanced'][1] = [ '', ['array', 'hash'], 
                                            _pair_style_,
                                           '','','', _kspace_,
                                           '', '', '', '', '',
                                           ['aniso', 'iso', 'tri'],
                                            _comb_rule_, '','','',
                                           '', '', ''
                                          ]
        _defvals_ = []
        
        for _ad_ in range(len(self._container_['advanced'][0])):
            if self._container_['advanced'][1][_ad_] <> '':
                _def_ = self._container_['advanced'][0][_ad_]
                _dfli_ = self._container_['advanced'][1][_ad_]
                _defvals_.append([ _def_, _dfli_])
            else:
                _defvals_.append(self._container_['advanced'][0][_ad_])
                
        self.fcb.config(bg = 'gray70')#, width = 155) #cyan')
        self.master._aux_ = []
        pop = PromptPopUp(master = self.master,
                          title = title_txt,
                          briefing = instructions, 
                          entries_txt = askfor, 
                          entries_val = _defvals_ ,
                          width = 400,
                          height = 665
                         )
        
        pop.wait_window()
        
        _, bnty_len, anty_len = self.check_datafile()
        print bnty_len, anty_len
        if self.master._aux_ <> []:
            _advanced_ = self.master._aux_
            
            _entries_ = [ 'int', '', '', 'float', 'float', 'float', '',
                         'float', 
                         ['<float::<', 0.0, 1.0],['<float::<', 0.0, 1.0],
                         'int', 'int', '', '',
                         'float', 'float',[list, '-','NVE','NVT','NPT','R','M']
                         ,'float',
                         ['<int-x-int<:0', 1, bnty_len],
                         ['<int-x-int<:0', 1, anty_len]
                         ]
            _flag_ = min( check_vars( _advanced_, _entries_,
                                     'Advanced settings not saved!'))
            if _flag_:
                self._container_['advanced'][0] = _advanced_
                print_dec_g('Advanced settings saved')
        self.fcb.config(bg = 'gray86')#, width = 145)
    
    def config_restrain( self ):
        
        title_txt = ' '*28+'+ Restrain Goups'
        instructions = 'Select the group to restrain'
        
        #============ grouping  ================
        max_index, _, _ = self.check_datafile()
        
        if max_index:
            
            _defvals_ = self._container_['restrain']
            if _defvals_ == []:
                
                g_names = ['all_group']
                d_ids = ['{}:{}'.format( 1, max_index)]
                kxyz_c = ['1:xyz']
                rest_ens = ['1-2'] #restrained_ensembles
                ck_init = [0]
                second_c = None
                
                if self._convertdata_<> None:
                    _mol_niifi_ = self._convertdata_['atomsdata'][1]
                    for mt in range(len( _mol_niifi_)):
                        g_names.append(_mol_niifi_[mt][0])
                        d_ids.append('{}:{}'.format(*_mol_niifi_[mt][1:]))
                        kxyz_c += ['1:xyz']
                        rest_ens += ['1-2']
                        ck_init += [0]
                
            else: 
                g_names, d_ids, kxyz_c, rest_ens, ck_init = _defvals_[0]
                #print g_names,'\n', d_ids,'\n', kxyz_c,'\n', ck_init 
                if _defvals_[1]<> None:
                    second_c = _defvals_[1]
                else:
                    second_c = None
                    
            self.resb.config(bg = 'gray70')#, width = 45) #cyan')
            self.master._aux_ = []
            
            pop = PromptPopUp_wck(master = self.master,
                                  title = title_txt,
                                  briefing = instructions, 
                                  entries_txt = g_names, 
                                  entries_val = kxyz_c,
                                  width = 530,
                                  #height = 365,
                                  range_id = d_ids,
                                  res_ens = rest_ens,
                                  chck_init = ck_init,
                                  extra_but = second_c,
                                 )
            
            pop.wait_window()
            
            if self.master._aux_ <> []:
                sim_len = 0
                for x in  self._container_['advanced'][0][-4].split('-'):
                    if x.strip(' ') <> 'R':
                        sim_len +=1
                _res_flag_= [[],[]]
                _restrain_ = self.master._aux_[:]
                _, _d_ids, _kxyz_c, _runs_c, _res_flag_[0] = _restrain_[0]
                
                if _restrain_[1] <> None:
                    _, au2, au3, au4, au5 = _restrain_[1][:] 
                    _restrain_aux = _d_ids+ au2+ _kxyz_c+ au3+ _runs_c+ au4
                    _res_flag_[1] = au5
                else:
                    _restrain_aux = _d_ids+ _kxyz_c+ _runs_c
                _multi_ = len(_restrain_aux)/3
                _entries_ = ([['<int:int<', 1, max_index]]*_multi_
                               + ['float:xyz']*_multi_
                               + [['<int-x-int<:0', 1, sim_len]]*_multi_)
                            
                
                _aux_ = check_vars( _restrain_aux, _entries_,
                                         'Restrain groups not saved!')
                #print _aux_
                _flag_ = min( _aux_)
                if _flag_:
                    
                    if max(max(_res_flag_)):
                        self._container_['restrain'] = _restrain_
                        print_dec_g('Restrain data saved')
                    else:
                        print ('Creating 0 groups, Restraining 0 atoms')
            self.resb.config(bg = 'gray86')#, width = 45)

    def check_datafile(self, _bflag_=None):
        ''' function to get the max atom number 
            also is used in case of no gromacs direct data conversion
            to somehow make a check if that file is ok
        '''
        max_at_index, bond_types, angle_types = 0, 0, 0
        _flag_ = True
        if self._convertdata_<> None:
            _numbers_ = self._convertdata_['numbers']
            max_at_index = _numbers_['total'][0]
            _, bond_types, angle_types, _, _ = _numbers_['type']
        else: 
            _filename_ = self.s_entry_c[0].get()
            try:
                with open(_filename_, 'r')  as indata:
                    for k_line in indata:
                        if not k_line.startswith('#'):
                            line_c = k_line.split()
                            if 'atoms' in line_c:
                                max_at_index = line_c[0]
                            if 'types' in line_c:
                                if 'bond' in line_c:
                                    bond_types = line_c[0]
                                elif 'angle' in line_c:
                                    angle_types = line_c[0]
                                    break
            except IOError:
                pop_wrg_1('Data file not found!')
                print ('Try performing a conversion first!')
                _flag_ = False
                
        if _bflag_<>None:
            return _flag_
        return max_at_index, bond_types, angle_types
        
    def test_hook(self, event=None):
        self.b1.invoke()         
# vim:tw=80
