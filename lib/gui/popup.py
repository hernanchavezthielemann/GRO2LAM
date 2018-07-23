#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'

from Tkinter import Frame, Toplevel, Label, Button, Checkbutton, Entry
from Tkinter import SUNKEN, X, Y, PhotoImage, IntVar
from tk_lib import create_entry, bottom_hline_deco, get_entriesvalue
from tkFont import Font
from webbrowser import open_new
from lib.misc.version import __version__

class Message_box(Frame):
    ''' It is a frame because at the end it is a message box launchpad'''
    def __init__(self, master=None, **options):
        
        if not master and options.get('parent'):
            master = options['parent']
        self.master  = master
        
        Frame.__init__(self, master)
        
        # Defaults
        if "title" not in options:
            options["title"] = 'Message box'
        if "message" not in options:
            options["message"] = 'Dumb message'
        if "icon" not in options:
            options["icon"] = 'info'
        if "type" not in options:
            options["type"] = 'ok'
        
        self.options = options

    def pop_up(self):
        '''Arise the message box, and after the ok try to destroy it'''
        bt = self.tk.call( "tk_messageBox", *self._options( self.options))
        try:
            self.destroy()
        except:
            pass
        return bt

def message_box( message='', title='Message box', **options):
    '''creates a message box through the implementation of an instance
     of class Message_box, these messages can be info, warning and error'''
    
    options["title"] = title
    options["message"] = message

    mb_selection = Message_box(**options).pop_up()
    
    return mb_selection


class FilePopUp(Frame):
    '''Neat & tidy pop up to search files'''
    
    def __init__(self, master=None, **options):
        
        if not master and options.get('parent'):
            master = options['parent']
        self.master  = master
        
        Frame.__init__(self, master)
        
        self._options_ = {}
        self._options_['filetypes']=(("Geometry", ".pdb"),("Force Field", ".frc"))
    
    @property
    def filetypes(self):
        return self._options_
    @filetypes.setter
    def filetypes(self, **value):
        print '-----------', value, type (value)
        value += (("All","*"),)
        self._options_ = {'filetypes': ("All","*")}
        
    def getfilepath(self):
        ''' Routine to return the file path of the one selected by user thru
            the "tk_getOpenFile" build in option of tkinter'''
        
        userchoice = self.tk.call("tk_getOpenFile",
                                  *self._options(self._options_))
        try:
            userchoice = userchoice.string
        except AttributeError:
            pass
        
        try:
            aux.destroy()
        except:
            pass
        return userchoice
    
class SaveAsPopUp():
    ''' to be implemented'''
    def __init__(self, master=None):
        self.master  = master
        self._options = {}
        print 'Soon ...  but save what?'
        
    @property
    def options(self):
        return self._options
    @options.setter
    def options(self, **value):
        self._options = value

class PromptPopUp_old():
    '''the future description:
            "Neat & tidy prompt pop up to request input"
        
        there is a lot of work to do here :
        make it class
        clean functions to make it generic
        add extra parameters such as:
                    buttons
                    title
                    dimensions*
                    
       >but is a functional starting point<
    '''
    def __init__(self, **kwargs):
        ''' (under development)'''
        
        master = None
        briefing = ''
        entries_txt = []
        entries_val = []
        title = 'PromptPopUp'
        
        if 'master' in kwargs.keys():
            master = kwargs['master']
        if 'briefing' in kwargs.keys():
            briefing = kwargs['briefing']
        if 'entries_txt' in kwargs.keys():
            entries_txt = kwargs['entries_txt']
        if 'entries_val' in kwargs.keys():
            entries_val = kwargs['entries_val']
        if 'title' in kwargs.keys():
            title = kwargs['title']
        
        self.master  = master
        self._briefing_ = briefing
        self._entries_ = entries_txt
        self._defvals_ = entries_val
        self._title_ = title
        
        self.ent_c = []
        
        self.set_self_vertex()
        self.create_content()
    
    def set_self_vertex(self):
        from main_gui import MAINVERTEX
        ws, hs, w_main, h_main, x_main, y_main = MAINVERTEX
        # calculate the greatness
        self.entr_maxlen = int(len(max(self._entries_, key=len))*2.25/3.0)
        w_pop = w_main - 40
        h_pop = h_main*12/21
        
        x_pop = x_main + w_main - 30
        y_pop = y_main + h_main - h_pop
        #print w_pop, h_pop, x_pop, y_pop
        self._vertex_= [w_pop, h_pop, x_pop, y_pop]

    def create_content(self):
        
        self.pop = Toplevel(self.master)
        self.pop.grab_set()# when you show the popup
        
        self.pop.wm_title(' '*20+self._title_)
        self.pop.geometry('{:d}x{:d}+{:d}+{:d}'.format(*self._vertex_))
        
        label0= Label(self.pop, text= self._briefing_ )
        label0.pack(side="top", fill="both", expand=True, padx=100, pady=20)
        #    just a line
        bottom_hline_deco(self.pop)
        # lets create space to do some stuff ...
        
        row2fill = Frame(self.pop)
        
        for e in range(len(self._entries_)):
            self.ent_c.append(create_entry(row2fill,
                                           self._entries_[e],
                                           self._defvals_[e],
                                           self.entr_maxlen)
                             )
        row2fill.pack(side="top", padx=1, pady=5)
        
        
        self.bottom_button_row()
        
        self.master.solv_b.config(bg = 'gray40', width = 45) #cyan')
        #self.master.solv_b.flash()
        #self.pop.mainloop()

    def bottom_button_row(self):
        
        _br_ = Frame(self.pop)
        b1 = Button(_br_, text='Save', command=(lambda: self.save_it()))
        b1.pack(side="right", padx=10, pady=20)
        b2 = Button(_br_, text='Quit', command=(lambda: self.exit_pop()))
        b2.pack(side="right", padx=10, pady=4)
        _br_.pack(side="bottom", expand=True)
        
    def save_it(self):
        
        self.master._solvatedinfo_= get_entriesvalue( self.ent_c)
        self.exit_pop()

    def exit_pop(self):
        
        self.pop.grab_release() # to return to normal
        self.master.solv_b.config(bg = 'lightgrey', width = 29)
        self.pop.destroy()

class PromptPopUp(Toplevel):

    def __init__(self, master = None, **kwargs):
        ''' (under development)
        Class - done
        dimensions - done
        
        '''
        Toplevel.__init__(self, master)
        
        
        briefing = ''
        entries_txt = []
        entries_val = []
        title = 'PromptPopUp'
        width, height = [None, None]
        
        if 'briefing' in kwargs.keys():
            briefing = kwargs['briefing']
        if 'entries_txt' in kwargs.keys():
            entries_txt = kwargs['entries_txt']
        if 'entries_val' in kwargs.keys():
            entries_val = kwargs['entries_val']
        if 'title' in kwargs.keys():
            title = kwargs['title']
        if 'width' in kwargs.keys():
            width = kwargs['width']
        if 'height' in kwargs.keys():
            height = kwargs['height']
        
        self.master  = master  

        self._briefing_ = briefing
        self._entries_ = entries_txt
        self._defvals_ = entries_val
        self._width_ = width
        self._height_ = height
        
        self.set_self_vertex()
        
        self.wm_title(' '*5+title)
        #print self._vertex_
        self.geometry('{:d}x{:d}+{:d}+{:d}'.format(*self._vertex_))
        
        self.ent_c = []
        
        if 'content' in kwargs.keys() and not kwargs['content']:
            pass
        else:
            self.create_content()
        self.grab_set()# when you show the popup
        self.bind('<Return>', self.save_it )
        
    def set_self_vertex(self ):
        
        ws, hs, w_main, h_main, x_main, y_main = self.master.MAINVERTEX
        #print ws, hs, w_main, h_main, x_main, y_main
        # calculate the greatness
        
        
        if  self._width_ == None:
            self._width_ = w_main - 40
        if self._height_ == None:
            self._height_ = h_main*12/21
        
        x_pop = x_main + w_main - 30
        y_pop = y_main + h_main - self._height_
        #print w_pop, h_pop, x_pop, y_pop
        self._vertex_= [self._width_, self._height_, x_pop, y_pop]

    def create_content(self):
        
        
        label0= Label(self, text= self._briefing_ )
        label0.pack(side="top", fill="both", expand=True, padx=50, pady=20)
        #    just a line
        bottom_hline_deco(self)
        # lets create space to do some stuff ...
        self.entr_maxlen = int(len(max(self._entries_, key=len))*2.5/3.0)
        row2fill = Frame(self)
        #print self._entries_,'\n', self._defvals_,
        #'\n',len(self._entries_),'\n', len(self._defvals_)
        
        aline=0
        for e in range(len(self._entries_)):
            if self._entries_[e] == '---':
                aline+=1
                bottom_hline_deco(row2fill)
                #print self._entries_[e]
            else:
                self.ent_c.append(create_entry(row2fill,
                                               self._entries_[e],
                                               self._defvals_[e-aline],
                                               self.entr_maxlen)
                                 )
                
        row2fill.pack(side="top", padx=1, pady=5)
        
        self.bottom_button_row()
        
        
            
    def bottom_button_row(self):
        ''' just to rder a little bit'''
        _br_ = Frame(self)
        b1 = Button(_br_, text='Save', command= self.save_it )
        b1.pack(side="right", padx=10, pady=20)
        b1.focus()
        
        b2 = Button(_br_, text='Quit', command=(lambda: self.exit_pop()))
        b2.pack(side="right", padx=10, pady=4)
        _br_.pack(side="bottom", expand=True)
        
    def save_it(self, event=None):
        self.master._aux_ = get_entriesvalue( self.ent_c)
        self.exit_pop()
        

    def exit_pop(self):
        self.grab_release() # to return to normal
        self.destroy()# quit()


class PromptPopUp_wck(Toplevel):
    ''' classic prompt setup with 
        advanced check button options'''
    def __init__(self, master = None, **kwargs):
        ''' (under development)'''
        Toplevel.__init__(self, master)
        
        
        briefing = ''
        entries_txt = []
        entries_val = []
        title = 'PromptPopUp_wck'
        width, height = [None, None]
        
        gr_ids, chck_init, res_ens = [0,[],'']
        extra_but =None
        
        if 'briefing' in kwargs.keys():
            briefing = kwargs['briefing']
        if 'entries_txt' in kwargs.keys():
            entries_txt = kwargs['entries_txt']
        if 'entries_val' in kwargs.keys():
            entries_val = kwargs['entries_val']
        if 'title' in kwargs.keys():
            title = kwargs['title']
        if 'width' in kwargs.keys():
            width = kwargs['width']
        if 'height' in kwargs.keys():
            height = kwargs['height']
            
        if 'range_id' in kwargs.keys():
            gr_ids = kwargs['range_id']     
        if 'chck_init' in kwargs.keys():
            chck_init = kwargs['chck_init']
        if 'res_ens' in kwargs.keys():
            res_ens = kwargs['res_ens']
        if 'extra_but' in kwargs.keys():
            extra_but = kwargs['extra_but']
            
        self.master  = master  

        self._briefing_ = briefing
        self._entries_ = entries_txt
        self._defvals_ = entries_val
        self._width_ = width
        self._height_ = height
        
        self.range_ids = gr_ids
        self.range_ens = res_ens
        self.ch_init = chck_init
        
        
        self.set_self_vertex()
        
        self.wm_title(' '*5+title)
        #print self._vertex_
        self.geometry('{:d}x{:d}+{:d}+{:d}'.format(*self._vertex_))
        
        self.ent_c = []
        self.ckb_c = []
        self.extra_checkb = extra_but
        #self._bstatus =[]
        
        self.create_content()
        self.grab_set()# when you show the popup grab the power
        self.bind('<Return>', self.save_it )
        
        
    def set_self_vertex(self ):
        
        ws, hs, w_main, h_main, x_main, y_main = self.master.MAINVERTEX
        
        if  self._width_ == None:
            self._width_ = w_main - 40
        if self._height_ == None:
            self._height_ = h_main*12/21
        
        x_pop = x_main + w_main - 60
        y_pop = y_main + h_main - self._height_
        #print w_pop, h_pop, x_pop, y_pop
        self._vertex_= [self._width_, self._height_, x_pop, y_pop]

    def create_content(self):
        
        label0= Label(self, text= self._briefing_ )
        label0.pack(side="top", fill="both", expand=True, padx=50, pady=20)
        #    just a line
        bottom_hline_deco(self)
        # lets create space to do some stuff ...
        self.entr_maxlen = int((len(max(self._entries_, key=len)))*2.5/3.0)+8
        
        
        self.row2fill = Frame(self)
        
        if self.ch_init == []:
            for e in range(len(self._entries_)):
                self.ent_c.append( create_entry(row2fill,
                                                self._entries_[e],
                                                self._defvals_[e],
                                                self.entr_maxlen
                                               )
                                 )
        else:
            #self.ent_c=[[],[]]
            for _e_ in range( len( self._entries_)):
                self.create_entry_ck( self.row2fill, _e_ )
            
            if self.extra_checkb==None:
            # - add 1 more x kind line
                self.add_new_line()
                self.ch_init+=[0]
            else:
                #print self.extra_checkb
                gr, ids, k_xyz, rns, cks =self.extra_checkb
                
                for _e_ in range( len( gr)):
                    
                    cnt = gr[_e_], ids[_e_], k_xyz[_e_], rns[_e_]
                    self.create_entry_ck( self.row2fill, None, cnt)
                
                self.ch_init+=cks
                
            
            self.set_ckbuttonstate(self.ch_init)
                
        self.row2fill.pack(side="top", padx=1, pady=5)
        
        self.bottom_button_row()        
    
    def create_entry_ck( self, _row2use_, _i_=None, container =[]):
        ''' creates a too custom check row so it aparts here'''
        _row_ = Frame(_row2use_)
        
        if _i_==None:
            _group_, _def_ids_,_def_fcoord_, _res_ens_ = container
            
        else:
            _group_ = self._entries_[_i_]
            _def_fcoord_ = self._defvals_[_i_]
            _def_ids_ = self.range_ids[_i_]
            _res_ens_ = self.range_ens[_i_]
        
        label0 = Label(_row_, width=1, text=" ", anchor='w')
        # first check button
        cvar = IntVar()
        label1 = Checkbutton(_row_, width=0
                               ,variable = cvar
                               ,command = self.checkbuttonstuff
                               , anchor = 'w')
        self.ckb_c.append([cvar, label1])
        # group description
        label2= Label(_row_,
                      width=6,
                      text= 'Group ', anchor='w')
        Ent_gr = Entry(_row_, width=8)
        Ent_gr.insert('end', _group_)
        
        label2_2= Label(_row_, width= 5, text= "  ids", anchor='w')
        # group ids
        Ent_ids = Entry(_row_, width=10)
        Ent_ids.insert('end', _def_ids_)
        
        label3= Label(_row_, width= 7,
                      text= "  K:xyz ", anchor='w')
        Ent_it = Entry(_row_, width=6)
        Ent_it.insert('end', _def_fcoord_)
        
        label4= Label(_row_, width= 5,
                      text= " In run", anchor='w')
        Ent_ens = Entry(_row_, width=6)
        Ent_ens.insert('end', _res_ens_)
        
        finalspace = Label(_row_, width=5, text=" ", anchor='w')
        
        # Just packing
        label0.pack(side='left', padx=0)
        label1.pack(side='left', padx=2)
        label2.pack(side='left', padx=0)
        Ent_gr.pack(side='left', expand=True, fill=X)
        label2_2.pack(side='left', padx=0)
        Ent_ids.pack(side='left', expand=True, fill=X)
        
        label3.pack(side='left', padx=0)
        Ent_it.pack(side='left', expand=True, fill=X)
        
        label4.pack(side='left', padx=0)
        Ent_ens.pack(side='left', expand=True, fill=X)
        finalspace.pack(side='right', padx=0)
        _row_.pack(side='top', fill=X, pady=3)
        
        # For tracing purposes list appending
        self.ent_c.append([Ent_gr, Ent_ids, Ent_it, Ent_ens])
        #self.ent_c[1].append(Ent_It)

    def add_new_line(self, g_num=1):
        _group_ = 'extra_g{}'.format(g_num)
        _fcoord_ = '1:xyz'
        _ids_= '1:2'
        _res_ens_ = '1-2'
        cnt = _group_, _ids_,_fcoord_, _res_ens_
        self.create_entry_ck( self.row2fill, None, container = cnt)
        
        if len(self.ckb_c)>6:
            self._vertex_[1] += 25
            self.geometry('{:d}x{:d}+{:d}+{:d}'.format(*self._vertex_))
        
        
        self.row2fill.pack(side="top", padx=1, pady=5)
        
        
        
    def set_ckbuttonstate(self, __sel__):
        '''Button setter in charge of set on or off 
        the entries acordingly to the check button status'''
        self.ch_init = __sel__
        for bck in range( len( self.ckb_c)):
            if __sel__[bck]:
                self.ckb_c[bck][1].select()
                for ent in range(len(self.ent_c[bck])):
                    self.ent_c[bck][ent].configure(state='normal')
            else:
                self.ckb_c[bck][1].deselect()
                for ent in range(len(self.ent_c[bck])):
                    self.ent_c[bck][ent].configure(state='disabled')

    def checkbuttonstuff(self):
        '''If this point is reached, some checkbutton changed,
        so this impose the available states'''
        auxi=-1
        loc = len(self._entries_)
        
        _ckvar_g_=[]
        ckbc_len = len(self.ckb_c)
        # First detect wich one change, comparing the fresh value
        for v in range(ckbc_len):
            _ckvar_g_.append(self.ckb_c[v][0].get())
            if self.ch_init[v]<>_ckvar_g_[v]:
                auxi=v
        
        if auxi>=loc and auxi == ckbc_len-1:
            num = ckbc_len - loc+1
            self.add_new_line(num)
            _ckvar_g_+=[0]
        
        self.set_ckbuttonstate(_ckvar_g_)
    
    
    def bottom_button_row(self):
        ''' just to order a little bit'''
        _br_ = Frame(self)
        b1 = Button(_br_, text='Save', command=(lambda: self.save_it()))
        b1.pack(side="right", padx=10, pady=20)
        b1.focus()
        
        b2 = Button(_br_, text='Quit', command=(lambda: self.exit_pop()))
        b2.pack(side="right", padx=10, pady=4)
        _br_.pack(side="bottom", expand=True)
        
    def save_it(self, event=None):
        
        g_names = []
        g_aids = []
        k_xyz_c = []
        runs_c = []
        lo = len(self._entries_)
        
        for g_e in range(len(self.ent_c))[:lo]:
            gr, ids, k_xyz, rns = get_entriesvalue( self.ent_c[g_e])
            
            #print gr, ids, k_xyz, self.ch_init[g_e]
            
            g_names.append(gr)
            g_aids.append(ids)
            k_xyz_c.append(k_xyz)
            runs_c.append(rns)
        self.master._aux_ = [[], None]
        self.master._aux_[0] = [ g_names, g_aids, k_xyz_c, runs_c,
                                self.ch_init[:lo] ]
        
        if len(self.ent_c)>lo and max(self.ch_init[lo:])>0:
            g_names = []
            g_aids = []
            k_xyz_c = []
            runs_c = []
            for g_e in range(len(self.ent_c))[lo:]:
                gr, ids, k_xyz, rns = get_entriesvalue( self.ent_c[g_e])
                g_names.append(gr)
                g_aids.append(ids)
                k_xyz_c.append(k_xyz)
                runs_c.append(rns)
            self.master._aux_[1] = [ g_names, g_aids, k_xyz_c, runs_c,
                                    self.ch_init[lo:] ]
        
        self.exit_pop() 

    def exit_pop(self):
        self.grab_release() # to return to normal
        self.destroy()# quit()

class AboutPopUp():
    '''
    there is a lot of work to do here also,
    but is a quite good and functional starting point...
    
    first put as child of Toplevel
    then change to grid
    '''
    def __init__(self, **kwargs):
        ''' (under development)'''
        
        master = None
        title = 'AboutPopUp'
        licence = None
        
        if 'master' in kwargs.keys():
            master = kwargs['master']
        if 'title' in kwargs.keys():
            title = kwargs['title']
        if 'licence' in kwargs.keys():
            licence = kwargs['licence']
            
        self.im_smlogo = PhotoImage( file= "./lib/gui/img/small_logo2.ppm")
        self.im_logo2 = PhotoImage( file= "./lib/gui/img/logo2.ppm")
        self.master  = master
        self._title_ = title
        self._licence_ = licence
        
        self.set_self_vertex()
        self.create_content()
    
    def set_self_vertex(self):
        
        ws, hs, w_main, h_main, x_main, y_main = self.master.MAINVERTEX
        # calculate the greatness
        w_pop = w_main
        h_pop = h_main*14/21
        
        x_pop = x_main + w_main + 30
        y_pop = y_main + h_main - h_pop - 140
        #print w_pop, h_pop, x_pop, y_pop
        self._vertex_= [w_pop, h_pop, x_pop, y_pop]

    def create_content(self):
        
        self.pop = Toplevel(self.master, bg = "white")
        self.pop.grab_set()# when you show the popup
        
        self.pop.wm_title(' '*5+self._title_)
        self.pop.geometry('{:d}x{:d}+{:d}+{:d}'.format(*self._vertex_))
        
        leftcolumn = Frame(self.pop ,bg = "white")
        Label(leftcolumn, bg = "white").pack(side="top", fill="both", pady=30)
        Label(leftcolumn, bg = "white",
              image= self.im_logo2).pack(side="top", fill="both", padx=10) #side= LEFT,
        leftcolumn.pack(side="left", fill='both', padx=1)
        
        
        rightcolumn = Frame(self.pop,bg = "white")
        firstrow = Frame(rightcolumn,bg = "white")
        Frame(rightcolumn,bg = "white").pack(side="top", pady=10 , padx=0)
        
        Label(firstrow, text="GROTOLAM",
                 fg = "Gray13", bg = "white" ,
                 font = "Verdana 13 bold").pack(side="left", pady=20)
        Label(firstrow, text='',bg = "white").pack(side="left", padx=40)
        firstrow.pack(side="top", padx=0)
        
        secrow = Frame(rightcolumn, bg = "white")
        Label(secrow, text="v "+__version__.split()[2],
                 fg = "Gray13",bg = "white" ,
                 font = "Verdana 10").pack(side="left")
        Label(secrow, text='',bg = "white").pack(side="left", padx=75)
        secrow.pack(side="top", padx=0)
        
        # lets create space to do some stuff ...
        Frame(rightcolumn,bg = "white").pack(side="top", pady=20 , padx=0)
        
        thirdrow = Frame(rightcolumn,bg = "white")
        
        Label(thirdrow, text="2018 Python version by",
                 fg = "Gray13", bg = "white",
                 font = "Verdana 10").pack(side="left")
        Label(thirdrow, text='',bg = "white").pack(side="left", padx=16)
        thirdrow.pack(side="top", padx=0)
        
        fourthrow = Frame(rightcolumn,bg = "white")
        Label(fourthrow, text="Hernan Chavez Thielemann",
                 fg = "Gray13", bg = "white",
                 font = "Verdana 10").pack(side="left")
        Label(fourthrow, text='',bg = "white").pack(side="left", padx=1)
        fourthrow.pack(side="top", padx=0)
        
        fifthrow = Frame(rightcolumn,bg = "white")
        Label(fifthrow, bg = "white",
              image= self.im_smlogo).pack(side="left", fill="both", padx=10)
        fifthrow.pack(side="top", padx=0)
        
        sixthrow = Frame(rightcolumn,bg = "white")
        href = Label(sixthrow, bg = "white", font = "Verdana 10",
                     text="Small web page", fg="blue",
                     cursor="hand2")
        f = Font(href, href.cget("font"))
        f.configure(underline = True)
        href.configure(font=f)
        href.pack(side="left")
        href.bind("<Button-1>", self.callback)
        
        Label(sixthrow, text='',bg = "white").pack(side="left", padx=40)
        sixthrow.pack(side="top", padx=0)
        
        lastrow = Frame(rightcolumn,bg = "white")
        self.bottom_button_row(lastrow)
        rightcolumn.pack(side="right", fill='both', padx=5)

    def callback(self, event):
        open_new(r"http://www.polito.it/small")
        
        
    def bottom_button_row(self, _row_):
        
        b2 = Button(_row_, text='Close',bg = "white", command= self.exit_pop)
        b2.pack(side="right", padx=10, pady=4)
        b1 = Button(_row_, text='Licence',bg="white",command= self._licence_)
        b1.pack(side="right", padx=10, pady=20)
        _row_.pack(side="bottom")
        
    def openlicence(self):
        
        print 'opening licence file'

    def exit_pop(self):
        self.pop.grab_release() # to return to normal
        self.pop.destroy()

class WarningPopUp2(PromptPopUp):

    def __init__(self, master = None, briefing=''):
        ''' (under development)
        '''
        PromptPopUp2.__init__(self, master, content = False)
            
        self._briefing_ = briefing
        self.wm_title(' '*30+'Warning! ')
        self._height_ = 100
        self.set_self_vertex()
        self.geometry('{:d}x{:d}+{:d}+{:d}'.format(*self._vertex_))
        
        self.create_content()
        

    def create_content(self, _txt_ = 'Texto de advertencia aqui'):
        _tr_ = Frame(self)
        label0= Label(_tr_, text = _txt_)
        label0.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        _tr_.pack(side="top", expand=True)
        self.bottom_button_row()
        

    def bottom_button_row(self):
        _br_ = Frame(self)
        b2 = Button(_br_, text='Ok', command= self.exit_pop )
        b2.pack(side="right", padx=10, pady=4)
        _br_.pack(side="bottom", expand = True)
        
# vim:tw=80

