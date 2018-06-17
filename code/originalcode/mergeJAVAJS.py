import sys, os, errno

_HTML_BODY_SCRIPT_OPEN = "<html><body><script>"
_SCRIPT_BODY_HTML_CLOSE = "</script></body></html>"

def main():
    if len(sys.argv) != 4:
        print "Usage:\nmergeJAVAJS <JAVA-FILE> <JS-FILE> <OUTPUT-DIRECTORY>"
    else:
        try:
            os.makedirs(sys.argv[3])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(sys.argv[1], 'rb') as fjava, \
        open(sys.argv[2], 'rb') as fjs, \
        open(sys.argv[3] + "/" + os.path.basename(fjava.name) + ".html", 'wb') as fout:
            fout.write("/*")
            fout.write(_HTML_BODY_SCRIPT_OPEN)
            fout.write(fjs.read())
            fout.write(_SCRIPT_BODY_HTML_CLOSE)
            fout.write("*/")
            fout.write(fjava.read())

if __name__ == "__main__":
    main()
