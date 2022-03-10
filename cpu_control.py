#!/usr/bin/python3
import re
import sys
import os


USAGE_DEFAULT = """usage: %s CPU_LIST
where CPU_LIST can be a comma- or hyphen-separated list of integers"""

USAGE_MANUAL = """usage: %s enable|disable CPU_LIST
where CPU_LIST can be a comma- or hyphen-separated list of integers"""

def enable_cpus(cpuids: list):
    errors = 0
    for cpu in cpuids:
        r = os.system("echo 1 >/sys/devices/system/cpu/cpu%d/online" % cpu)
        if r:
            errors += 1
    return errors


def disable_cpus(cpuids: list):
    errors = 0
    for cpu in cpuids:
        r = os.system("echo 0 >/sys/devices/system/cpu/cpu%d/online" % cpu)
        if r:
            errors += 1
    return errors


def dehyphenate(s: str):
    if '-' in s:
        bounds = s.split('-')
        if len(bounds) != 2:
            raise ValueError("Error parsing hyphenated list")
        a = int(bounds[0])
        b = int(bounds[1]) + 1
        return list(range(a, b))
    return [int(s)]


def parse_list(s: str):
    cpu_list = []
    comma_separated = s.split(',')
    for item in comma_separated:
        n = dehyphenate(item)
        if n[0] not in cpu_list:
            cpu_list += n
    return cpu_list


def main(argv):
    basename = os.path.basename(argv[0])
    argc = len(argv)
    cpufunc = None
    
    if basename == "cpu_enable":
        if argc != 2:
            print(USAGE_DEFAULT % basename, file=sys.stderr)
            return 1
        cpufunc = enable_cpus

    elif basename == "cpu_disable":
        if argc != 2:
            print(USAGE_DEFAULT % basename, file=sys.stderr)
            return 1
        cpufunc = disable_cpus

    else:
        if argc != 3:
            print(USAGE_MANUAL % basename, file=sys.stderr)
            return 1

        if argv[1] == "enable":
            cpufunc = enable_cpus
        elif argv[1] == "disable":
            cpufunc = disable_cpus
        else:
            print(USAGE_MANUAL % basename, file=sys.stderr)
            return 1

    try:
        cpu_list = parse_list(argv[-1])
        e = cpufunc(cpu_list)
        if e:
            return 1
    except ValueError:
        print("Error parsing CPU list", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    exit(main(sys.argv))
