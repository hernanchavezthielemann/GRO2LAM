#!/usr/bin/python
#    By Hernan Chavez Thielemann
__author__ = 'Hernan Chavez Thielemann <hchavezthiele at gmail dot com>'

from Tkinter import Entry, Button, Frame, StringVar
from tk_lib import format_dec
from popup import FilePopUp


class File_Entry(Frame):
    ''' Quite self explanatoy...
    creates a row in which is possible to search for a file'''
    def __init__(self, master=None, **kwargs):
        # this was a nice frame, but considering that needs 
        # from popup import FilePopUp, was moved elsewere
        # meaning this is not as low level as tk_lib
        
        #if not master and options.get('parent'):
        #    master = options['parent']
        self.master  = master
        Frame.__init__(self, master)
        
        self.entries_txt    = None
        self.entries_val    = None
        
        if 'e_txt' in kwargs.keys():
            self.entries_txt = kwargs['e_txt']
        if 'e_val' in kwargs.keys():
            self.entries_val = kwargs['e_val']
            
        # File extension
        if 'f_ext' in kwargs.keys():
            self.file_ext = kwargs[ 'f_ext']
        else:
            self.file_ext = ['.' + self.entries_val.split('.')[-1],]
        # File extension description
        if 'f_ext_d' in kwargs.keys():
            self.fex_description = kwargs[ 'f_ext_d']
        else:
            self.fex_description = [self.entries_txt,]
        
        # file icon image, part of the master's personal library
        self.file_img = self.master.img['file']
        # inner class object container
        self._entry = []
        self._button = []
        self._strvar = StringVar()
        
        self.createWidgets()
    
    def createWidgets(self):
        '''creates the row content and stores the
           objects
        '''
        # INIT
        file_row = Frame(self)
        fi_text     =   self.entries_txt
        _def_file_  =   self.entries_val
        f_ext_txt   =   ()
        for i in range(len(self.file_ext)):
            f_ext_txt += ((self.fex_description[i] , self.file_ext[i]),)
        
        # Building
        _f_labels = format_dec([file_row, fi_text], _pack_=False)

        self._entry = Entry(file_row, width=13, textvariable = self._strvar)
        self._entry.insert('end', _def_file_)
        
        self._entry.bind("<Key>", lambda e: "break") # Magic
        
        self._entry.xview_moveto(1)
        self._button = Button(file_row,
                         image= self.file_img,
                         command= ( lambda El = self._entry:
                                   self.browsefile(El, f_ext_txt))
                        )
        
        # Just packing
        format_dec(_f_labels, _create_=False)
        self._entry.pack(side='left', expand='yes', fill='x')
        self._button.pack(side='right', padx=0, pady=0)
        file_row.pack(side='top', fill='x', pady=3)
    
    def browsefile(self, entry, ext=None):
        '''Browse a file <button> action binder'''
        
        pop = FilePopUp( master = self)
        if ext<>None and isinstance(ext, tuple):
            #print '--- ', ext, type(ext)
            pop.filetypes['filetypes'] = ext #(("All","*"),) # 
        filepath = pop.getfilepath()
        
        try:
            fito = open(filepath,"r")
            fito.close()
            entry.delete(0, 'end')
            entry.insert(0, filepath)
            entry.xview_moveto(1)
        except:
            if filepath not in [ '', ()]:
                print "Could not open File: ", filepath
                print exc_info()[1]
    
    def setter(self, value):
        
        if value:
            self.enable_entr()
        else:
            self.disable_entr()
        
    def disable_entr(self):
        self._entry.configure( state = 'disabled')
        self._button.configure( state = 'disabled')

    def enable_entr(self):
        self._entry.configure( state = 'normal')
        self._button.configure( state = 'normal')

def createfileentry(frame, label_txt, entry_val, extension, ex_descrptn, flag):
    ''' creates a file entry and returns just the entry object'''
    FE = File_Entry( frame, e_txt = label_txt,
                     e_val = entry_val,
                     f_ext = extension,
                     f_ext_d = ex_descrptn
                   )
    FE.setter( flag )
    FE.pack(fill='x')
    return FE._entry
        
# vim:tw=80
