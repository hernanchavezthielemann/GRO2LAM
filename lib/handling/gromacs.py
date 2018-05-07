#!/usr/bin/python
#    Ported to Python and barely optimized by Hernan Chavez Thielemann

__merged_files__ = ['main.m', 'Reading_top.m', 'Reading_bon.m',
                    'Reading_nb.m','Counting_lines.m', 'Reading_xyz.m']



from lib.misc.warn import wrg_1, wrg_3, pop_err_1, pop_wrg_1
from lib.misc.file import check_file, write_list2file, debugger_file
from sys import exit

#%% DATABASE
''' this "data base" seems not used at all'''
#=================================================
#%%%%-------------------BOND---------------%%%%%%%
# database of bond potentials type
BondDataBase=['harmonic','G96','morse','cubic','connection','harmonic',
		  'fene','tabulated','tabulated','restraint'] 
#%%%%-------------------ANGLE--------------%%%%%%%
# database of angle potentials type
AngleDataBase=['harmonic','G96','cross bond-bond','cross bond-angle',
		   'charmm','quartic angle','','tabulated'] 
#%%%%-------------------DIHEDRALS----------%%%%%%%
# database of dihedral potential types, %Fourier is called opls
DihedralDataBase=['charmm','improper','Ryckaert-Bellemans','periodic',
		      'opls','tabulated','charmm'] 
#%% END DATABASE

def extract_gromacs_data( _data_files_, _water_names_, _ck_buttons_):
    
    ''' data files['gro file', 'top file', 'non bonded file', 'bonded file']'''
    data_container = {}
    
    filename_nb = _data_files_[3]
    #filename_ff = '/'.join(filename_nb.split('/')[:-1])+'/forcefield.itp'
    filename_ff = _data_files_[2]
    print filename_ff
    data_container['defaults'], ok_flag = ck_forcefield( filename_ff)
    if not ok_flag:
        return {}, ok_flag
    
    
    
    buckorlj = int(data_container['defaults'][0])
    
    _solvated_f_, _paramfi_f_= _ck_buttons_
    print 'Solvation: {} | Parametrization: {}\n'.format( *_ck_buttons_)
    #################################################
    '''-----------------  FILE NB  ---------------'''
    #===============================================#
    startstrings = ['[ atomtypes ]', '[ nonbond_params ]']
    
    data_container['atomtypes'], ok_flag = get_gro_line( filename_nb, startstrings)
    if not ok_flag:
        return {}, ok_flag
    
    n_atomtypes = len( data_container['atomtypes'])
    
    #debugger_file( 'atomtypes',data_container['atomtypes'])
    #################################################
    '''----------------  FILE BON  ---------------'''
    #===============================================#
    filename_bon = _data_files_[4]
    
    startstrings=['[ bondtypes ]', '[ angletypes ]', '[ dihedraltypes ]', '']
    
    for bi in range(len(startstrings))[:-1]:
        _char_str_ = startstrings[bi][ 2:-2]
        
        data_container[_char_str_], ok_flag = get_gro_line( filename_bon
                                                           ,startstrings
                                                           ,bi)
        #debugger_file(_char_str_, data_container[_char_str_])
        if not ok_flag:
            return {}, ok_flag
        
    n_bondstypes = len(data_container['bondtypes'])
    n_anglestypes = len(data_container['angletypes'])
    n_dihedraltypes = len(data_container['dihedraltypes'])
    
    
    #################################################
    '''----------------  FILE TOP  ---------------'''
    #===============================================#
    filename_top = _data_files_[1]
    
    startstrings=['[ moleculetype ]', '[ atoms ]','[ bonds ]', '[ pairs ]',
                  '[ angles ]', '[ dihedrals ]', '[ system ]',
                  '[ molecules ]', '']
    
    for ti in range(len(startstrings))[:-1]:
        _char_str_ = startstrings[ti][ 2:-2]
        ''' here is possible to insert a selector in case pairs and 
        others can be ovbiated'''
        data_container[_char_str_], ok_flag = get_gro_line( filename_top
                                                           ,startstrings
                                                           ,ti)
        if not ok_flag:
            return {}, ok_flag
        
        #debugger_file( _char_str_, data_container[_char_str_])
            
    n_atoms = len(data_container['atoms'])
    n_bonds = len(data_container['bonds'])
    n_angles = len(data_container['angles'])
    n_dihedrals = len(data_container['dihedrals'])
    
    #################################################
    '''----------------  FILE GRO  ---------------'''
    #===============================================#
    filename_gro = _data_files_[0]
    ok_flag, gro_pack, b_xyzhi = get_gro_fixed_line( filename_gro)
    if not ok_flag:
        return {}, ok_flag
    
    _mol_, _mtype_, _type_, _xyz_ = gro_pack
    data_container['atomsdata'] = [_mol_, _mtype_, _type_, _xyz_]
    
    
    #################    BOX DEF   ##################
    xlo = 0
    xhi = b_xyzhi[0]*10
    ylo = 0
    yhi = b_xyzhi[1]*10
    zlo = 0
    zhi = b_xyzhi[2]*10   
    data_container['box']=[xlo,xhi, ylo,yhi, zlo,zhi]
    
    
    #################################################
    '''--------------   Solvation   --------------'''
    #===============================================#
    if _solvated_f_:
        n_molwater=0
        _aux_m_ = data_container['molecules']
        for i in range(len(_aux_m_)) :
            if _aux_m_[i][0]=='SOL':
                n_molwater = int(_aux_m_[i][1])
                break
        
        n_bondsnew = n_bonds + 2*n_molwater
        n_anglesnew = n_angles + n_molwater
        
        _ch_H_ = float(_water_names_[4])
        _ch_O_= float(_water_names_[4])*-2
        _charge_ = {_water_names_[0]: _ch_O_, _water_names_[1]: _ch_H_}
        
        oxy_gf = _water_names_[2].split(',')
        hyd_gf = _water_names_[3].split(',')
        _conv_dict_= {}
        for Ox in oxy_gf:
            _conv_dict_[Ox.strip(' ')] = _water_names_[0]
            #_charge_[Ox] = _ch_O_
        for Hy in hyd_gf:
            _conv_dict_[Hy.strip(' ')] = _water_names_[1]
            #_charge_[Hy] = _ch_H_
            
        data_container['S_charge'] =_charge_
        data_container['S_translation'] =_conv_dict_
        
        #oxy = _water_names_[2]
        #hyd = _water_names_[3]
        
        #if len(_water_names_)>4:#===--------------------  <WFS>
        #    sod =_water_names_[4]
        #    if len(_water_names_)>5:
        #        clo =_water_names_[5]
        # as the indexes themselves are not needed the next lines conversion 
        # were avoided 
        #indexchangeoxy =  find(strncmp(type_,oxy,2) == 1)
        #indexchangeoxy = [ i for i in range(len(_type_))
        #                       if _type_[i][:2]==oxy[:2]]
        # there is no need to store this indexes so:
        
        #for i in range( len( _type_)):
        #    if _type_[i][:2]==oxy[:2]:
        #        _type_[i]= _water_names_[0]
        #    elif _type_[i][:2]==hyd[:2]:
        #        _type_[i]= _water_names_[1]
        
        #indexoxy = [ i for i in range(len(_type_)) if _type_[i][:2]==oxy[:2]]
        #indexhyd = [ i for i in range(len(_type_)) if _type_[i][:2]==oxy[:2]]
        
        #indexoxy = find(strcmp(atom_inbondtype,_water_names_[1]) == 1)
        #indexhyd = find(strcmp(atom_inbondtype,_water_names_[2]) == 1)
        n_atomsnew = len(_type_)
    else:
        n_bondsnew = n_bonds
        n_anglesnew = n_angles
        indexoxy = 0
        indexhyd = 0
        #indexsod=0;
        n_atomsnew = n_atoms
        
    data_container['numbers']={}
    data_container['numbers']['total'] = [n_atomsnew, n_bondsnew,
                                          n_anglesnew, n_dihedrals]
    data_container['numbers']['type'] = [n_atomtypes, n_bondstypes,
                                         n_anglestypes, n_dihedraltypes]
    

    return data_container, ok_flag

def get_gro_fixed_line(_filename_):
    ''' reading gromacs gro fixed lines'''
    _content_ = []
    _mol_=[]
    #_mtype_=[]
    g_names =[]
    _type_=[]
    _xyz_=[]
    _corrupt = True
    with open(_filename_, 'r')  as indata:
        read_flag = False
        at=0
        at_num = 0
        
        _buffer = []
        for j_line in indata:
            if read_flag:
                at+=1
                
                mtype = j_line[5:10].strip(' ')
                
                _mol_.append( j_line[:5].lstrip(' '))
                #_mtype_.append(mtype)
                _type_.append(j_line[10:15].lstrip(' '))
                _xyz_.append([j_line[20:28], j_line[28:36], j_line[36:44]])
                
                if _buffer==[]:
                    _buffer = [ mtype, at]
                    
                elif mtype<>_buffer[0]:
                    
                    _buffer += [at-1]
                    g_names.append(_buffer)
                    _buffer = [ mtype, at]
                
                
                if at == at_num:
                    read_flag = False
                    g_names.append(_buffer+ [at])
                    
            elif j_line.startswith(';'):
                pass
            elif at_num==0:
                j_line = indata.next()
                at_num = int(j_line)
                read_flag = True
            elif at == at_num:
                _corrupt = False
                box_xyz_hi = [float(x) for x in j_line.split(';')[0].split()]
                
                
    if at_num<>len(_type_):
        pop_err_1('Atom number mismatch in .gro file')
        return False, 0 ,0
    elif _corrupt:
        pop_err_1('Corrupt .gro file')
        return False, 0,0
    else:
        return  True, [_mol_, g_names, _type_, _xyz_], box_xyz_hi

def top_groups(mtype, _buffer, g_names):
    
    return _buffer, g_names # hook

def get_gro_line(_filename_, _startstrings_, _i_=0):
    ''' reading gromacs content lines'''
    content_line = []
    _ss_=_startstrings_
    # \* TODO: aply a metod just in case that
    #       some _startstrings_ are not there
    with open(_filename_, 'r')  as indata:
        read_flag = False
        #print _i_, _ss_[_i_], _ss_[_i_+1]
        for j_line in indata:
            if j_line.startswith(';'):
                pass
            if j_line.startswith('#include'):
                print wrg_3(j_line.rstrip('\n')+' not included in this line\n')
            elif read_flag:
                _line_ = j_line.split(';')[0].split()
                
                if _ss_[_i_+1]<>'' and j_line.startswith( _ss_[_i_+1]):
                    #print _ss_[_i_+1] + ' -exit-'
                    break
                elif len(_line_)>=2:
                    #if _i_==7: print _line_
                    content_line.append( _line_)
            
            elif j_line.startswith( _ss_[_i_]):
                #print _ss_[_i_]
                read_flag = True
                
    if content_line == [] or not read_flag:
        if '/' in _filename_:
            _filename_ = _filename_.split('/')[-1]
        pop_err_1('The {} section is missing on {} file'.format(_ss_[_i_] ,
                                                                _filename_)
                 )
        return 0, read_flag
    else:
        return content_line, read_flag

def ck_forcefield(_ff_file_):
    '''
    podria pedirse solo este archivo y 
    de aqui sacar la iformacion de los otros dos....
    '''
    _flag_ = False
    comb_rule = -1
    with open(_ff_file_, 'r')  as indata:
        for j_line in indata:
            line_c = j_line.split()
            if j_line.startswith('[ defaults ]'):
                _flag_ = True
            if len(line_c)>1 and 'fudgeQQ'==line_c[-1]:
                j_line = indata.next()
                comb_rule= j_line.split()
                print('---> comb_rule {}'.format(comb_rule[1]))
                
            
    if comb_rule<0 or not _flag_:
        pop_err_1('forcefield.itp file is missing or incomplete')
        return 0, _flag_
    else:
        return comb_rule, _flag_

def get_top_groups(_mtype_container_, _group_):
    
    _mtype_ = _mtype_container_
    _buffer = []
    for mt in range(len( _mtype_)):
        
        mtype = _mtype_[mt].strip(' ')
        if _buffer==[] and mtype==_group_:
            buffer = [ mtype, mt+1]
            
        elif _buffer<>[] and mtype<>_group_:
            _buffer += [mt]
            break
            
        elif mt==(len(_mtype_)-1):
            
            _buffer += [mt+1]
                
    print''
    print 'Group characterized as: {} with ids {} to {}'.format(*_buffer)
    return _buffer


if __name__ == '__main__':
    
    pass
    
