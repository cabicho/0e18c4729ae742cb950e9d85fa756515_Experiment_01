import sys

def main():
    if len(sys.argv) != 4:
        print "Usage:\nmergeFiles <FILE-1> <FILE-2> <OUTPUT-FILE>"
    else:
        with open(sys.argv[1], 'rb') as f1, open(sys.argv[2], 'rb') as f2, open(sys.argv[3], 'wb') as fout:
            fout.write(f1.read())
            fout.write(f2.read())

if __name__ == "__main__":
    main()
