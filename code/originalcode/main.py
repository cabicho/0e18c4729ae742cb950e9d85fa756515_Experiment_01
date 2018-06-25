# author: Cem Bicer cem.bicer@gmail.com, 2018

import sys, os, errno

def makedirs(dir):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def write_crpyt_script(dir, to_read, to_write):
    with open(dir + "/tmp.py", "r") as tmp_script:
        content = tmp_script.readlines()
    with open(dir + "/crypt.py", "w") as script:
        script.write("# GENERATED WITH: \'angecryption.py\'\n")
        script.write("\n")
        script.write("# This script decrypts the file \'zipflv.zip\' that is located\n")
        script.write("# in \'result/ZIPFLV\' and writes the result into the file\n")
        script.write("# \'zipflv.flv\' that will also be located in \'result/ZIPFLV\'.\n")
        script.write("# The decryption key is \'MySuperSecureKey\'\n")
        script.write("".join(content[:4]))
        script.write("with open('%s', 'rb') as f:\n" % to_read)
        script.write("".join(content[5:9]))
        script.write("with open('%s', 'wb') as f:\n" % to_write)
        script.write("".join(content[10:]))
    os.remove(dir + "/tmp.py")

if __name__ == "__main__":
    result_dir = "../../result"
    data_dir = "../../data/originaldata"
    code_dir = "../"
    print("Current working directory: ")
    print(os.getcwd())
    print("")
    makedirs(result_dir)
    print("Crafting schizophrenic files:")
    print("    - BMP schizophrenia")
    print("      executing mergeBMP.py")
    os.system("python mergeBMP.py %s/BMP/image.bmp %s/BMP/image_1.bmp %s/bmp_schizo.bmp" % (data_dir, data_dir, result_dir))
    print("      output file: %s/bmp_schizo.bmp" % result_dir)
    print("    - GIF schizophrenia")
    print("      executing mergeGIF.py")
    print("      NOTE: this may take a while")
    os.system("python mergeGIF.py %s/GIF/image_1.jpg %s/GIF/image_2.jpg %s/gif_schizo.gif" % (data_dir, data_dir, result_dir))
    print("      output file: %s/gif_schizo.gif" % result_dir)
    print("")
    print("Crafting polyglot files:")
    print("    - by concatenation: PDF ZIP")
    print("      executing mergeFiles.py")
    os.system("python mergeFiles.py %s/PDF/file.pdf %s/ZIP/animals.zip %s/pdfzip.pdf" % (data_dir, data_dir, result_dir))
    print("      output file: %s/pdfzip.pdf" % result_dir)
    print("    - host/parasite:")
    print("        - GIF JS")
    makedirs("%s/GIFJS" % result_dir)
    print("          executing mergeGIFJS.py")
    os.system("python mergeGIFJS.py %s/JS/alert.js %s/GIFJS/gifjs.gif" % (data_dir, result_dir))
    print("          output files: %s/GIFJS/gifjs.gif %s/GIFJS/index.html" % (result_dir, result_dir))
    print("        - JAVA JS")
    print("          executing mergeJAVAJS.py")
    os.system("python mergeJAVAJS.py %s/JAVA/HelloWorld.java %s/JS/alert.js %s" % (data_dir, data_dir, result_dir))
    print("          output file: %s/HelloWorld.java.html" % result_dir)
    makedirs("%s/ZIPFLV" % result_dir)
    print("    - encryption: ZIP FLV")
    print("      executing angecryption.py")
    os.system("python angecryption.py %s/ZIP/a.zip %s/FLV/video.flv %s/ZIPFLV/zipflv.zip MySuperSecureKey aes > %s/tmp.py" % (data_dir, data_dir, result_dir, code_dir))
    write_crpyt_script(code_dir, "../result/ZIPFLV/zipflv.zip", "../result/ZIPFLV/zipflv.flv")
    print("      output files: %s/ZIPFLV/zipflv.zip %s/crypt.py" % (result_dir, code_dir))
    print("    - chimera: PDF ZIP JPG")
    print("      executing mergePDFZIPJPGchimera.py")
    os.system("python mergePDFZIPJPGchimera.py %s/JPG/image.jpg %s/chimera.pdf" % (data_dir, result_dir))
    print("      output file: %s/chimera.pdf" % result_dir)
    print("DONE.")
