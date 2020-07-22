"""
Few lines of python for taking the files downloaded and stored by Tachiyomi on Android and converting them into a single PDF.  
"""

from fpdf import FPDF   # PDF Building
from PIL import Image
import sys, getopt      # Command Line Opts
import os               # Directory directing
import re               # Regular Expressions because sorting sucks

outputFileName = ''
inputDir = ''

def makePdf(pdfFileName, listPages, dir):
    if (dir):
        dir += "/"

    #cover = Image.open(str(listPages[0][0]))
    #width, height = cover.size

    #pdf = FPDF('P', 'mm', (180,270))
    pdf = FPDF('P', 'mm', (210,297))
    pdf.set_margins(0,0,0)
    
    for chapter in listPages:
        for page in chapter:
            #print (str(page))
            pdf.add_page()

            # Code for attempting to fit manga page to the pdf page size while keeping ratios. Kept breaking height 
            """
            im = Image.open(page)
            ratio = im.width / im.height
            if ratio > 1:
                width = 210
                height = 297/ratio
            else:
                width = 210*ratio
                height = 297
            """                
            pdf.image(str(page), w=210, h=297)

    pdf.output(dir + pdfFileName, "F")

# Takes a single directory and creates a list of all *.png within sorted by Ch.XX.XX then YY.png
def buildPages(dir):
    chapters = []
    pages = []
    chapterPages = []
    for dI in os.listdir(dir):
        if os.path.isdir(os.path.join(dir,dI)):
            chapters.append(dir + '/' + dI)
    chapters = sortChapters(chapters)

    for chapter in chapters:
        chapterPages = []
        for page in os.listdir(chapter+'/'):
            if page.endswith(".png"):       
                chapterPages.append(chapter + '/' + page)
        chapterPages.sort()
        pages.append(chapterPages)
    return (pages)

# Takes a list of directories and sorts them based on Ch.XX.XX
def sortChapters(chapters):
    numbers = []
    for ch in chapters:
        num = [float(s) for s in re.findall(r'(?<=Ch\.)[0-9]*\.?[0-9]*',ch)]
        numbers.append(num[0])
    sortedChapters = [chapter for index,chapter in sorted(zip(numbers,chapters))]
    return (sortedChapters)


def main(argv):
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "ho:d:c:ev", ["help", "output=", "dir=", "cover=", "extras"])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('TachiToPDF.py -o <outputfile> -d <inputdirectory>')
            sys.exit(2)
        elif opt in ("-o", "--output"):
            if not arg.endswith(".pdf"):        # If the argument doesn't include ".pdf"
                arg += ".pdf"
            outputFileName = arg
        elif opt in ("-d", "--dir"):
            inputDir = arg
        elif opt == '-v':
            # TODO verbose mode?
            pass
        elif opt in ("-e", "--extras"):
            # TODO preserve extras
            pass
        elif opt in ("-c", "--cover"):
            # TODO add cover
            pass
        else:
            assert False, "unhandled option"

    listPages = buildPages(inputDir)
    #print (listPages)
    makePdf(outputFileName, listPages,inputDir)

if __name__ == "__main__":
   main(sys.argv[1:])
