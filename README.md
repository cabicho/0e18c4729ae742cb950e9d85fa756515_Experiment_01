# CheckResearch.org [Experiment](https://checkresearch.org/Experiment/View/9fc99c57-b861-44e3-bf23-d44f4bb208b1)  

 Publication [""schizophrene" und "polyglotte" Dateien"](https://dblp.uni-trier.de/search?q=%22schizophrene%22+und+%22polyglotte%22+Dateien) by "Cem Bicer"  

## HOWTO  

In this experiment I demonstrate to you how file format hacks can lead to so called "schizophrenic" files and file "polyglots".  

"Schizophrenic" files are files that show different outputs when opened with different parsers. They are crafted by merging two files with the same file format into a single file. Some parsers show the first file content some the other.  

"Polyglot" files are files that merge two or more different file formats into one valid file which can be openend with parsers that support at least one of the merged formats. Depending on the parser the file identifies as a different file type.  

Execute the `main.py` script to run all proof of concepts (PoCs).  

All PoCs present in this experiment are adopted from Ange Albertini's ["Funky File Formats"](https://events.ccc.de/congress/2014/Fahrplan/system/attachments/2562/original/Funky_File_Formats.pdf).  

## Experiment Setup  

### Experiment Content  

This experiment consists of two parts: schizophrenic and golyglot files. Each of these parts contains subsections that contain one or more PoCs. Following list shows all PoCs that are present in this experiment and there respective ID in brackets.  

1. schizophrenic files **(S)**  
   1. BMP **(S1)**  
   2. GIF **(S2)**  
2. polyglot files **(P)**  
   1. by concatenation  
      1. PDF ZIP **(P1)**  
   2. host/parasite  
      1. GIF JS **(P2)**  
      2. JAVA JS **(P3)**  
   3. encryption  
      1. ZIP FLV **(P4)**  
   4. chimera  
      1. PDF ZIP JPG **(P5)**  

### Hardware/Software  

The scripts where executed on a MacBook Pro Retina Mid-2014 with MacOs High Sierra 10.13.5 but should also work on other operating systems that can run python scripts.  

To verify the resulting schizophrenic files and polyglots use these programs in their respective versions and OS environment:  
* 7zip (16.04, Windows)  
* Adobe Acrobat Reader (2018.011, MacOS)  
* Apple Preview (10, MacOS)  
* GIMP (2.8.20, MacOS)  
* Google Chrome (67, MacOS)  
* iZip (1.9, MacOS)  
* JPDFViewer (1.0, MacOS)  
* Microsoft Paint (18.03, Windows)  
* Mozilla Firefox (60, MacOS)  
* Universal Viewer (1.0, Windows)  
* UnZip (6, MacOS)  
* Windows Photos (2018, Windows)  

Note: whenever this document refers to any program without explicitly giving the version number, the respective version from this list is used  

To run the script "mergeGIF.py" you neet to install the python module "imageio v2.3.0".

To run the script "angecrpytion.py" you need to install the python module "pycrypto v2.6.1" to be able to import "AES" from "Crpyto.Cipher".  

No other libraries or modules are needed.  

Run the script(s) with python 2.7.  

## Experiment Assumptions  

No significant assumptions were made.

## Preconditions  

To avoid unpredictable outcomes, make sure to execute this experiment with input data that is neither schizophrenic nor a polyglot. Also make sure that they do not have any prepended or appended data because some scripts check for a magic signature at offset 0. In general, all input data should be valid files, i.e. they should not violate the file format specification. Please only use the file types that are compatible when running a script manually. There is no guarantee that the scripts run correctly for input data that do not meet these prerequisites.

## Experiment Steps  

This experiment contains multiple scripts that all create a single PoC. There is a `main.py` script that runs all of the scripts with the right arguments. 

**The command to execute the whole experiment (i.e. main-script) is as simple as `python main.py`.**

The main-script executes following commands:  
(NOTE: all paths are relative from the `code` directory)  
(`<DATA-DIR>` = ../../data/originaldata)  
(`<RESULT-DIR>` = ../../result)  
(`<CODE-DIR>` = ../../code)  
1. **(S1)** `python mergeBMP.py <DATA-DIR>/BMP/image.bmp <DATA-DIR>/BMP/image_1.bmp <RESULT-DIR>/bmp_schizo.bmp`
2. **(S2)** `python mergeGIF.py <DATA-DIR>/GIF/image_1.jpg <DATA-DIR>/GIF/image_2.jpg <RESULT-DIR>/gif_schizo.gif`
3. **(P1)** `python mergeFiles.py <DATA-DIR>/PDF/file.pdf <DATA-DIR>/ZIP/animals.zip <RESULT-DIR>/pdfzip.pdf`
4. **(P2)** `python mergeGIFJS.py <DATA-DIR>/JS/alert.js <RESULT-DIR>/GIFJS/gifjs.gif`
5. **(P3)** `python mergeJAVAJS.py <DATA-DIR>/JAVA/HelloWorld.java <DATA-DIR>/JS/alert.js <RESULT-DIR>`
6. **(P4)** `python angecryption.py <DATA-DIR>/ZIP/a.zip <DATA-DIR>/FLV/video.flv <RESULT-DIR>/ZIPFLV/zipflv.zip 'MySuperSecureKey' aes > <CODE-DIR>/tmp.py` (NOTE: `<CODE-DIR>/tmp.py` contains python code to decrypt the resulting polyglot. This script will be manipulated to fit the paths of this experiment and the resulting script will be saved in `code/` as `crypt.py`)
7. **(P5)** `python mergePDFZIPJPGchimera.py <DATA-DIR>/JPG/image.jpg <RESULT-DIR>/chimera.pdf`

You can also call one or more scripts manually by using the commands from this list.

## Results  

`bmp_schizo.bmp` (**S1**):  
Open with Apple-Preview/Google-Chrome/Mozilla-Firefox/Safari to see the blue-red image and open with Universal Viewer to see the black-white image.  

`gif_schizo.gif` (**S2**):  
Open with Apple-Preview/Google-Chrome/Mozilla-Firefox/MS-Preview to see the orange GIF text and open with MS-Paint to see the violet GIF text. MS-Paint ignores frame rate and shows last frame.  

`pdfzip.pdf` (**P1**):  
Open with any PDF-Viewer (e.g. Apple-Preview or Adobe-Acrobat-Reader) to see the PDF file and execute "unzip polyglot.pdf" (on MacOS) to extract the ZIP-archive.  

`GIFJS/gifjs.gif` (**P2**):  
Open GIFJS/index.html with any browser to execute gifjs.gif as javascript and as gif image.  

`HelloWorld.java.html` (**P3**):  
Rename to HelloWorld.java to use it as java source file. Rename to HelloWorld.java.html (or HelloWorld.html or any other name with the extention .html) to execute javascript code.  

`ZIPFLV/zipflv.zip` (**P4**):  
Unzip with any unzipping tool to see archive content. Run crypt.py to decrypt to a valid FLV video.  

`chimera.pdf` (**P5**):  
Open with Apple-Preview to see PDF content, open with GIMP to see JPEG content, extract with any unzipping tool to get the archive content.  
