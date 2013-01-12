#!/bin/sh

## Cube 7
#echo `date` >> queuewkend.log
#echo -n "   Processing cube 7 ... " >> queuewkend.log
#
#cd cube7/wkend ; ./dofit-wud.sh ; cd ../../
#if [ -f "cube7/wkend/done" ]
#then echo "done" >> queuewkend.log
#else echo "   ERROR - Crashed? Hung?" >> queuewkend.log
#fi
#echo `date` >> queuewkend.log

# Cube 8
#echo `date` >> queuewkend.log
#echo -n "   Processing cube 8 ... " >> queuewkend.log
#
#cd cube8/wkend ; ./dofit-wud.sh ; cd ../../
#if [ -f "cube8/wkend/done" ]
#then echo "done" >> queuewkend.log
#else echo "   ERROR - Crashed? Hung?" >> queuewkend.log
#fi
#echo `date` >> queuewkend.log

# Cube 9
echo `date` >> queuewkend.log
echo -n "   Processing cube 9 ... " >> queuewkend.log

cd cube9/wkend ; ./dofit-wud.sh ; cd ../../
if [ -f "cube9/wkend/done" ]
then echo "done" >> queuewkend.log
else echo "   ERROR - Crashed? Hung?" >> queuewkend.log
fi
echo `date` >> queuewkend.log

# Cube 10
echo `date` >> queuewkend.log
echo -n "   Processing cube 10 ... " >> queuewkend.log

cd cube10/wkend ; ./dofit-wud.sh ; cd ../../
if [ -f "cube10/wkend/done" ]
then echo "done" >> queuewkend.log
else echo "   ERROR - Crashed? Hung?" >> queuewkend.log
fi
echo `date` >> queuewkend.log
