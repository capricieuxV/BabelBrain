BabelBrain v0.2.5-1
=============
Samuel Pichardo, Ph.D  
Associate Professor  
Radiology and Clinical Neurosciences, Hotchkiss Brain Institute  
Cumming School of Medicine,  
University of Calgary   
samuel.pichardo@ucalgary.ca  
www.neurofus.ca


[![License: BSD-3](https://img.shields.io/badge/BSD-3-Clause.svg)](LICENSE)
[![Documentation](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://proteusmrighifu.github.io/BabelBrain)


**GUI application for the modeling of transcranial ultrasound for neuromodulation applications**
BabelBrain is a frontend application specially designed to work in tandem with neuronavigation software to perform focused ultrasound research. BabelBrain uses [BabelViscoFDTD](https://github.com/ProteusMRIgHIFU/BabelViscoFDTD) extensively for calculations. BabelViscoFDTD is optimized for multiple GPU backends (Metal, OpenCL and CUDA). In its initial inception, BabelViscoFDTD is focused on MacOS systems based on Apple ARM64 processors. However, BabelViscoFDTD can run on any system (Mac, Linux, Windows) that has a decent GPU from NVidia or AMD. 

# Disclaimer
This software is provided "as is" and it is intended exclusively for research purposes.

# Standalone application
Ready-to-use applications (no need for Python installation) for macOS are available in the [Releases](https://github.com/ProteusMRIgHIFU/BabelBrain/releases) section. Download, open and drag "BabelBrain" into the Applications folder. The first time you use you will be prompted to authorize to run and access directories. You may also need to authorize it in the Security settings of macOS.

# Instructions for use
Please consult the [online manual](https://proteusmrighifu.github.io/BabelBrain/) for details on instructions for use.

# Manual Installation for Development 
If you prefer to run the code in a Python environment, the requirements are roughly a clean Python 3.9-3.10 environment, a healthy XCode installation in macOS, or CUDA (up to v11.8) + Visual Studio/gcc in Windows/Linux. Consult [BabelViscoFDTD](https://github.com/ProteusMRIgHIFU/BabelViscoFDTD) for details on what is needed for the FDTD solvers
# Requirements
* A decent GPU (AMD, Nvidia or Apple Silicon) with 12 GB RAM or more. For AMD and Nvidia GPUS, 32 GB or more is highly recommended. For Apple Silicon, M1 Max/Ultra or M2 Max with 32 GB RAM or more highly recommended. Intel-based Mac systems need a dedicated AMD GPU (internal or external). Intel-based iMac Pro and MacPro systems have internal GPUs suitable for sub 500 kHz simulations (i.e., Vega 56, Vega 64). An external GPU (i.e., AMD W6800 Pro) offers excellent performance and capability for high-frequency simulations.
* 32 GB RAM or more for main CPU memory for Intel-based systems.
* Python 3.9-3.10. Anaconda/miniconda is recommended. - if running in Apple new ARM64 processors (M1, M1 Max, etc.), be sure to use a native ARM64 version. Consult [BabelViscoFDTD](https://github.com/ProteusMRIgHIFU/BabelViscoFDTD) for further details.
* [Blender](www.blender.org)
* [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki) 

Be sure FSL init scripts are properly activated in your .bash_profile or .zsh_profile.

## Recommended settings
* macOS and Windows: create a conda environment using the appropriate yaml file.
* Linux: Create first and activate a new environment with some basics libraries from Conda

  `conda create --name babel python=3.10 numpy scipy`

  `activate babel`

`pip install -r requirements_linux.txt`

## Running
If running from the GitHub source code, just change to the BabelBrain directory and execute

`python BabelBrain.py`

## Building an standalone application for macOS
A Pyinstaller specification file is ready for use. To build the MacOS application, just change to the BabelBrain directory and run

`pyinstaller BabelBrain.spec`

A new application ready to use will be created at `BabelBrain/BabelBrain/dist/Babelbrain.app`

# Version log
- 0.2.6. Apr 4, 2023:
  - BUG fix: Issue #14 - Reduced precision with single Elem Tx with low F#
  - BUG fix: Issue #13 - Inadequate use of SimpleITK SetSpacing to create isotropic scans 
  - Minor bugs for minimal requirements
- 0.2.5-1. March 15, 2023:
  - BUG fix: Issue #7 - Matplotlib backends are now included in macOS application 
  - BUG fix: Remove CPU from engine
- 0.2.5 -  Jan 10, 2023:
  - First public release

