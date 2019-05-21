#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>' 

from warn import pop_err_1

def check_vars( _vars_, _varstype_, _endtext_ = 'Input script not created!'):
    
    _flag_c_ = []
    for v in range(len(_vars_)):
        #print _vars_[v], _varstype_[v]
        err_txt = ''
        if _varstype_[v] =='int':
            try:
                int(_vars_[v])
                _flag_c_.append(1)
            except ValueError:
                _flag_c_.append(0)
                aux_here = _vars_[v]
                if _vars_[v] == '':
                    aux_here = '<void>'
                err_txt = ' {} is not a valid type of integer'.format( aux_here)
                
        elif _varstype_[v] =='float':
            #print _vars_[v]
            try:
                float(_vars_[v])
                _flag_c_.append(1)
            except ValueError:
                _flag_c_.append(0)
                aux_here = _vars_[v]
                if _vars_[v] == '':
                    aux_here = '<void>'
                err_txt = ' {} is not a valid type of float'.format( aux_here)
                
        elif _varstype_[v] =='str':
            try:
                str(_vars_[v])
                _flag_c_.append(1)
            except ValueError:
                _flag_c_.append(0)
                err_txt = ' {} is not a valid type of string'.format( _vars_[v])
            
            '''**** Special re Combos ****'''
            
        elif _varstype_[v] == 'int:':
            _aux_ = _vars_[v].split(':')
            if len( _aux_) <> 2:
                err_txt = ( 'Please separate two integers with one colon (:)'
                           +' instead of {}'.format(_vars_[v]))
                _flag_c_ += [0,0]
            else:
                _flag_c_ += check_vars( _aux_, ['int']*2, _endtext_)
            
        elif _varstype_[v] =='float:':
            _aux_ = _vars_[v].split(':')
            if len( _aux_) <> 2:
                err_txt = ( 'Please separate two floats with one colon (:)'
                           +' instead of {}'.format(_vars_[v]))
                _flag_c_ += [0,0]
            else:
                _flag_c_ += check_vars( _aux_, ['float']*2, _endtext_)
        
                        
        elif _varstype_[v] == 'float:xyz':
            _aux_ = _vars_[v].split(':')
            if len( _aux_) <> 2:
                err_txt = ( 'Please separate the integer and "xyz" with one'
                           +'colon (:) instead of {}'.format(_vars_[v]))
                _flag_c_ += [0,0]
            else:
                _int_flag_ = check_vars( [_aux_[0]], ['int'], _endtext_)
                _o_flag_ = 1
                for l in _aux_[1]:
                    if l not in 'xyz':
                        _o_flag_*=0
                if not _o_flag_:
                    err_txt = ( 'Please correct {}, accepted leters are "x" '
                               +'and/or "y" and/or "z"'.format(_aux_[1]))
                    
                _flag_c_ += _int_flag_ + [ _o_flag_]
                
        
        
        elif type(_varstype_[v]) == list and _varstype_[v][0] =='<float::<':
            
            _aux_v_ = [x.strip(' ') for x in _vars_[v].split(':')]
            _min, _max = _varstype_[v][1:]
            if len( _aux_v_) <> 3:
                err_txt = ( 'Please separate three floats with two colons (:)'
                           +' instead of {}'.format(_vars_[v]))
                _flag_c_ += [0,0,0]
            else:
                _flag_c_ += check_vars( _aux_v_,
                                       [['<float<', _min, _max]] * len( _aux_v_),
                                       _endtext_)
                
                
        
        elif type(_varstype_[v]) == list and _varstype_[v][0] == '<int<':
            _min, _max = _varstype_[v][1:]
            _flag_ = check_vars( [_vars_[v]], ['int'], _endtext_)
            #print _flag_c_, _flag_
            if _flag_[0]:
                if _min <= int(_vars_[v]) <= _max:
                    _flag_c_ += _flag_
                else:
                    _txt_ = ('The available range is {}:{}.\n'
                             'Consequently {} is out of range')
                    err_txt = ( _txt_.format( _min, _max, _vars_[v]))
                    _flag_c_ += [0]
            else:
                _flag_c_ += _flag_
            #print _flag_c_
            
        elif type(_varstype_[v]) == list and _varstype_[v][0] == '<float<':
            _min, _max = _varstype_[v][1:]
            _flag_ = check_vars( [_vars_[v]], ['float'], _endtext_)
            #print _flag_c_, _flag_
            if _flag_[0]:
                if _min <= float(_vars_[v]) <= _max:
                    _flag_c_ += _flag_
                else:
                    _txt_ = ('The available range is {}:{}.\n'
                             'Consequently {} is out of range')
                    err_txt = ( _txt_.format( _min, _max, _vars_[v]))
                    _flag_c_ += [0]
            else:
                _flag_c_ += _flag_
        
        elif type(_varstype_[v]) == list and _varstype_[v][0]==list:
            #print _varstype_[v]
            _sep_ = _varstype_[v][1]
            _aux_v_ = [x.strip(' ') for x in _vars_[v].split(_sep_)]
            
            for _v_ in _aux_v_:
                if _v_ in _varstype_[v]:
                    _flag_c_.append(1)
                else:
                    err_txt += ( 'Unknown value <{}>.\n'.format( _v_))
                    _flag_c_.append(0)
            if err_txt <> '':
                err_txt += '\nAllowed values are:\n'
                for av in _varstype_[v][2:-1]:
                    err_txt += '"{}" or '.format(av)
                err_txt += '"{}"'.format(_varstype_[v][-1])
                
        elif type(_varstype_[v]) == list and _varstype_[v][0] == '<int:int<':
            
            _min, _max = _varstype_[v][1:]
            
            _aux_ = check_vars( [_vars_[v]], ['int:'], _endtext_)
            
            if min( _aux_):
                _aux_v_ = [int(x.strip(' ')) for x in _vars_[v].split(':')]
                if _aux_v_[0]>_aux_v_[1]:
                    _txt_ = 'Please check {} must be lo:hi'
                    err_txt = ( _txt_.format( _vars_[v]))
                    _flag_c_ += [0,0]
                elif _aux_v_[0] < _min or _aux_v_[1] > _max:
                    _txt_ = 'The available range is {}:{}'
                    err_txt = ( _txt_.format( _min, _max))
                    _flag_c_ += [0,0]
                    
                else:
                    _flag_c_ += _aux_
            else:
                _flag_c_ += _aux_
                
        elif type(_varstype_[v]) == list and _varstype_[v][0] == '<int-x-int<':
            _min, _max = _varstype_[v][1:]
            _aux_v_ = [x.strip(' ') for x in _vars_[v].split('-')]
            _aux_flag_c_ = check_vars( _aux_v_,
                                      [['<int<', _min, _max]] * len( _aux_v_),
                                      _endtext_)
            if min(_aux_flag_c_):
                if len(set( _aux_v_)) < len( _aux_v_):
                    _txt_ = 'Please check {}, there is a repeated number'
                    err_txt = ( _txt_.format( _vars_[v]))
                    _flag_c_ += [0]*len( _aux_v_)
                else:
                    _flag_c_ += _aux_flag_c_
                    
            else:
                _flag_c_ += _aux_flag_c_
        
        elif type( _varstype_[v])== list and _varstype_[v][0]=='<int-x-int<:0':
            _min, _max = _varstype_[v][1:]
            if not _vars_[v].isdigit():
                _flag_c_ += check_vars( [ _vars_[v]],
                                       [[ '<int-x-int<', _min, _max]],
                                        _endtext_)
                
            elif int(_vars_[v]) > 0:
                _flag_c_ += check_vars( [ _vars_[v]],
                                       [['<int<', _min, _max]] ,
                                       _endtext_)
            
            elif int(_vars_[v]) == 0:
                    _flag_c_ += [1]
                    
            else:
                err_txt = 'Not valid number, check {}!'.format(_vars_[v])
                _flag_c_ += [0]
        else:
            #print _varstype_[v]
            print 'Unhandled variable check for: ', _vars_[v]
            _flag_c_.append(1)
        
        '''**** Message ****'''
        if err_txt<>'':
            pop_err_1( err_txt+'\n'+_endtext_)
    
        
    return _flag_c_

def isnot_num( _string_):
    ''' return True if the string is not numeric
    '''
    _flag_ = True
    try:
        float( _string_)
        _flag_ = False
    except ValueError:
        pass
    return _flag_
    
# vim:tw=80
