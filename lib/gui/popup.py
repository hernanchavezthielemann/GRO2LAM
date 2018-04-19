#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'

from Tkinter import Frame, Toplevel, Label, Button, SUNKEN, X, Y, PhotoImage
from tk_lib import create_entry, bottom_hline_deco, get_entriesvalue
from tkFont import Font
from webbrowser import open_new

class FilePopUp():# checked ok 16/09 -----------WF
    '''Neat & tidy pop up to search files'''
    
    def __init__(self, master=None):
        self.master  = master
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
        try:
            aux = Frame(self.master)
            userchoice = aux.tk.call("tk_getOpenFile", *aux._options(self._options_))
            try:
                userchoice = userchoice.string
            except AttributeError:
                pass
        finally:
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
        print 'Soon ...'
        
    @property
    def options(self):
        return self._options
    @options.setter
    def options(self, **value):
        self._options = value

class PromptPopUp():
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

class PromptPopUp2(Toplevel):

    def __init__(self, master = None, **kwargs):
        ''' (under development)'''
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
        
        self.create_content()
        self.grab_set()# when you show the popup
    
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
        for e in range(len(self._entries_)):
            self.ent_c.append(create_entry(row2fill,
                                           self._entries_[e],
                                           self._defvals_[e],
                                           self.entr_maxlen)
                             )
        row2fill.pack(side="top", padx=1, pady=5)
        
        self.bottom_button_row()        

    def bottom_button_row(self):
        ''' just to rder a little bit'''
        _br_ = Frame(self)
        b1 = Button(_br_, text='Save', command=(lambda: self.save_it()))
        b1.pack(side="right", padx=10, pady=20)
        b2 = Button(_br_, text='Quit', command=(lambda: self.exit_pop()))
        b2.pack(side="right", padx=10, pady=4)
        _br_.pack(side="bottom", expand=True)
        
    def save_it(self):
        self.master._aux_ = get_entriesvalue( self.ent_c)
        self.exit_pop() 

    def exit_pop(self):
        self.grab_release() # to return to normal
        self.destroy()# quit()

class AboutPopUp():
    '''
    there is a lot of work to do here also,
    but is a quite good and functional starting point
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
        from main_gui import MAINVERTEX
        ws, hs, w_main, h_main, x_main, y_main = MAINVERTEX
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
        Label(secrow, text="v 1.0",
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

# vim:tw=80
