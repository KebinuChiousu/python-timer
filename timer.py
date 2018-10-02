#!/usr/bin/env python3
import argparse
import util

def main():
    parser = argparse.ArgumentParser(description='timer')
    parser.add_argument('NUM', type=int, default=1, help='time to wait')
    parser.add_argument('--period', choices=['min','sec'], default='min', help='period for input')
    args = parser.parse_args()

    seconds = args.NUM

    if args.period == 'min':
        seconds = seconds * 60

    util.sleep(seconds)

if __name__ == '__main__':
    main()
