#!/usr/bin/python
#    Ported to Python and barely optimized by Hernan Chavez Thielemann

from lib.misc.file import write_file
from lib.misc.warn import print_dec_g

__merged_files__ = ['main.m', 'Writing_input.m', ]
                    
                    
def extract_lammps_data(_data_file_,_ck_buttons_, _forcefield_):
    ''' already implemented in  topology analizer
            MIXER
    '''

def write_lammps_data(_topodata_, data_name, _config_):
    ''' Write a lammps data file'''
    print_dec_g ('Writing Lammps data file...')
    ####---------------  Unpacking data  ----------------####
    atomstyle, _, _ = _config_
    atsty = [ 'atomic', 'angle', 'full', 'charge', 'bond', 'molecular']
    style_str = '####-------  ATOM STYLE < {} >  --------####'
    _flag_ = False
    if atomstyle in atsty:
        nam = ''.join([ chr( ord(l) - 32) for l in atomstyle])
        print_dec_g(style_str.format(nam))
        _content_ = write_lammps_data_all(_topodata_, data_name, _config_)
        _flag_ = True
    else: #if atomstyle == 'Angle':
        _content_=''
        exit(('Error 037!!  -  Atom style {} '
              +'not implemented yet').format(atomstyle))
    
    write_file( data_name, _content_)
    
    print_dec_g ('Successful writing!!')
    
    return _flag_

def write_lammps_data_all( _topodata_, data_name, _config_):
    
    ''' Write a lammps data file'''
    ####---------------  Unpacking data  ----------------####
    _numbers_ = _topodata_['numbers']
    n_atoms, n_bonds, n_angles, n_dihedrals = _numbers_['total']
    n_atomtypes, n_bondtypes, n_angletypes, n_dihedraltypes= _numbers_['type']
    _box_= _topodata_['box']
    _mol_, _mtype_, _atype_, _xyz_ = _topodata_['atomsdata'] 
    
    atomstyle, _solvated_f_, _ = _config_ 
    
    _asty_d_ ={ 'atomic':1, 'charge':1, 'bond':2, 'angle':3,
                'full':4, 'molecular':4}
    ####--------------- TITLE ----------------####
    _text_ = '#Lammps data file. Geometry for PEG\n\n'
    ####---------------     NUMBERS      ----------------####
    _aux_txt =[' {} atoms\n'.format(n_atoms)]
    _aux_txt.append(' {} bonds\n'.format( n_bonds))
    _aux_txt.append(' {} angles\n'.format( n_angles))
    _aux_txt.append(' {} dihedrals\n'.format( n_dihedrals))
    _text_+= ''.join(_aux_txt[:_asty_d_[atomstyle]])+'\n'
    ####----------------    TYPES       -----------------####
    _aux_txt =[' {} atom types\n'.format(n_atomtypes)]
    _aux_txt.append(' {} bond types\n'.format(n_bondtypes))
    _aux_txt.append(' {} angle types\n'.format(n_angletypes))
    _aux_txt.append(' {} dihedral types\n\n'.format(n_dihedraltypes))
    _text_+= ''.join(_aux_txt[:_asty_d_[atomstyle]])+'\n'
    ####----------------    BOX     -----------------####
    _text_ +=(' {:.4f} {:.4f} xlo xhi\n {:.4f} {:.4f} ylo yhi\n'
              +' {:.4f} {:.4f} zlo zhi\n').format(*_box_)
    #####------             MASSES              ------####
    _text_ +='\n Masses\n\n'
    atom_info = _topodata_['atomtypes']
    for i in range( n_atomtypes):
        _text_ +=' {} {}\n'.format( i+1, atom_info[i][1])
        
    #####------             Force field potentials               ------####
    
    #for na in range(len(known_atoms)):
        #if known_atoms[na][4] not in charge.keys():
        #   print known_atoms[na][4], known_atoms[na][6]
        #charge[known_atoms[na][4]]= float(known_atoms[na][6])
        #conv_dict[known_atoms[na][4].lstrip(' ')] = known_atoms[na][1]
    #_topodata_['S_translation'] = conv_dict
        
    aux_pot_txt, dicts = write_lammps_potentials( _topodata_, atomstyle)
    _text_ += aux_pot_txt
    #a_dict={}
    #print dicts[0]
    #for key in conv_dict.keys(): # key - short
    #    
    #    a_dict[key]= dicts[0][conv_dict[key]]
    #print a_dict
    
    
    ####------ATOMS------####
    known_atoms = _topodata_['atoms']
    if _solvated_f_ == 1:
        charge = _topodata_['S_charge']
        conv_dict = _topodata_['S_translation'] # key s_tag : val l_tag
    
    
    _text_ +='\n Atoms\n\n'
    
    if atomstyle in ['charge','full']:
        atom_shape = ' {}'*3+' {:7.4f}'*4+' # {}\n'# idx mol atype charge x y z
    elif atomstyle in ['bond','angle','molecular']:
        atom_shape = ' {0} {1} {2} {4:7.4f} {5:7.4f} {6:7.4f} # {7}\n'
    elif atomstyle =='atomic':
        atom_shape = ' {0} {2} {4:7.4f} {5:7.4f} {6:7.4f} # {7}\n'
        
    base_atoms_n = len( known_atoms)
    for i in range( base_atoms_n):
        aty = known_atoms[i][1]
        _text_ += atom_shape.format( i+1, _mol_[i],
                                    dicts[0][aty],
                                    float(known_atoms[i][6]),
                                    float(_xyz_[i][0])*10,
                                    float(_xyz_[i][1])*10,
                                    float(_xyz_[i][2])*10,
                                    aty
                                   )
    solv_bonds = []
    solv_angles = []
    if _solvated_f_ == 1:
        solv_at_v = range(n_atoms )[ base_atoms_n:]
        for i in solv_at_v:
            aty = conv_dict[_atype_[i]]
            _text_ += atom_shape.format(i+1, _mol_[i], dicts[0][aty],
                                        charge[aty],
                                        float(_xyz_[i][0])*10,
                                        float(_xyz_[i][1])*10,
                                        float(_xyz_[i][2])*10,
                                        aty
                                       )
            if charge[aty] <0:
                # better way to do this is trough coords ---------  <WFS>
                # but anyway works perfectly
                aty2 = conv_dict[_atype_[i+1]]
                aty3 = conv_dict[_atype_[i+2]]
                solv_bonds.append([aty+'-'+aty2, i+1, i+2])
                solv_bonds.append([aty+'-'+aty3, i+1, i+3])
                solv_angles.append([aty2+'-'+aty+'-'+aty3, i+2, i+1, i+3])
    
    
    ####------BONDS------####
    if _asty_d_[atomstyle]>=2:
        known_bonds = _topodata_['bonds']
        base_bonds_n = len (known_bonds)
        _text_ +='\n Bonds\n\n'
        bond_shape = ' {}'*4+'\n'
        for i in range(base_bonds_n):
            
            at1 = int(known_bonds[i][0])
            at2 = int(known_bonds[i][1])
            
            _bond_ty_ = dicts[1][known_atoms[at1-1][1]+'-'
                                 +known_atoms[at2-1][1]]
            _text_ += bond_shape.format( i+1, _bond_ty_, at1, at2)
                        
        if _solvated_f_ == 1:
            # better way to do this is trough corrds ---------  <WFS>
            for i in range(n_bonds-base_bonds_n):
                _bond_ty_ = dicts[1][solv_bonds[i][0]]
                _text_ += bond_shape.format(i+1+base_bonds_n,_bond_ty_,
                                            solv_bonds[i][1],solv_bonds[i][2])
    
    
    ####------ANGLES------#########
    if _asty_d_[atomstyle]>=3:
        known_angles = _topodata_['angles']
        base_angles_n = len(known_angles)
        _text_ +='\n Angles\n\n'
        angle_shape = ' {}'*5+'\n'
        for i in range(base_angles_n):
            
            at1 = int(known_angles[i][0])
            at2 = int(known_angles[i][1])
            at3 = int(known_angles[i][2])
            
            angle_t = (known_atoms[at1-1][1]+'-'+ known_atoms[at2-1][1]
                       +'-'+known_atoms[at3-1][1])
            _angle_ty_ = dicts[2][angle_t]
            
            #print angle_t, _angle_ty_
            _text_ += angle_shape.format( i+1, _angle_ty_, at1, at2, at3)
            
        if _solvated_f_ == 1:
            
            for i in range(n_angles-base_angles_n):
                _angle_ty_ = dicts[2][solv_angles[i][0]]
                
                _text_ += angle_shape.format(i+1+base_angles_n, _angle_ty_,
                                             solv_angles[i][1],
                                             solv_angles[i][2],
                                             solv_angles[i][3]
                                            )
    
    
    ####------DIHEDRAL------####
    if _asty_d_[atomstyle]==4:
        known_dihedrals = _topodata_['dihedrals']
        base_dihedrals_n = len(known_dihedrals)
        _text_ +='\n Dihedrals\n\n'
        dihedral_shape = ' {}'*6+'\n'
        for i in range(base_dihedrals_n):
            
            at1 = int(known_dihedrals[i][0])
            at2 = int(known_dihedrals[i][1])
            at3 = int(known_dihedrals[i][2])
            at4 = int(known_dihedrals[i][3])
            
            _dihe_ty_ = dicts[3][known_atoms[at1-1][1]+'-'
                                 +known_atoms[at2-1][1]+'-'
                                 +known_atoms[at3-1][1]+'-'
                                 +known_atoms[at4-1][1]
                                ]
            _text_+= dihedral_shape.format( i+1, _dihe_ty_, at1, at2, at3, at4)
    
    
    return _text_

def write_lammps_data_atomic(_topodata_, data_name, _config_):
    ''' Write a lammps data file
    
        Deprecated
    '''
    ####---------------  Unpacking data  ----------------####
    _numbers_ = _topodata_['numbers']
    n_atoms, _, _, _ = _numbers_['total']
    n_atomtypes, _, _, _= _numbers_['type']
    _box_= _topodata_['box']
    _, _, _atype_, _xyz_ = _topodata_['atomsdata']
    known_atoms = _topodata_['atoms']
    atom_info = _topodata_['atomtypes']
    atomstyle, _solvated_f_, _ = _config_ 
    ####--------------- TITLE ----------------####
    _text_ = '#Lammps data file. Geometry for PEG\n\n'
    ####---------------     NUMBERS      ----------------####
    _text_ +=' {} atoms\n'.format(n_atoms)
    ####----------------    TYPES       -----------------####
    _text_ +=' {} atom types\n'.format(n_atomtypes)
    ####----------------    BOX     -----------------####
    _text_ +=(' {:.4f} {:.4f} xlo xhi\n {:.4f} {:.4f} ylo yhi\n'
              +' {:.4f} {:.4f} zlo zhi\n').format(*_box_)
    #####------             MASSES              ------####
    _text_ +='\n Masses\n\n'
    for i in range( n_atomtypes):
        _text_ +=' {} {}\n'.format( i+1, atom_info[i][1])
    #####------             Force field potentials               ------####
    aux_pot_txt, adict = write_lammps_potentials( _topodata_, atomstyle)
    _text_ += aux_pot_txt
    ####------ATOMS------####
    if _solvated_f_ == 1:
        conv_dict = _topodata_['S_translation'] # key s_tag : val l_tag
        
    _text_ +='\n Atoms\n\n'
    
    atom_shape = ' {}'*2+' {:7.4f}'*3+'\n'# index mol atype charge x y z
    base_atoms_n = len( known_atoms)
    for i in range( base_atoms_n):
        aty = known_atoms[i][1]
        _text_ += atom_shape.format( i+1,
                                    adict[aty],
                                    float(_xyz_[i][0])*10,
                                    float(_xyz_[i][1])*10,
                                    float(_xyz_[i][2])*10
                                   )
    if _solvated_f_ == 1:
        solv_at_v = range(n_atoms )[ base_atoms_n:]
        for i in solv_at_v:
            aty = conv_dict[_atype_[i]]
            _text_ += atom_shape.format(i+1, adict[aty],
                                        float(_xyz_[i][0])*10,
                                        float(_xyz_[i][1])*10,
                                        float(_xyz_[i][2])*10
                                       )
    return _text_

def write_lammps_potentials( _topodata_, atomstyle = 'full'):
    
    atom_info = _topodata_['atomtypes'] # index 1: mass ; index 4 -5 : eps-sig
    _numbers_ = _topodata_['numbers']
    n_atomtypes, n_bondtypes, n_angletypes, n_dihedraltypes= _numbers_['type']
    #n_bondstypes = len(data_container['bondtypes'])
    
    buckorlj = int( _topodata_[ 'defaults'][0]) # 1 -2 lj/buc
    comb_rule = int( _topodata_[ 'defaults'][1]) # 1-2-3
    
    sigma = []
    epsilon = []
    buck3 = []
    atom_type_d = {}
        
    for x in range( n_atomtypes):
        atom_type_d[atom_info[x][0]] = x+1
        
        _A_ = float(atom_info[x][5])
        _B_ = float(atom_info[x][4])
        
        
        if comb_rule==1:
            _eps_ = (_B_**2)/(4*_A_)
            _sig_ = (_A_/_B_)**(1/6.0)
            
        else:
            _eps_ = _A_
            _sig_ = _B_
            
            
        epsilon.append(_eps_ / 4.186)
        
        if buckorlj == 2:#------------------------------------------  <WFS>
            _C_ = loat(atom_info[x][6])
            buck3.append(' '+ str(f_C_/ 4.186 / (10** 6)))
            sigma.append( 10 / _sig_)
            
        else:
            buck3.append('')
            sigma.append(_sig_* 10)
            
    ####----------- DEFINING LJ INTERACTIONS     ----------####
    #-------------------------------------------------------  <WFS> 
    #                        make function- buck
    '''potential'''
    txt_p_p ='\n Pair Coeffs\n\n'
    for i in range( n_atomtypes):
        txt_p_p +=' {} {} {}{}\n'.format( i+1, epsilon[i], sigma[i], buck3[i])
    
    
    ####----------- DEFINING BONDED INTERACTIONS     ----------####
    txt_p_b ='\n Bond Coeffs\n\n' # bond_style hybrid
    bty = _topodata_['bondtypes']
    bondtypes_d = {}
    for i in range(n_bondtypes):
        bondtypes_d[bty[i][0]+'-'+bty[i][1]]= i+1
        bondtypes_d[bty[i][1]+'-'+bty[i][0]]= i+1
        txt_p_b += ' {} {:.4f} {:.4f}\n'.format( i+1,
                                              float(bty[i][-1])/ 100/ 4.186/2,
                                              float(bty[i][-2])*10)
    
    txt_p_a ='\n Angle Coeffs\n\n'
    aty = _topodata_['angletypes']
    angletypes_d = {}
    i=0
    for i in range(n_angletypes):
        angletypes_d[aty[i][0]+'-'+aty[i][1]+'-'+aty[i][2]]= i+1
        angletypes_d[aty[i][2]+'-'+aty[i][1]+'-'+aty[i][0]]= i+1
        txt_p_a += ' {} {:.4f} {:.4f}\n'.format( i+1,
                                              float(aty[i][-1])/ 4.186/2,
                                              float(aty[i][-2]))
    
    txt_p_d ='\n Dihedral Coeffs\n\n'
    dty = _topodata_['dihedraltypes']
    dihedraltypes_d = {}
    i=0
    for i in range(n_dihedraltypes):
        _type_forward_ = dty[i][0]+'-'+dty[i][1]+'-'+dty[i][2]+'-'+dty[i][3]
        _type_backward_ = dty[i][3]+'-'+dty[i][2]+'-'+dty[i][1]+'-'+dty[i][0]
        dihedraltypes_d[ _type_forward_ ] = i+1
        dihedraltypes_d[ _type_backward_] = i+1
        txt_p_d += ' {} {:.4f} {} {} {}\n'.format( i+1,
                                                  float(dty[i][-2])/4.186/2,
                                                  int(float(dty[i][-1])),
                                                  int(float(dty[i][-3])),
                                                  '0.0'
                                                 )
    
    if atomstyle in ['full', 'molecular']:
        dicts = [ atom_type_d, bondtypes_d, angletypes_d, dihedraltypes_d]
        txt_p_ = txt_p_p+txt_p_b+txt_p_a+txt_p_d
    elif atomstyle == 'angle':
        dicts = [ atom_type_d, bondtypes_d, angletypes_d]
        txt_p_ = txt_p_p+txt_p_b+txt_p_a
    elif atomstyle == 'bond':
        dicts = [ atom_type_d, bondtypes_d]
        txt_p_ = txt_p_p+txt_p_b
    elif atomstyle == 'atomic' or atomstyle == 'charge':
        dicts = [atom_type_d]
        txt_p_ = txt_p_p
    else:
        print ('\nWeird thing, it is supposed impossible to reach this place\n')
    
    return txt_p_, dicts


def write_lammps_input(  _simconfig_, _topodata_= None, in_name= 'in.gro2lam'):
    ''' _simconfig_ contains the data gathered from the gui
        _topodata_ comes from the converted gromacs file
        in_name is intended as name for the input'''
    
    #===================================================
    '''====   Gathering and ordering the data   ====='''
    #===================================================
    
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
    thermo, atommap, pairwiseint, lj_rcutoff, c_rcutoff = _simconfig_[1][:i]
    neighbordistance, lrsolver, lrerror, in12_13_14 = _simconfig_[1][i:i+4]
    neighbordelay, neighborupdate, npt_kind = _simconfig_[1][i+4:i+7]
    f_comb_rule, _order_, T_init_vel = _simconfig_[1][i+7:]
    
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
            
            aux1,aux2,aux3,aux4,aux5 = _simconfig_[2][1][:] 
            g_names = g_names + aux1
            g_aids =  g_aids  + aux2
            k_xyz_c = k_xyz_c + aux3
            runs_c =  runs_c  + aux4
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
                'full':5, 'molecular':5}
    
    #===================================================
    ####------------      TOPO DATA         --------####
    
    print '\n'+data_file + '\n'
    if _topodata_<>None:
        atomstyle, _solvated_, _parametric_ = _topodata_['config'] 
        
        buckorlj, comb_rule, _, f_LJ, _ = _topodata_['defaults']
        
    else:
        print 'non _topodata_'
        atomstyle = 'full'
        comb_rule = ''
        buckorlj = 0
        
        
    if f_comb_rule in mix_value.values():
        mix_value_s=' mix '+f_comb_rule
    elif f_comb_rule=='from_gromacs' and _topodata_<>None:
        mix_value_s=' mix '+mix_value[comb_rule]
    else:
        print 'Using default mixing rule'
        mix_value_s = ''
        

    #===================================================
    '''=======    Writing Lammps data file    ======='''
    #===================================================
    _dtxt_= '\n'+'#INIT\n'+'units real\n'+'boundary p p p\n'+'atom_style '
    # as I understand lammps default is 3
    #_dtxt_+= '%s %d\n'.format('dimension',dimension)
    _dtxt_+= atomstyle+'\n'
    if atomstyle not in ['full', 'charge]']: # no charges
        if 'coul' in pairwiseint:
            pairwiseint = pairwiseint.split('/coul')[0]
        c_rcutoff = ''
    elif 'coul' not in pairwiseint:
        c_rcutoff = ''
        
    if pairwiseint == 'zero':
            c_rcutoff = 'nocoeff'
        
    _dtxt_+= '\natom_modify map {}\n'.format(atommap)
    #===================================================
    ####------------  SYSTEM CONFIGURATION  --------####
    
    _dsc_txt=['pair_style {} {}'.format( pairwiseint, lj_rcutoff)]
    _dsc_txt.append(' {}\n'.format( c_rcutoff))
    _dsc_txt.append( 'bond_style harmonic\n')
    _dsc_txt.append( 'angle_style harmonic\n')
    _dsc_txt.append( 'dihedral_style charmm\n')
    _dtxt_+= ''.join(_dsc_txt[:_asty_d_[atomstyle]])+'\n'
    
    
    if 'data' in data_file:
        _dtxt_+= 'read_data {}\n'.format(data_file)
    else:
        _dtxt_+= 'read_restart {}\n'.format(data_file)
    
    #===================================================
    ####--------------   NEIGHBOR LIST   -----------####
    _dtxt_+= '\nneighbor {} bin\n'.format( neighbordistance)
    
    if lrsolver <> '' and atomstyle in ['full','charge']:
        if '/coul/long' in pairwiseint:
            _dtxt_+= 'kspace_style {} {}\n'.format( lrsolver, lrerror)
    _dtxt_+= 'pair_modify shift no tail yes'+mix_value_s+'\n'
    
    _dtxt_+= 'special_bonds lj/coul {} {} {}\n'.format( *in12_13_14.split(':'))
    
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
            
        if tounfix <> [ [], []] and en in tounfix[0]: #       UNFIX RESTRAIN
            for unf in range( len( tounfix[0])):
                if tounfix[0][unf] == en:
                    _dtxt_ += 'unfix ' + tounfix[1][unf] + '\n'
    
    print ('Writing Lammps input script...')
    
    write_file( in_name , _dtxt_)
    print_dec_g ('Successful writing!!')
    
    
     #-------------------- here would be optimum some further check
    return True


if __name__ == '__main__':
    pass
    
    
