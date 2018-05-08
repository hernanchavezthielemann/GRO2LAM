[![Build Status]()]

# GRO2LAM
Gromacs to Lammps simulation converter



## Authors

- Python version:
    Hernan Chavez Thielemann

- Matlab version:


## Description
This program was designed for easy conversion of solvated structures between 
the GROningen MAchine for Chemical Simulations([Gromacs]) and the 
Large-scale Atomic Molecular Massively Parallel Simulator ([Lammps]).

## Installation

### Quantum start:

    wget https://raw.githubusercontent.com/hernanchavezthielemann/utils/master/grotolam/G2L_installer
    bash G2L_installer
    
### Quick start:

    #!/bin/bash
    wget https://github.com/hernanchavezthielemann/GRO2LAM/archive/07may18.zip
    unzip master.zip
    cd GRO2LAM-*
    python setup
    ./run


### Step by step:

Download from:

https://github.com/hernanchavezthielemann/GRO2LAM/archive/master.zip

Unpack, or you can open a terminal and then execute:
    
    ~$ wget https://github.com/hernanchavezthielemann/GRO2LAM/archive/master.zip
    ~$ unzip master.zip
    
Then, make sure that terminal is in the GROTOLAM folder. As example:
    
    user@system:~/Downloads/GRO2LAM-master$
    
Once there, execute the setup file through the terminal as:
    
    ~$ python setup
Then, without changing the folder, execute the run script:
    
    ~$ ./run
After that an intuitive graphical user interface should appear


## Usage

## # GUI
   Follow the secuential menu bar.
   
   This will create [Lammps] simulation files with setup parameters inherited from [Gromacs].
    
## # Command line interface
   there is no implementation of comand line interface


## Licence
   MIT
   This work is also licensed under the Creative Commons Attribution 4.0 International License. 
   To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, 
   PO Box 1866, Mountain View, CA 94042, USA.

## Citation
   The publication associated with this code is found here:



[Lammps]: http://lammps.sandia.gov/
[Gromacs]: http://www.gromacs.org/
