 
python 2.7: [![Build Status](https://travis-ci.org/hernanchavezthielemann/GRO2LAM.svg?branch=27ene19)](https://travis-ci.org/hernanchavezthielemann/GRO2LAM)

# GRO2LAM
   Gromacs to Lammps simulation converter
   
   <p align="center">
   <img src="https://i.imgur.com/fEVcyxY.gif" title="source: imgur.com" />
   </p>


## Version

   ### Stable
   GRO2LAM version 1.25 (27 Jan 2019) - BETA
   
   ### Beta-Stable
   GRO2LAM version 1.3 (06 Jan 2021) - BETA-beta (Python 3 compatible)
   
    wget https://raw.githubusercontent.com/hernanchavezthielemann/utils/master/grotolam/G2L_iBeta && bash G2L_iBeta
   
   
   
   :new:New features : 
<!--ts-->
   * Option to autoload 'itp' force field files, including side molecules.
   * Works with more than one side molecule (eg. water + ions +...).
   * Accepts Ryckaert-Bellemans dihedral, direct conversion to opls dihedral Lammps style.
   * Accepts #define tag in dihedrals in the 'top' file.
   * Accepts improper dihedral type. (:warning:under tests:wrench:)
   * Accepts G96 bond and angle types. (:warning:under tests:wrench:) 
   * Accepts GROMOS force field define. (:warning:under tests:wrench:)
   * Accepts AMBER Periodic improper dihedral. (:warning:under tests:wrench:) 
   * Accepts AMBER Proper dihedral (multiple). (:warning:under tests:wrench:)
   * :new: Python 3 compatible
<!--te-->
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
   - Python coding:
       Hernan Chavez Thielemann  
   - Protocol definition:
       Gianmarco Ciorra, Matteo Fasano, Annalisa Cardellini, Luca Bergamasco, Hernan Chavez Thielemann

## Description
   This program was designed for easy conversion of solvated structures between 
   the GROningen MAchine for Chemical Simulations ([Gromacs]) and the 
   Large-scale Atomic Molecular Massively Parallel Simulator ([Lammps]). 
   It is a python 2.7 modular routine used to convert [Gromacs] input files to [Lammps] input files,
   which include topology, force field coefficients and simulation commands.
   
## License
   [MIT](./LICENSE)
   Copyright 2018 Hernan Chavez Thielemann, Annalisa Cardellini, Matteo Fasano, Gianmarco Ciorra, Luca Bergamasco, Matteo Alberghini, Eliodoro Chiavazzo, Pietro Asinari

## Citation
   The publication associated with this code is found here: [s00894-019-4011-x]
   
   Hernán Chávez Thielemann, Annalisa Cardellini, Matteo Fasano, Luca Bergamasco, Matteo Alberghini, Gianmarco Ciorra, Eliodoro Chiavazzo, Pietro Asinari. From GROMACS to LAMMPS: GRO2LAM A converter for molecular dynamics software.  Journal of Molecular Modeling (2019) 25: 147.

## Installation
   To download the latest version there are at least three ways:

### Quantum start
   Copy&paste the following command in your bash console and execute it, this will download and execute Grotolam in about 5 seconds:

    wget https://raw.githubusercontent.com/hernanchavezthielemann/utils/master/grotolam/G2L_installer && bash G2L_installer
    
E.g.
    
<!--ts-->
 * First create a folder in your desktop (lets say "Untitled Folder")
 * Inside that folder open a terminal ( in Ubuntu: right click inside the folder-space to open a context menu > Open in Terminal )
 * In that terminal copy&paste the previous "quantum start" command:
     
       wget https://raw.githubusercontent.com/hernanchavezthielemann/utils/master/grotolam/G2L_installer && bash G2L_installer
 
 * Then hit intro key to start the setup
 * If you have no errors, at this point a folder called GRO2LAM-27ene19 should exist in a path like:
 
       /home/*YourUser*/Desktop/Untitled Folder/GRO2LAM-27ene19
         
 * Now, inside that folder it is possible to find the "run" file,  that was generated during the setup.
 * To run this file open a terminal in that folder, and execute *./run* or *python run*
<!--te-->
    
### Quick start
   Download the compressed package of GRO2LAM:
   
     wget https://github.com/hernanchavezthielemann/GRO2LAM/archive/27ene19.zip
  
   Decompress it:
   
     unzip 27ene19.zip
   
   Make sure that terminal is in the GRO2LAM folder, then:
   
     cd GRO2LAM-*
   
   Execute the setup file through the terminal as follows:
   
     ~/Desktop/GRO2LAM-27ene19$python setup
   
   Then, without changing the folder, execute the run script:
   
     ~/Desktop/GRO2LAM-27ene19$./run
  
   After that, an intuitive graphical user interface should appear.

### Step by step
   The download page of GRO2LAM can be found at the following link:

     https://github.com/hernanchavezthielemann/GRO2LAM/archive/27ene19.zip

   The installation package can be downloaded through the bash console as:

    ~$ wget https://github.com/hernanchavezthielemann/GRO2LAM/archive/27ene19.zip
    
   This will download a zipped file, that you can uncompress with right click or with the command:

    ~$ unzip 27ene19.zip
    
   Then, make sure that terminal is in the GROTOLAM folder. For example:
    
    user@system:~/Downloads/GRO2LAM-27ene19$
    
   Once there, execute the setup file through the terminal as:
    
    ~$ python setup
   
   Then, without changing the folder, execute the run script:
    
    ~$ ./run
    
   After the ./run command, an intuitive graphical user interface should appear.
   This GUI interface will guide the user through all the inputs needed to perform the conversion correctly, as shown in the next section.

## Usage

 To perform the conversion, there are two ways to proceed:
   
   The "easy one":
   
   <!--ts-->
   * First select the gro and top files.
   * Then press the autoload button.
   * Finally press the convert button,  you can press this last one using space-key also.
   <!--te-->
   
   The second option would be:
   
   <!--ts-->
   * First select gro and top files
   * Then select the itp files containing the defaults, atomtypes and bondtypes directives.
   * Finally press the convert button,  you can press this last one using space-key also.
   <!--te-->
   
### GUI
   In the GIF below, the typical protocol to convert Gromacs input file into Lammps input files is summed up.
   
   <p align="center">
   <img src="https://i.imgur.com/gbI5H7y.gif" title="source: imgur.com" />
   </p>
   
   This procedure will create [Lammps] simulation files with setup parameters inherited from [Gromacs] input files.

### GUI input data
   In this section, the simulation data that can be imported are listed (that is the entries required by the GUI).

  #### Lammps data file generation:
   > Enter the gro file
   
   Gromacs .gro file with the system coordinates, and the box size specified at the end of file.
   
   > Enter the top file
   
   Gromacs .top (topology) file with [ moleculetype ], [ atoms ], [ bonds ], [ pairs ], [ angles ], [ dihedrals ], [ system ] and [ molecules ]. Any #include is omitted. In the atoms section, at least one atom should be declared.
   
   > Enter the forcefield file
   
   Gromacs forcefield.itp file with [ defaults ] section, also with nbfun, comb-rule, gen-pairs, fudgeLJ and fudgeQQ columns. Any #include or #define is omitted.
   
   > Enter the non bonded file
   
   Gromacs forcefield_nonbonded.itp file with [ atomtypes ], where [ nonbond_params ] and [ pairtypes ] are ignored.
   
   > Enter the bonded file
   
   Gromacs forcefield_bonded.itp file with [ bondtypes ], [ angletypes ] and [ dihedraltypes ].
   
   > Choose an atom style
   
   Atom style according to Lammps styles, which can be full, charge, molecular, angle, bond and atomic.
   
   > Solvation atoms
   
   >> yes
   
   Water atoms are taken into account, and water configuration popup is enabled.
   
   >> Configuration Popup
   
   The following data can be extracted from the water_model.itp according the user chosen model. 
   
   >>> O in the non bonded file
   
   Label for the oxigen atom in the non bonded .itp file.
   
   >>> H in the non bonded file
   
   Label for the hydrogen atom in the non bonded .itp file.
   
   >>> O in the .gro file
   
   Label for the oxigen atom in the .gro file.
   
   >>> H in the .gro file
   
   Label for the hydrogen atom in the .gro file.
   
   >>> H - O partial charge
   
   Partial charge increment magnitude from H to O, equal to the whole H charge (or the half of O).
   
   After inserting the solvation parameters, data must be saved by clicking on the Save button.
   
   >> no
   
   Solvation molecules are not converted by GRO2LAM.
   
  #### Lammps input file generation:
  
  ##### Main page
  >Timestep [fs]
  
  The simulation time step, expressed in femtoseconds (floating point number).
  
  >NVE steps  [#ts]
  
  Number of steps in the NVE ensembles (integer number).
  
  >NVT steps  [#ts]
  
  Number of steps in the NVT ensembles (integer number).
  
  >Temperature at start:end [K]
  
  Temperature gradient to apply in the NVT ensemble, as start_temperature:ending_temperature (floating point numbers).
 
  >Temperature damping [fs]
  
  Characteristic time constant of the thermostat.
  
  >NPT steps  [#ts]
  
  Number of steps in the NPT ensembles (integer number).
  
  >Pressure at start:end  [atm]
  
  Pressure gradient to apply in the NPT ensemble, as start_presure:ending_presure (floating point numbers).
  
  >Pressure damping [fs]
  
  Characteristic time constant of the barostat.
  
  >Temperature at start:end [K]
  
  Same thing that in the NVT case, but for the thermostat coupled with the barostat in the NPT runs.
  
  >Temperature damping [fs]
  
  Same thing that in NVT, but for the thermostat coupled with the barostat in the NPT runs.
  
  ##### Advanced Settings
  Section to change further default simulation parameters. 
  
  >Thermo output every  [#ts]
  
  Print thermodynamic info on time steps that are a multiple of this number of time steps.
  >Atom mapping
  
  Array, in each processor stores a lookup table of length as the atoms in the system, else, hash value uses a hash table, being slower.
  >Pairwise interactions
  
  To set wich set of formulas will LAMMPS use to compute pairwise interactions. (where, cut = cut off distance, long = long-range interactions, coul = Coulombics and zero = do not compute any pairwise and build neighbor list)
  >L-J/Buck rcutoff  [Å]
  
  Global cut off distance in Angstrom for Lennard Jones or Buckingham interactions.
  >Coulomb rcutoff  [Å]
  
  Global cutoff distance in Angstrom for Coulombic interactions.
  >Neighbor skin distance  [Å]
  
  Extra skin distance beyond force cutoff in Angstrom.
  >Long-range solver
  
  Define a long-range solver to use each timestep to compute long-range Coulombic and/or 1/r^6 interactions.
  >Long-range relative error
  
  Desired relative RMS error in per-atom forces calculated by the long-range-solver.
  >Interaction 1-2:1-3:1-4
  
  Sets weighting coefficients for pairwise contributions between atoms that are permanently bonded to each other.
  The 1st of the 3 numbers is the factor on 1-2 atom pairs, atoms directly bonded to each other. The 2nd number is the factor on 1-3 atom pairs which are separated by 2 bonds or 1 angle. And the 3rd is the factor on 1-4 atom pairs which are those separated by 3 bonds or 2 angles.
  >Neighbor delay  [#ts] 
  
  Delays the building until this many time steps since last build.
  >Neighbor update  [#ts]
  
  Build the neighbor list every this many time steps.
  >Pressure control
  
  To specify an isometric or anisometric external stress tensor in the constant-pressure simulation adjust 3 dimensions. In triclinic simulation boxes adjust 6 dimensions.
  >Force mixing rule  
  
  Mixing rule that affects pair coefficients for pairwise interactions, mixing the "Pair Coeffs" of the data file, according to geometric, arithmetic or sixth power combination formulas.
  >Velocity creation Temp  [K]
  
  Set the velocities of all atoms in the system as the specified temperature demands.
  >Energy minimization tolerance
  
  Stopping tolerance for force (force units) when an energy minimization of the system is performed.
  >Simulation order
  
  The order in which the simulated ensembles perform. The possible keys are: NVE, NVT, NPT, R and M. The key R stands for restart point and M stands for energy minimization. The different components must be separated by a minus dash, as example NVE-M-M-NVT-NPT-NPT-NVT.
  >Shake tolerance
  
  Accuracy tolerance of SHAKE solution for 20 iterations.
  >Shake bonds [b#]
  
  Bond types that will be constrained.
  >Shake angles [a#]
  
  Angle types that will be constrained.
  ##### Restraint
  Definition of the harmonic potentials to restrain some groups of atoms in their initial positions. 
  
  #### Lammps simulation launching:
  This GUI can be employed to test the congruency of the Lammps data and input files.

  >Select the script to run
  
  A valid input data file to run.

  >Machine
  
  Select the Lammps run file, according to the version installed on the local machine.

  >Cores
  
  Select the amount of computational cores to be used for the Lammps simulation, according to the characteristics of the local machine.

### Command line interface
   Currently, there is no implementation of command line interface. The only available command is:
   ```bash
   ~$ python setup -t
   ```
   that creates a test GUI.

# Files

    ./run
    ./lib/README.md
    ./lib/LICENSE
    ./lib/setup
    ./lib/gui/__init__.py
    ./lib/misc/data.py
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
    ./lib/gui/custom_row.py
    ./lib/gui/script_gui.py
    ./lib/gui/popup.py
    ./lib/gui/img/README.md
    ./lib/gui/tk_lib.py
    ./lib/docs/README.md
    ./lib/gui/img/file.ppm

# Code Datastream Highlights
  In this section, the most important routines in the GRO2LAM package are described.

  > run
  
  Starts GRO2LAM calling grotolam_launcher() function in grotolam.py.

  > grotolam.py
  
  Works as cap of the library, and calls the GUI (main_gui.py).

  > main_gui.py
  
  Background window, it handles the three different stages in the menu bar as well as the help button. It relies on conversion_gui.py, script_gui.py, run_gui.py, popup.py and tk_lib.py.

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
     |      Hook to create conversion GUI
     |  
     |  create_run_gui(self)
     |      Hook to create run GUI
     |  
     |  create_script_gui(self)
     |      Hook to create script GUI
     |  
     |  createfileentry(self, parent_frame, fi_text, _def_fi_, **kwargs) 
     |      Creates a row in which it is possible to search for a file
     |  
     |  createmainPennon(self)
     |      Improve readibility
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
     |      In this case just one, but it could be modified 
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
     |      Mainly to obtain values beside check buttons
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
     |      Function to get the max atom number 
     |      It is also used in case of no Gromacs direct data conversion
     |      to make a check if that file is ok
     |  
     |  config_restrain(self)
     |  
     |  createWidgets(self)
     |      Create the script GUI
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

This file neats everything that comes out as a popup.

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
         of class Message_box. These messages can be info, warning and error
```        

> tk_lib.py

Home made tkinter library.

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
        Adds a sunken line in the bottom of a tkinter function
    
    create_check_row(_s_row_, _text_, func, _desc_=[''])
        Creates a tkinter entry with a check button

    create_entry(_main_row_, _desc_txt, _def_txt_, t_len, ckbc=None, fn=None)
        Creates a tkinter entry
    
    create_file_entry(_master_, ups_frame, fi_text, _default_file)
        Creates a row in which is possible to search for a file
    
    createmenubar(_root_window_, _listofentriesdicts_)
        Under development. 
        Input format example: 
            <class app>
            [{ 'title' : 'Title1', 'title_com' : (print , '>command11<') },
            { 'title' : 'Title2',
            'cascade' : (('cnd_label' ,'>command31<'),('cnd_label' ,'>command33<'),
            ('separator'),('cnd_label' ,'>command33<'))}]
    
    format_dec(_rnt_or_lc_, _create_=True, _pack_=True, _lastline_=True)
        Can be re-thought as a function wrapper or as a class... but for now works perfectly
    
    generate_listbox(row, fill_list)
    
    get_entriesvalue(entries_container)
        ---   entry getter app ----
        Mainly to obtain values of entries
 ```   


## Repository:
   https://github.com/hernanchavezthielemann/GRO2LAM


[s00894-019-4011-x]: https://doi.org/10.1007/s00894-019-4011-x
[Lammps]: http://lammps.sandia.gov/
[Gromacs]: http://www.gromacs.org/
