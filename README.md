# Copyright

Copyright (c) 2025 The Regents of the University of Michigan, IDEAS Lab

**************************

# MagicDraw API for MBSA&E

The MagicDraw API For MBSA&E allows users to transfer data from a Model-Based Systems Analysis (MBSA) module to a Model-Based Systems Engineering (MBSE) software.
Users may read/write an Aircraft Data Hierarchy (ADH) file into/out of Magic Systems of Systems Architect (MagicDraw).
This software provides an API between MagicDraw and a JSON file that can create and update system models, as well as export a system model to a JSON file.

Principal Investigator and Point of Contact:
- [Dr. Gokcin Cinar](cinar@umich.edu)

Principal Author:
- [Paul Mokotoff](prmoko@umich.edu)

Additional Contributors:
- Safa Bakhshi
- Alex Kerlee

README last updated: 05 Mar 2025

***************************

# Installation Instructions

The MagicDraw API for MBSA&E may be installed by cloning [this GitHub repository](https://github.com/ideas-um/MBSAE-API).
This may be done using the following command:

```
git clone https://github.com/ideas-um/MBSAE-API.git
```

After cloning the repository, each folder must be copied into the following MagicDraw sub-folder:

```
<Root>\Magic Systems of Systems Architect\plugins\com.nomagic.magicdraw.jpython\scripts
```

where ```<Root>``` is the root directory containing the MagicDraw software contents.
Then, open MagicDraw on your computer to check that the scripts installed properly.
This is done by checking the console log to see if there were any compilation errors after MagicDraw opens.
The console log can be found in:

```
<Path>\AppData\Local\.magic.systems.of.systems.architect\<Version>\msosa.log
```

where ```<Path>``` is the filepath to your AppData and ```<Version>``` is the version of MagicDraw running on your computer.

If there are no printouts with error messages in the console log, then the installation was successful.

*************

# Basic Usage

Each of the scripts provided in this repository is considered to be a "Browser Action", meaning that the function can only be accessed by right-clicking on a model element.
Once the model element is selected and a dropdown menu appears, the following functions (depending on what you install) should appear:

- **Import ADH to Stereotype**: reads a JSON file and creates a stereotype for any component with a Work Breakdown Structure (WBS) Number in the ADH. The stereotypes are stored in a profile. This code is located in the "CreateStereotype" folder.
- **Read ADH**: reads a JSON file and creates the system model (blocks, value properties, requirements, and packages) in MagicDraw. Any component nested within another one is assigned as a part property of the higher level component. This code is located in the "ReadADH" folder.
- **Update ADH**: reads an ADH file and compares the value of each value property to the system model. If any values are not equal, the value from the ADH is overwritten into the system model. This code is located in the "UpdateADH" folder.
- **Write from MagicDraw to ADH**: generates a JSON file from the system model in MagicDraw. The model element that is selected acts as the highest-level container; anything nested within that block/package will be written to the JSON file. This code is located in the "WriteADH" folder.

Currently, the ADH being read must be in the following directory.

```
<Root>\Magic Systems of Systems Architect
```

where ```<Root>``` is the same path as previously mentioned.
Similarly, any ADH that is written from MagicDraw will reside in this folder.

### Notice: Writing from MagicDraw to an ADH

On the systems that this code was developed on, administrative access was required to create a JSON file within the plugin.
If you obtain an error when trying to write an ADH from MagicDraw, please check that you run MagicDraw as an administrator.

******************

# Acknowledgements

This work was funded by The Boeing Company project: "Phase I Model-Based Systems Analysis and Engineering (MBSA&E) Framework Development & Assessment for NASA Sustainable Flight National Partnership (SFNP)".
The contract number is "SSOW-BRT-L1023-0237".
Alex Carrere was the Technical Monitor.
The developers also want to thank Sean Wakayama, Ron Engelbeck, and Mingxuan Shi for their support and valuable technical input throughout the duration of this contract.