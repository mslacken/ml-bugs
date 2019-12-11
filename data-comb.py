#!/usr/bin/python3
import argparse
import json
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read in json.')
    parser.add_argument('--file1',dest='file1',type=str)
    parser.add_argument('--file2',dest='file2',type=str)
    parser.add_argument('--outfile',dest='outfile',type=str)

    args = parser.parse_args()

    if not args.file1 or not args.file2 or not args.outfile:
        parser.print_help()
        sys.exit(0)

    file1_data = {}
    file2_data = {}

    try: 
        file1_data  = json.load(open(args.file1))
    except Exception as excep_reader:
        print("Could not read %s" % args.file1)
        print(excep_reader)
        sys.exit(1)

    try: 
        file2_data  = json.load(open(args.file2))
    except Exception as excep_reader:
        print("Could not read %s" % args.file2)
        print(excep_reader)
        file2_empty = 1
    else:
        file2_empty = 0

    if not file2_empty:
        for key,val in file2_data.items():
            file1_data[key] = val

    ofile = open(args.outfile,'w')
    ofile.write(json.dumps(file1_data))
    ofile.write("\n")
    ofile.flush()
