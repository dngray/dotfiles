#!/usr/bin/env python

# https://unix.stackexchange.com/questions/92493/sorting-down-processes-by-memory-usage/490647#490647

import subprocess
from collections import OrderedDict


def run_cmd(cmd_string):
    """Runs commands and saves output to variable"""
    cmd_list = cmd_string.split(" ")
    popen_obj = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    output = popen_obj.stdout.read()
    output = output.decode("utf8")
    return output

def sum_process_resources():
    """Sums top X cpu and memory usages grouped by processes"""
    ps_memory, ps_cpu, ps_rss = {}, {}, {}
    top = 20
    output = run_cmd('ps aux').split("\n")
    for i, line in enumerate(output):
        cleaned_list = " ".join(line.split())
        line_list = cleaned_list.split(" ")
        if i > 0 and len(line_list) > 10:
            cpu = float(line_list[2])
            memory = float(line_list[3])
            rss = float(line_list[5])
            command = line_list[10]
            ps_cpu[command] = round(ps_cpu.get(command, 0) + cpu, 2)
            ps_memory[command] = round(ps_memory.get(command, 0) + memory, 2)
            ps_rss[command] = round(ps_rss.get(command, 0) + rss, 2)
    sorted_cpu = OrderedDict(sorted(ps_cpu.items(), key=lambda x: x[1], reverse=True))
    sorted_memory = OrderedDict(sorted(ps_memory.items(), key=lambda x: x[1], reverse=True))
    sorted_rss = OrderedDict(sorted(ps_rss.items(), key=lambda x: x[1], reverse=True))
    print("====   CPU%   ====")
    for i, k in enumerate(sorted_cpu.items()):
        if i < top:
            print("{}. {} | {}".format(i, k[0], k[1]))
    print("====   MEM%   ====")
    for i, k in enumerate(sorted_memory.items()):
        if i < top:
            print("{}. {} | {}".format(i, k[0], k[1]))
    print("====   RSS MB   ====")
    for i, k in enumerate(sorted_rss.items()):
        if i < top:
            print("{}. {} | {} MB".format(i, k[0], round((k[1]/1024), 2)))

if __name__ == '__main__':
    sum_process_resources()
