/TODO: update 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   GROTOLAM v:1.0   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Matlab modular routine used to convert GROMACS input files to LAMMPS format.


The process can be started lauching "General.m". The same folder must contain also "main.m",
"Counting_lines" "Reading_bon.m", "Reading_nb", "Reading_top.m", "Reading_xyz.m", "Write_Geometry.m"
and "Writing_input.m". The same folder must also contain the following GROMACS input files to be
converted: a topology file ".top", two ".itp" files for bonded and non-bonded interactions and 
a coordinate file ".gro".

GUI interfaces will guide the user through all the inputs needed to perform the conversion correctly. 
In the following, every routine is described, explaining the several input and output arguments, 
the entries required by the GUI and the mathematical models supported by the code. In the folowing, 
a warning will follow every section where some features aren't already implemented or where some 
default parameters has to be changed by the user directly in the code instead of recurring to the GUI interface.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   License   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Copyright 2017 Annalisa Cardellini, Hernan Chavez Thielemann,
Matteo Fasano, Gianmarco Ciorra, Luca Bergamasco,
Matteo Alberghini, Eliodoro Chiavazzo, Pietro Asinari

This file is part of GROTOLAM.
This work is licensed under the Creative Commons Attribution 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, 
PO Box 1866, Mountain View, CA 94042, USA.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   General.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Main script to lauch the conversion. The inputs required from the user by the GUI are:

(I) ATOM STYLE, the description of the current system.
    (i) Atomic: Van der Waals interactions are the only one considered;
    (ii) Angle: only considers van der Waals interaction, linear bonds and angle potentials;
    (iii) Full: complete parametrization of a model. Considers van der Waals and Coulomb as non-bonded interactions 
                and linear bonds angle and dihedral potentials.

(II) SOLVATION:
    (i) Yes:    if a solvent is present in the box, its atoms names and numbers will be transcripted as well as their 
                bond and non-bond interactions;
    (ii) No:    no solvent conversion.

                              !!!!!  WARNING  !!!!!
Only SPC and SPC/E water models are available in the current verson of GROTOLAM.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   main.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Matlab function used to read the input parameters of the force field and initial coordinates of the atoms. 
All the following reading and writing routines are called by this function. As reminded in the warning section, 
some default inputs have to be manually changed directly in this code. 

The input required by the user are:

(I) PARAMETRIZATION:
    (i) Yes: the force field paramenters are read from the topology ".top" file;
    (ii) No: the force field paramenters are read from two ".itp" files.

(II) INPUT NAME: the user can specify the GROMACS input file names. Default names are already provided.

(III) WATER NAME: GUI interface used to identify the solvent atoms and their coded name in the ".gro" file in order 
                  to assing them their correct physical properties, bond and non-bonded parameters.

                              !!!!!  WARNING  !!!!!
Since the current version of GROTOLAM supports only the conversion of SPC and SPC/E water, any entry corresponding 
to different solvents leads to a program failure.
Default LAMMPS input parameters controlling timestep, neighbors list settings, cut-off radius for non-bonded 
interactions and the number of dimensions of the simulation must be changed manually fromline 170 to line 176.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Reading_nb.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Matlab function used to read the non-bonded parameters from the ".itp" file.
The function saves in a numerical matrix the mass, charge and SIGMA-EPSILON parameters of the LJ potential of 
the atoms composing the system, solvent included. The potential can be given in the Buckingham form.

LJ: V(r_ij) = 4*EPSILON*[(SIGMA/r_ij)^12 - (SIGMA/r_ij)^6]
BUCKINGHAM: V(r_ij) = (A*e^(-r_ij/RHO) - C/(r_ij)^6

INPUT: 
    (i) filename_nb:    character string containing the non-bonded ".itp" file name;
    (ii) formatspec:    character string setting the format of the interaction parameters of interest. This input is 
                        automatically set.
    
OUTPUT:
    (i) atom_inbondtype: cell array containing the atom types names found in the ".itp" file;
    (ii) mass_type: numerical array containing the mass of each atom type identified;
    (iii) pot1: numerical array containing the first potential parameter, 
                SIGMA if the interaction is LJ or A if Buckingham;
    (iv) pot2:  numerical array containing the second potential parameter, 
                EPSILON if the interaction is LJ or C if Buckingham;
    (v) pot3:   numerical array containing the third potential parameter for Buckingham potential, RHO. 
                This array has "NaN" entries if the potential is given in the LJ form.
    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Reading_bon.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Matlab function used to read bond, angle and dihedral potential parameters. 
The bond types are supposed to be expressed by a maximum of 3 parameters, otherwise other specifications 
can be added in the proper format specifier, line 42 if "main.m", 
The equation of this interaction is expressed through a coded number, "func".
i.e. code number "1" refers to the equation: Vb(r_ij)=0.5*K*(r_ij- R0_ij)^2 .

The angle interactions can be expressed by a maximum of 4 numerical parameters. Like the previous interaction, 
the possible potential equations are referred to by a coded number, "func".
i.e. code number "1" refers to the equation: Va(theta_ij)=0.5*K*(theta_ij- T0_ij)^2 .

The dihedral interactions are expressed by a maximum of 4 numerical parameters, depending on the formulation choosen. 
As in the previous two cases, the equations are referred to by a coded number, "func".

                              !!!!!  WARNING  !!!!!
The interactions supported in the current version of GROTOLAM are
    (-) "harmonic" and "Morse" for linear bond itneractions;
    (-) "periodic" and "Urey-Bradley" for angular type;
    (-) "harmonic" for dihedral itneractions;
If more than one bond, angle or diherdal interaction is recognized during the reading process, the "hybrid" style 
is used in LAMMPS.

INPUT: 
    (i) filename_bon:           character string containing the bonded .itp file name;
    (ii) formatspec_bondbon:    character string setting the format of the BONDED interaction parameters of interest. 
                                This input is automatically set.
    (iii) formatspec_anglebon:  character string setting the format of the ANGLE interaction parameters of interest. 
                                This input is automatically set.
    (iv) formatspec_dihedralbon: character string setting the format of the DIHEDRAL interaction parameters of interest. 
                                This input is automatically set.

OUTPUT:
    (i-ii) Cell arrays listing the 2 atom type names for each BOND interaction;
    (iii) bondtypenumber:   numeric array of the code numbers "func" expressing the mathematical formulation of the 
                            BOND interaction;
    (iv-vi) Numerical arrays containing the numerical parameters if the BOND interactions.
    (vii-viii) Cell arrays listing the 2 atom type names for each ANGLE interaction;
    (ix) angletypenumber:   numeric array of the code numbers "func" expressing the mathematical formulation of the 
                            ANGLE interaction;
    (x-xiii) Numerical arrays containing the numerical parameters if the ANGLE interactions;
    (xiv-xvii) Cell arrays listing the 4 atom type names for each DIHEDRAL interaction;
    (xviii) dihedraltypenumber: numeric array of the code numbers "func" expressing the mathematical formulation of the 
                                DIHEDRAL interaction;
    (xix-xxii) Numerical arrays containing the numerical parameters if the DIHEDRAL interactions;
    
If any of the OUTPUT numerical arrays is not used for the current interaction, it will be composed of "NaN" entries.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Reading_top.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Matlab routine used to retrieve system information from the topology file. If the user required parametrization, 
the force field are not retried from the ".itp" files but from the ".top" instead. 
INPUT: 
    (i) filename_top: character string containing the topology .top file name;
    (ii-iii) Format specifications for atoms parameters and bond interaction, automatically defined by the code;
    (iv) choice_param: input parameter tocheck wheter the .top file has to be used to retrieve the forcefiled parameters;
    (v-viii) Format specifications for forcefiled and molecules type parameters, automatically defined by the code;
    
OUTPUT:
    (i) atom_ID: integer vector listing the ID number of the atoms composing the geometry. The solvent atoms are not included in this list;
    (ii) atom_inbond: cell array specifiying, for each atom, which kind of bond interaction has to be used, i.e. depending on the number of neighbors;
    (iii) charge: numerical array containing the partial charge (eV) on each atom;
    (iv-v) Cell arrays containing the name and number of objects present in the system. Solvent molecules are included;
    (vi-vii) ID numbers of each couple of atoms for BOND interactions; 
    (viii-x) Numerical arrays for BOND parameters. If the "parametrization" option is "No", these arrays will contain "0" entries. If the "parametrization" option is "Yes", but any of the parameters are not used, these arrays will contain "NaN" entries;
    (xi-xiii) ID numbers of each triplets of atoms for ANGLE interactions;
    (xiv-xvii) Numerical arrays for ANGLE parameters. If the "parametrization" option is "No", these arrays will contain "0" entries. If the "parametrization" option is "Yes", but any of the parameters are not used, these arrays will contain "NaN" entries;
    (xviii-xxi) ID numbers of each atom for DIHEDRAL interactions;
    (xxii-xxv) Numerical arrays for DIHEDRAL parameters. If the "parametrization" option is "No", these arrays will contain "0" entries. If the "parametrization" option is "Yes", but any of the parameters are not used, these arrays will contain "NaN" entries;

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Reading_xyz.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The standard coordinate file for GROMACS is the .gro format. Here every atom of the system, solvent included, is reported with its coordinates and, optionally, velocities. This Matlab routines retrieves the total number of atoms present in the system and their initial coordinates.
INPUT: 
    (i) filename_top: character string containing the coordinates .gro file name;
    (ii) Format specifications for coordinates, atom type and ID, automatically defined by the code;

OUTPUT:
    (i) n_mol: numerical array containing, for each atom, the molecule number it belongs to;
    (ii) type: cell array containing the coded name of each atom chemical element. Solvent is included; 
    (iii-v) Coordinates x, y and z of each atom;
    (vi-viii) Dimensions in the 3 direction of the simulation box.
    
                              !!!!!  WARNING  !!!!!
The current version of GROTOLAM assumes cubic or parallelepiped box.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Write_geometry.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Matlab routine used to translate in a single LAMMPS geometry file the informations  acquired from the GROMACS files. Atoms properties, bond and non-bonded interactions couples, coordinates and solvent informations are translated in the LAMMPS fromat. The INPUT arguments match the OUTPUT arguments of the previous reading functions.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Writing_input.m   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Matlab routine to write LAMMPS input file. This routine is  divided in 3 parts:

(I) INIZIALIZATION: the type of units of measurements, number of dimension, boundary conditions and atom style (atomic, angle or full) are specified. This section has some default inputs parameters:
    (i) real units of measurement;
    (ii) the system develops in 3 dimensions;
    (iii) periodic boundary conditions along the three axes;
    (iv) atom_modify map array option.

                              !!!!!  WARNING  !!!!!
Default entries (i), (iii), (iv) can be modified directly in the code of this function, while the dimensions number involved must be changed in the file "main.m".

(II) SYSTEM CONFIGURATION: the numerical constants of electrostatic non-bonded interaction are computed for each possible couple of atoms. LJ SIGMA and EPSILON or Buckingham potential parameters are computed according to the Lorentz-Berthelot mixing rule: 
SIGMA_ij=(SIGMA_i+SIGMA_j)/2; EPSILON_ij=(EPSILON_i+EPSILON_j)^0.5.
The electrostatic interactions follow the common Coulomb equation.
Finally, the parameters for each type of bond, angle and dihedral interaction is listed. Each couple, triplet or quadruplet of atoms for each bonded interaction refers to these parameters through a coded number, estimated from the ".gro" file.

                              !!!!!  WARNING  !!!!!
If the LJ potential was implemented in the form: V(r_ij)= A/(r_ij)^12 - B/(r_ij)^6 the conversion to the SIGMA-EPSILON form must occur manually according the following equations:
SIGMA =(A/B)^(1/6);  EPSILON = B/4*(SIGMA)^6
Furthermore, other warning messages will appear if the a non-implemented potential entry is chosen.

(III) INTEGRATION PARAMETERS: in the last section of the routine the integration parameters are listed:
    (i) neighbor distance update list and delay are automatically set, respectively, to 2.0 [Angstom], 1 [step] and 1 [step];
    (ii) timestep is automatically set to 1.0 [ps];
    
Finally a GUI guides the user chosing the statistical ensemble to be adopted for the simulation:

    (i) NVT: requires the temperatures [K] at the beginning and end of the simulation, subset of atoms which the coupling has to be applined, damping factor [ps] and number of steps to be performed. The temperature coupling is performed through a Nose-Hoover thermostat. Default answers are available;
    (ii) NPT: adds to the temperature coupling a pressure coupling, the GUI asks to insert pressure values [bar] at the beginning and at the end of the simulation, damping factor [ps] and number of steps to be performed. The Nose-Hoover coupling is adopted. Default answers are available;
    (iii) NVE: the GUI asks an ensemble to apply the energy conservation and the number of steps to be performed. Default answers are available;
