import argparse
import re
import os
import sys
import gzip


def _is_gz(infile):
    """ Checks if the infile is Gzipped and returns a boolean """
    ext = infile.split(".")
    if ext[len(ext)-1] == "gz":
        return True
    else:
        return False


def _file_police(infile):
    """ Check's if the provided file exists in the directory. """
    try:
        i = open(infile, 'r')
        i.close()
    except FileNotFoundError:
        print("There is no file with", infile+",", "Exiting!")
        sys.exit()


def _read_fastq(INFILE, Size, RMode):
    """ open a FASTQ file and yield each read"""
    # Check if file exists
    _file_police(INFILE)
    if RMode == 'rb':
        fh = gzip.open(INFILE, RMode)
    elif RMode == 'r':
        fh = open(INFILE, RMode)
    counter, reads_count = 0, 0
    reads = ''
    for line in fh:
        counter += 1
        if RMode == 'rb':
            reads = reads+line.decode()
        else:

        if counter == 4:
            yield str.encode(reads)
            counter = 0
            reads = ''
            reads_count += 1
        if reads_count == int(Size):
            break
    fh.close()


def split_fastq(infile1, Size, out1="splitted1.fastq", out2="splitted2.fastq", infile2=False):
    """ Takes fastq file(s), max number of reads and output file(s)
        to write the data to """
    if infile2 == False:
        # Check if the files are raw or compressed
        is_gz1 = _is_gz(infile1)
        if is_gz1 == True:
            RMode = 'rb'
            outfh = gzip.open(out1, 'wb')
        elif is_gz1 == False:
            RMode = 'r'
            outfh = open(out1, 'w')
        for line in _read_fastq(infile1, Size, RMode):
            outfh.write(line)
        outfh.close()

    else:
        # Check if the files are raw or compressed
        is_gz1 = _is_gz(infile1)
        is_gz2 = _is_gz(infile2)
        if is_gz1 == True and is_gz2 == True:
            RMode = 'rb'
            WMode = 'wb'
        elif is_gz1 == False and is_gz2 == False:
            RMode = 'r'
            WMode = 'w'
        else:
            exit("Error! make sure both the files have the same extension.")


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Split FASTQ file into smaller files")
    PARSER.add_argument("-t", "--type", dest="type", help="Please give the FASTQ file type,"
                                                          "-t se(single-end) / pe(pair-end)", required=True)
    PARSER.add_argument("-i1", "--file1", dest="infile1", help="provide path to the first file", required=True)
    PARSER.add_argument("-i2", "--file2", dest="infile2", help="provide path to the second file", required=False)
    PARSER.add_argument("-s", "--size", dest="Size", help="please provide number of reads you would like "
                                                          "to retain", required=True)
    PARSER.add_argument("-o1", "--output1", dest="out1", help="please provide a file name to store the output",
                        required=False)
    PARSER.add_argument("-o2", "--output2", dest="out2", help="please provide a file name to store the output",
                        required=False)
    ARGS = PARSER.parse_args()
    if ARGS.infile2:
        split_fastq(ARGS.infile1, ARGS.Size, ARGS.out1, ARGS.out2, ARGS.infile2)
    else:
        split_fastq(ARGS.infile1, ARGS.Size, ARGS.out1)