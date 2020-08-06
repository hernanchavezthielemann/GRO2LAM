#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'

from lib.misc.file import write_file, make_dir
from lib.misc.warn import print_dec_g, pop_wrg_1, pop_err_1, wrg_1

from sys import exit

                    

def extract_lammps_data(_data_file_,_ck_buttons_, _forcefield_):
    ''' already implemented in  topology analizer
            MIXER
    '''

def write_lammps_data( _topodata_, df_name, _config_):
    ''' Write a lammps data file'''
    print_dec_g ('Writing Lammps data file...')
    ####---------------  Unpacking data  ----------------####
    atomstyle, _, _autoload_, root_folder = _config_
    atsty = [ 'atomic', 'angle', 'full', 'charge', 'bond', 'molecular']
    style_str = '####-------  ATOM STYLE < {} >  --------####'
    _flag_ = False
    _content_=''
    if atomstyle in atsty:
        nam = ''.join([ chr( ord(l) - 32) for l in atomstyle])
        print_dec_g(style_str.format(nam))
        
        print '\n'+'='*14+'  Still in BETA here  '+'='*14+'\n'
        _content_, _flag_ = write_lammps_data_auto( _topodata_,
                                                    df_name,
                                                    _config_[:-1]
                                                  )
            
        errmsg = 'Error writing lammps data file'
        if _flag_:
            path_dir = make_dir( root_folder, 'g2l_dir')
            write_file( df_name, _content_, path_dir)
            print_dec_g ('Successful writing!!')
        elif _autoload_:
            pop_err_1(errmsg + '\nAutoload failed!')
        else:
            pop_err_1(errmsg)
    else: #if atomstyle == 'Angle':
        print '\n\nExit'
        exit(('Error 037!!  -  Atom style {} '
              +'not implemented yet').format(atomstyle))
    
    return _flag_, path_dir + df_name

def write_lammps_data_auto( _topodata_, data_name, _config_):
    ''' Write a lammps data file
        now with autoload,
        including impropers dihedrals (Aka Wop)
    '''
    
    _flag_ = False
    ####---------------  Unpacking data  ----------------####
    _numbers_ = _topodata_['numbers']
    n_atoms, n_bonds, n_angles, n_dihedrals, n_impropers = _numbers_['total']
    n_atomtypes, n_bondtypes, n_angletypes = _numbers_['type'][:3]
    n_dihedraltypes, n_impropertypes = _numbers_['type'][3:]
    [_box_, _box_apend] = _topodata_['box']
    _mol_, _mtype_g_, _atype_, _xyz_, _mtype_ = _topodata_['atomsdata'] 
    _x_, _y_, _z_ = _xyz_
    atomstyle, _sidemol_f_, _autoload_ = _config_ 
    
    if _sidemol_f_:
        sidemol = _topodata_['sidemol']
        
    #======================-------------------------==========================#
    #####------                    Force field                       ------####
    aux_forcefield_cont = write_lammps_potentials( _topodata_, atomstyle)
    aux_pot_txt, dicts, _flag_, rg_sgep, n_dihedraltypes = aux_forcefield_cont
        
    _asty_d_ ={ 'atomic':1, 'charge':1, 'bond':2, 'angle':3,
                'full':4, 'molecular':4}
    
    #########################################################
    '''--------------      1st  Header      --------------'''
    #=======================================================#
    
    ####---------------     TITLE        ----------------####
    _text_ = '#Lammps data file. Generated with GRO2LAM converter.\n\n'
    ####---------------     NUMBERS      ----------------####
    _aux_txt = [' {} atoms\n'.format( n_atoms)]
    _aux_txt.append(' {} bonds\n'.format( n_bonds))
    _aux_txt.append(' {} angles\n'.format( n_angles))
    _aux_txt.append(' {} dihedrals\n'.format( n_dihedrals) + 
                    ' {} impropers\n'.format( n_impropers))
    _text_ += ''.join( _aux_txt[:_asty_d_[atomstyle]])+'\n'
    
    ####----------------    TYPES       -----------------####
    _aux_txt = [ ' {} atom types\n'.format( n_atomtypes)]
    _aux_txt.append( ' {} bond types\n'.format( n_bondtypes))
    _aux_txt.append( ' {} angle types\n'.format( n_angletypes))
    _aux_txt.append( ' {} dihedral types\n'.format( n_dihedraltypes) +
                     ' {} improper types\n\n'.format( n_impropertypes))
    _text_ += ''.join( _aux_txt[ : _asty_d_[ atomstyle]]) + '\n'
    
    ####----------------    BOX     -----------------####
    
    _text_ +=(' {:.4f} {:.4f} xlo xhi\n {:.4f} {:.4f} ylo yhi\n'
              +' {:.4f} {:.4f} zlo zhi\n').format(*_box_)
    
    if _box_apend <> [0,0,0]:
        _text_ +=(' {:.4f} {:.4f} {:.4f} xy xz yz\n').format( *_box_apend)
    
    
    #######################-------------------------###########################
    '''---------           2nd  Atom kind Properties             -----------'''
    #======================-------------------------==========================#
    
    #####------                       MASSES                         ------####
    _text_ +='\n Masses\n\n'
    atom_info = _topodata_['atomtypes']
    minr = 1 - int( _topodata_[ 'defaults'][0]) # 0 lj and -1 buck
    already_warned = 0
    for i in range( n_atomtypes):
        _atom_mass_ = atom_info[i][ -5 + minr]
        _atom_type_ = atom_info[i][0]
        
        if not float( _atom_mass_) and _sidemol_f_: #meaning that is 0
            
            smols = sidemol['tag']
            #print 'here1', smols
            for ad in range( len(smols)):
                _smda_ = sidemol['data'][ad]['atoms']
                #print _smda_
                at_ = 0
                for at_ in range( len( _smda_)):
                    #print _smda_[at_], at_
                    if _smda_[at_][1] == _atom_type_ and len(_smda_[at_]) == 8:
                        _atom_mass_ = _smda_[at_][7]
                        print ( ('Mass for {} not found in atomtypes, taking' 
                                 + ' {} as substitute').format( _atom_type_, 
                                                                _atom_mass_)
                              )
                        break
                #if len(_smda_[at_]) == 8 and _atom_mass_ == _smda_[at_][7]:
                #    print at_
                #    break
        
        if not float( _atom_mass_):
            _atom_mass_ = '0.01008' # H_mass/100 as minimum seems reasonable
            if not already_warned:
                pop_wrg_1( ('0.0 mass not supported! using {} instead for {} '
                            + 'atom type').format( _atom_mass_, _atom_type_) )
                already_warned += 1
                
            else: # just to avoid the pain in the ass caused by these popups
                if already_warned == 1:
                    pop_wrg_1( ( 'All 0.0 mass are converted as: {}\nSee the '
                              +'terminal for more info.').format( _atom_mass_))
                    already_warned += 1
                    
                wrg_1(('0.0 mass not supported! using {} instead for {} '
                            + 'atom type').format( _atom_mass_, _atom_type_))
        
        _text_ +=' {} {} # {}\n'.format( i+1, _atom_mass_, _atom_type_)
        
    #======================-------------------------==========================#
    #####------                    Force field                       ------####
    _text_ += aux_pot_txt
    
    #########################################################
    '''-----------       3rd  Atom Coords     ------------'''
    #=======================================================#
    
    ####------                       ATOMS                           ------####
    known_atoms = _topodata_['atoms']
    
    
    _text_ +='\n Atoms #{}\n\n'.format( atomstyle)
    
    if atomstyle in ['charge','full']:
        atom_shape = ' {}'*3+' {:7.4f}'*4+' # {}\n'# idx mol atype charge x y z
    elif atomstyle in ['bond','angle','molecular']:
        atom_shape = ' {0} {1} {2} {4:7.4f} {5:7.4f} {6:7.4f} # {7}\n'
    elif atomstyle =='atomic':
        atom_shape = ' {0} {2} {4:7.4f} {5:7.4f} {6:7.4f} # {7}\n'
        
    #print( dicts[ 0])
    base_atoms_n = len( known_atoms)
    for i in range( base_atoms_n):
        aty = known_atoms[i][1]
        _text_ += atom_shape.format( i+1, _mol_[i],
                                    dicts[ 0][ aty],
                                    float(known_atoms[ i][6]), # charge?? WF
                                    _x_[i]*10, _y_[i]*10, _z_[i]*10,
                                    aty
                                   )
    sm_bonds = []
    sm_angles = []
    sm_dihedrals = []
    sm_impropers = []
    # asumption: all solvated structures are water??
    # 
    # =============== Solvated topogoly generation ================= #
    TRASH_CAN =  ''' next time better to reccon the structure, the repeating
                    unit, and then get the involved atoms, order, and then 
                    bonds, angles.... get this with the coordinates is another
                    option that probably is going to take longer rt
                 '''
    
    _residue_buffer_    =   '00'
    _mol_buffer_        =   'nk_type'
    side_at_v           =   []
    #print dicts[0]
    if _sidemol_f_ == 1:
        
        #charge = _topodata_['S_charge']
        #conv_dict = _topodata_['S_translation'] # key s_tag : val l_tag
        sm_cont         =   {}
        sm_charge       =   []
        sm_aty          =   []
        sm_data         =   {}
        ji_             =   0
        side_at_v       =   range( n_atoms)[ base_atoms_n:]
        multi_residue   =   0
        prev_mult_res   =   0
        sms_tags        =   [] + ['']*base_atoms_n
        _sm_i           =   -1 # side molecule index
        sm_m            =   1 # side mol multiplier
        for i in range( len ( sidemol['tag'])): 
            sm_at_num = len(sidemol['data'][ i]['atoms'])
            #print (sidemol['tag'][i],sidemol['num'][i],sm_at_num)
            sms_tags +=  [sidemol['tag'][i]]*sidemol['num'][i]*sm_at_num
            
        
        print( 'Sidemols: ' + str( sum(sidemol['num'][:] ) ) )
        
        
    #print( len(sms_tags), len(side_at_v), side_at_v[-1])
        #print n_atoms, base_atoms_n, len( _mtype_), side_at_v, _atype_
    for i in side_at_v:
        _res_n_ = _mol_[i]
        #aty = conv_dict[_atype_[i]] # _atype_ is the atag in TOP
        #print _atype_[i], aty
        # meaning new residue or new molecule
        clause1 = (_res_n_ <> _residue_buffer_)
        #if clause1:
            #print(clause1,_mol_[i], _residue_buffer_, multi_residue,prev_mult_res,sm_m)
        if multi_residue and clause1: # mol number
            _residue_buffer_ = _res_n_
            multi_residue -= 1
            if not multi_residue and not sm_m:
                _mol_buffer_ = 'nk_type'
                
            #print ji_, sm_aty[ ji_], _residue_buffer_
            #print _mol_[i], bool(multi_residue)
                
        elif clause1: # mol number
            
            _residue_buffer_ = _res_n_
            
            
            # New molecule kind test
            # entering here first time too
            #print(sm_m)
            if sms_tags[ i] <> _mol_buffer_:
                #print (i, sms_tags[ i], _mol_buffer_ )
                # I can change mol-buffer for sms_tags[i-1], but case = 0
                _mol_buffer_ = sms_tags[i]
                _sm_i += 1
                sm_m = sidemol['num'][_sm_i] - 1
                prev_mult_res = 0
            # enters here seccond time and first time of the seccod, third... repetition
            # side mol of the same kind
            elif sm_m:
                    sm_m -= 1
                    multi_residue = prev_mult_res
                    if sm_m == 0:
                        print ('here 0')
                        
            else:
                 exit('**** Unhandled case 001')
            
            ji_ = 0 # j index # atom index per side molecule
            _smol_tag_ = sidemol['tag'][ _sm_i]
            #sm_qty = sidemol['num'][ _sm_i]
            
            #print i+1, sms_tags[i], _mtype_[i], _smol_tag_
            #print '\n'+'here ', _sm_i
                
            # meaning also a new type of molecule ???
            if _smol_tag_ not in sm_cont.keys():
                
                new_smol_str = '** New side molecule : {} 1st atom : {} **'
                print( '\n' + new_smol_str.format( _smol_tag_, _atype_[i]))
                ###########     New side mol data     ########
                sm_data = sidemol['data'][  _sm_i]
                ##############################################
                first_atom_check = _atype_[i] == sm_data['atoms'][0][4]
                #print( sm_data['atoms'][0][4])
                # In the weird case of a missing residue tag in the GRO file
                # happens often
                if _mtype_[i] == '':
                    print ('\n')
                    pop_wrg_1('Missing residue tag in .gro file.\n'
                              + 'atom #'+ str( i+1)+ '. Asuming: ' +_smol_tag_)
                    
                    atom_x_ress = len( sm_data['atoms']) * sidemol['num'][ _sm_i]
                    #print atom_x_ress, len( sm_data['atoms']), sidemol['num'][ _sm_i]
                    _mol_buffer_ = _smol_tag_
                    
                    if first_atom_check:
                        for i_s in range( atom_x_ress):
                            if _mtype_[ i + i_s ] == '':
                                _mtype_[ i + i_s ] = _smol_tag_
                        
                    
                #""""""""""""""""""""""""""""""""""""""""""""#
                
                sm_charge   = []
                sm_aty      = []
                ##############################################
                
                aux_buffer = ''
                if not first_atom_check:
                    print('xx/0   Atoms order mismatch '
                         +'between residue definition and gro file!')
                    
                    exit('xx/0   Error /lammps.py 001!')
                    
                elif _mtype_[i] == sm_data['atoms'][0][3]:
                    for ath in sm_data['atoms']:
                        sm_charge.append(float( ath[6]))
                        sm_aty.append( ath[1])
                        
                        # multiple residues per side mol???
                        #lets see how many
                        if ath[2] <> aux_buffer:
                            #print ath[2]
                            if aux_buffer <> '':
                                multi_residue += 1
                            aux_buffer = ath[2]
                        
                    if multi_residue:
                        print ( '** It is a multi residual structure.\n** '
                               +'With: '+str( multi_residue +1)+' residues.')
                        #multi_residue -= 1
                        prev_mult_res = multi_residue
                    
                else:
                    print('xx/0   Residue: ' + _mtype_[i])
                    fst_line = (' ').join( sm_data['atoms'][0]) 
                    print('xx/0   First line: ' + fst_line)
                    print('xx/0   Molecules order mismatch '
                         +'between [ molecules ] definition and gro file!')
                    exit('xx/0   Error /lammps.py 002!')
                try:
                    print 'hop!',sm_data['atoms'][0][3]
                    sm_cont[ _smol_tag_] = {}
                    sm_cont[ _smol_tag_]['data']    = sm_data
                    sm_cont[ _smol_tag_]['charge']  = sm_charge
                    sm_cont[ _smol_tag_]['aty']     = sm_aty
                    
                except UnboundLocalError as Err_here:
                    print('Upa mala cosa!')
                    exit( Err_here[0])
                ######################################################
            else:
                #print('-> {} +1'.format( _smol_tag_))
                sm_data     = sm_cont[ _smol_tag_]['data']
                sm_charge   = sm_cont[ _smol_tag_]['charge']
                sm_aty      = sm_cont[ _smol_tag_]['aty']
            ''' ///////////-------------------------------------\\\\\\\\\\ '''
            '''<<<<<<<<<<<<    Side Molecule topology builder   >>>>>>>>>>>'''
            ''' \\\\\\\\\\\-------------------------------------////////// '''
            # This should be done in gromacs.py?? , in a near future
            # changes acording to the molecule kind topology
            #print sm_data
            dirtv_data = sm_data[ 'bonds']
            #print('here')
            #print dirtv_data
            #print( ji_, len(sm_aty))
            for xx in range( len( dirtv_data)):
                _row = dirtv_data[ xx]
                
                #print _row
                i1 =    int( _row[0])
                i2 =    int( _row[1])
                aty1 = sm_aty[ i1 - 1 ] 
                aty2 = sm_aty[ i2 - 1 ]
                
                sm_bonds.append([ aty1 + '-' + aty2, i + i1, i + i2])
                #print sm_bonds[-1]
                #if sm_bonds[-1][0]=='HC-HC':
                #    exit('opls_116-opls_116')
            dirtv_data = sm_data[ 'angles']
            for xx in range( len( dirtv_data)):
                _row = dirtv_data[ xx]
                i1 =    int( _row[0])
                i2 =    int( _row[1])
                i3 =    int( _row[2])
                aty1 = sm_aty[ i1 - 1 ] 
                aty2 = sm_aty[ i2 - 1 ] 
                aty3 = sm_aty[ i3 - 1 ]
                angle_str = '{}-{}-{}'.format( aty1, aty2, aty3)
                sm_angles.append([ angle_str, i + i1, i + i2, i + i3])
                
            dirtv_data = sm_data[ 'dihedrals']
            for xx in range( len( dirtv_data)):
                _row = dirtv_data[ xx]
                i1 = int( _row[0])
                i2 = int( _row[1])
                i3 = int( _row[2])
                i4 = int( _row[3])
                aty1 = sm_aty[ i1 - 1 ] 
                aty2 = sm_aty[ i2 - 1 ] 
                aty3 = sm_aty[ i3 - 1 ]
                aty4 = sm_aty[ i4 - 1 ]
                dih_str = '{}-{}-{}-{}'.format( aty1, aty2, aty3, aty4)
                sm_dihedrals.append([ dih_str, i + i1, i + i2, i + i3, i + i4])
                
            dirtv_data = sm_data[ 'impropers']
            for xx in range( len( dirtv_data)):
                _row = dirtv_data[ xx]
                i1 = int( _row[0])
                i2 = int( _row[1])
                i3 = int( _row[2])
                i4 = int( _row[3])
                aty1 = sm_aty[ i1 - 1 ] 
                aty2 = sm_aty[ i2 - 1 ] 
                aty3 = sm_aty[ i3 - 1 ]
                aty4 = sm_aty[ i4 - 1 ]
                imp_str = '{}-{}-{}-{}'.format( aty1, aty2, aty3, aty4)
                sm_impropers.append([ imp_str, i + i1, i + i2, i + i3, i + i4])
        
        
        #print ji_, sm_aty[ ji_]#, sm_aty
        #print sm_aty[ ji_]
        _text_ += atom_shape.format(i+1, _res_n_,
                                    dicts[0][ sm_aty[ ji_]],
                                    sm_charge[ ji_],
                                    _x_[i]*10, _y_[i]*10, _z_[i]*10,
                                    sm_aty[ ji_]
                                   )
        ji_+=1
                    
    ###########################################################################
    '''==========-----------   4th - Chemical topology   ---------=========='''
    #=========================================================================#
    print('\n> Checking chemical topology-coefficients')
    ''' Building auxiliar atom tag1_tag2 data dictionary -/- OPLS Case '''
    xf = 1
    aat_ddic = {}
    if len(atom_info[0]) - minr > 7:
        for i in range( n_atomtypes):
            aat_ddic[ atom_info[i][0]] = atom_info[i][1]
    
    ####################        ------BONDS------          ####################
    print('>> bonds')
    if _asty_d_[ atomstyle] >= 2:
        known_bonds = _topodata_['bonds']
        base_bonds_n = len (known_bonds)
        _text_ +='\n Bonds\n\n'
        bond_shape = ' {}'*4+'\n'
        
        a_g_d = {} #aux_goofy_dic
        for i in range(base_bonds_n):
            # print known_bonds[i][0], known_bonds[i][1]
            at1 = int(known_bonds[i][0])
            at2 = int(known_bonds[i][1])
            #print at1, at2
            to_print = '{} {}'.format(at1, at2)
            try:
                at1_tag = known_atoms[at1-1][xf]
                at2_tag = known_atoms[at2-1][xf]
                _bond_ty_ = dicts[1][ at1_tag + '-'+ at2_tag]
                
            except KeyError:
                # meaning that is trying with the big name
                try:
                    at1_tag = aat_ddic[ at1_tag]
                    at2_tag = aat_ddic[ at2_tag]
                    _bond_ty_ = dicts[1][ at1_tag + '-'+ at2_tag]
                    
                except KeyError:
                    print at1_tag + '-'+ at2_tag
                    print('Bond type not found for: ' + to_print)
                    print 'Exception {}-{}\n'.format( known_atoms[at1-1][4], 
                                               known_atoms[at2-1][4])
                    _bond_ty_ = 0
            
            _text_ += bond_shape.format( i+1, _bond_ty_, at1, at2)
                        
        if _sidemol_f_ == 1:
            #print dicts[1]
            # better way to do this is trough corrds ---------  <WFS>
            for i in range( n_bonds - base_bonds_n):
                # print sm_bonds[i]
                try:
                    _bond_ty_ = dicts[1][ sm_bonds[i][0]]
                except KeyError:
                    # OPLS ??
                    try:
                        at1_tag, at2_tag = sm_bonds[i][0].split('-')
                        #print(at1_tag, at2_tag)
                        at1_tag = aat_ddic[ at1_tag]
                        at2_tag = aat_ddic[ at2_tag]
                        _bond_ty_ = dicts[1][ at1_tag + '-'+ at2_tag]
                        
                    except KeyError:
                        
                        print('Bond type not found for:' + sm_bonds[i][0])
                        print('Or ' + at1_tag + '-'+ at2_tag)
                        exit( dicts[1] )
                        
                _text_ += bond_shape.format(i+1 + base_bonds_n,
                                            _bond_ty_,
                                            sm_bonds[i][1],
                                            sm_bonds[i][2])
    
    
    ####################        ------ANGLES------      #######################
    print('>> angles')
    if _asty_d_[ atomstyle] >= 3:
        known_angles = _topodata_['angles']
        base_angles_n = len(known_angles)
        _text_ +='\n Angles\n\n'
        angle_shape = ' {}'*5+'\n'
        for i in range(base_angles_n):
            
            at1 = int( known_angles[i][0])
            at2 = int( known_angles[i][1])
            at3 = int( known_angles[i][2])
            
            try:
                at1_tag = known_atoms[at1-1][xf]
                at2_tag = known_atoms[at2-1][xf]
                at3_tag = known_atoms[at3-1][xf]
                _angle_ty_ = dicts[2][at1_tag + '-'+ at2_tag+ '-'+ at3_tag]
            except KeyError:
                try:
                    at1_tag = aat_ddic[ at1_tag]
                    at2_tag = aat_ddic[ at2_tag]
                    at3_tag = aat_ddic[ at3_tag]
                    _angle_ty_ = dicts[2][at1_tag + '-'+ at2_tag+ '-'+ at3_tag]
                except KeyError as Er_here:
                    print 'Error ----- '+Er_here.args[0]
                    
            #print angle_t, _angle_ty_
            _text_ += angle_shape.format( i+1, _angle_ty_, at1, at2, at3)
            
        if _sidemol_f_ == 1:
            
            for i in range( n_angles - base_angles_n):
                
                try:
                    _angle_ty_ = dicts[2][ sm_angles[i][0]]
                except KeyError:
                    # OPLS ??
                    at1_tag, at2_tag, at3_tag = sm_angles[i][0].split('-')
                    at1_tag = aat_ddic[ at1_tag]
                    at2_tag = aat_ddic[ at2_tag]
                    at3_tag = aat_ddic[ at3_tag]
                    _angle_ty_ = dicts[2][at1_tag + '-'+ at2_tag+ '-'+ at3_tag]
                    
                _text_ += angle_shape.format( i+1 + base_angles_n,
                                             _angle_ty_,
                                             sm_angles[i][1],
                                             sm_angles[i][2],
                                             sm_angles[i][3]
                                            )
    
    
    ####################        ------DIHEDRAL------       ####################
    print('>> dihedrals')
    if _asty_d_[ atomstyle] >= 4:
        known_dihedrals = _topodata_['dihedrals']
        base_dihedrals_n = len(known_dihedrals)
        if base_dihedrals_n or ( n_dihedrals > base_dihedrals_n):
            _text_ +='\n Dihedrals\n\n'
        dihedral_shape = ' {}'*6+'\n'
        for i in range( base_dihedrals_n):
            err_str = ''
            _dihe_ty_ = '0'
            at1 = int( known_dihedrals[i][0])
            at2 = int( known_dihedrals[i][1])
            at3 = int( known_dihedrals[i][2])
            at4 = int( known_dihedrals[i][3])
            
            try:
                at1_tag = known_atoms[at1-1][xf]
                at2_tag = known_atoms[at2-1][xf]
                at3_tag = known_atoms[at3-1][xf]
                at4_tag = known_atoms[at4-1][xf]
                _dihe_ty_ = dicts[3][at1_tag + '-'+ at2_tag+ '-'+
                                     at3_tag + '-'+ at4_tag]
            except KeyError:
                try:
                    at1_tag = aat_ddic[ at1_tag]
                    at2_tag = aat_ddic[ at2_tag]
                    at3_tag = aat_ddic[ at3_tag]
                    at4_tag = aat_ddic[ at4_tag]
                    _dihe_ty_ = dicts[3][at1_tag + '-'+ at2_tag+ '-'+
                                     at3_tag + '-'+ at4_tag]
                except KeyError:
                    options = ['X-'+at2_tag+'-'+at3_tag +'-'+at4_tag,
                              at1_tag+'-'+at2_tag+'-'+at3_tag +'-X',
                              'X-' + at2_tag + '-' + at3_tag + '-X',
                              ]
                    for _opt_ in options:
                        try:
                            _dihe_ty_ = dicts[3][ _opt_]
                            break
                        except KeyError:
                            if _opt_ == options[-1]:
                                try:
                                    _dihe_ty_ = dicts[3][ 'X-' + at2_tag[0] +
                                                         'X-'+ at3_tag[0] +
                                                         'X-X']
                                except KeyError as Er_here:
                                    err_str = Er_here.args[0]
            if _dihe_ty_ == '0' and err_str <> '':
                print 'Atoms {}-{}-{}-{} : '.format( at1, at2, at3, at4),
                print (at1_tag +'-'+ at2_tag+'-'+ at3_tag+'-'+ at4_tag)
                print ( 'Error dihedral ----- '+ err_str +' not found!')
            
            _text_+= dihedral_shape.format( i+1, _dihe_ty_, at1, at2, at3, at4)
            
        if _sidemol_f_ == 1:
            for i in range( n_dihedrals - base_dihedrals_n):
                err_str = ''
                _dihe_ty_ = '0'
                
                try:
                    _dihe_ty_ = dicts[3][ sm_dihedrals[i][0]]
                    
                except KeyError:
                    # OPLS ??
                    try:
                        aux_here = sm_dihedrals[i][0].split('-')
                        aux_here = [ aat_ddic[ at_tag] for at_tag in aux_here]
                        _dihe_ty_ = dicts[3][ '-'.join( aux_here)]
                        
                    except KeyError:
                        options = [ 'X-{}-{}-X'.format( *aux_here[1:-1]),
                                   'X-{}-{}-X'.format( *aux_here[2:0:-1]),
                                    'X-{}-{}-{}'.format( *aux_here[1:]),
                                    '{}-{}-{}-X'.format( *aux_here[:-1]),
                              ]
                        for _opt_ in options:
                            try:
                                _dihe_ty_ = dicts[3][ _opt_]
                                break
                            except KeyError as Er_here:
                                err_str += ' // ' + Er_here.args[0]
                        
                if _dihe_ty_ == '0' and err_str <> '':
                    print( 'Atoms {}-{}-{}-{} '.format( *aux_here) + ' '
                           + err_str + '  //  ' + 
                           wrg_1( 'Dihedral > '+ sm_dihedrals[i][0] +
                                 ' < not found!')
                         )
                    
                _text_ += dihedral_shape.format( i+1 + base_dihedrals_n,
                                                 _dihe_ty_,
                                                 sm_dihedrals[i][1],
                                                 sm_dihedrals[i][2],
                                                 sm_dihedrals[i][3],
                                                 sm_dihedrals[i][4]
                                               )
    
    ###################        ------IMPROPERS------       ####################
    print('>> impropers')
    # TODO SECTION
    if _asty_d_[ atomstyle] >= 4:
        known_impropers = _topodata_['impropers']
        base_impropers_n = len( known_impropers)
        if base_impropers_n or ( n_impropers > base_impropers_n):
            _text_ +='\n Impropers\n\n'
        improper_shape = ' {}'*6+'\n'
        for i in range( base_impropers_n):
            err_str = ''
            _impr_ty_ = '0'
            at1 = int( known_impropers[i][0])
            at2 = int( known_impropers[i][1])
            at3 = int( known_impropers[i][2])
            at4 = int( known_impropers[i][3])
            
            try:
                at1_tag = known_atoms[ at1-1][xf]
                at2_tag = known_atoms[ at2-1][xf]
                at3_tag = known_atoms[ at3-1][xf]
                at4_tag = known_atoms[ at4-1][xf]
                _impr_ty_ = dicts[4][at1_tag + '-'+ at2_tag+ '-'+
                                     at3_tag + '-'+ at4_tag]
            except KeyError:
                try:
                    at1_tag = aat_ddic[ at1_tag]
                    at2_tag = aat_ddic[ at2_tag]
                    at3_tag = aat_ddic[ at3_tag]
                    at4_tag = aat_ddic[ at4_tag]
                    _impr_ty_ = dicts[4][ at1_tag + '-'+ at2_tag+ '-'+
                                          at3_tag + '-'+ at4_tag]
                except KeyError:
                    options = ['X-' + at2_tag + '-' + at3_tag + '-' + at4_tag,
                               'X-X-' + at3_tag + '-' + at4_tag,
                               at1_tag + '-X-X-' + at4_tag,
                              ]
                    
                    for _opt_ in options:
                        try:
                            _impr_ty_ = dicts[4][ _opt_]
                            break
                        except KeyError as Er_here:
                            if _opt_ == options[-1]:
                                err_str = Er_here.args[0]

            if _impr_ty_ == '0' and err_str <> '':
                print 'Atoms {}-{}-{}-{} : '.format( at1, at2, at3, at4),
                print (at1_tag +'-'+ at2_tag+'-'+ at3_tag+'-'+ at4_tag)
                print ( 'Error improper dihedral ---- '+ err_str +' not found!')
                
            
            _text_+= improper_shape.format( i+1, _impr_ty_, at1, at2, at3, at4)
            
        if _sidemol_f_ == 1:
            for i in range( n_impropers - base_impropers_n):
                _impr_ty_ = '0'
                err_str = ''
                try:
                    _impr_ty_ = dicts[4][ sm_impropers[i][0]]
                    
                except KeyError as Er_here:
                    
                    err_str += Er_here.args[0]
                    
                    aux_here = sm_impropers[i][0].split('-')
                    options = [aux_here[0] + '-X-X-' + aux_here[3],
                               aux_here[3] + '-X-X-' + aux_here[0],
                              ]
                    
                    for _opt_ in options:
                        try:
                            _impr_ty_ = dicts[4][ _opt_]
                        
                        except KeyError as Er_here:
                            err_str += Er_here.args[0]
                
                if _impr_ty_ == '0' and err_str <> '':
                    print( wrg_1('Improper dihedral > ' + err_str
                                             + ' < not found!') 
                             )
                
                _text_ += improper_shape.format( i+1 + base_impropers_n,
                                                 _impr_ty_,
                                                 sm_impropers[i][1],
                                                 sm_impropers[i][2],
                                                 sm_impropers[i][3],
                                                 sm_impropers[i][4]
                                               )
    return _text_, _flag_
    
def side_mol_topology_builder( data_in):
    ''' ///////////-------------------------------------\\\\\\\\\\ '''
    '''<<<<<<<<<<<<    Side Molecule topology builder   >>>>>>>>>>>'''
    ''' \\\\\\\\\\\-------------------------------------////////// '''
    # This should be done in gromacs.py?? , in a near future
    # changes acording to the molecule kind topology
    tag_str = [ 'bonds', 'angles', 'dihedrals', 'impropers']
    print conv_dict
    for _st_ in tag_str:# range( len( tag_str)):
        #print _st_, i
        
        for xx in range( len( sm_data[ _st_])):
            index_c = sm_data[ _st_][ xx]
            #print index_c
            i1 = int(index_c[0])
            i2 = int(index_c[1])
            print _atype_[ i + i1-1],  _atype_[ i + i2-1]
            
            aty1 = conv_dict[ _atype_[ i + i1-1]]
            aty2 = conv_dict[ _atype_[ i + i2-1]]
            print aty1, aty2
            
            if _st_ == 'bonds':
                sm_bonds.append([ aty1+'-'+aty2, i1, i2])
                
            elif _st_ == 'angles':
                i3 = int(index_c[2])
                aty3 = conv_dict[ _atype_[ i + i3-1]]
                
                angle_str = '{}-{}-{}'.format( aty1, aty2, aty3)
                sm_angles.append( [ angle_str, i1, i2, i3])
                
            elif _st_ == 'dihedrals':
                i3 = int( index_c[ 2])
                i4 = int( index_c[ 3])
                aty3 = conv_dict[ _atype_[ i + i3-1]]
                aty4 = conv_dict[ _atype_[ i + i4-1]]
                
                dihe_str = '{}-{}-{}-{}'.format( aty1, aty2, aty3,
                                                aty4)
                sm_dihedrals.append( [ dihe_str, i1, i2, i3, i4])
                
            elif _st_ == 'impropers':
                i3 = int( index_c[ 2])
                i4 = int( index_c[ 3])
                aty3 = conv_dict[ _atype_[ i + i3-1]]
                aty4 = conv_dict[ _atype_[ i + i4-1]]
                
                impr_str = '{}-{}-{}-{}'.format( aty1, aty2, aty3,
                                                aty4)
                sm_impropers.append( [ impr_str, i1, i2, i3, i4])
                
            else:
                print aty, _mol_[i], _residue_buffer_, len( _atype_)
                exit('')
        
    
def write_lammps_potentials( _topodata_, atomstyle = 'full'):
    ''' writes the potential part in the data file'''
    _flag_ = True
    atom_info = _topodata_['atomtypes'] # index 1: mass ; index 4 -5 : eps-sig
    # unpacking
    _numbers_ = _topodata_['numbers']
    n_atomtypes, n_bondtypes, n_angletypes = _numbers_['type'][:3]
    n_dihedraltypes, n_impropertypes = _numbers_['type'][3:]
    #exit(_numbers_)
    #n_bondstypes = len(data_container['bondtypes'])
    
    buckorlj = int( _topodata_[ 'defaults'][0]) # 1 -2 lj/buc
    comb_rule = int( _topodata_[ 'defaults'][1]) # 1-2-3
    
    sigma = []
    epsilon = []
    buck3 = []
    atom_type_d = {}
    # find ptype index, since len can change and the user could put some garbage
    # in between the previous commented line. Eg:
    # ; name  mass charge ptype  V(sigma)  (epsilon) if the comb-rule "2"
    #ptypei = atom_info[0].index('A')
    # Second options second the combination rule, and count from behind:
    minr = 1 - buckorlj # 1 lj and 2 buc --> minr = 0 lj and -1 buck
    
    # Any 0 check, to check the feasibility of the conversion to sig and eps
    regular_se = True
    pairtypename = ''
    if buckorlj == 1 and comb_rule == 1:
        for x in range( n_atomtypes):
            _A_ = float( atom_info[x][ -1 + minr])
            _B_ = float( atom_info[x][ -2 + minr])
            if _A_ <> 0 and _B_ == 0 or _A_ == 0 and _B_ <> 0:
                regular_se = False
                pairtypename = 'hybrid/overlay'
                wr_str = ('Using pair style lennard/mdf!!\nThis style can '
                          + 'only be used if LAMMPS was built with the '
                          + 'USER-MISC package')
                pop_wrg_1( wr_str.format( pairtypename) ) ## ?? TOChecK
                break
    
    for x in range( n_atomtypes):
        #print atom_info[x]
        atom_type_d[atom_info[x][0]] = x+1
        
        _A_ = float( atom_info[x][ -1 + minr])
        _B_ = float( atom_info[x][ -2 + minr])
        
        
        if comb_rule == 1 and regular_se:
            _eps_ = 0
            _sig_ = 0
            if _A_:
                _eps_ = ( _B_**2)/( 4*_A_)
                _sig_ = ( _A_/_B_)**( 1/6.0)
                
        elif comb_rule == 1:
            _eps_ = _A_*(10**12)
            _sig_ = _B_*(10**6)/ 4.186 /10# the last /10 just to make it easier
        else:
            _eps_ = _A_
            _sig_ = _B_
            
            
        epsilon.append(_eps_ / 4.186)
        
        if buckorlj == 2:#------------------------------------------  <WFS>
            _C_ = float( atom_info[x][ -1])
            buck3.append(' {:.5f}'.format( _C_*(10**6)/ 4.186 ))
            sigma.append( 10 / _sig_)
        else:
            buck3.append('')
            sigma.append( _sig_* 10)
            
    ####----------- DEFINING LJ INTERACTIONS     ----------####
    #-------------------------------------------------------  <WFS> 
    #                        make function- buck
    '''potential'''
    txt_p_p ='\n Pair Coeffs #{}\n\n'.format( pairtypename)
    for i in range( n_atomtypes):
        txt_p_p +=' {} {:.5f} {:.5f}{}\n'.format( i+1, epsilon[i], sigma[i], buck3[i])
    
    
    ########    -----------     BOND        ----------     ########
    BondDataBase = ['harmonic','gromos','morse','cubic','connection','harmonic',
                    'fene','tabulated','tabulated','restraint']
    Bonds_structures = {'harmonic': {},
                       'morse': {}}
    
    bty =  _topodata_['bondtypes']
    bond_kind_names = _topodata_['bond_kinds'] # set with numbers as string
    
    bondtypename = []
    if len( bond_kind_names) > 1:
        bondtypename.append( 'hybrid')
        _bdb_ = BondDataBase[:]
        for b in range( len( _bdb_)):
            _bdb_[ b] = ' '+ _bdb_[ b]
    else:
        _bdb_  = ['',]*len( BondDataBase)
        
    for bo in bond_kind_names:
        bondtypename.append( BondDataBase[ int( bo)- 1])
    
    txt_p_b = ''
    if bondtypename <> []:
        txt_p_b ='\n Bond Coeffs #{}\n\n'.format( bondtypename[0]) # bond_style hybrid
    
    bondtypes_d = {}
    
    for i in range( n_bondtypes):
        extra_end_str = '\n'
        bondtypes_d[ bty[i][0] + '-' + bty[i][1]] = i+1
        bondtypes_d[ bty[i][1] + '-' + bty[i][0]] = i+1
        
        _bi_ = int(bty[i][2])
        if _bi_ == 1:
            info_cont = [ i+1, _bdb_[ _bi_ - 1],
                          float( bty[i][4])/ 100/ 4.186/2,
                          float( bty[i][3])*10 ]
            
        elif _bi_ == 2: # bond_style  G96 in gromacs
            print bty[i]
            info_cont = [ i+1, _bdb_[ _bi_ - 1],
                          float( bty[i][4])/ 100/ 4.186/4,
                          float( bty[i][3])*10 ]
            
        elif _bi_ == 3:
            extra_end_str = ' {:.4f}\n'
            info_cont = [ i+1, _bdb_[ _bi_ - 1],
                         float( bty[i][4])/ 100/ 4.186/2,
                         float( bty[i][5])/10,
                         float( bty[i][3])*10 ]
        else:
            wr_str = 'Bond type {} not implemented yet!'
            pop_wrg_1( wr_str.format( bondtypename) )
            info_cont = [ i+1, _bdb_[ _bi_ - 1], 0, 0 ]
            _flag_ = False
        txt_p_b += ( ' {}{} {:.4f} {:.4f}' + extra_end_str).format( *info_cont)
    
    
    ########    -----------     ANGLE      ----------     ########
    AngleDataBase = ['harmonic','cosine/squared','cross bond-bond',
                     'cross bond-angle',
                     'charmm','quartic angle','','tabulated'] 
    
    aty = _topodata_['angletypes']
    angl_kind_names = _topodata_['angl_kinds'] # set with numbers as string
    
    angletypename = []
    if len( angl_kind_names) > 1:
        angletypename.append( 'hybrid')
        _adb_ = AngleDataBase[:]
        for a in range( len( _adb_)):
            _adb_[ a] = ' '+ _adb_[ a]
    else:
        _adb_  = ['',]*len( AngleDataBase)
        
    for an in angl_kind_names:
        angletypename.append( AngleDataBase[ int( an)- 1])
    
    txt_p_a = ''
    if angletypename <> []:
        txt_p_a ='\n Angle Coeffs #{}\n\n'.format( angletypename[0]) 
    
    angletypes_d = {}
    i=0
    info_cont = []
    for i in range( n_angletypes):
        extra_end_str = '\n'
        angletypes_d[aty[i][0]+'-'+aty[i][1]+'-'+aty[i][2]]= i+1
        angletypes_d[aty[i][2]+'-'+aty[i][1]+'-'+aty[i][0]]= i+1
        _ai_ = int(aty[i][3])
            
        if _ai_ == 1:
            info_cont = [ i+1, _adb_[ _ai_ - 1],
                         float(aty[i][5])/ 4.186/2,
                         float(aty[i][4]) ]
            
        elif _ai_ == 2:# angle_style G96 in gromacs
            info_cont = [ i+1, _adb_[ _ai_ - 1],
                         float(aty[i][5])/ 4.186/2,
                         float(aty[i][4]) ]
            
        elif _ai_ == 5:## Urey-Bradley
            extra_end_str = ' {:.5f} {:.5f}\n'
            info_cont = [ i+1, _adb_[ _ai_ - 1],
                         float(aty[i][5])/ 4.186/2, #  k_theta (kJ mol-1rad-2)
                         float(aty[i][4]),          #  theta_0 (deg)
                         float(aty[i][7])/ 4.186/2/100, #  kUB (kJ mol-1 nm-2)
                         float(aty[i][6])*10 ]      #  r13 (nm)
        else:
            wr_str = 'Angle type {} not implemented yet!'
            pop_wrg_1( wr_str.format( angletypename) )
            info_cont = [ i+1, _adb_[ _ai_ - 1], 0, 0 ]
            _flag_ = False
        txt_p_a += ( ' {}{} {:.5f} {:.5f}' + extra_end_str).format( *info_cont)
    
    # >===========================================================< #
    ########    -----------     DIHEDRAL      ----------     ########
    # TODO: improve this "DataBase" thing - maybe with a dictionary?
    # opls=RyckaertBellemans // fourier=Proper dihedral (multiple)
    DihedralDataBase = [ 'charmm', 'improper_1', 'opls', 'improper_2', 
    # Not implemented ones:
                          'ex1','periodic','tabulated', 'ex2', 'fourier'] 
    # asuming that impropers can not be here, purged previously in gromacs.py
    dty = _topodata_['dihedraltypes']
    dihe_kind_names = _topodata_['dihe_kinds'] # set with numbers as string
    type9_flag = False
    dihedtypename = []
    if len( dihe_kind_names) > 1:
        dihedtypename.append( 'hybrid')
        _ddb_ = DihedralDataBase[:]
        for d in range( len(_ddb_)):
            _ddb_[d] = ' '+ _ddb_[d]
    else:
        _ddb_  = ['',]*len( DihedralDataBase)
    for di in dihe_kind_names:
        dihedtypename.append( DihedralDataBase[ int( di)- 1])
        if int( di) == 9:
            type9_flag = True
    
    txt_p_d = ''
    if dihedtypename <> []:
        txt_p_d ='\n Dihedral Coeffs #{}\n\n'.format( dihedtypename[0])
    
    rb_warning = (' Ryckaert-Bellemans angle style conversion in Fourier form' +
                  ' can only be used if LAMMPS was built with the MOLECULE' +
                  ' package!!! quite a base, so this is not printed')
    ###== Type 9 > Proper dihedral (multiple) // <
    if type9_flag:
        # Warn and re-Pack the potentials - multiplexing potentials ;)
        pop_wrg_1(' Type 9 Proper dihedral (multiple) angle style conversion'
                  + ' in Fourier form can only be used if LAMMPS was built'
                  + ' with the USER-MISC package!!')
        print( '='*20 + '  MuXInG  ' + '='*20 )
        aux_type9 = []
        aux_type9_types = []
        new_dty = []
        print('Dihedrals before muxing: {}'.format( n_dihedraltypes))
        for i in range( n_dihedraltypes):
            if int( dty[i][4]) == 9:
                aux_tag = '{}-{}-{}-{}'.format( *dty[i][:4])
                if aux_tag not in aux_type9_types:
                    aux_type9_types.append( aux_tag)
                    aux_type9.append( dty[i][:5] + [[dty[i][5:], ]]) 
                else:
                    j = aux_type9_types.index( aux_tag)
                    aux_type9[ j][5].append( dty[i][5:])
                
            else:
                new_dty.append( dty[i])
                
        dty = new_dty + aux_type9
        n_dihedraltypes = len( dty) #########Check cases when this is not valid?
        
        print('Dihedrals after muxing: {}'.format( n_dihedraltypes))
    ###== end Type 9
    
    dihedraltypes_d = {} # types dictionary
    i=0
    info_cont = ''
    for i in range( n_dihedraltypes):
        # tag creation
        _type_forward_ = dty[i][0]+'-'+dty[i][1]+'-'+dty[i][2]+'-'+dty[i][3]
        # FIFO type number asigment
        dihedraltypes_d[ _type_forward_ ] = i+1
        ##  need also in backward direction in the lysozyme case
        _type_backward_ = dty[i][3]+'-'+dty[i][2]+'-'+dty[i][1]+'-'+dty[i][0]
        dihedraltypes_d[ _type_backward_] = i+1
        
        _di_ = int(dty[i][4])
        # Charmm / Amber -> coeff_4 = 0.0
        if _di_ == 1:
            info_cont = ( i+1, _ddb_[ _di_ - 1],
                         '{:.5f}'.format( float( dty[i][6])/4.186), # k_phi(kJ mol-1)
                         int(float(dty[i][7])),                     # multiplicity
                         '{}'.format( int( float(dty[i][5]))),        # phi_s(deg);
                         '0.0'
                        )
        # Ryckaert-Bellemans
        elif _di_ == 3:
            C0 = float(dty[i][5])    # (kJ mol-1)
            C1 = float(dty[i][6])    # (kJ mol-1)
            C2 = float(dty[i][7])    # (kJ mol-1)
            C3 = float(dty[i][8])    # (kJ mol-1)
            C4 = float(dty[i][9])    # (kJ mol-1)
            C5 = float(dty[i][10])   # (kJ mol-1)
            
            info_cont = ( i+1, _ddb_[ _di_ - 1],
                         '{:.5f}'.format( ( -2*C1 - (3/2)*C3) /4.186),#K1
                         '{:.5f}'.format( ( -C2 - C4) /4.186),#K2
                         '{:.5f}'.format( ( -(1/2)*C3) /4.186),#K3
                         '{:.5f}'.format( ( -(1/4)*C4) /4.186) #K4
                        )
        # Amber03
        elif _di_ == 9:
            # Here 
            _m_ = len( dty[i][5])
            _K1_ = '{:.5f}'.format( float( dty[i][5][0][1]) /4.186) # k_phi(kJ mol-1)
            _n1_ = dty[i][5][0][2]                                  # multiplicity
            _d1_ = '{}'.format( int( float( dty[i][5][0][0])))        # phi_s(deg);
            
            multispace = '' + _d1_
            for _ei in range( _m_)[1:]:
                _K_ei_ = '{:.5f}'.format( float( dty[i][5][ _ei][1]) /4.186)
                _n_ei_ = dty[i][5][ _ei][2]
                _d_ei_ = '{}'.format( int( float( dty[i][5][ _ei][0] )))
                
                multispace += ' {} {} {}'.format( _K_ei_, _n_ei_, _d_ei_)
                
            info_cont = ( i+1, _ddb_[ _di_ - 1],
                         _m_, _K1_, _n1_, multispace,
                        )
            
        else:
            wr_str = 'Dihedral type {} not implemented yet!'
            pop_wrg_1( wr_str.format( DihedralDataBase[ _di_- 1]))
            info_cont = ( i+1, _ddb_[ _di_ - 1],0,0,0,0)
            _flag_ = False
            break
            
        txt_p_d += ' {}{} {} {} {} {}\n'.format( *info_cont)
        
    ########    -----------     IMPROPER      ----------     ########
    # TODO: correct also here this 
    # improper comes with type number "2", 
    ImproperDataBase = ['not_here', 'harmonic', 'cossq', 'cvff','class2'] 
    ity = _topodata_['impropertypes']
    impr_kind_names = _topodata_['impr_kinds'] # set with numbers as string
    
    imprtypename = []
    
    if len( impr_kind_names) > 1:
        imprtypename.append( 'hybrid')
        _idb_ = ImproperDataBase[:]
        for i in range( len( _idb_)):
            _idb_[i] = ' '+ _idb_[i]
    else:
        _idb_  = ['',]*len( ImproperDataBase)
    for im in impr_kind_names:
        imprtypename.append( ImproperDataBase[ int( im)- 1])
    
    txt_p_i = ''
    if imprtypename <> []:
        txt_p_i ='\n Improper Coeffs #{}\n\n'.format( imprtypename[0])
            
    impropertypes_d = {} # types dictionary
    i=0
    info_cont = ''
    cosine_dic = {180:-1, -180:-1, 0:1}
    
    for i in range( n_impropertypes):
        # tag creation
        _type_forward_ = ity[i][0]+'-'+ity[i][1]+'-'+ity[i][2]+'-'+ity[i][3]
        # FIFO type number asigment IJKL
        impropertypes_d[ _type_forward_ ] = i+1
        ##  need also in other direction LJKI in silk case
        _type_backward_ = ity[i][3]+'-'+ity[i][2]+'-'+ity[i][1]+'-'+ity[i][0]
        impropertypes_d[ _type_backward_] = i+1
        
        _ii_ = int( ity[i][4])
        if _ii_ == 2:
            info_cont = ( i+1, _idb_[ _ii_ - 1],
                         float(ity[i][6]) /4.186/2,
                         # what would be better here? warn or int(float ?
                         '{:.2f}'.format( float( ity[i][5]) ), 
                         '','',
                        )
        
        elif _ii_ == 4:
            try:
                cosine_phi_s = cosine_dic[ float( ity[i][5])]
            except KeyError:
                pop_wrg_1( 'Phi_s in the improper periodic should be 0 or 180,'
                          + 'instead {} was received,'.format(ity[i][5])
                          + ' using default value -1 for cos(phi_s)!')
                cosine_phi_s = -1
                
            info_cont = ( i+1, _idb_[ _ii_ - 1],
                         float(ity[i][6])/4.186,
                         cosine_phi_s,
                         ' ', int(ity[i][7]),
                        )
        
        else:
            wr_str = 'Improper type {} not implemented yet!'
            pop_wrg_1( wr_str.format( ImproperDataBase[ _ii_- 1]))
            info_cont = ( i+1, _idb_[ _ii_ - 1],0,0,0,0)
            _flag_ = False
            break
        txt_p_i += ' {}{} {:.5f} {}{}{}\n'.format( *info_cont)
        
    # === for cycle end
    
    ########    ---------    Final selector section   ----------     ########
    #bad_sty = [ bondtypename, angletypename, dihedtypename]
    if atomstyle in ['full', 'molecular']:
        dicts = [ atom_type_d, bondtypes_d, angletypes_d,
                  dihedraltypes_d, impropertypes_d]
        txt_p_ = txt_p_p + txt_p_b + txt_p_a + txt_p_d + txt_p_i
    elif atomstyle == 'angle':
        dicts = [ atom_type_d, bondtypes_d, angletypes_d]
        txt_p_ = txt_p_p + txt_p_b + txt_p_a
    elif atomstyle == 'bond':
        dicts = [ atom_type_d, bondtypes_d]
        txt_p_ = txt_p_p + txt_p_b
    elif atomstyle == 'atomic' or atomstyle == 'charge':
        dicts = [atom_type_d]
        txt_p_ = txt_p_p
    else:
        print ('\nWeird thing, it is supposed impossible to reach this place\n')
        _flag_ = False
        
        
    return txt_p_, dicts, _flag_, regular_se, n_dihedraltypes


def write_lammps_input(  _simconfig_, _topodata_= None, in_name= 'in.gro2lam'):
    ''' _simconfig_ contains the data gathered from the gui
        _topodata_ comes from the converted gromacs file
        in_name is intended as name for the input to create'''
    
    #================================================================
    '''===========   Gathering and ordering the data   ==========='''
    #================================================================
    
    #===================================================
    ####-----------    SIM RAW CONFIG       --------####
    
    _simconfig_ = _simconfig_[:]
    ( data_file, timestep, nve_steps, nvt_steps, nvt_tss,
    nvt_tdamp, npt_steps, npt_pss, npt_pdamp, npt_tss,
     npt_tdamp) = _simconfig_[0]
    
    nvt_tstart, nvt_tend = nvt_tss.split(':')
    npt_pstart, npt_pend = npt_pss.split(':')
    npt_tstart, npt_tend = npt_tss.split(':')
    
    #print (data_file, timestep, nve_steps, nvt_steps, nvt_tstart, nvt_tend,
    #nvt_tdamp, npt_steps, npt_pstart, npt_pend, npt_tdamp, npt_tdamp,
    #npt_ystart, npt_yend)
    
    i = 5
    thermo, atommap, pairwiseint, lj_rcutoff, c_rcutoff = _simconfig_[1][ :i]
    neighbordistance, lrsolver, lrerror = _simconfig_[1][ i:i+3]
    lj12_13_14, co12_13_14 = _simconfig_[1][ i+3: i+5]
    neighbordelay, neighborupdate, npt_kind = _simconfig_[1][ i+5:i+8]
    f_comb_rule, T_init_vel, f_min_tol, _order_ = _simconfig_[1][ i+8:i+12]
    shake_tol, shake_bn, shake_an = _simconfig_[1][ i+12:]
    
    #===================================================
    ####------------    RESTRAIN DATA       --------####
    
    rest_line = ''
    group_lines = ''
    torestrain = []
    ens_af = []
    if _simconfig_[2] <> []:
        g_names, g_aids, k_xyz_c, runs_c, ch_init = _simconfig_[2][0][:]
        if _simconfig_[2][1] <> None:
            ####### ------------------------------------ Super interesante!!
            ##              este es uno de esos casos donde no es posible 
            ##              utilizar += a pesar de desligar con [:] ... 
            
            aux1, aux2, aux3, aux4, aux5 = _simconfig_[2][1][:] 
            g_names = g_names + aux1
            g_aids  = g_aids  + aux2
            k_xyz_c = k_xyz_c + aux3
            runs_c  = runs_c  + aux4
            ch_init = ch_init + aux5
        print'\n'
        for re in range(len(g_names)):
            if ch_init[re]==1:
                print 'Restraining group '+g_names[re]+' in '+runs_c[re]
                groupinfo = [g_names[re], g_aids[re]]
                group_lines += 'group {} id {}\n'.format( *groupinfo)
                
                if runs_c[re] not in ['', 'No', 'no', '0']:
                    ens = [int(x)-1 for x in runs_c[re].split('-')]
                    torestrain.append( [g_names[re], k_xyz_c[re], ens ])
                
                    for e in ens:
                        if e not in ens_af:
                            ens_af.append(e)
        if group_lines <> '':
            group_lines +='\n'
    
    mix_value = {'1':'geometric', '2':'arithmetic',
                 '3':'geometric', '4':'sixthpower'}
    
    
    #for mt in range(len( _mtype_)):
        #group_lines += 'group {} id {}:{}\n'.format(*_mtype_[mt])
    _asty_d_ ={ 'atomic':1, 'charge':2, 'bond':3, 'angle':4,
                'full':6, 'molecular':6}
    
    #===================================================
    ####------------      TOPO DATA         --------####
    
    print '\n'+data_file + '\n'
    if _topodata_ <> None:
        atomstyle_o, _solvated_, _autoload_, root_folder = _topodata_['config']
        _, comb_rule, _, _, _ = _topodata_['defaults']
        
    else:
        print '**** Without _topodata_ !!'
        root_folder = './'
        atomstyle_o = ''
        comb_rule = ''
        
    ## -------------------------- getting styles
    _aux_her = get_style_info( data_file)
    
    atomstyle, pairstyle, bondstyle, anglstyle, dihestyle, imprstyle = _aux_her
    if atomstyle_o <> '' and atomstyle_o <> atomstyle[0]:
        pop_wrg_1( 'Incongruence between atom styles!')
        print atomstyle_o, atomstyle[0]
    
    ## ---------------- MIXING RULE
    if f_comb_rule in mix_value.values():
        mix_value_s=' mix '+f_comb_rule
    elif f_comb_rule=='from_gromacs' and _topodata_<>None:
        mix_value_s=' mix '+mix_value[comb_rule]
    else:
        print 'Using default mixing rule'
        mix_value_s = ''
        

    #================================================================
    '''===========   Writing Lammps input command file  =========='''
    #================================================================
    _dtxt_= '# Generated with Gro2lam\n\n'+'units real\nboundary p p p\n'
    # as I understand lammps default is 3
    #_dtxt_+= '%s %d\n'.format('dimension',dimension)
    _dtxt_+= 'atom_style '+atomstyle[0]+'\n'
    if pairstyle[0] == '':
        if atomstyle[0] not in ['full', 'charge]']: # no charges
            if 'coul' in pairwiseint:
                pairwiseint = pairwiseint.split('/coul')[0]
            c_rcutoff = ''
        elif 'coul' not in pairwiseint:
            c_rcutoff = ''
        
        if pairwiseint == 'zero':
                c_rcutoff = 'nocoeff'
    else:
        pairwiseint = 'hybrid/overlay lennard/mdf 8 {}'.format( lj_rcutoff)
        if atomstyle[0] in ['full', 'charge]']: # no charges
            lj_rcutoff = ' coul/long'
        else:
            lj_rcutoff = ''
            c_rcutoff  = ''
                          
    _dtxt_+= '\natom_modify map {}\n'.format( atommap)
    #===================================================
    ####------------  SYSTEM CONFIGURATION  --------####
    
    ###############    TODO_WF this for sure can be improved----------- please!
    # options like full and non bonded interactions could be asked by the user
    _dsc_txt=['pair_style {} {}'.format( pairwiseint, lj_rcutoff)]
    _dsc_txt.append(' {}\n'.format( c_rcutoff))
    if bondstyle[0] <> '':
        _dsc_txt.append( 'bond_style '+' '.join( bondstyle)+'\n')
    if anglstyle[0] <> '':
        _dsc_txt.append( 'angle_style '+' '.join( anglstyle)+'\n')
    if dihestyle[0] <> '':
        _dsc_txt.append( 'dihedral_style '+' '.join( dihestyle)+'\n')
    if imprstyle[0] <> '':
        _dsc_txt.append( 'improper_style '+' '.join( imprstyle)+'\n')
    _dtxt_+= ''.join(_dsc_txt[:_asty_d_[atomstyle[0]]])+'\n'
    
    
    if 'data' in data_file:
        _dtxt_+= 'read_data {}\n'.format( data_file)
    else:
        _dtxt_+= 'read_restart {}\n'.format( data_file)
    
    #===================================================
    ####--------------   NEIGHBOR LIST   -----------####
    
    _dtxt_+= '\nneighbor {} bin\n'.format( neighbordistance)
    
    if lrsolver <> '' and atomstyle[0] in ['full','charge']:
        if 'long' in pairwiseint:
            _dtxt_+= 'kspace_style {} {}\n'.format( lrsolver, lrerror)
        
        aux_here1 = lj12_13_14.split(':')
        if lj12_13_14 == co12_13_14:
            sp_bon_3 = ['/coul {}'.format( aux_here1[0])] + aux_here1[1:]
        else:
            aux_here2 = co12_13_14.split(':')
            aux_here1 += [ aux_here2[0]]
            aux_txt = ' {} {} {} coul {}'.format( *aux_here1)
            sp_bon_3 = [ aux_txt] + aux_here2[1:]
                            
    elif lrsolver <> '':
        sp_bon_3 = lj12_13_14.split(':')
        
    
    if lrsolver <> '':
        _dtxt_+= 'special_bonds lj{} {} {}\n'.format( *sp_bon_3)
        
    _dtxt_+= 'pair_modify shift no tail yes'+mix_value_s+'\n'
    
    _aux_s_ = 'neigh_modify every {} delay {} check yes\n\n'
    _dtxt_+= _aux_s_.format( neighborupdate, neighbordelay)
    
    #===================================================
    ####---------------  TIMESTEP   ----------------####
    _dtxt_+= 'timestep {}\n\n\n'.format(timestep)
    _dtxt_+= 'thermo {}\n'.format(thermo)
    _dtxt_+= ('thermo_style custom step temp press vol '
              +'epair emol etotal enthalpy'
              +'\n\n')
    
    #===================================================
    ####--------------  Init VELOCITIES   ----------####
    aux_vel_str = 'velocity all create {} 1234567 rot yes dist gaussian\n\n'
    _dtxt_+= aux_vel_str.format(T_init_vel)
    
    #===================================================
    ####----------------   GROUPS   ----------------####
    _dtxt_+= group_lines
    
    #===================================================
    ####---------------     SHAKE       ------------####
    shake_bn, shake_an
    shake_txt = 'fix shake_name1 all shake {} 20 0'.format( shake_tol)
    print shake_bn, shake_an
    if shake_bn <> '0' or shake_an <> '0':
        
        if shake_bn <> '0':
            shake_txt += ' b'
            shake_bn = shake_bn.split('-')
            for bn in range(len(shake_bn)):
                shake_txt += ' '+shake_bn[bn]

        if shake_an <> '0':
            shake_txt += ' a'
            shake_an = shake_an.split('-')
            for an in range(len(shake_an)):
                shake_txt += ' '+shake_an[an]
        _dtxt_+= shake_txt+'\n\n'
    
    #===================================================
    ####---------------   SIMULATION    ------------####
    ensembles = _order_.split('-')
    curr_time = 0
    timestep = float(timestep)
    
    tounfix = [[],[]]
    _dtxt_ += '\n'
    for en in range(len(ensembles)):
        
        
        if ens_af<>[] and en in ens_af: #       RESTRAIN 
            
            for re in range(len(torestrain)):
                if en in torestrain[re][2]:
                    
                    if en-1 not in torestrain[re][2]:
                        spring_f = 'fix rest_{0}_{1} {0} spring/self {2} {3}\n'
                        k, xyz = torestrain[re][1].split(':')
                        _dtxt_ += spring_f.format( torestrain[re][0], en+1 ,
                                                  k, xyz)
                        unr= 0+en
                        while unr+1 in torestrain[re][2]:
                            unr+=1
                        
                        name_2uf = 'rest_{0}_{1}'.format( torestrain[re][0],
                                                         en+1)
                        tounfix= [ tounfix[0]+ [unr], tounfix[1]+ [name_2uf]]
            _dtxt_ += '\n'
            
        if ensembles[en]=='NVE' and nve_steps <> '' and nve_steps.isdigit():
            steps = int(nve_steps)
            nve_frm = 'fix nve_name1 all nve\nrun {}\nunfix nve_name1\n\n'
            _dtxt_ += nve_frm.format(steps)
            curr_time += steps*timestep
        
        elif ensembles[en]=='NPT' and npt_steps <> '' and npt_steps.isdigit():
            steps = int(npt_steps)
            npt_frm = 'fix npt_name1 all npt temp {} {} {} {} {} {} {}\n'
            _dtxt_ += npt_frm.format( npt_tstart, npt_tend, npt_tdamp,
                                     npt_kind, npt_pstart, npt_pend, npt_pdamp)
            _dtxt_+= 'run {}\nunfix npt_name1\n\n'.format( steps)
            curr_time += steps*timestep
        
        elif ensembles[en]=='NVT' and nvt_steps <> '' and nvt_steps.isdigit():
            steps = int(nvt_steps)
            nvt_frm = 'fix nvt_name1 all nvt temp {} {} {}\n'
            _dtxt_ += nvt_frm.format( nvt_tstart, nvt_tend, nvt_tdamp )
            _dtxt_+= 'run {}\nunfix nvt_name1\n\n'.format( steps)
            curr_time += steps*timestep
        
        elif ensembles[en]=='R':
            restart_txt = '\nwrite_restart restart.g2l_{}fs\n'
            _dtxt_ += restart_txt.format(int(curr_time))
            
        elif ensembles[en]=='M':
            if float(f_min_tol) > 1.0e-3:
                e_min_tol = 1.0e-2
                f_min_tol = 1.0e-3
            else:
                e_min_tol = float(f_min_tol)*100
            
            emin_frm = 'minimize {} {} 10000 100000\n\n'
            _dtxt_+= emin_frm.format( e_min_tol, f_min_tol )
            
            
        if tounfix <> [ [], []] and en in tounfix[0]: #       UNFIX RESTRAIN
            for unf in range( len( tounfix[0])):
                if tounfix[0][unf] == en:
                    _dtxt_ += 'unfix ' + tounfix[1][unf] + '\n'
    
    print ('Writing Lammps input script...')
    if root_folder <> './':
        _folder_ = '/'.join( data_file.split('/')[:-1]+[''])
    else:
        _folder_ = root_folder
    write_file( in_name , _dtxt_, _folder_)
    print_dec_g ('Successful writing!!')
    
    
     #-------------------- here would be optimum some further check
    return True

def get_style_info( lammps_datafile):
    
    #atom_sty, bond_sty, angl_sty, dihe_sty, impr_sty = '', '', '', '', ''
    styles = ['Pair', 'Bond', 'Angle', 'Dihedral', 'Improper', 'Atoms' ]
    sty_qty = [0,]*len( styles)
    default_styles = [ '',]+ ['harmonic']*2 + [ 'charmm', 'harmonic', 'full']
    sty_container = [ [], [], [], [], [], []]
    
    def_wrg_str = ( '{} style info not found or missing in the data file!'
                       + 'Using default : {}')
    try:
        
        with open( lammps_datafile, 'r')  as indata:
            
            # types collection
            for k_line in indata:
                line_c =  k_line.split()
                if len (line_c) == 3 and line_c[2] == 'types':
                    for st in range( len( styles)):
                        if line_c[1][1:] in styles[ st]:
                            sty_qty[st] = int( line_c[0])
                            break
                elif len (line_c) > 3 and  line_c[2] == 'xlo':
                    break
            sty_qty[ 0] = sty_qty[ 5]
            print 'Quantities : ',
            for st in range( len( styles)):
                print styles[st] + ' : ' + str( sty_qty[st]),
            print '\n'
            read_flag = False
            reading_flag = False
            index = 0
            for k_line in indata:
                line_c =  k_line.split()
                #print line_c
                # in cases with hybrid type, it should read from the second 
                # position in the data line of bond, angle, dihedral and impr
                if read_flag:
                    
                    if len( line_c) < 1 and reading_flag:
                        read_flag = False
                        reading_flag = False
                        index += 1
                        while not sty_qty[ index]:
                            sty_container[ index].append( '')
                            index += 1
                        print '... done!'
                    elif len( line_c) < 1 or line_c[0][0] == '#':
                        pass
                    else:
                        reading_flag = True
                        new_sty = line_c[1]
                        if new_sty not in sty_container[ index]:
                            print styles[ index] + 'Style : ' , new_sty,
                            sty_container[ index].append( new_sty)
                    
                # cutting out the crap, normal empty and commented lines
                elif len( line_c) < 1 or line_c[0][0] == '#':
                    pass
                    
                elif  ( styles[ index] == line_c[0] and 
                      ( index == 5 or 'Coeffs' == line_c[1]) ):
                    
                    print index, styles[ index], k_line.rstrip()
                    aux_cont = k_line.split('#')
                    
                    if len( aux_cont) > 1:
                        sty_container[ index].append( aux_cont[1].strip())
                        if sty_container[ index][0] == 'hybrid':
                            read_flag = True
                            index -= 1
                    else:
                        sty_container[ index].append( default_styles[ index])
                        pop_wrg_1( def_wrg_str.format( styles[ index], 
                                                       sty_container[ index]))
                    if index + 1 < len(sty_qty):
                        index += 1
                        while not sty_qty[ index]:
                            sty_container[ index].append( '')
                            index += 1
                    
    except IOError:
        pop_wrg_1( 'Data file not found!')
        print ( 'Maybe try performing a conversion first! ;)')
        _flag_ = False
    
    print('\n')
    sty_container = [sty_container[5],] + sty_container[:5]
    print sty_container
    return sty_container

if __name__ == '__main__':
    pass
    
# vim:tw=80
