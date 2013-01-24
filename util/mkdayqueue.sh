#!/bin/sh

echo '#!/bin/sh'
echo

i=$1
while ((i <= $(($2))))
do
  echo '# Cube '$((i))
  echo 'echo `date` >> queue.log ; echo -n "   Processing cube '$((i))' ... " >> queue.log'
  echo 'cd cube'$((i))'/day ; ./dofit.sh ; cd ..'
  echo 'if [ -f "cube'$((i))'/done" ]'
  echo 'then echo "done" >> queue.log'
  echo 'else echo "   ERROR - Crashed?" >> queue.log'
  echo 'fi'
  echo 'echo `date` >> queue.log'
  echo
  
  i=$((i+1))
done
