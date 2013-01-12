#!/bin/csh
alias mksnrpop '/home/labrie/prgc/img/artdata/mksnrpop'
alias artimg '/home/labrie/prgc/img/artdata/artimg'

### n5253 ###

#nambient 0.5 cm-3
mksnrpop -o rad2500_0015_05.pop --nsnr=2500 --snrate=0.015 --nambient=0.5
mksnrpop -o rad2500_0001_05.pop --nsnr=1000 --snrate=0.001 --nambient=0.5
mksnrpop -o rad1000_001_05.pop --nsnr=1000 --snrate=0.01 --nambient=0.5
artimg -o rad2500_0015_05.fits --inputpop=rad2500_0015_05.pop,addsrc.pop
artimg -o rad2500_0001_05.fits --inputpop=rad2500_0001_05.pop,addsrc.pop
artimg -o rad1000_001_05.fits --inputpop=rad1000_001_05.pop,addsrc.pop

#nambient 1 cm-3
mksnrpop -o rad1000_0001_1.pop --nsnr=1000 --snrate=0.001 --nambient=1
mksnrpop -o rad1500_0025_1.pop --nsnr=1500 --snrate=0.025 --nambient=1
mksnrpop -o rad300_001_1.pop --nsnr=300 --snrate=0.01 --nambient=1
artimg -o rad1000_0001_1.fits --inputpop=rad1000_0001_1.pop,addsrc.pop
artimg -o rad1500_0025_1.fits --inputpop=rad1500_0025_1.pop,addsrc.pop
artimg -o rad300_001_1.fits --inputpop=rad300_001_1.pop,addsrc.pop

#nambient 2 cm-3
mksnrpop -o rad500_0001_2.pop --nsnr=500 --snrate=0.001 --nambient=2
mksnrpop -o rad500_001_2.pop --nsnr=500 --snrate=0.01 --nambient=2
mksnrpop -o rad250_001_2.pop --nsnr=250 --snrate=0.01 --nambient=2
artimg -o rad500_0001_2.fits --inputpop=rad500_0001_2.pop,addsrc.pop
artimg -o rad500_001_2.fits --inputpop=rad500_001_2.pop,addsrc.pop
artimg -o rad250_001_2.fits --inputpop=rad250_001_2.pop,addsrc.pop

#nambient 3 cm-3
mksnrpop -o rad400_0008_3.pop --nsnr=400 --snrate=0.008 --nambient=3
mksnrpop -o rad400_0001_3.pop --nsnr=400 --snrate=0.001 --nambient=3
mksnrpop -o rad150_0008_3.pop --nsnr=150 --snrate=0.008 --nambient=3
artimg -o rad400_0008_3.fits --inputpop=rad400_0008_3.pop,addsrc.pop
artimg -o rad400_0001_3.fits --inputpop=rad400_0001_3.pop,addsrc.pop
artimg -o rad150_0008_3.fits --inputpop=rad150_0008_3.pop,addsrc.pop

#nambient 10 cm-3
mksnrpop -o rad100_0001_10.pop --nsnr=100 --snrate=0.001 --nambient=10
mksnrpop -o rad150_0008_10.pop --nsnr=150 --snrate=0.008 --nambient=10
mksnrpop -o rad250_0025_10.pop --nsnr=250 --snrate=0.025 --nambient=10
artimg -o rad100_0001_10.fits --inputpop=rad100_0001_10.pop,addsrc.pop
artimg -o rad150_0008_10.fits --inputpop=rad150_0008_10.pop,addsrc.pop
artimg -o rad250_0025_10.fits --inputpop=rad250_0025_10.pop,addsrc.pop
