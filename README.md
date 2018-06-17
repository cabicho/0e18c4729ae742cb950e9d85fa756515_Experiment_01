# CheckResearch.org [Experiment](https://checkresearch.org/Experiment/View/9fc99c57-b861-44e3-bf23-d44f4bb208b1)

 Publication [""schizophrene" und "polyglotte" Dateien"](https://dblp.uni-trier.de/search?q=%22schizophrene%22+und+%22polyglotte%22+Dateien) by "Cem Bicer"

## HOWTO

In this experiment I demonstrate to you how file format hacks can lead to so called "schizophrenic" files and file "polyglots".

"Schizophrenic" files are files that show different outputs when opened with different parsers. They are crafted by merging two files with the same file format into a single file. Some parsers show the first file content some the other.

"Polyglot" files are files that merge two or more different file formats into one valid file which can be openend with parsers that support at least one of the merged formats. Depending on the parser the file identifies as a different file type.

To run all proof of concepts (PoCs) execute the main.py script.

All PoCs present in this experiment are adopted from Ange Albertini's ["Funky File Formats"](https://events.ccc.de/congress/2014/Fahrplan/system/attachments/2562/original/Funky_File_Formats.pdf).

## Experiment Setup

### Experiment Content

This experiment consists of two parts: schizophrenic and golyglot files. Each of these parts contains subsections that contain one or more PoCs. Following list shows all PoCs that are present in this experiment and there respective ID in brackets.

1. schizophrenic files **(S)**
   1. PDF **(S1)**
   2. BMP **(S2)**
   3. GIF **(S3)**
2. polyglot files **(P)**
   1. by concatenation
      1. PDF ZIP **(P1)**
   2. host/parasite
      1. GIF JS **(P2)**
      2. JAVA JS **(P3)**
   3. encryption
      1. FLV ZIP **(P4)**
   4. chimera
      1. PDF ZIP JPG **(P5)**

### Hardware/Software

Describe your Hardware & Software setup

## Experiment Assumptions

Make it explicit here if you made any assumptions in your experiment

## Preconditions

Something others need to prepare in order to run your code (e.g. libraries, python modules, ...)

## Experiment Steps

Describe each step of the experiment

## Results

Describe your results
