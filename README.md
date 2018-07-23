
[![Build Status](https://travis-ci.org/hernanchavezthielemann/GRO2LAM.svg?branch=20jul18)](https://travis-ci.org/hernanchavezthielemann/GRO2LAM)

# GRO2LAM
Gromacs to Lammps simulation converter

## Version:
   GROTOLAM version 1.11 (20 Jul 2018)
   
## Table of contents

<!--ts-->
   * [Version](#version)
   * [Table of contents](#table-of-contents)
   * [Authors](#authors)
   * [Description](#description)
   * [License](#license)
   * [Citation](#citation)
   * [Installation](#installation)
      * [Quantum start](#quantum-start)
      * [Quick start](#quick-start)
      * [Step by step](#step-by-step)
   * [Usage](#usage)
      * [GUI](#gui)
      * [GUI input data](#gui-input-data)
      * [Command line interface](#command-line-interface)   
   * [Files](#files)   
   * [Code Datastream Highlights](#code-datastream-highlights)
   * [Repository](#repository)   
<!--te-->

## Authors

- Python version:
    Hernan Chavez Thielemann

## Description
This program was designed for easy conversion of solvated structures between 
the GROningen MAchine for Chemical Simulations([Gromacs]) and the 
Large-scale Atomic Molecular Massively Parallel Simulator ([Lammps]). 
It is a python modular routine used to convert 5 [Gromacs] files to 2 [Lammps] format files,
this includes topology, force field coefficients and simulation commands.
   
## Licence
   [MIT](./LICENSE)
   Copyright 2018 Hernan Chavez Thielemann, Annalisa Cardellini, Matteo Fasano, Gianmarco Ciorra, Luca Bergamasco, Matteo Alberghini, Eliodoro Chiavazzo, Pietro Asinari
   
   This file is part of GROTOLAM.
   This work is also licensed under the Creative Commons Attribution 4.0 International License. 
   To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, 
   PO Box 1866, Mountain View, CA 94042, USA.

## Citation
   The publication associated with this code is found here:
   
   Hernan Chavez Thielemann, Annalisa Cardellini, Matteo Fasano, Gianmarco Ciorra, Luca Bergamasco, Matteo Alberghini, Eliodoro Chiavazzo, Pietro Asinari.


## Installation

### Quantum start:

    wget https://raw.githubusercontent.com/hernanchavezthielemann/utils/master/grotolam/G2L_installer && bash G2L_installer
    
### Quick start:

    #!/bin/bash
    wget https://github.com/hernanchavezthielemann/GRO2LAM/archive/20jul18.zip
    unzip 20jul18.zip
    cd GRO2LAM-*
    python setup
    ./run


### Step by step:

Download from:

https://github.com/hernanchavezthielemann/GRO2LAM/archive/20jul18.zip

Unpack, or you can open a terminal and then execute:
    
    ~$ wget https://github.com/hernanchavezthielemann/GRO2LAM/archive/20jul18.zip
    ~$ unzip master.zip
    
Then, make sure that terminal is in the GROTOLAM folder. As example:
    
    user@system:~/Downloads/GRO2LAM-20jul18$
    
Once there, execute the setup file through the terminal as:
    
    ~$ python setup
Then, without changing the folder, execute the run script:
    
    ~$ ./run
After that an intuitive graphical user interface should appear.


## Usage

### GUI
   Follow the secuential menu bar.
   
   <p align="center">
   <img src="https://i.imgur.com/gbI5H7y.gif" title="source: imgur.com" />
   </p>
   
   This will create [Lammps] simulation files with setup parameters inherited from [Gromacs].

### GUI input data
In this section, every possible data to input is described (the entries required by the GUI).

  #### Lammps data file generation:
   > Enter the gro file

   Gromacs .gro file with all the system coordinates, and the box size specified at the end
   > Enter the top file
   
   Gromacs .top file with [ moleculetype ], [ atoms ], [ bonds ], [ pairs ], [ angles ], [ dihedrals ], [ system ] and [ molecules ]. Any #include is omitted. In the atoms section atleast one atom should be declared.   
   > Enter the forcefield file
   
   Gromacs forcefield.itp file with [ defaults ] section, also with nbfun, comb-rule, gen-pairs, fudgeLJ and fudgeQQ columns. Any #include or #define is omitted.
   
   > Enter the non bonded file
   
   Gromacs forcefield_nonbonded.itp file with [ atomtypes ]. Where [ nonbond_params ] and [ pairtypes ] are ignored.
   > Enter the bonded file
   
   Gromacs forcefield_bonded.itp file with [ bondtypes ], [ angletypes ] and [ dihedraltypes ].
   > Choose an atom style
   
   Atom style accordingly to lammps styles, in this software can be full, charge, molecular, angle, bond and atomic.
   
   > Solvation atoms
   
   >> yes: water atoms are taken into account and water configuration popup is enabled as a must.
   
   generally the following data comes from the water.stp
   >>> O in the non bonded file
   
   Name of the oxigen in the non bonded itp file
   >>> H in the non bonded file
   
   Name of the hydrogen in the non bonded itp file
   >>> O in the .gro file
   
   Name of the oxigen in the gro file
   >>> H in the .gro file
   
   Name of the oxigen in the gro file
   >>> H - O partial charge
   
   Partial charge increment magnitude from H to O, equal to the whole H charge or the half of O.
   
   At this poit without saving you cannot go on.
   
   >> no: just the core particle is converted.
   
  #### Lammps input file generation:
  
  
  
  #### Lammps simulation launching:
This GUI is mainly to test the congruency of the lammps data and input file.

>Select the script to run

A valid input data file to run
>Machine

According the one installed in your computer, you can select the lammps machine.
>Cores

According to your needs and computer capacity, you can select the amount of cores to launch your simulation.

### Command line interface
   There is no implementation of comand line interface, more than:
   ```bash
   ~$ python setup -t
   ```
   That creates a not fully useful test GUI.

# Files:

    ./run
    ./lib/README.md
    ./lib/LICENSE
    ./lib/setup
    ./lib/gui/__init__.py
    ./lib/misc/data.py
    ./lib/docs/COPYING.LESSER
    ./lib/misc/file.py
    ./lib/gui/img/help.ppm
    ./lib/misc/version.py
    ./lib/__init__.py
    ./lib/handling/gromacs.py
    ./lib/gui/img/gear.ppm
    ./lib/gui/conversion_gui.py
    ./lib/gui/img/small_logo2.ppm
    ./lib/handling/__init__.py
    ./lib/misc/__init__.py
    ./lib/grotolam.py
    ./lib/gui/img/logo2.ppm
    ./lib/gui/main_gui.py
    ./lib/misc/warn.py
    ./lib/gui/run_gui.py
    ./lib/handling/lammps.py
    ./lib/gui/img/logo.ppm
    ./lib/docs/COPYING
    ./lib/gui/script_gui.py
    ./lib/gui/popup.py
    ./lib/gui/img/README.md
    ./lib/gui/tk_lib.py
    ./lib/docs/README.md
    ./lib/gui/img/file.ppm

# Code Datastream Highlights:

In this section, every important routine is described.


> run

Starts grotolam calling grotolam_launcher() function in grotolam.py

> grotolam.py

Works as cap of the library and calls the GUI (main_gui.py)

> main_gui.py

Background window, it handles the three different stages in the menu bar plus the help button.
Relyes in conversion_gui.py, script_gui.py, run_gui.py, popup.py and tk_lib.py.

```
CLASSES
    Tkinter.Frame(Tkinter.Widget)
     |  Gro2Lam_GUI
     |      Graphic User Interface
     |  
     |  Methods defined here:
     |  
     |  browsefile(self, entry, ext=None)
     |      Browse a file <button> action binder
     |  
     |  create_conversion_gui(self)
     |      Hook to create conversion gui
     |  
     |  create_run_gui(self)
     |      Hook to create run gui
     |  
     |  create_script_gui(self)
     |      Hook to create script gui
     |  
     |  createfileentry(self, parent_frame, fi_text, _def_fi_, **kwargs)
     |      Quite self explanatoy...
     |      creates a row in which is possible to search for a file
     |  
     |  createmainPennon(self)
     |      Self explanatory neated with subroutines to make it more readable
     |  
     |  quit_hook(self, event=None)
     |  
     |  swap_hook(self)
     |  
     |  swapbody(self, _pbody_)
     |      Deletes and clean the last generated body
```

> conversion_gui.py

```
CLASSES
    Tkinter.Frame(Tkinter.Widget)
class Conversion(Tkinter.Frame)
     |  Script creation graphical user interface.
     |  Methods defined here:
     |  
     |  __init__(self, master=None, **options)
     |  
     |  atomstyle(self)
     |      in this case just one, but could be modified 
     |      to be generic, accepting <row>, <text> and <options>
     |  
     |  build_finalbuttons(self)
     |  
     |  build_solvation_section(self)
     |  
     |  check_solvation_inputs(self, _app_aux_, _vbs_=False)
     |  
     |  config_solvation(self)
     |  
     |  createWidgets(self)
     |  
     |  create_conversion_gui(self)
     |  
     |  get_entriesvalues(self)
     |      ---   app entry getter   ----
     |      mainly to obtain values beside check buttons
     |  
     |  getdata_and_convert(self)
     |  
     |  radio_part(self, _s_row_, _text_, _desc_=[''], _vals_=[])
     |  
     |  solvastuff(self)
     |      If this point is reached, some button changed
```

> script_gui.py

```
CLASSES
    Tkinter.Frame(Tkinter.Widget)
        Script_GUI
    
    class Script_GUI(Tkinter.Frame)
     |  Script creation graphical user interface.
     |  Methods defined here:
     |  
     |  __init__(self, master=None, **options)
     |  
     |  build_finalbuttons(self)
     |      Final Buttons section builder
     |  
     |  check_datafile(self, _bflag_=None)
     |      function to get the max atom number 
     |      also is used in case of no gromacs direct data conversion
     |      to somehow make a check if that file is ok
     |  
     |  config_restrain(self)
     |  
     |  createWidgets(self)
     |      create the script gui
     |  
     |  createWidgets_n_pack(self)
     |  
     |  create_main_section(self)
     |      Section for main input values
     |  
     |  further_config_script(self)
     |  
     |  write_script(self)
```
> run_gui.py

```
CLASSES
    Tkinter.Frame(Tkinter.Widget)
        Run_GUI
    
    class Run_GUI(Tkinter.Frame)
     |  Run script graphical user interface.
     |  Methods defined here:
     |  
     |  __init__(self, master=None, **options)
     |  
     |  build_finalbuttons(self)
     |      Final Buttons
     |  
     |  createWidgets(self)
     |      create the script gui
```
> popup.py

This file neats everything that comes out as a PopUp

```
CLASSES
    Tkinter.Frame(Tkinter.Widget)
        FilePopUp
        Message_box
    Tkinter.Toplevel(Tkinter.BaseWidget, Tkinter.Wm)
        PromptPopUp
            WarningPopUp2
        PromptPopUp_wck
    AboutPopUp
    PromptPopUp_old
    SaveAsPopUp

FUNCTIONS
    message_box(message='', title='Message box', **options)
         Creates a message box through the implementation of an instance
         of class Message_box, these messages can be info, warning and error
```        

> tk_lib.py

Home made tkinter library

```
CLASSES
    Tkinter.Widget(Tkinter.BaseWidget, Tkinter.Pack, Tkinter.Place, Tkinter.Grid)
        Drop_Down_List

class Drop_Down_List(Tkinter.Widget)
     |  The lean version of the Ttk Combobox from ttk library
     |  
     |  Methods defined here:
     |  
     |  current(self, newindex=None)
     |  
     |  set(self, value)

FUNCTIONS
    bottom_hline_deco(row, func=None)
        adds a sunken line in the bottom of a tkinter function
    
    create_check_row(_s_row_, _text_, func, _desc_=[''])
        creates a tkinter entry with a check button

    create_entry(_main_row_, _desc_txt, _def_txt_, t_len, ckbc=None, fn=None)
        creates a tkinter entry
    
    create_file_entry(_master_, ups_frame, fi_text, _default_file)
        Quite self explanatoy...
        creates a row in which is possible to search for a file
    
    createmenubar(_root_window_, _listofentriesdicts_)
        under development 
        input format example: 
            <class app>
            [{ 'title' : 'Title1', 'title_com' : (print , '>command11<') },
            { 'title' : 'Title2',
            'cascade' : (('cnd_label' ,'>command31<'),('cnd_label' ,'>command33<'),
            ('separator'),('cnd_label' ,'>command33<'))}]
    
    format_dec(_rnt_or_lc_, _create_=True, _pack_=True, _lastline_=True)
        can be re-thought as a function wrapper
        furthermore as a class... but for now works perfect
    
    generate_listbox(row, fill_list)
    
    get_entriesvalue(entries_container)
        ---   entry getter app ----
        mainly to obtain values of entries
 ```   


## Repository:
   https://github.com/hernanchavezthielemann/GRO2LAM



[Lammps]: http://lammps.sandia.gov/
[Gromacs]: http://www.gromacs.org/
