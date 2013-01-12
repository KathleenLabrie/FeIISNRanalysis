#!/bin/sh

i=$1
while ((i <= $(($2))))
do
   mkdir cube$((i))
   i=$((i+1))
done

