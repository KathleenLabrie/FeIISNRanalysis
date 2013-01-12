#!/bin/sh
alias snrpopfit='/net/nihal/home/klabrie/prgc/bin/snrpopfit'

if [ -f 'done' ]; then
    rm 'done'
fi

echo `date` >> cube10.log
i=1
while ((i <= 100))
do
    echo -n '  Launching 1 model - Model '$((i))' at ' >> cube10.log
    echo `date` >> cube10.log
    wud -l 115 ; snrpopfit -o fitn5253 -n 1 --index=$((i)) >> spool 2>&1 &
    sleep 5m
    i=$((i+1))
done

if [ -f fitn5253probap100.dat ]; then
    echo "    Completed" >> cube10.log
    echo "done 100" > done
else
    echo "    ERROR - Crashed? Hung?" >> cube10.log
fi
echo `date` >> cube10.log
