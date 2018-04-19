#!/usr/bin/python
#    Ported to Python and barely optimized by Hernan Chavez Thielemann

__merged_files__ = ['main.m', 'Reading_top.m', 'Reading_bon.m',
                    'Reading_nb.m','Counting_lines.m', 'Reading_xyz.m']



from lib.misc.warn import wrg_1, wrg_3
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
    data_container['defaults'] = ck_forcefield( filename_nb)
    
    buckorlj = int(data_container['defaults'][0])
    
    _solvated_f_, _paramfi_f_= _ck_buttons_
    print 'Solvation: {} | Parametrization: {}\n'.format( *_ck_buttons_)
    #################################################
    '''-----------------  FILE NB  ---------------'''
    #===============================================#
    startstrings = ['[ atomtypes ]', '[ nonbond_params ]']
    
    data_container['atomtypes'] = get_gro_line( filename_nb, startstrings)
    
    n_atomtypes = len( data_container['atomtypes'])
    debugger_file( 'atomtypes',data_container['atomtypes'])
    #################################################
    '''----------------  FILE BON  ---------------'''
    #===============================================#
    filename_bon = _data_files_[4]
    
    startstrings=['[ bondtypes ]', '[ angletypes ]', '[ dihedraltypes ]', '']
    
    for bi in range(len(startstrings))[:-1]:
        _char_str_ = startstrings[bi][ 2:-2]
        
        data_container[_char_str_]= get_gro_line( filename_bon
                                                 ,startstrings
                                                 ,bi)
        debugger_file(_char_str_, data_container[_char_str_])
        
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
        data_container[_char_str_]= get_gro_line( filename_top
                                                 ,startstrings
                                                 ,ti)
        
        debugger_file( _char_str_, data_container[_char_str_])
            
    n_atoms = len(data_container['atoms'])
    n_bonds = len(data_container['bonds'])
    n_angles = len(data_container['angles'])
    n_dihedrals = len(data_container['dihedrals'])
    
    #################################################
    '''----------------  FILE GRO  ---------------'''
    #===============================================#
    filename_gro = _data_files_[0]
    sttd_anum, _mol_, _type_, _xyz_, b_xyzhi= get_gro_fixed_line( filename_gro)
    
    data_container['atomsdata'] = [_mol_, _type_, _xyz_]
    
    if sttd_anum<>len(_type_):
        exit('Error! -- Atom number mismatch in .gro file --')
    
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
        n_atomsnew = sttd_anum
    else:
        n_bondsnew = n_bonds[:]
        n_anglesnew = n_angles[:]
        indexoxy = 0
        indexhyd = 0
        #indexsod=0;
        n_atomsnew = n_atoms
        
    data_container['numbers']={}
    data_container['numbers']['total'] = [n_atomsnew, n_bondsnew,
                                          n_anglesnew, n_dihedrals]
    data_container['numbers']['type'] = [n_atomtypes, n_bondstypes,
                                         n_anglestypes, n_dihedraltypes]
    
    
    return data_container

def get_gro_fixed_line(_filename_):
    ''' reading gromacs gro fixed lines'''
    _content_ = []
    _mol_=[]
    _type_=[]
    _xyz_=[]
    with open(_filename_, 'r')  as indata:
        read_flag = False
        at=0
        at_num = 0
        for j_line in indata:
            if read_flag:
                _mol_.append( j_line[:5])
                _type_.append(j_line[12:15].lstrip(' '))
                _xyz_.append([j_line[20:28], j_line[28:36], j_line[36:44]])
                
                at+=1
                if at == at_num:
                    read_flag = False
                
            elif j_line.startswith(';'):
                pass
            elif at_num==0:
                j_line = indata.next()
                at_num = int(j_line)
                read_flag = True
            elif at == at_num:
                box_xyz_hi = [float(x) for x in j_line.split(';')[0].split()]
                
    return at_num, _mol_, _type_, _xyz_, box_xyz_hi

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
                
    return content_line

def ck_forcefield(_nonb_file_):
    '''
    podria pedirse solo este archivo y 
    de aqui sacar la iformacion de los otros dos'''
    
    _ff_file_ = '/'.join(_nonb_file_.split('/')[:-1])+'/forcefield.itp'
    comb_rule = -1
    if check_file(_ff_file_):
            with open(_ff_file_, 'r')  as indata:
                for j_line in indata:
                    line_c = j_line.split()
                    if len(line_c)>1 and 'fudgeQQ'==line_c[-1]:
                        j_line = indata.next()
                        comb_rule= j_line.split()
                        print('---> comb_rule {}'.format(comb_rule[1]))
                        return comb_rule
    elif comb_rule<0:
        exit('forcefield.itp file is missing or incomplete')

        
        
        
if __name__ == '__main__':
    
    pass
    
