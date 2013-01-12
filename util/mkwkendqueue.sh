#!/bin/sh

echo '#!/bin/sh'
echo

i=$1
while ((i <= $(($2))))
do
  echo '# Cube '$((i))
  echo 'echo `date` >> queuewkend.log'
  echo 'echo -n "   Processing cube '$((i))' ... " >> queuewkend.log'
  echo 'cd cube'$((i))'/wkend ; ./dofit-wud.sh ; cd ../../'
  echo 'if [ -f "cube'$((i))'/wkend/done" ]'
  echo 'then echo "done" >> queuewkend.log'
  echo 'else echo "ERROR - Crashed? Hung?" >> queuewkend.log'
  echo 'fi'
  echo 'echo `date` >> queuewkend.log'
  echo
  
  i=$((i+1))
done
