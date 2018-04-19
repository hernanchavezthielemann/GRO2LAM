#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'

from Tkinter import Tk, Entry, Button, Frame, Toplevel, Label, Scrollbar
from Tkinter import Listbox, Menu

from Tkinter import X, Y, SUNKEN, VERTICAL, END, LEFT, RIGHT


def bottom_hline_deco(row, func=None):
    ''' adds a sunken line in the bottom of a tkinter function'''
    if func <> None:
        func()
    line = Frame( row ,height=2, bd=1, relief= SUNKEN)
    line.pack(fill=X, padx=1, pady=5)

def create_entry( _main_row_, _desc_txt, _def_txt_, t_len):
        ''' creates a tkinter entry '''
        _row_ = Frame(_main_row_)
        label0 = Label(_row_, width=3, text=" >", anchor='w')
        label1 = Label(_row_, width=t_len, text = _desc_txt, anchor='w')
        label2 = Label(_row_, width=2, text=" :", anchor='w')
        
        Ent_It = Entry(_row_, width=13)
        Ent_It.insert('end', _def_txt_)

        finalspace = Label(_row_, width=5, text=" ", anchor='w')
        
        # Just packing
        label0.pack(side='left', padx=1)
        label1.pack(side='left', padx=6)
        label2.pack(side='left', padx=0)
        Ent_It.pack(side='left', expand=True, fill=X)
        finalspace.pack(side='right', padx=0)
        _row_.pack(side='top', fill=X, pady=3)
        
        # For tracing purposes list appending
        return Ent_It

def get_entriesvalue(entries_container):
        ''' ---   entry getter app ----
        mainly to obtain values of entries'''
        e_values=[]
        for ent in range(len(entries_container)):
            e_values.append(entries_container[ent].get())
        return e_values

def generate_listbox(row, fill_list):
    
    scrollbar = Scrollbar(row , orient=VERTICAL)
    Flistbox = Listbox(row , yscrollcommand= scrollbar.set, height=1)#,
    scrollbar.config(command= Flistbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    for item in fill_list:
        Flistbox.insert(END, item);
    Flistbox.pack(side=LEFT, fill=X , expand=1)
    
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
        
        label0.pack(side=LEFT, padx=1)
        label1.pack(side=LEFT, padx=6)
        label2.pack(side=LEFT, padx=0)
        if _lastline_:
            label3.pack(side=RIGHT, padx=0)

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

def garbage_container1():
    
    class MainWindow(Frame):
        counter = 0
        def __init__(self, *args, **kwargs):
            Frame.__init__(self, *args, **kwargs)
            self.button = Button(self, text="Create new window", 
                                    command=self.create_window)
            self.button.pack(side="top")
    
        def create_window(self):
            self.counter += 1
            t = Toplevel(self)
            t.wm_title("Window #%s" % self.counter)
            l = Label(t, text="This is window #%s" % self.counter)
            l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    #if __name__ == "__main__":
    root = Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()

def garbage_container2():
    '''https://stackoverflow.com/questions/26568890/
    how-do-i-flash-a-button-with-a-keypress-in-tkinter'''
    r = Tk()

    l = Label(text = 'press f to make button flash')
    l.pack()

    b = Button(text = 'useless button')
    b.config(bg = 'lightgrey')
    b.pack()

    def flash(event):
        b.config(bg = 'yellow')
        r.after(100, lambda: b.config(bg = 'lightgrey'))

    r.bind("<KeyPress-f>", flash)

    r.mainloop()
    
# vim:tw=80
