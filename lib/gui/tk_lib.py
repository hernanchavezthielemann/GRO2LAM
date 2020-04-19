#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'

from Tkinter import Entry, Button, Frame, Label, Scrollbar, StringVar, Menu
from Tkinter import Listbox, IntVar, Checkbutton, Widget, Spinbox
from Tkinter import X, Y, SUNKEN, VERTICAL, END

'''     Home made ttk library     '''

#================================
#        Classes definition
#================================
        
class Drop_Down_List(Widget):
    """The lean version of the Ttk Combobox from ttk library"""

    def __init__(self, master=None, **kw):
        Widget.__init__(self, master, "ttk::combobox", kw)
        self.bind("<Key>", lambda e: "break") # Magic
    
    def current(self, newindex=None):
        """If newindex is supplied, sets the combobox value to the
        element at position newindex in the list of values. Otherwise,
        returns the index of the current value in the list of values
        or -1 if the current value does not appear in the list."""
        if newindex is None:
            return self.tk.getint(self.tk.call(self._w, "current"))
        return self.tk.call(self._w, "current", newindex)

    def set(self, value):
        """Sets the value of the combobox to value."""
        self.tk.call(self._w, "set", value)

#================================
#        Functions definition
#================================

def create_entry( _main_row_, _desc_txt, _def_txt_, t_len, ckbc=None, fn=None):
    ''' creates a tkinter entry '''
    _row_ = Frame(_main_row_)
    
    if ckbc<>None and fn<>None:
        label0 = Label(_row_, width=3, text="  ", anchor='w')
        cvar = IntVar()
        label1 = Checkbutton(_row_, width=0
                               ,variable = cvar
                               ,command = fn
                               , anchor = 'w')
        label2= Label(_row_, width=t_len, text=_desc_txt+"  ", anchor='w')
        
        ckbc.append([cvar, label1])
        
    else:
        label0 = Label(_row_, width=3, text=" >", anchor='w')
        label1 = Label(_row_, width=t_len, text = _desc_txt, anchor='w')
        label2 = Label(_row_, width=2, text=" :", anchor='w')
    
    if type(_def_txt_)==str: 
        Ent_It = Entry(_row_)#, width=13)
        Ent_It.insert('end', _def_txt_)
        
        
    elif type(_def_txt_) in [list, tuple]:
        
        if type(_def_txt_[1]) in [set]:
            
            _nums_ = [str(x) for x in sorted(list(_def_txt_[1]))]
            Ent_It = StringVar()
            aux_spin = Spinbox(_row_,
                               textvariable = Ent_It,
                               values = tuple(_nums_)
                              )
            
            Ent_It.set(_def_txt_[0])
        else:
            Ent_It = StringVar()
            aux_ddl = Drop_Down_List(_row_,
                                     textvariable = Ent_It,
                                     values = tuple( _def_txt_[1]),
                                     #state = "readonly"
                                    )
            aux_ddl.bind("<Key>", lambda e: "break") # Magic
            Ent_It.set(_def_txt_[0])
        
        
    
    finalspace = Label(_row_, width=5, text=" ", anchor='w')
    
    # Just packing
    label0.pack(side='left', padx=1)
    label1.pack(side='left', padx=6)
    label2.pack(side='left', padx=0)
    
    
    if type(_def_txt_)==str: 
        Ent_It.pack(side='left', expand=True, fill=X)
    elif type(_def_txt_) in [list, tuple] and type(_def_txt_[1]) == set:
        aux_spin.pack(side='left', expand=True, fill=X)
    else:
        aux_ddl.pack(side='left', expand=True, fill=X)
        
    finalspace.pack(side='right', padx=0)
    _row_.pack(side='top', fill=X, pady=1)
    
    # For tracing purposes list appending
    return Ent_It

def get_entriesvalue(entries_container):
        ''' ---   entry getter app ----
        mainly to obtain values of entries'''
        e_values=[]
        for ent in range(len(entries_container)):
            e_values.append(entries_container[ent].get())
        return e_values

def bottom_hline_deco(row, func=None):
    ''' adds a sunken line in the bottom of a tkinter function'''
    if func <> None:
        func()
    line = Frame( row ,height=2, bd=1, relief= SUNKEN)
    line.pack(fill=X, padx=1, pady=5)

def create_check_row( _s_row_, _text_, func, _desc_=['']):
        
        _f_labels = format_dec([_s_row_, _text_], _pack_=False)
        _ckvar =[]
        for d in range(len(_desc_)):
            cvar = IntVar()
            _ckvar.append(cvar)
            label_ck = Checkbutton(_s_row_, width=0, text= _desc_[d]
                                   ,variable=cvar
                                   ,command=func
                                   , anchor='w')
            _ckbut_container.append(label_ck)
        
        format_dec(_f_labels, _create_=False)
        
        for d in range(len(_desc_)):
            _ckbut_container[-len(_desc_)+d].pack(side='left', padx=6)
            
        return _ckvar, _ckbut_container

def create_file_entry( _master_, ups_frame, fi_text, _default_file):
    ''' Quite self explanatoy...
        creates a row in which is possible to search for a file'''
    file_row = Frame(ups_frame)
    f_ex = ((fi_text ,'.'+ _default_file.split('.')[-1]),)
    
    _f_labels = format_dec([file_row, fi_text], _pack_=False)
    
    Efile = Entry(file_row, width=13)
    Efile.insert(END, _default_file)
    Efile.xview_moveto(1)
    Bsearch = Button(file_row,
                     image= get_file_img(),
                     command=(lambda El=Efile: _master_.browsefile(El, f_ex)))
    
    # Just packing
    format_dec(_f_labels, _create_=False)
    
    Efile.pack(side='left', expand='yes', fill=X)
    
    Bsearch.pack(side='right', padx=0, pady=0)
    file_row.pack(side='top', fill=X, pady=3)
    
    # For tracing purposes list appending
    return Efile

def generate_listbox(row, fill_list):
    
    scrollbar = Scrollbar(row , orient=VERTICAL)
    Flistbox = Listbox(row , yscrollcommand= scrollbar.set, height=1)#,
    scrollbar.config(command= Flistbox.yview)
    scrollbar.pack(side='right', fill=Y)
    for item in fill_list:
        Flistbox.insert(END, item);
    Flistbox.pack(side='left', fill=X , expand=1)
    
    return Flistbox

def format_dec(_rnt_or_lc_, _create_=True, _pack_=True, _lastline_=True):
    ''' can be re-thought as a function wrapper
        furthermore as a class... but for now works perfect'''
    if _create_:
        row_fst, _text_=_rnt_or_lc_
        label0 = Label(row_fst, width=3, text=" >", anchor='w')
        label1 = Label(row_fst, width=21, text=_text_, anchor='w')
        label2 = Label(row_fst, width=2, text=" :", anchor='w')
        
        if _lastline_:
            label3 = Label(row_fst, width=2, text=" ", anchor='w')
            if not _pack_:
                return label0, label1, label2, label3
        elif not _pack_:
            return label0, label1, label2
    else:
        label0 =_rnt_or_lc_[0]
        label1 =_rnt_or_lc_[1]
        label2 =_rnt_or_lc_[2]
        if _lastline_:
            label3 =_rnt_or_lc_[3]
        
    if _pack_:
        
        label0.pack(side='left', padx=1)
        label1.pack(side='left', padx=6)
        label2.pack(side='left', padx=0)
        if _lastline_:
            label3.pack(side='right', padx=0)

def createmenubar( _root_window_, _listofentriesdicts_):
    ''' under development 
    input format example: 
        <class app>
        [{ 'title' : 'Title1', 'title_com' : (print , '>command11<') },
        { 'title' : 'Title2',
        'cascade' : (('cnd_label' ,'>command31<'),('cnd_label' ,'>command33<'),
        ('separator'),('cnd_label' ,'>command33<'))}]
    '''
    # using list of list instead dict because an order is needed
    # First create the menu bar
    menu_bar = Menu( _root_window_) # menubar "object"
    _root_window_.config( menu= menu_bar)
    
    for i in range( len( _listofentriesdicts_)):
        entry_dict = _listofentriesdicts_[i]
        if 'title_com' in entry_dict.keys():
            _com_ = entry_dict['title_com']
            if len(_com_)>1:
                menu_bar.add_command( label = entry_dict['title']
                                     , command= (lambda com = _com_: 
                                                 com[0]( com[1])))
            else:
                menu_bar.add_command( label = entry_dict['title']
                                     , command= _com_[0])
            
        elif 'cascade' in entry_dict.keys():
            # allocating space
            sub_menu = Menu( menu_bar)
            # Create a menu button labeled "File" as example, that brings up a
            # menu this comes in the entry_dict['title']
            if 'titlei' in entry_dict.keys():
                menu_bar.add_cascade(image = entry_dict['titlei'],
                                     menu = sub_menu)
            else:
                menu_bar.add_cascade(label = entry_dict['title'],
                                     menu = sub_menu)
            # Create cascades in menus
            content = entry_dict['cascade']
            for cc in range( len( content)):
                _ccc_ = content[cc]
                
                if len( _ccc_)==3:
                    sub_menu.add_command(label = content[cc][0],
                                         command = (lambda com = _ccc_: 
                                                    _ccc_[1]( _ccc_[2])))
                elif len( _ccc_)==2:
                    sub_menu.add_command(label = content[cc][0],
                                         command = _ccc_[1])
                else:
                    sub_menu.add_separator(  )
        else:
             print ' - incomplete data - '

def testprint():
    print '>command33<'

# vim:tw=80
