#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Logline = namedtuple('Logline', 'level timestamp message')
starts_line=re.compile("\[(TRACE|DEBUG|INFO|WARN|ERROR|FATAL)").match

def apply_filter(current_log_line, filtered_lines):
    parsed_line = parse_line(current_log_line)
    if filter(parsed_line):
        filtered_lines.append(parsed_line)


def get_filtered_lines(source):
    filtered_lines = []
    line_buffer = ''
    for line in source:
        if starts_line(line) and line_buffer:
            apply_filter(line_buffer, filtered_lines)
            line_buffer = ''
        line_buffer += line
    apply_filter(line_buffer, filtered_lines)
    return filtered_lines


def parse_line(log_line):
    prefix, message = log_line.split(']', 1)
    level, timestamp = parse_prefix(prefix)
    return Logline(level, timestamp, message)


def parse_prefix(prefix):
    prefix = prefix.strip('[]')
    tokens = prefix.split(' ')
    level = tokens[0]
    timestamp = tokens[-1]
    return level, timestamp


def filter(log_line):
    return log_line.timestamp > "12:00:00" and log_line.timestamp < "12:01:00"

def console_out(lines):
    for line in lines:
        print('{}{}'.format(line.timestamp, line.message.rstrip('\n')))


def main():
    if len(sys.argv) != 2:
        print('Usage: {0} $logfile'.format(sys.argv[0]))
    else:
        file_name = sys.argv[1]
        with open(file_name, encoding="utf-8") as file:
            console_out(get_filtered_lines(file))

if __name__ == '__main__':
    main()
