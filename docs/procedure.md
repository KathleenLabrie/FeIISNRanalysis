# Procedure

Here I explain how to produce the best fit maps of n_ambient, nsnr, snrate based on simulation of [Fe II] emitting SNR population and chisq fitting to real observations.



### Overview

1. Get [Fe II] observations
1. Measure characteristics from compact sources
1. Measure characteristics from galaxy
1. Install software
1. Set inputs and input parameters
1. For parameter space in n_ambient, nsnr, snrate, generate n realizations
1. Average realizations to get chisq map
1. If parameter space realized in subsets, merge best cubes to recreate the full parameter space.
1. Generate contour plots from master best cube.


### 1. Get [Fe II] Observations



For now, I'm working on improving the map for the data I've already obtained and measured as part of the thesis.  The galaxies I will be studying are NGC 1569 and NGC 5253.



From what I remember, I need a [Fe II] emission image (with continuum removed) as the reference observation.



### 2. Measure characteristics from compact sources



Again, for the time being, I'm working from the thesis results.



From memory, I need the position, the size, the flux.  Not sure what units are expected.  I'll update that info when I know.  For now, the input files already exist.



### 3. Measure characteristics from galaxy



For the time being, I'm working from the thesis results.



From memory, I need position on the frame, size and shape.  I believe I need the surface brightness distribution to simulate the SNR/stars distribution.  I'll update this section when I know more.  For now, the input files and input parameter lists already exist.



### 4. Install modeling software



The repositories are on github.  If you have hg-git on the machine, get the software from there.  If not, get it from rana, or any other source that is up-to-date and can get the software from github.  (At this time I don't know how to use git, so I use mercurial with hg-git.)



#### Installing the SNR Modeling software

The software is in the SNRmodel(KLSoft) repository on github.  The package 'snrpopfit' is required, along with its dependencies which are: artdata, phot, libKLutil, libKLcfitsio, libKLfunc, libKLsort, libKLstats, libKLfile, cfitsio.   The old plotting routines depended on PGPLOT.  I do not think I will be using that again, so the SNRmodel Makefile was modified to not compile those by default, removing the mandatory dependency.  The package artdata additionally depends on libKLran and KLfft.  The package phot additionally depends on libKLinter.



From github:

    $ git clone git://github.com/KathleenLabrie/SNRmodel.git
    $ git clone git://github.com/KathleenLabrie/KLlibc.git



Install CFITSIO first if it isn't already installed.  The webpage is heasarc.gsfc.nasa.gov/fitsio.  The current version is v3.310.  It is a standard installation process: ./configure ; make ; make install.  I normally install cfitsio in /usr/local.



Install my C libraries, if they are not already installed.  My standard install location is ${HOME}/local.

    $ cd KLlibc/libKLutil
    $ make;  make shared;  make test;  ./testcube;  make install; make install-shared; make clean
    $
    $ cd ../libKLcfitsio
    $ make; make shared; make test; ./test; make install; make install-shared;  make clean
    $
    $ cd ../libKLfunc
    $ make;  make shared;  make install;  make install-shared;  make clean
    $
    $ cd ../libKLsort
    $ make;  make shared;  make test; ./testshell;  make install;  make install-shared; make clean
    $
    $ cd ../libKLstats
    $ make;  make shared;  make install;  make install-shared; make clean
    $
    $ cd ../libKLfile
    $ make;  make shared;  make test; ./test;  ./testcube(broken); make install;  make install-shared;  make clean
    $
    $ cd ../libKLran
    $ make; make shared; make install; make install-shared; make clean
    $
    $ cd ../libKLfft
    $ make; make shared; make test; ./testconv; ./testndim; make install; make install-shared; make clean
    $
    $ cd ../libKLinter   
    $ make; make shared; make install; make install-shared; make clean

    

Install the modeling software:

    $ cd SNRmodel
    $ cd phot
    $ make; make install; make clean
    $ 
    $ cd ../artdata
    $ make; make install; make clean
    # 
    $ cd ../snrpopfit
    $ make; make install; make clean



#### Installing FeIISNRanalysis

The utility software and the input data and parameters are stored in a repository, FeIISNRanalysis (KLredux).  That software is not really "installed" per se, but simply retrieved from the repository and the util directory is added to the PATH.  The utility software is used once to set up the directories, I really don't see a reason for an account-wide installation.



From github:

    git clone git://github.com/KathleenLabrie/FeIISNRanalysis.git


Then:

    $ cd FeIISNRanalysis/util
    $ PATH=`pwd`:$PATH
    $ cd ..
    $ FEIISNR=`pwd`



### 5. Set inputs and input parameters



There's a whole slew of inputs and input parameters to set.  For now, I'm just reusing the files I used for the thesis observations.  Yet, the directory structure must be set up, those directories populated with the relevant input files, and the input files properly configured.  Two scripts are used to get that done.



Here are the steps, using NGC 1569 with 1e5 yrs emitting lifetime as an example:

    $ mkdir -p <somewhere>/FeIISNR
    $ cd <somewhere>/FeIISNR
    $ mkdirstructure n1569 1e5
    $ cd unresolvedSNRs/n1569/1e5/inputs
    $ cp $FEIISNR/inputs-n1569/* .
    $ cd ..
    $ mkcube.py 'nsnr=50:2500:50' 'snrate=0.0005:0.1:0.0005' 'nambient=0.5:10:0.5' 1e5 ./inputs --split=5,20,2



This sequence will create all the necessary directories (e.g. cube1), copy the n1569 inputs to the cubes, then configure the dofit scripts, the mksnrpop.param, and the snrpopfit.param files.  Finally, a README_cube and the doqueue scripts will be created.



### 6. Generate realizations



This is where I resume the work.



The grid for the parameter space is:

* <u>n_ambient</u> : 0.5 to 10, in intervals of 0.5.  (ambient density)
* <u>nsnr</u> : 50 to 2500, in intervals of 50  (number of SNR)
* <u>snrate</u> : 0.0005 to 0.1, in intervals of 0.0005  (supernova rate)



This grid will be explored for unlimited [Fe II] lifetime and for <u>1e5 yrs</u> [Fe II] lifetime.



The plan is to generate for each points in the parameter space <u>100 realizations</u>.  The output of each realization is a cube covering the parameter space.



Because the parameter space is finely sampled, generating realization for the entire grid in one go would be too risky (if it crashes midway) and might require  too much memory (depending on how the code is written).  Instead, subsection of the parameter space will be realized separately and the best fit cubes merged later to create the cube that will represent the full parameter space.



The nsnr - snrate plane has 10,000 grid points.  The plane will be divided in 100 sections, making each section cover 100 grid points.  Each section is called a "cube" and will be numerically identified from 1 to 100, "cube1", "cube2", etc.  Note that I have more or less doubled the number of points on the nambient grid, and now this axis is split in 2.  So in total, I have 200 cubes.



Each section is processed separately in its own directory named after the name of the section, ie. "cube1", "cube2", etc.



For each section, there will be 100 realizations generated.



Each section can be computed on different computers and core.  It is preferable to run all of the 100 realizations for a section from the same computer just to avoid a file handling mess.   It is not necessary to launch all 100 realizations in one go. The number of realizations to launch overnight for example, will depend on how long a single realization takes to complete.  The idea is to have the set completed by the morning to avoid hogging the CPU during the day.



The software used to generate the realization is "snrpopfit".  The simulations are normally driven via the doqueue scripts created in the previous section.



Chi square maps for pixels (chisq) and chi square maps for an aperture matching the galaxy (chisqap) are generated.  Probability maps are also generated, as well as "best fit" files which are simply a list of the minimum point in each realization.



Comparing the thesis and the snrpopfit code, the files we are interested in are the chisqap files.  Those will be the inputs to the next step, snrpopbfit.



### 7. Average realizations to get chisq maps



For each section ("cube1", "cube2", etc) there are 100 realizations.  The result for that section is the average of the results for the 100 realizations.  The average of the 100 realization is obtained by running snrpopbfit on the chisqap outputs. 



### 8. Merge sections



Because the parameter space is explored in sections, the best fit averaged cube from all sections need to be merged together into a master cube.  The program call "mergecubes" (from KLlibc, the file utility library) is used.  Note that the program seems to be expecting only 2 input cubes at this time.  It might need to be modified, or a utility script be written to merge all the cubes together two at a time.



### 9. Plot results



I will have to look into the SM macros.  I might want to replace the SM macros with a Python matplotlib script for better looking plots.



