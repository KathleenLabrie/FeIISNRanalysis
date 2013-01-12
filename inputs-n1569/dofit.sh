#!/bin/sh
alias snrpopfit='/home/klabrie/prgc/bin/snrpopfit'

echo `date` >> cube1.log
echo '   Launching 100 models - Models 1 to 100.' >> cube1.log
snrpopfit -o fitn1569 -n 100 --index=1 > spool 2>&1
echo "   Completed" >> cube1.log
echo `date` >> cube1.log
echo "done 100" > done
