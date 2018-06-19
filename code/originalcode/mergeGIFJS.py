# author: Cem Bicer cem.bicer@gmail.com, 2018

import sys, os

# Lines:
# 1. GIF signature 'GIF89a'
# 2. Javascript comment start '/*' and GIF width '10799'
# 3. heigth (\x32 = 50 pixel)
# 4. global color table
# 5. background color
# 6. default aspect ratio
# 7. image descriptor always start with \x2C
# 8. image position in pixel from left
# 8. image position in pixel from top
# 9. image width (same as 2.)
# 10. image height (same as 3.)
# 11. packed field for image descriptor
# 12. LZW compression data
# 13. GIF terminator
_GIF_BINARY =   "\x47\x49\x46\x38\x39\x61" + \
                "\x2F\x2A" + \
                "\x32\x00" + \
                "\x00" + \
                "\x00" + \
                "\x00" + \
                "\x2C" + \
                "\x00\x00" + \
                "\x00\x00" + \
                "\x2F\x2A" + \
                "\x32\x00" + \
                "\x00" + \
                "\x02\x00" + \
                "\x3B"

_HTML_BODY_OPEN = "<html><body>"
_BODY_HTML_CLOSE = "</body></html>"

def main():
    if len(sys.argv) != 3:
        print "Usage:\nmergeGIFJS <JS-FILE> <OUTPUT-GIF-FILE>"
    else:
        output_dir = os.path.abspath(os.path.join(sys.argv[2], os.pardir))
        with open(sys.argv[1], 'rb') as fjs, open(sys.argv[2], 'wb') as f_gif_out, open("%s/index.html" % output_dir, 'wb') as f_html_out:
            # write gif file
            f_gif_out.write(_GIF_BINARY)
            f_gif_out.write("*/") # close JS comment that was opened in the GIF binary (see 2.)
            f_gif_out.write("=1;") # do something with the variable
            f_gif_out.write(fjs.read())
            # write html file
            f_html_out.write(_HTML_BODY_OPEN)
            f_html_out.write("<img src=\"" + os.path.basename(f_gif_out.name) + "\">")
            f_html_out.write("<script src=\"" + os.path.basename(f_gif_out.name) + "\"></script>")
            f_html_out.write(_BODY_HTML_CLOSE)

if __name__ == "__main__":
    main()
