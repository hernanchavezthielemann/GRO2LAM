#!/usr/bin/python
#    Ported to Python and barely optimized by Hernan Chavez Thielemann

from lib.misc.file import write_file
from lib.misc.warn import print_dec_g

__merged_files__ = ['main.m', 'Writing_input.m', ]
                    
                    
def extract_lammps_data(_data_file_,_ck_buttons_, _forcefield_):
    ''' already implemented in  topology analizer'''

def write_lammps_data(_topodata_, data_name, _config_):
    ''' Write a lammps data file'''
    print_dec_g ('Writing Lammps data file...')
    ####---------------  Unpacking data  ----------------####
    atomstyle, _, _ = _config_
    if atomstyle == 'Full':
        print_dec_g('####-------  ATOMIC STYLE(FULL)  --------####')
        _content_ = write_lammps_data_full(_topodata_, data_name, _config_)
        
    else: #if atomstyle == 'Angle':
        _content_=''
        exit('Error 011!!  -  Not implemented yet')
        
        
    write_file( data_name, _content_)
    
    print_dec_g ('Successful writing!!')

def write_lammps_data_full(_topodata_, data_name, _config_):
    
    ''' Write a lammps data file'''
    ####---------------  Unpacking data  ----------------####
    _numbers_ = _topodata_['numbers']
    n_atoms, n_bonds, n_angles, n_dihedrals = _numbers_['total']
    n_atomtypes, n_bondtypes, n_angletypes, n_dihedraltypes= _numbers_['type']
    _box_= _topodata_['box']
    _mol_, _atype_, _xyz_ = _topodata_['atomsdata'] 
    
    atomstyle, _solvated_f_, _ = _config_ 
    
    
    ####--------------- TITLE ----------------####
    _text_ = '#Lammps data file. Geometry for PEG\n\n'
    ####---------------     NUMBERS      ----------------####
    _text_ +=' {} atoms\n'.format(n_atoms)
    _text_ +=' {} bonds\n'.format( n_bonds)
    _text_ +=' {} angles\n'.format( n_angles)
    _text_ +=' {} dihedrals\n'.format( n_dihedrals)
    ####----------------    TYPES       -----------------####
    _text_ +=' {} atom types\n'.format(n_atomtypes)
    _text_ +=' {} bond types\n'.format(n_bondtypes)
    _text_ +=' {} angle types\n'.format(n_angletypes)
    _text_ +=' {} dihedral types\n\n'.format(n_dihedraltypes)
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
        
    aux_pot_txt, dicts = write_lammps_potentials( _topodata_)
    _text_ += aux_pot_txt
    #a_dict={}
    #print dicts[0]
    #for key in conv_dict.keys(): # key - short
    #    
    #    a_dict[key]= dicts[0][conv_dict[key]]
    #print a_dict
    
    ####------ATOMS------####
    known_atoms = _topodata_['atoms']
    
    charge =_topodata_['S_charge']
    conv_dict = _topodata_['S_translation'] # key s_tag : val l_tag
    
    # totally dislike this, but still better ---------  <WFS>
    _text_ +='\n Atoms\n\n'
    
    atom_shape = ' {}'*3+' {:7.4f}'*4+'\n'# index mol atype charge x y z
    base_atoms_n = len( known_atoms)
    for i in range( base_atoms_n):
        aty = known_atoms[i][1]
        _text_ += atom_shape.format( i+1, _mol_[i],
                                    dicts[0][aty],
                                    float(known_atoms[i][6]),
                                    float(_xyz_[i][0])*10,
                                    float(_xyz_[i][1])*10,
                                    float(_xyz_[i][2])*10
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
                                        float(_xyz_[i][2])*10
                                       )
            if charge[aty] <0:
                # better way to do this is trough corrds ---------  <WFS>
                aty2 = conv_dict[_atype_[i+1]]
                aty3 = conv_dict[_atype_[i+2]]
                solv_bonds.append([aty+'-'+aty2, i+1, i+2])
                solv_bonds.append([aty+'-'+aty3, i+1, i+3])
                solv_angles.append([aty2+'-'+aty+'-'+aty2, i+2, i+1, i+3])
    
    ####------BONDS------####
    known_bonds = _topodata_['bonds']
    base_bonds_n = len (known_bonds)
    _text_ +='\n Bonds\n\n'
    bond_shape = ' {}'*4+'\n'
    for i in range(base_bonds_n):
        
        at1 = int(known_bonds[i][0])
        at2 = int(known_bonds[i][1])
        
        _bond_ty_ = dicts[1][known_atoms[at1-1][1]+'-'+known_atoms[at2-1][1]]
        _text_ += bond_shape.format( i+1, _bond_ty_, at1, at2)
                    
    if _solvated_f_ == 1:
        # better way to do this is trough corrds ---------  <WFS>
        for i in range(n_bonds-base_bonds_n):
            _bond_ty_ = dicts[1][solv_bonds[i][0]]
            _text_ += bond_shape.format(i+1+base_bonds_n,_bond_ty_,
                                        solv_bonds[i][1],solv_bonds[i][2])
            

    ####------ANGLES------#########
    known_angles = _topodata_['angles']
    base_angles_n = len(known_angles)
    _text_ +='\n Angles\n\n'
    angle_shape = ' {}'*5+'\n'
    for i in range(base_angles_n):
        
        at1 = int(known_angles[i][0])
        at2 = int(known_angles[i][1])
        at3 = int(known_angles[i][2])
        
        _angle_ty_ = dicts[2][known_atoms[at1-1][1]+'-'+
                              known_atoms[at2-1][1]+'-'+known_atoms[at3-1][1]]
        _text_ += angle_shape.format( i+1, _angle_ty_, at1, at2, at3)
        
    if _solvated_f_ == 1:
        
        for i in range(n_angles-base_angles_n):
            _angle_ty_ = dicts[2][solv_angles[i][0]]
            
            _text_ += angle_shape.format(i+1+base_angles_n, _angle_ty_,
                                         solv_angles[i][1],
                                         solv_angles[i][2],
                                         solv_angles[i][2]
                                        )
    
    ####------DIHEDRAL------####
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
        _text_ += dihedral_shape.format( i+1, _dihe_ty_, at1, at2, at3, at4)

    return _text_

def write_lammps_potentials(_topodata_):
    
    txt_p_=''
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
        
        _B_ = float(atom_info[x][4])
        _A_ = float(atom_info[x][5])
        
        if comb_rule==1:
            _sig_ = (_A_/_B_)**(1/6.0)
            _eps_ = (_B_**2)/(4*_A_)
        else:
            _sig_ = _B_
            _eps_ = _A_
            
        sigma.append(_sig_* 10)
        epsilon.append(_eps_ / 4.186)
        
        if buckorlj == 2:#------------------------------------------  <WFS>
            buck3.append(float(atom_info[x][6]) / 4.186 / (10 ** 6))
    
    
    ####----------- DEFINING LJ INTERACTIONS     ----------####
    #-------------------------------------------------------  <WFS> make function- buck
    '''potential'''
    txt_p_ +='\n Pair Coeffs\n\n'
    for i in range( n_atomtypes):
        txt_p_ +=' {} {} {}\n'.format( i+1, epsilon[i], sigma[i])
    ####----------- DEFINING BONDED INTERACTIONS     ----------####
    txt_p_ +='\n Bond Coeffs\n\n' # bond_style hybrid
    bty = _topodata_['bondtypes']
    bondtypes_d = {}
    for i in range(n_bondtypes):
        bondtypes_d[bty[i][0]+'-'+bty[i][1]]= i+1
        bondtypes_d[bty[i][1]+'-'+bty[i][0]]= i+1
        txt_p_+= ' {} {:.4f} {:.4f}\n'.format( i+1,
                                              float(bty[i][-1])/ 100/ 4.186/2,
                                              float(bty[i][-2])*10)
    
    
    txt_p_ +='\n Angle Coeffs\n\n'
    aty = _topodata_['angletypes']
    angletypes_d = {}
    for i in range(n_angletypes):
        angletypes_d[aty[i][0]+'-'+aty[i][1]+'-'+aty[i][2]]= i+1
        angletypes_d[aty[i][2]+'-'+aty[i][1]+'-'+aty[i][0]]= i+1
        txt_p_+= ' {} {:.4f} {:.4f}\n'.format( i+1,
                                              float(aty[i][-1])/ 4.186/2,
                                              float(aty[i][-2]))
    
    txt_p_ +='\n Dihedral Coeffs\n\n'
    dty = _topodata_['dihedraltypes']
    dihedraltypes_d = {}
    for i in range(n_dihedraltypes):
        dihedraltypes_d[dty[i][0]+'-'+dty[i][1]+'-'+dty[i][2]+'-'+dty[i][3]]= i+1
        dihedraltypes_d[dty[i][3]+'-'+dty[i][2]+'-'+dty[i][1]+'-'+dty[i][0]]= i+1
        txt_p_+= ' {} {:.4f} {} {} {}\n'.format( i+1,
                                                     float(dty[i][-2])/4.186/2,
                                                     int(float(dty[i][-1])),
                                                     int(float(dty[i][-3])),
                                                     '0.0'
                                                    )
        
    dicts = [ atom_type_d, bondtypes_d, angletypes_d, dihedraltypes_d]
                                    
    return txt_p_, dicts
        
def write_lammps_input(  _simconfig_, _topodata_= None, in_name= 'in.gro2lam'):
    
    _dtxt_=('#dimension,rcutoff,F,bondtypenumber,angletypenumber,'
            + '#dihedraltypenumber,neighbordistance,neighbordelay,'
            + '#neighborupdate,timestep, atom_inbondtype,n_typeatoms,'
            + '#param_bond1,param_bond2,param_bond3, param_angle1,'
            + '#param_angle2, param_angle3,param_angle4,param_dihedral1,'
            + '#param_dihedral2,param_dihedral3,param_dihedral4,n_typebonds,'
            + '#n_typeangles,n_typedihedrals,pot1,pot2,pot3,buckorlj,choice,'
            + '#bonddatabase,angledatabase,dihedraldatabase')
    _dtxt_ =''
    
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
    neighbordistance, lrsover, lrerror = _simconfig_[1][i:i+3]
    in12_13_14, neighbordelay, neighborupdate, npt_kind = _simconfig_[1][i+3:]
    
    #==================          _topodata_            ============
    if _topodata_<>None:
        atomstyle, _solvated_, _parametric_ = _topodata_['config'] 
        
    else:
        atomstyle = 'Full'
        buckorlj = 0
        
    #========================================================
    _dtxt_+= '\n'+'#INIT\n'+'units real\n'+'boundary p p p\n'+'atom_style '
    # as I understand lammps default is 3
    #_dtxt_+= '%s %d\n'.format('dimension',dimension) 
    if atomstyle == 'Atomic':
        _dtxt_+= 'atomic\n'
    elif atomstyle == 'Angle':
        _dtxt_+= 'angle\n'
    elif atomstyle == 'Full':
        _dtxt_+= 'full\n'
    
    _dtxt_+= 'atom_modify map {}\n'.format(atommap)
    ####---------------SYSTEM CONFIGURATION----------####
    
    _dtxt_+= 'bond_style harmonic\n'
    _dtxt_+= 'angle_style harmonic\n'
    _dtxt_+= 'dihedral_style charmm\n'
    _dtxt_+= 'pair_style {} {} {}\n'.format( pairwiseint, lj_rcutoff, c_rcutoff)
    
    
    if 'data' in data_file:
        print data_file
        _dtxt_+= 'read_data {}\n'.format(data_file)
    else:
        _dtxt_+= 'read_restart {}\n'.format(data_file)
        
    ####----------------NEIGHBOR LIST-----------####
    _dtxt_+= 'neighbor {} bin\n'.format( neighbordistance)
    if lrsover <> '':
        _dtxt_+= 'kspace_style {} {}\n'.format( lrsover, lrerror)
    _dtxt_+= 'pair_modify shift no tail yes\n'
    _dtxt_+= 'special_bonds lj/coul {} {} {}\n'.format(*in12_13_14.split(':'))
    _dtxt_+= 'neigh_modify every {} delay {} check yes\n\n'.format(
                                                  neighborupdate, neighbordelay)
    
    ####----------------TIMESTEP----------------####
    _dtxt_+= 'timestep {}\n\n\n'.format(timestep)
    ####---------------EQUILIBRATION------------####
    
    
    
    if nve_steps <> '' and nve_steps.isdigit():
        _dtxt_+= 'fix nve_name1 all nve\nrun {}\nunfix nve_name1\n\n'.format(nve_steps)
        
    if npt_steps <> '' and npt_steps.isdigit():
        npt_frm = 'fix npt_name1 all npt temp {} {} {} {} {} {} {}\n'
        _dtxt_ += npt_frm.format( npt_tstart, npt_tend, npt_tdamp,
                                  npt_kind, npt_pstart, npt_pend, npt_pdamp )
        _dtxt_+= 'run {}\nunfix npt_name1\n\n'.format( npt_steps)

    if npt_steps <> '' and npt_steps.isdigit():
        nvt_frm = 'fix nvt_name1 all nvt {} {} {}\n'
        _dtxt_ += nvt_frm.format( nvt_tstart, nvt_tend, nvt_tdamp )
        _dtxt_+= 'run {}\nunfix nvt_name1\n\n'.format( nvt_steps)
            
    print_dec_g ('Writing Lammps input script...')
    
    write_file( in_name , _dtxt_)
    print_dec_g ('Successful writing!!')

def write_lammps_data_lib(_topodata_, data_name, _config_):
    
    ''' Write a lammps data file'''
    ####---------------  Unpacking data  ----------------####
    _numbers_ = _topodata_['numbers']
    n_atoms, n_bonds, n_angles, n_dihedrals = _numbers_['total']
    n_atomtypes, n_bondtypes, n_angletypes, n_dihedraltypes= _numbers_['type']
    _box_= _topodata_['box']
    
    atom_info = _topodata_['atomtypes']
    mass_type = []
    for x in range( len( atom_info)):
        mass_type.append(atom_info[x][1])
    
    atomstyle, ckbuttons = _config_ 
    
    ####--------------- TITLE ----------------####
    _text_ += '#Lammps data file. Geometry for PEG\n\n'
    ####---------------NUMBERS----------------####
    _text_ +=' {} atoms\n'.format(n_atoms)
    
    if atomstyle in ['Angle','Full']:
        _text_ +=' {} bonds\n {} angles\n'.format( n_bonds, n_angles)
        if atomstyle == 'Full':
            _text_ +=' {} dihedrals\n'.format( n_dihedrals)
    else:
        _text_ +='\n'
    ####----------------TYPES-----------------####
    _text_ +=' {} atom types\n',n_atomtypes,'atom types'
    
    if atomstyle == 'Angle' or atomstyle == 'Full':
        _text_ +=' {} bond types\n'.format(n_bondtypes)
        _text_ +=' {} angle types\n'.format(n_angletypes)
        if atomstyle == 'Full':
            _text_ +=' {} dihedral types\n\n'.format(n_dihedraltypes)
    else:
        _text_ +='\n'
    
    ####----------------BOX-----------------####
    _text_ +=(' {:.4f} {:.4f} xlo xhi\n {:.4f} {:.4f} ylo yhi\n'
              +'{:.4f} {:.4f} zlo zhi\n').format(*_box_)
    
    # ####------MASSES------####
    _text_ +='\nMasses\n'
    for i in range( n_atomtypes):
        _text_ +=' {} {}\n'.format( i+1, mass_type[i])
    
    print_dec_g('WRITING ATOMS....')
    ####------ATOMS------####
    charge_water = matlabarray( cat( -0.8476,+ 0.4238))
    
    _text_ +='\n%1s\n\n','Atoms'
    ####-------ATOMIC STYLE(FULL)--------####
    ####---------------------------------####
    if atomstyle == 'Full':
        for i in arange( 1, n_atoms).reshape(-1):
            for j in arange( 1, n_atomtypes).reshape(-1):
                if strcmp( atom_inbond[i], atom_inbondtype[j]) == 1:
                    _text_ +='\t\t%d\t %d\t %d\t %7.4f\t %7.4f\t %7.4f\t %7.4f\n',i,n_mol[i],j,charge[i],dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
        if choice_solv == 1:
            for i in arange(n_atoms + 1,(dot((n_mol[end()] - 1),3) + n_atoms),1).reshape(-1):
                if strcmp(type_[i],'opls_116') == 1:
                    _text_ +='\t\t%d\t %d\t %d\t %7.4f\t %7.4f\t %7.4f\t %7.4f\n',i,n_mol[i],indexoxy,charge_water[1],dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                elif strcmp(type_[i],'opls_117') == 1:
                    _text_ +='\t\t%d\t %d\t %d\t %7.4f\t %7.4f\t %7.4f\t %7.4f\n',i,n_mol[i],indexhyd,charge_water[2],dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                else:
                    print_dec_g('error')
    
    ####------ATOMIC STYLE(ATOMIC)------####
    ####---------------------------------####
    if atomstyle == 'Atoms':
        for i in arange(1,n_atoms).reshape(-1):
            for j in arange(1,n_atomtypes).reshape(-1):
                if strcmp(atom_inbond[i],atom_inbondtype[j]) == 1:
                    _text_ +='\t\t%d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,j,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
        if choice_solv == 1:
            for i in arange(n_atoms + 1,(dot((n_mol[end()] - 1),3) + n_atoms),1).reshape(-1):
                if strcmp(type_[i],'opls_116') == 1:
                    _text_ +='\t\t%d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,indexoxy,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                else:
                    if strcmp(type_[i],'opls_117') == 1:
                        _text_ +='\t\t%d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,indexhyd,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                    else:
                        if strcmp(type_[i],'NA') == 1:
                            _text_ +='\t\t%d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,indexhyd,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                        else:
                            print_dec_g('error')
    
    ####------ATOMIC STYLE(ANGLE)------####
    ####-------------------------------####
    if atomstyle == 'Angle':
        for i in arange(1,n_atoms).reshape(-1):
            for j in arange(1,n_atomtypes).reshape(-1):
                if strcmp(atom_inbond[i],atom_inbondtype[j]) == 1:
                    _text_ +='\t\t%d\t %d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,n_mol[i],j,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
        if choice_solv == 1:
            for i in arange(n_atoms + 1,(dot((n_mol[end()] - 1),3) + n_atoms),1).reshape(-1):
                if strcmp(type_[i],'opls_116') == 1:
                    _text_ +='\t\t%d\t %d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,n_mol[i],indexoxy,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                else:
                    if strcmp(type_[i],'opls_117') == 1:
                        _text_ +='\t\t%d\t %d\t %d\t %7.4f\t %7.4f\t %7.4f\n',i,n_mol[i],indexhyd,dot(coor_x[i],10),dot(coor_y[i],10),dot(coor_z[i],10)
                    else:
                        print_dec_g('error')
    
    print_dec_g('ATOMS COMPLETED !!!')
    ####-----------------------####
    ####-----------------------####
    
    if atomstyle == 'Full' or atomstyle == 'Angle':
        print_dec_g('WRITING BONDS...')
        ####------BONDS------####
        _text_ +='\n%1s\n\n','Bonds'
        count2=zeros(n_bonds,1)

        for i in arange(1,n_bonds).reshape(-1):
            for j in arange(1,n_typebonds).reshape(-1):
                if ((strcmp(atom_inbond[atom1_bond[i]],atom_bondcoeffi[j]) == 1 and strcmp(atom_inbond[atom2_bond[i]],atom_bondcoeffj[j]) == 1) or (strcmp(atom_inbond[atom1_bond[i]],atom_bondcoeffj[j]) == 1 and strcmp(atom_inbond[atom2_bond[i]],atom_bondcoeffi[j]) == 1)):
                    _text_ +='\t\t%d\t %d\t %d\t %d\n',i,j,atom1_bond[i],atom2_bond[i]
                    count2[i]=i

                    if choice_param == 1:
                        param_bond1[j]=parametrization_bond1[i]

                        param_bond2[j]=parametrization_bond2[i]

                        param_bond3[j]=parametrization_bond3[i]

        if choice_solv == 1:
            countb=1

            for i in arange(n_atoms + 1,(dot((n_mol[end()] - 1),3) + n_atoms)).reshape(-1):
                for j in arange(1,n_typebonds).reshape(-1):
                    if ((strncmp(type_[i],atom_bondcoeffi[j],2) == 1 or (strncmp(type_[i],atom_bondcoeffj[j],2)) == 1) and n_mol[i] != n_mol[i - 1]):
                        _text_ +='\t\t%d\t %d\t %d\t %d\n',n_bonds + countb,j,i,i + 1
                        _text_ +='\t\t%d\t %d\t %d\t %d\n',n_bonds + countb + 1,j,i,i + 2
                        countb=countb + 2

        print_dec_g('BONDS COMPLETED !!!')
    
    if atomstyle == 'Full' or atomstyle == 'Angle':
        print_dec_g('WRITING ANGLES...')
        ####------ANGLES------#########
        count=zeros(n_angles,1)

        _text_ +='\n%1s\n\n','Angles'
        for i in arange(1,n_angles).reshape(-1):
            for j in arange(1,n_typeangles).reshape(-1):
                if ((strcmp(atom_inbond[atom1_angle[i]],atom_anglecoeffi[j]) == 1 and strcmp(atom_inbond[atom2_angle[i]],atom_anglecoeffj[j]) == 1 and strcmp(atom_inbond[atom3_angle[i]],atom_anglecoeffk[j]) == 1) or (strcmp(atom_inbond[atom1_angle[i]],atom_anglecoeffk[j]) == 1 and strcmp(atom_inbond[atom2_angle[i]],atom_anglecoeffj[j]) == 1 and strcmp(atom_inbond[atom3_angle[i]],atom_anglecoeffi[j]) == 1)):
                    _text_ +='\t\t%d\t %d\t %d\t %d\t %d\n',i,j,atom1_angle[i],atom2_angle[i],atom3_angle[i]
                    count[i]=i

                    FLAG=1

                    if choice_param == 1:
                        param_angle1[j]=parametrization_angle1[i]

                        param_angle2[j]=parametrization_angle2[i]

                        param_angle3[j]=parametrization_angle3[i]

                        param_angle4[j]=parametrization_angle4[i]

        if choice_solv == 1:
            counta=1

            for i in arange(n_atoms + 1,(dot((n_mol[end()] - 1),3) + n_atoms)).reshape(-1):
                for j in arange(1,n_typeangles).reshape(-1):
                    if ((strncmp(type_[i],atom_anglecoeffi[j],2) == 1 or (strncmp(type_[i],atom_anglecoeffj[j],2)) == 1 or (strncmp(type_[i],atom_anglecoeffk[j],2)) == 1) and n_mol[i] != n_mol[i - 1]):
                        _text_ +='\t\t%d\t %d\t %d\t %d\t %d\n',n_angles + counta,j,i + 1,i,i + 2
                        counta=counta + 1

    
    print_dec_g('ANGLES COMPLETED !!!')
    ####------DIHEDRAL------####
    if atomstyle == 'Full':
        print_dec_g('WRITING DIHEDRALS...')
        _text_ +='\n%1s\n\n','Dihedrals'
        for i in arange(1,n_dihedrals).reshape(-1):
            for j in arange(1,n_typedihedrals).reshape(-1):
                if ((strcmp(atom_inbond[atom1_dihedral[i]],atom_dihedralcoeffi[j]) == 1 and strcmp(atom_inbond[atom2_dihedral[i]],atom_dihedralcoeffj[j]) == 1 and strcmp(atom_inbond[atom3_dihedral[i]],atom_dihedralcoeffk[j]) == 1 and strcmp(atom_inbond[atom4_dihedral[i]],atom_dihedralcoeffl[j]) == 1)):
                    _text_ +='\t\t%d\t %d\t %d\t %d\t %d\t %d\n',i,j,atom1_dihedral[i],atom2_dihedral[i],atom3_dihedral[i],atom4_dihedral[i]
                    if choice_param == 1:
                        param_dihedral1[j]=parametrization_dihedral1[i]
                        param_dihedral2[j]=parametrization_dihedral2[i]
                        param_dihedral3[j]=parametrization_dihedral3[i]
                        param_dihedral4[j]=parametrization_dihedral4[i]
    
    print_dec_g('DIHEDRALS COMPLETED !!!')
    
    return (param_bond1,param_bond2,param_angle1,param_angle2,param_dihedral1,
            param_dihedral2,param_dihedral3,param_dihedral4)

if __name__ == '__main__':
    pass
    
    
