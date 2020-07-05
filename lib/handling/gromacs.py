#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'


from lib.misc.warn import wrg_1, wrg_3, pop_err_1, pop_wrg_1
from lib.misc.file import check_file, debugger_file, fileseeker
from lib.misc.geometry import rotate, arcos, raiz
from lib.misc.data import isnot_num
from sys import exit


def extract_gromacs_data( _data_files_, _autoload_):
    
    ''' data files ---> ['gro file', 'top file', 'forcefield',
        'non bonded file', 'bonded file']'''
    # _water_names_
    filename_gro    =   _data_files_[0]
    filename_top    =   _data_files_[1]
    filename_ff     =   _data_files_[2]
    filename_nb     =   _data_files_[3]
    filename_bon    =   _data_files_[4]
    
    data_container  =   {}
    data_container['define'] = {}
    #_solvated_f_, _autoload_= _ck_buttons_
    print 'Autoload: {}\n'.format( _autoload_)
    
    if not _autoload_:
        print filename_ff # or not
        
    _sidemol_f_ = False
    
    ###########################################################################
    ###########################################################################
    section = '''---------------    FILE GRO      ----------------------'''
    #=========================================================================#
    
    ok_flag, gro_pack, b_xyz = get_gro_fixed_line( filename_gro)
    if not ok_flag:
        pop_err_1('Problem detected in :\n' + section)
        return {}, [ ok_flag, _sidemol_f_]
    
    _mol_, _mtype_, _type_, _xyz_, _mtypes_ = gro_pack
    
    
    ################# ------------   BOX DEF   ------------- ##################
    data_container['box'] = [[],[]]
    b_xyz = [ x_y_z*10 for x_y_z in b_xyz ]
    angles = []
    Ar = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        Ar[i][i] = b_xyz[i]
            
    if sum( b_xyz) < 2.8:
        exit('xx/0 Error in .gro file, box dimension 000')
            
    elif len( b_xyz) == 3:
        pass
    
    elif len( b_xyz) == 9:
        
        k = 0
        for i in range(3):
            for j in range(3):
                if i != j:
                    Ar[i][j] = b_xyz[ k + 3]
                    k += 1
                    
        cero = 1e-12
        if Ar[1][0] < cero or Ar[2][0] < cero or Ar[2][1] < cero:
            print('Your triclinic cell will be rotated to make it!')
            # y rotation
            a_tor_y = -arcos( (Ar[0][0])/(raiz(Ar[0][0]*Ar[0][0]+Ar[2][0]*Ar[2][0])) )
            Ar = rotate( Ar, a_tor_y, 'y')
            # z rotation
            a_tor_z = arcos( (Ar[0][0])/(raiz(Ar[0][0]*Ar[0][0]+Ar[1][0]*Ar[1][0])) )
            Ar = rotate( Ar, a_tor_z, 'z')
            
            a_tor_x = arcos( Ar[1][1]/( raiz( Ar[1][1]*Ar[1][1] + Ar[2][1]*Ar[2][1])) )
            Ar = rotate( Ar, a_tor_x)
            
            _xyz_ = rotate( rotate( rotate( _xyz_, a_tor_y, 'y'),
                                        a_tor_z, 'z'), a_tor_x)
        
    else:
        exit('xx/0 Error box dimension 001')
        
    _x_, _y_, _z_ = _xyz_
    xlo = min( _x_)*10
    xhi = xlo + Ar[0][0]
    ylo = min( _y_)*10
    yhi = ylo + Ar[1][1]
    zlo = min( _z_)*10
    zhi = zlo + Ar[2][2]
    
    data_container['box'][0] = [ xlo, xhi, ylo, yhi, zlo, zhi]
    data_container['box'][1] = [ Ar[0][1], Ar[0][2], Ar[1][2]]
    data_container['atomsdata'] = [ _mol_, _mtypes_, _type_, _xyz_, _mtype_]
    ###########################################################################
    
    ###########################################################################
    ###########################################################################
    section = '''----------------  .FILE TOP.  ---------------'''
    #=========================================================================#
    
    #################   Defaults   ##################
    
    data_container['defaults'], ok_flag, _a_fff_ = ck_forcefield( filename_ff,
                                                                  filename_top)
    filename_ff = _a_fff_
    
    if not ok_flag:
        pop_err_1('Problem detected in :\n' + section.split('.')[1])
        return {}, [ ok_flag, _sidemol_f_]
    
    buckorlj = int(data_container['defaults'][0])
    
    ############
    startstrings = ['[ moleculetype ]', '[ atoms ]', '[ bonds ]', '[ pairs ]',
                    '[ angles ]', '[ dihedrals ]', '[ system ]',
                    '[ molecules ]', '']
    exclusions_ = ['[ bonds ]', '[ pairs ]', '[ angles ]', '[ dihedrals ]']
    # Scheme type????
    pure_side_mol_flag = ( ( seek_for_directive( [ filename_top],
                                                'moleculetype') == '') or 
                           ( filename_nb == filename_ff and
                             filename_nb == filename_bon))
    
    if pure_side_mol_flag:
        startstrings = startstrings[-3:]
        print wrg_3( 'Using pure side molecule scheme')
        #n_atoms     =   0
        #n_bonds     =   0
        #n_angles    =   0
        data_container['atoms']     =   []
        data_container['bonds']     =   []
        data_container['angles']    =   []
        data_container['dihedrals']     =   []
        
    for ti in range(len(startstrings))[:-1]:
        s_str_ = startstrings[ ti][ 2:-2]
        ''' here is possible to insert a selector in case pairs and 
        others can be obviated'''
        data_container[ s_str_], ok_flag, _ = get_topitp_line( filename_top,
                                                               startstrings[ti]
                                                             )
        
        if not ok_flag:
            
            if startstrings[ti] not in exclusions_:
                print wrg_3( 'Not ok flag in <extract_gromacs_data> top file' +
                         'section, in ' + s_str_)
                return {}, [ ok_flag, _sidemol_f_]
            else:
                ok_flag = True
        #debugger_file( s_str_, data_container[s_str_])
    
    n_atoms     =   len( data_container['atoms'])
    n_bonds     =   len( data_container['bonds'])
    n_angles    =   len( data_container['angles'])
    
    ###########################################################################
    section = '''----------  .SIDE MOLE FILES.   -------------'''
    #=========================================================================#
    #### re-search in topology for new molecules / side molecules
    if _autoload_:
        data_container, ok_flag, _sidemol_f_ = sidemol_data( filename_top,
                                                            data_container)
    if not ok_flag:
        pop_err_1( 'Problem detected in :\n' + section.split('.')[1])
        return {}, [ ok_flag, _sidemol_f_]
    
    
    ###########################################################################
    section = '''-----------------  .FILE NB.  ---------------'''
    #=========================================================================#
    startstrings = ['[ atomtypes ]', '[ nonbond_params ]']
    
    data_container['atomtypes'], ok_flag, _ = get_topitp_line( filename_nb,
                                                               '[ atomtypes ]')
    if not ok_flag:
        pop_err_1('Problem detected in :\n' + section.split('.')[1])
        return {}, [ ok_flag, _sidemol_f_]
    
    n_atomtypes     =   len( data_container['atomtypes'])
    
    #debugger_file( 'atomtypes',data_container['atomtypes'])
    ###########################################################################
    section = '''----------------  .FILE BON.  ---------------'''
    #=========================================================================#
    
    
    startstrings = ['[ bondtypes ]', '[ angletypes ]', '[ dihedraltypes ]', '']
    if filename_nb == filename_ff and filename_nb == filename_bon:
        
        for bi in range( len( startstrings))[:-1]:
            s_str_ = startstrings[ bi][ 2:-2]
            data_container[ s_str_] =   []
            data_container['define'][s_str_[:-5]] = {}
            
        #data_container['impropers']     =   []
        #data_container['impropertypes'] =   []
        startstrings = startstrings[-1]
    
    aux_strings = [ 'bonds', 'angles', 'dihedrals']
    for bi in range( len( startstrings))[:-1]:
        s_str_ = startstrings[ bi][ 2:-2]
        
        _aux_here_ = get_topitp_line( filename_bon, startstrings[ bi])
        data_container[ s_str_], ok_flag, _data_define_ = _aux_here_
        
        
        ################################################################################### flag
        # Make a function like dihedral integrity check
        if bi == 2:
            for di in range( len(data_container[ s_str_])):
                # isnot_num return true if is string
                dih_pt_line = data_container[ s_str_][di]
                if not isnot_num( dih_pt_line[2]):
                    pop_wrg_1(   'Dihedral potential problem found!!\nAdopting'
                               + ' X-A1-A2-X configuration for: '
                               + ' {}-{}'.format( *dih_pt_line[:2]) ) 
                    new_row = ['X'] + dih_pt_line[:2] + ['X'] + dih_pt_line[2:]
                    data_container[ s_str_][di] = new_row
                    
                elif not isnot_num( dih_pt_line[3]):
                    exit('Error 0031 undefined dihedral')
        
        data_container['define'][s_str_[:-5]] = _data_define_
        #debugger_file(s_str_, data_container[s_str_])
        
        if not ok_flag:
            
            if data_container[ aux_strings[ bi]] != []:
                pop_err_1('Problem detected in :\n' + section.split('.')[1])
                return {}, [ ok_flag, _sidemol_f_]
            else:
                ok_flag = True
    
    ###########################################################################
    section = '''------------     .#define & Impropers.       ------------'''
    #=========================================================================#
    gromosff_flag = False
    data_container[ 'define'][ 'improper'] = {}
    aux_here = {}
    print( section.split('.')[1])
    if filename_nb != filename_ff and filename_nb != filename_bon:
        print(" Is it GROMOS there ?? ")
        aux_here = get_gromos_define( filename_bon)
        
    else:
        print('no gromos check')
        
    for key_ in aux_here.keys():
        if aux_here[ key_] != {}:
            print ( 'GROMOS ' + key_ + ' kind detected!')
            data_container[ 'define'][ key_].update( aux_here[ key_])
            gromosff_flag = True
            
            dihe_g_data = data_container[ 'dihedraltypes']
            if 'dihedraltypes' == key_+'types' and dihe_g_data != []:
                rewrite_flag = False
                for gd_ in range( len( dihe_g_data)):
                    #print dihe_g_data[gd_][2]
                    if dihe_g_data[gd_][2].isdigit():
                        if not rewrite_flag:
                            print('Dihedral with 2 atoms re-formating to 4: ')
                        rewrite_flag = True
                        dihe_g_data[gd_] = ( [ 'X',] + dihe_g_data[ gd_][:2]
                                            + [ 'X',] + dihe_g_data[ gd_][2:])
                        print (dihe_g_data[ gd_]) 
                if rewrite_flag:
                    data_container[ 'dihedraltypes'] = dihe_g_data
                
            
        
    if gromosff_flag:
        for ss_ in startstrings[:-1]:
            s_str_ = ss_[ 2:-2]
            data_aux = data_container[ s_str_]
            cont_k = s_str_[ :-5]
            cddd = data_container[ 'define'][ cont_k]
            for i in range( len( data_aux)):
                if len( data_aux[i][-1].split('.')) < 2:
                    if  not data_aux[i][-1].isdigit():
                        aux = data_aux[i][:-1] + cddd[ data_aux[i][-1]]
                        #print aux
                        data_container[ s_str_][i] = aux
                    
    
    
        #print data_container['define']['bond']['gb_33']
    # Search for impropers in TOP and BON, using crossreference if needed
    data_container = split_define_dihe_impr( data_container)
    
    n_dihedrals     =   len( data_container['dihedrals'])
    n_impropers     =   len( data_container['impropers'])
    
    ###########################################################################
    '''--------------              "Side Mol"                 --------------'''
    #=========================================================================#
    n_atomsnew = len( _type_)
    
    if _sidemol_f_:
        
        ###   A_02 maths
        # "previewing / preallocating" // computing side mol size 
        sidemol = data_container['sidemol']
        side_bonds_n    = 0
        side_angles_n   = 0
        side_dihed_n    = 0
        side_improp_n   = 0
        
        for sb in range( len( sidemol['tag'])):
            bonds_x_mol = len( sidemol['data'][sb]['bonds'])
            angles_x_mol = len( sidemol['data'][sb]['angles'])
            dihedr_x_mol = len( sidemol['data'][sb]['dihedrals'])
            improp_x_mol = len( sidemol['data'][sb]['impropers'])
            
            sm_quantity = sidemol['num'][sb]
            #print(sm_quantity, bonds_x_mol,sm_quantity * bonds_x_mol)
            side_bonds_n    += sm_quantity * bonds_x_mol
            side_angles_n   += sm_quantity * angles_x_mol
            side_dihed_n    += sm_quantity * dihedr_x_mol
            side_improp_n   += sm_quantity * improp_x_mol
        
        n_bondsnew  =   n_bonds + side_bonds_n
        n_anglesnew =   n_angles + side_angles_n
        n_dihednew  =   n_dihedrals + side_dihed_n
        n_impropnew =   n_impropers + side_improp_n
        #print n_bonds, side_bonds_n, n_bonds + side_bonds_n
        #print n_angles, side_angles_n, n_angles + side_angles_n
        
        ###   A_03
        # tester in case is an asigment for define ore something like that
        contentkey = [ 'bond', 'angle', 'improper', 'dihedral']
        for cont_k in contentkey:
            # memorandum:
            # 'define' stores in a contentkey dictionary each define key:value
            cddd = data_container[ 'define'][ cont_k]
            if cddd.keys() != []:
                for sb in range( len( sidemol['tag'])): # in each side mol
                    datacont = sidemol['data'][sb][cont_k+'s']# in its cont-key
                    for dc in range( len( datacont)):# lets look their content
                        if isnot_num( datacont[dc][-1]):#
                            #print( '{} {} {}'.format( cont_k+'s', dc,
                            #                         datacont[dc][-1])) 
                            aux = datacont[dc][:-1] + cddd[ datacont[dc][-1]]
                            sidemol['data'][sb][cont_k+'s'][dc] = aux
                        #else:
                            #print datacont[dc]
        
        #######################################################################
        ###   A_04
        # I think that this part is deprecated... however I am not sure
        # Regarding the itp format:
        #   charges index 6 in data-atoms
        #   opls names in index 1
        #   atom tags in index 4
        _charge_ = {}
        _conv_dict_ = {}
        
        for sb in range( len( sidemol['tag'])):
            for at in range( len( sidemol['data'][sb]['atoms'])):
                a_opls_tag = sidemol['data'][sb]['atoms'][at][1]
                a_elem_tag = sidemol['data'][sb]['atoms'][at][4]
                a_charge = float( sidemol['data'][sb]['atoms'][at][6])
                _charge_[a_opls_tag] = a_charge
                _conv_dict_[ a_elem_tag] = a_opls_tag
                
        print '='*45+'\n'+'='*5+'  Charges found: '
        print _charge_
        print _conv_dict_
        
        data_container['S_charge'] = _charge_
        data_container['S_translation'] = _conv_dict_
        
        #######################################################################
        ###   A_05
        ############               Esoteric part ;)             ###############
        ####    ----------- DEFINING BONDED INTERACTIONS     ----------    ####
        # load the side molecules data if exist
        #sidemol = _topodata_['sidemol']
        smol_extra_bondtypes        =   []
        smol_extra_angletypes       =   []
        smol_extra_dihedraltypes    =   []
        smol_extra_impropertypes    =   []
        
        bn_namelist = []
        an_namelist = []
        di_namelist = []
        im_namelist = []
        
        for sb in range( len( sidemol['tag'])):
            _smd_ = sidemol['data'][sb]
            
            _at_dic_here = {}
            for _at in range( len( _smd_['atoms'])):
                _smat_ = _smd_['atoms'][_at]
                _at_dic_here[ _smat_[0]] = _smat_[1]
                
            
            for _bn in range( len( _smd_['bonds'])):
                _smbn_ = _smd_['bonds'][_bn]
                aux_here = [_at_dic_here[ _smbn_[0]], _at_dic_here[ _smbn_[1]]]
                name = '{}-{}'.format(*aux_here)
                if name not in bn_namelist and len( _smbn_[2:]) > 1:
                    bn_namelist.append( name)
                    smol_extra_bondtypes.append( aux_here + _smbn_[2:])
                    
            for _an in range( len( _smd_['angles'])):
                _sman_ = _smd_['angles'][_an]
                aux_here = [_at_dic_here[ _sman_[0]], _at_dic_here[ _sman_[1]],
                            _at_dic_here[ _sman_[2]] ]
                name = '{}-{}-{}'.format(*aux_here)
                if name not in an_namelist and len( _sman_[3:]) > 1:
                    an_namelist.append( name)
                    smol_extra_angletypes.append( aux_here + _sman_[3:])
                    
            for _dh in range( len( _smd_['dihedrals'])):
                _smdh_ = _smd_['dihedrals'][_dh]
                aux_here = [_at_dic_here[ _smdh_[0]], _at_dic_here[ _smdh_[1]],
                            _at_dic_here[ _smdh_[2]], _at_dic_here[ _smdh_[3]]]
                name = '{}-{}-{}-{}'.format(*aux_here)
                if name not in di_namelist and len( _smdh_[4:]) > 1:
                    di_namelist.append( name)
                    smol_extra_dihedraltypes.append( aux_here + _smdh_[4:])
            
            for _im in range( len( _smd_['impropers'])):
                _smim_ = _smd_['impropers'][_im]
                aux_here = [_at_dic_here[ _smim_[0]], _at_dic_here[ _smim_[1]],
                            _at_dic_here[ _smim_[2]], _at_dic_here[ _smim_[3]]]
                name = '{}-{}-{}-{}'.format(*aux_here)
                if name not in im_namelist and len( _smim_[4:]) > 1:
                    im_namelist.append( name)
                    smol_extra_impropertypes.append( aux_here + _smim_[4:])
                
            if len( _smd_.keys()) > 5:
                print ('Uuupa!! This thing is not implemented yet' +
                       ' as side mol part')
                a_key = [ 'atoms', 'bonds', 'angles', 'dihedrals', 'impropers']
                for ky in _smd_.keys():
                    if ky not in a_key:
                        print ('-- > this key : ' + ky)
                
                
            # ---------   !!!!    Update the info    !!!!
        data_container['bondtypes'] = ( smol_extra_bondtypes +
                                       data_container['bondtypes'] )
        data_container['angletypes'] = ( smol_extra_angletypes + 
                                        data_container['angletypes'])
        data_container['dihedraltypes'] = ( smol_extra_dihedraltypes + 
                                        data_container['dihedraltypes'])
        data_container['impropertypes'] = ( smol_extra_impropertypes + 
                                        data_container['impropertypes'])
        #print(data_container['bondtypes'])
    else:
        n_bondsnew  = n_bonds
        n_anglesnew = n_angles
        n_atomsnew  = n_atoms
        n_dihednew  = n_dihedrals
        n_impropnew = n_impropers
    
    ###################### trabajo
    # marker: 'bond_kinds'angl_kinds'dihe_kinds'impr_kinds'
    nice_list = [ 'bondtypes', 'angletypes', 'dihedraltypes','impropertypes']
    
    for it in range( len( nice_list)):
        _aux_set_here = set()
        poss = it + 2
        if poss > 4:
            poss = 4
        for i in range( len ( data_container[ nice_list[it] ])):
            _aux_set_here.add( data_container[ nice_list[it] ][i][ poss ])
        #print( nice_list[it][:4])
        #print(_aux_set_here)
        data_container[ nice_list[it][:4]+'_kinds'] = _aux_set_here
    
    
    n_bondstypes    =   len( data_container['bondtypes'])
    n_anglestypes   =   len( data_container['angletypes'])
    n_dihedraltypes =   len( data_container['dihedraltypes'])
    n_impropertypes =   len( data_container['impropertypes'])
    
    data_container['numbers']={}
    data_container['numbers']['total'] = [n_atomsnew, n_bondsnew,
                                          n_anglesnew, n_dihednew, n_impropnew
                                         ]
    #print( 'here', data_container['numbers']['total'])
    #exit('')
    data_container['numbers']['type'] = [n_atomtypes, n_bondstypes,
                                         n_anglestypes, n_dihedraltypes,
                                         n_impropertypes]
    print 'Ending gromacs data parsing\n'
    return data_container, [ ok_flag, _sidemol_f_]

def sidemol_data( _file_top_, data_container):
    ''' -- getter of the side molecules data --
        Per each side mole returns a dictionary with:
            tag : side mole tag
            num : number in this instance of this kind of side mol
            data : dictionary with topology data
                {atoms bonds angles dihedrals impropers}
    '''
    
    sidemol = {'tag': [],'num':[], 'data':[] }# Tag # mol_number
    sm_flag = False
    # all molecules info
    _aux_m_ = data_container[ 'molecules']
    
    # names of non side molecules
    if 'moleculetype' in data_container.keys():
        non_sm = data_container['moleculetype']
        non_sm = [non_sm[i][0] for i in range(len(non_sm))]
        _buffer_ = ''
    else:
        # non conventional case // the one in the main top
        non_sm = ['']
        _buffer_ = '0'
        
    # side molecules info filtering
    for i in range( len( _aux_m_)) :
        if _aux_m_[i][0] not in non_sm:
            sidemol['tag'].append( _aux_m_[i][0])
            sidemol['num'].append( int(_aux_m_[i][1]))
            sm_flag = True
        
    
    if sm_flag:
        #////////======= Side molecule >>> file <<< search   ==========////////
        print ('\nLoading side molecule files: ' )
        _sm_files_ = []
        root_dir = '/'.join( _file_top_.split('/')[:-1]+[''])
        ok_flag = False
        with open( _file_top_, 'r')  as topdata:
            if sidemol['tag'] == []:
                topdata = []
            for k_line in topdata:
                if k_line.startswith('#'):
                    
                    logic_test = ('#if' not in _buffer_ and _buffer_ != '')
                    
                    if k_line.startswith('#include') and logic_test:
                        if _sm_files_ == []:
                            ok_flag = True
                        
                        try:
                            new_filename = k_line.split('"')[1].lstrip('.')
                        except IndexError:
                            auxt = wrg_1( 'Format error with {}')
                            print( auxt.format( k_line.split()[-1] ) ) 
                        
                        new_filename = new_filename.lstrip('/').split('/')[-1]
                        po_file = fileseeker( root_dir, new_filename)
                        if po_file != []:
                            _sm_files_.append( po_file[0])
                            print( 'SM_file : {}'.format(_sm_files_[-1]))
                            ok_flag *= check_file( po_file[0],
                                                  content='[ atoms ]')
                    else:
                        _buffer_ = k_line
        # do it in the same loop or not that is the thing... maybe is better
        # to not just beacause the indentation going to +inf atoms
        #////////======= Side molecule >>> data <<< search   ==========////////
        if ok_flag:
            for sm in sidemol['tag']:
                aux_data, aux_flag = sidemol_data_gatherer( _sm_files_, sm)
                #print aux_data
                ok_flag *= aux_flag
                sidemol['data'].append( aux_data)
                
        
        data_container['sidemol'] = sidemol
        
    else:
        print ('No side molecule files detected!' )
        ok_flag = True
        
    return data_container, ok_flag, sm_flag

def sidemol_data_gatherer( _sm_files_, _sm_):
    ''' collects all the data related with one kind of side molecule
        the data types are specified in startstrings
    '''
    print( '\nSearching for: {}'.format( _sm_ ))#, ' in: ' ,_sm_files_
    _flag_ = True
    _file_ = ''
    _sm_data_c_ = {}
    
    # is sm in sm_file?? in cases with more than one file
    for smfile in _sm_files_:
        with open( smfile, 'r')  as sm_data:
            read_flag = False
            i = 0
            for j_line in sm_data:
                j_line = j_line.split(';')[0].strip()
                
                #print j_line, read_flag, j_line.startswith(sm)
                
                if j_line.startswith('['):
                    if j_line.startswith('[ moleculetype ]'):
                        read_flag = True
                        i = 0
                    else:
                        read_flag = False
                        
                elif read_flag and j_line.startswith( _sm_):
                    _file_ = smfile
                    break
                elif read_flag:
                    i +=1
                    if i > 3:
                        read_flag = False
                
                        
    if _file_=='':
        pop_err_1('Error!! side molecule {} not found in itp -- '.format( _sm_))
        _flag_ = False
    else:
        print( 'Success!, found in : {}\n'.format( _file_))
        tag_str = [ 'atoms', 'bonds', 'angles', 'dihedrals','fin']
        _sm_data_c_ = { x:[] for x in tag_str if x != 'fin'}
        read_flag = False
        iner_flag = False
        cd_tag = ''
        i = 0
        with open( _file_, 'r')  as sm_data:
            
            for j_line0 in sm_data:
                j_line = j_line0.split(';')[0].split()
                if not j_line:
                    pass
                elif read_flag:
                    if j_line[0][0] == '#':
                        pass
                    elif j_line[0][0] == '[':
                        if  j_line[1]  != tag_str[i] :
                            if j_line[1] in tag_str[i+1:]:
                                i = tag_str.index( j_line[1])
                                cd_tag = tag_str[i]
                                iner_flag = True
                                print( '** Gathering {} data'.format( cd_tag))
                            elif j_line[1] == 'moleculetype':
                                break
                            else:
                                txt_s = '> {} not considered in {}'
                                print txt_s.format( j_line[1], _sm_)
                                iner_flag = False
                        else :
                            cd_tag = tag_str[i]
                            print( '* Gathering {} data'.format( cd_tag))
                            iner_flag = True
                            
                    elif iner_flag:
                        #print j_line
                        _sm_data_c_[ cd_tag].append( j_line)
                            
                            
                elif j_line0.lstrip().startswith( _sm_):
                    read_flag = True
                    
        # todo add a new check in case of empty container
        #print _sm_data_c_
        
        ######### Split impropers and dihedrals
        _sm_data_c_, _ = split_dihedral_improper( _sm_data_c_)
        
        #if _sm_data_c_['impropers'] <>[]:
        #    print _sm_data_c_['impropers']
        
    return _sm_data_c_, _flag_

def split_dihedral_improper( _data_container_):
    ''' New function to neat just the split
    
        Seems that in GROMACS, impropers are present as a kind of 
        dihedral type, so this function is meant to pick the dihedral
        data and split it resizing the original container and creating
        a new improper-container.
    '''
    ###              ////////////////////\\\\\\\\\\\\\\\\\\\\\              ###
    
    dh_dict_kind = {'1':"Proper dihedral", '2':"Improper dihedral",
                    '3':"Ryckaert-Bellemans dihedral",
                    '4':"Periodic improper dihedral", '5':"Fourier dihedral",
                    '8':"Tabulated dihedral", '9':"Proper dihedral (multiple)",
                    '10':"Restricted dihedral", '11':"Combined bending-torsion"}
    
    _dihedrals_data_ = _data_container_[ 'dihedrals']
    _admitted_dihe_ = ['1', '3', '9']#['1', '3', '9']
    _admitted_impr_ = ['2', '4']# ['2']
    
    im_data_ = []
    dh_data_ = []
    define_dihe_extra = []
    def_impr_extra = []
    dh_bf_err = ""
    
    for i in range( len ( _dihedrals_data_)):
        #  Dihedral line format in :
        #  ai  aj  ak  al  funct   c0  c1  c2  c3  c4  c5
        dihe_funct = _dihedrals_data_[i][4]
        
        if dihe_funct in _admitted_dihe_:
            dh_data_.append( _dihedrals_data_[i])
            if len (_dihedrals_data_[i])>5:
                define_dihe_extra.append( _dihedrals_data_[i])
            
        elif dihe_funct in _admitted_impr_:
            im_data_.append( _dihedrals_data_[i])
            if len (_dihedrals_data_[i])>5:
                def_impr_extra.append( _dihedrals_data_[i])
            
        else:
            print 'Problem #008 here #split_dihedral_improper'
            dihe_err = "#008_" + dh_dict_kind[ dihe_funct]
            
            if dihe_err != dh_bf_err:
                if dihe_funct in dh_dict_kind.keys():
                    pop_err_1( dh_dict_kind[ dihe_funct] + 
                              ' not implemented yet')
                    dh_bf_err = dihe_err
                else:
                    exit( dihe_funct + ' is not a valid dihedral function')
            
    
    # Save/overwriting point
    _data_container_['impropers'] = im_data_
    _data_container_['dihedrals'] = dh_data_
    
    return _data_container_, define_dihe_extra

def split_define_dihe_impr( _data_container_, smt_flag = False):
    ''' This picks the dihedral data and splits it 
        Creates #define data in dihedrals
        
        Also creates the data regarding kinds of functions. Useful when
        '1' and '3' are used in the same file
    '''
    
    ###              =========================================              ###
    ''' =============             Dihedral TOP data           ============= ''' 
    # Save/overwriting point
    _data_container_, define_dh_ex = split_dihedral_improper( _data_container_)
    _admitted_impr_ = ['2', '4']
    #====================================================
    ''' ======== "Type" Dihedral BONDED data  ======= '''
    _dihe_type_data_ = _data_container_['dihedraltypes']
    im_type_ = []
    dh_type_ = []
    #print _dihe_type_data_
    for i in range( len ( _dihe_type_data_)):
        #  Dihedral line format:
        #  ai  aj  ak  al  funct   c0  c1  c2  c3  c4  c5
        try:
            if _dihe_type_data_[i][4] in _admitted_impr_:
                im_type_.append( _dihe_type_data_[i])
            else:
                dh_type_.append( _dihe_type_data_[i])
        except IndexError as _err:
            print( _err)
            exit( _dihe_type_data_[i] )
    #====================================================
    ''' ========  Dihedral "#define" data  ========== ''' 
    def_dihe_dic = {}
    def_impr_dic = {}
    # If there are define potentials, I have to process... by types and kind
    '''    Make it homogeneous - New kind creations   '''
    # first_clause = ( maybe should be an inner clause
    '''     Now supposing that just #define exist with a tag in the c0
            position...'''
    new_dihedraltypes = {}
    define_dic = _data_container_['define']['dihedral']
    if define_dic != {}:
        
        known_atoms = _data_container_['atoms']
        for dh in range( len( define_dh_ex)):
            _dhi_ = define_dh_ex[ dh]
            
            a_tag = ['',]*4
            for at1 in range( 4): # at1 0 1 2 3
                atnum = int( _dhi_[at1])
                if ( known_atoms[ atnum - 1][0] == _dhi_[ at1]):
                    a_tag[at1] = known_atoms[ atnum - 1][1]
                # Si no esta ordenado nos vamos casi a la...
                else:
                    # Brute force, till should be found
                    for at2 in range( len( known_atoms)):
                        if known_atoms[at2][0] == _dhi_[at1]:
                            a_tag[at1] = known_atoms[at2][1]
                            break
                            
                if '' == a_tag[at1]:
                    _string_ = 'Error!! atom number {} not found in .top -- '
                    pop_err_1( _string_.format( atnum))
                    
            #### TODO Flag
            ## First case with coefs in the top file... c0  c1  c2  c3  c4  c5
            if len( _dhi_) > 6:
                print ('Coefficients in the top file are not supported yet' +
                        '... or maybe they are '+ u'\u00AC'*2)
                new_dihedraltypes['-'.join(a_tag)] = (a_tag + _dhi_[4:])
            
            ## Second case with #define
            elif len( _dhi_) == ( 4 + 1 + 1):
                dh_kind_, dihedral_tag = _dhi_[4:]
                _content_ = a_tag + [dh_kind_] + define_dic[ dihedral_tag]
                # with a dictionary instead a set because, sets do not allow
                # unhashable lists as items
                new_dihedraltypes[ '-'.join( a_tag)] = _content_
                
        for key in new_dihedraltypes.keys():
            dh_type_.append( new_dihedraltypes[key])
        
    
    # Save/overwriting point
    _data_container_['impropertypes'] = im_type_
    _data_container_['dihedraltypes'] = dh_type_
    
    return _data_container_

def get_gro_fixed_line( _filename_):
    ''' reading gromacs gro fixed lines'''
    _content_   =   []
    _mol_       =   []
    _mtype_     =   []
    g_names     =   []
    _type_      =   []
    _xyz_       =   []
    _x_         =   []
    _y_         =   []
    _z_         =   []
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
                _mtype_.append(mtype)
                _type_.append(j_line[10:15].lstrip(' '))
                _x_.append( float( j_line[20:28]) )
                _y_.append( float( j_line[28:36]) )
                _z_.append( float( j_line[36:44]) )
                
                if _buffer==[]:
                    _buffer = [ mtype, at]
                ## TODO : Analyze if it is possible to improve here using sets
                elif mtype != _buffer[0]:
                    
                    _buffer += [at-1]
                    g_names.append( _buffer)
                    _buffer = [ mtype, at]
                
                
                if at == at_num:
                    read_flag = False
                    g_names.append(_buffer + [at])
                    
            elif j_line.startswith(';'):
                pass
            elif at_num == 0:
                j_line = indata.next()
                at_num = int( j_line)
                read_flag = True
            elif at == at_num:
                box_xyz_hi = [float(x) for x in j_line.split(';')[0].split()]
                if len( box_xyz_hi) in [ 3, 9]:
                    _corrupt = False
                    
                
    if at_num != len(_type_):
        pop_err_1('Atom number mismatch in .gro file')
        return False, 0 ,0
    elif _corrupt:
        pop_err_1('Corrupt .gro file box definition')
        return False, 0,0
    else:
        _xyz_ = [ _x_, _y_, _z_]
        return  True, [_mol_, _mtype_, _type_, _xyz_, g_names], box_xyz_hi

def top_groups( mtype, _buffer, g_names):
    
    return _buffer, g_names # hook

def get_topitp_line( _filename_, _ss_):
    ''' reading gromacs content lines
        spliting by the space between info
    '''
    _verbose_ = True
    content_line = []
    _define_ = {}
    
    # \* TODO: apply a method just in case that
    #          some _startstrings_ are not there ??
    with open(_filename_, 'r')  as indata:
        read_flag = False
        ok_flag = True
        tag_not_found = True
        if _verbose_:
            print  _ss_
        for j_line in indata:
            # I just whant to read once the flag is on
            j_line_s0 = j_line.split(';')[0].split()
            if read_flag and j_line_s0:
                #if _verbose_: ### is beter to store and print outside the
                # cycle with just one if 
                #print j_line_s0
                _line_ = j_line_s0
                # getting out comments and empty lines
                if len( _line_) <0: 
                    pass
                    
                elif _line_[0][0] == '#':
                    if _line_[0] == '#include':
                        print( wrg_3( _line_[1] + ' skipped this time'))
                    elif _line_[0] == '#define':
                        _define_[_line_[1]] = _line_[2:]
                    else:
                        print wrg_3( str(_line_) + '  ??')
                        
                elif _line_[0][0] == '[':
                    print( ' '.join(_line_) + 'Checked!')
                    if  ' '.join(_line_) != _ss_ :
                        read_flag = False
                    #print 'exit here 424'
                    
                elif len( _line_) > 0:
                    content_line.append( _line_)
                else:
                    print('Ups... please raise an issue at GitHub ;)')
            elif j_line.lstrip().startswith( _ss_):
                if _verbose_:
                    print( _ss_+' found!')
                read_flag = True
                tag_not_found = False
    
    if content_line == [] or tag_not_found:
        if '/' in _filename_:
            _filename_ = _filename_.split('/')[-1]
        pop_err_1( 'The {} section is missing on {} file'.format( _ss_ ,
                                                                  _filename_)
                 )
        ok_flag = False
    return content_line, ok_flag, _define_

def get_gromos_define( _bondedfile_):
    ''' reading GROMOS define forcefield format
        gb_ : bond
        ga_ : angle
        gi_ : wop - improper
        gd_ : dihedral
        eg. #define gb_12
    '''
    _dedic_ = {'b':'bond', 'a':'angle', 'i':'improper', 'd':'dihedral'}
    _define_ = {}
    for k in _dedic_.keys():
        _define_[ _dedic_[k]] = {}
    
    with open(_bondedfile_, 'r')  as indata:
        for j_line in indata:
            _line_ = j_line.split(';')[0].split()
            if _line_ and _line_[0][0] == '#':
                if _line_[0] == '#define':
                    if _line_[1][0] == 'g':
                        if _line_[1][2] == '_' and _line_[1][3].isdigit():
                            aux_dic = { _line_[1] : _line_[2:]}
                            _define_[ _dedic_[ _line_[1][1]]].update( aux_dic)
                        else:
                            print('Whojojoooh...')
                    
                elif _line_[0] == '#include':
                    print(wrg_3( _line_[1] + ' skipped!'))
                else:
                    print(wrg_3( str(_line_) + '  ??'))
    
    return _define_

def get_ffldfiles( _topfile_):
    ''' 
    self explanatory... sub routine to get the force field files
    if they are stated in the top file.
    starts from the top file
    '''
    ff_file = ''
    nonerr_flag = True
    with open( _topfile_, 'r')  as indata:
        for j_line in indata:
            if j_line.startswith('#include'):
                ff_file =  j_line.split('"')[1]
                break
            elif j_line.startswith('[ moleculetype ]'):
                break
    
    root_folder = '/'.join(_topfile_.split('/')[:-1]+[''])
    ff_file = ff_file.lstrip('.').lstrip('/')
    
    if ff_file != '':
        # if there is at least one itp, lets parse it
        # first seek for further includes itp
        aux_file_cont = [_topfile_, '']
        print '----- Loading :'
        i = 1
        aux_file_cont[i] =  root_folder + ff_file
        print aux_file_cont[i]
        
        root_folder = '/'.join( aux_file_cont[i].split('/')[:-1]+[''])
        try:
            with open( aux_file_cont[i], 'r')  as indata2:
                for k_line in indata2:
                    if k_line.startswith('#include'):
                        i+=1
                        aux_file_cont.append( root_folder+k_line.split('"')[1])
                        print aux_file_cont[i]
                        if i==3:
                            break
                
        except IOError:
            pop_err_1('xx/0 Read error 030, file not found!!.\n')
            nonerr_flag *= False
        # the first one is [ defaults ]
        # second nonbonded atomtypes
        # third bonded 
        _directives_ = ['defaults', 'atomtypes', 'bondtypes']
        file_cont = []
        for _di_ in _directives_:
            file_cont.append( seek_for_directive( aux_file_cont, _di_))
            if file_cont[-1] == '':
                pop_wrg_1('Directive ' + _di_ + ' not found!')
                
                if _di_ == _directives_[-1]:
                    file_cont[-1] = file_cont[0] 
                
            else:
                print ('Using :' +file_cont[-1]+' for ' + _di_) 
    else:
        pop_err_1('Force field files #include not found!')
        nonerr_flag *= False
        
    # final check of non error flag
    if nonerr_flag and len(file_cont) < 3 :
        pop_wrg_1('Your structure seems unfamiliar, just ' +
                  '{} itp found.'.format( len(file_cont)) +
                  '\nthe conversion could fail!')
        # Meaning that the directive seeker could not find the correspondin one
        while len(file_cont) < 3:
            file_cont.append( file_cont[-1])
    # a file integrity check should be done outside
    return file_cont, nonerr_flag

def ck_forcefield( _the_file_, _secondoption_ = None):
    '''
    podria pedirse solo este archivo y 
    de aqui sacar la iformacion de los otros dos....
    '''
    _flag_ = False
    comb_rule = -1
    with open( _the_file_, 'r')  as indata:
        for j_line in indata:
            line_c = j_line.split()
            if j_line.startswith('[ defaults ]'):
                _flag_ = True
            if len(line_c)>1 and 'fudgeQQ'==line_c[-1]:
                j_line = indata.next()
                comb_rule= j_line.split()
                print('---> comb_rule {}'.format(comb_rule[1]))
                
    if not _flag_ and _secondoption_ != None:
        comb_rule, _flag_, _the_file_ = ck_forcefield( _secondoption_)
        
    if comb_rule < 0 or not _flag_:
        pop_err_1('forcefield.itp file is missing or incomplete')
        comb_rule, _flag_, _the_file_ = [ 0, 0, '']
    
    return comb_rule, _flag_, _the_file_

def seek_for_directive( _list_of_files_, _directive_):
    ''' search for a certain directive in a bunch of files
        and then returns the file in which it is, or an empty string
        PS: a directive is a word wrapped with [] 
    '''
    content_file = ''
    for file_ in _list_of_files_:
        try:
            with open( file_, 'r')  as indata:
                for j_line in indata:
                    line_c = j_line.split(';')[0].split(' ]')[0].split('[ ')
                    if len( line_c) > 1:
                        if line_c[1] == _directive_:
                            content_file = file_
                            break
        except IOError:
            exit('xx/0 Read error 030, file not found.\n' + file_)
            
        if content_file != '':
            break
    
    return content_file
    
    
    
    
def get_top_groups( _mtype_container_, _group_):
    
    _mtype_ = _mtype_container_
    _buffer = []
    for mt in range(len( _mtype_)):
        
        mtype = _mtype_[mt].strip(' ')
        if _buffer == [] and mtype == _group_:
            buffer = [ mtype, mt+1]
            
        elif _buffer != [] and mtype != _group_:
            _buffer += [mt]
            break
            
        elif mt==(len(_mtype_)-1):
            
            _buffer += [mt+1]
                
    print''
    print 'Group characterized as: {} with ids {} to {}'.format(*_buffer)
    return _buffer


if __name__ == '__main__':
    
    pass
    
# vim:tw=80
