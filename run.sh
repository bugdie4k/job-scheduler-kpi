#!/usr/bin/env sh

N='number_of_iterations'
python3 -i -c "exec(open(\"./lab4.py\").read()); print(\"use functions:\n new(), \n dump(), \n iter([ $N ]), \n iterdump([ $N ]), \n newdumpiter([ $N ])\")"
