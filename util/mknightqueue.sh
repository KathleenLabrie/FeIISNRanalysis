#!/bin/sh

echo '#!/bin/sh'
echo

i=$1
echo '# Cube '$((i))' - 20 models, overnight (~8.5 hours if 22 min/run)'
echo 'echo `date` >> queuenight.log'
echo 'echo -n "   Processing cube '$((i))' ... " >> queuenight.log'
echo 'cd cube'$((i))'/night ; sleep 3h ; ./dofit.sh ; cd ../..'
echo 'if [ -f "cube'$((i))'/night/done" ]'
echo 'then echo "done" >> queuenight.log'
echo 'else echo "   ERROR - Crashed?" >> queuenight.log'
echo 'fi'
echo 'echo `date` >> queuenight.log'
echo

i=$((i+1))
while ((i <= $(($2))))
do
  echo '# Cube '$((i))' - 20 models, overnight (~8.5 hours if 22 min/run)'
  echo '#echo `date` >> queuenight.log'
  echo '#echo -n "   Processing cube '$((i))' ... " >> queuenight.log'
  echo '#cd cube'$((i))'/night ; sleep 3h ; ./dofit.sh ; cd ../..'
  echo '#if [ -f "cube'$((i))'/night/done" ]'
  echo '#then echo "done" >> queuenight.log'
  echo '#else echo "   ERROR - Crashed?" >> queuenight.log'
  echo '#fi'
  echo '#echo `date` >> queuenight.log'
  echo
  
  i=$((i+1))
done
