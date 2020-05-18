# Author: Matthew Baker
# Date Created: 5/16/2020
# Date Modified: 5/17/2020

import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path

def ExtractInformation(pdfpath):
	with open(pdfpath,'rb') as f:
		pdf=PdfFileReader(f)
		info= pdf.getDocumentInfo()
		NumOfPages = pdf.getNumPages()
		
	output=f"""
	Information about {pdfpath}:
	
	Author: {info.author}
	Creator: {info.creator}
	Producer: {info.producer}
	Subject: {info.subject}
	Title: {info.title}
	Number of Pages: {NumOfPages}
	"""
	print(output)

def MergePDFs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdfreader = PdfFileReader(path)
        for page in range(pdfreader.getNumPages()):
            pdf_writer.addPage(pdfreader.getPage(page))	# Add each page to the writer object

    # Write the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def RotateRight(PDFPath,RotatePage):
    pdfwriter = PdfFileWriter()
    pdfreader = PdfFileReader(PDFPath)
    
    for PageNum in range(pdfreader.getNumPages()):
    	if PageNum == RotatePage-1:
    		pdfwriter.addPage(pdfreader.getPage(PageNum).rotateClockwise(90))
    		print("Page " + str(RotatePage)+" Rotated CW 90 Degrees In " + PDFPath)
    	else:
    		pdfwriter.addPage(pdfreader.getPage(PageNum))


    with open(PDFPath, 'wb') as fh:
        pdfwriter.write(fh)
	

def RotateLeft(PDFPath,RotatePage):
    pdfwriter = PdfFileWriter()
    pdfreader = PdfFileReader(PDFPath)
    
    for PageNum in range(pdfreader.getNumPages()):
    	if PageNum == RotatePage-1:
    		pdfwriter.addPage(pdfreader.getPage(PageNum).rotateCounterClockwise(90))
    		print("Page " + str(RotatePage)+" Rotated CCW 90 Degrees In " + PDFPath)
    	else:
    		pdfwriter.addPage(pdfreader.getPage(PageNum))

    with open(PDFPath, 'wb') as fh:
        pdfwriter.write(fh)


def RemovePage(PDFPath,PageNum):
	pdfwriter= PdfFileWriter()
	pdfreader= PdfFileReader(PDFPath)
	
	for page in range(pdfreader.getNumPages()):
		if page != PageNum-1:
			pdfwriter.addPage(pdfreader.getPage(page))
		else:
			print("Page Removed")
	
	with open(PDFPath,'wb') as fh:
		pdfwriter.write(fh)


# Create the Help Menu
my_parser = argparse.ArgumentParser(prog='python3 pdfman.py',usage='%(prog)s [options] PDF', description='Manipulates PDF files. Merge PDF files. View metadata. Rotate pages')

# Add Arguments to the Help Menu
my_parser.add_argument('file', metavar='PDF', type=str,nargs='+', help='the path to PDF files')	# Add the URL argument
my_parser.add_argument('-i','--info',action='store_true',help='View metadata from the PDF File')
my_parser.add_argument('-m','--merge',metavar='[Output File]',default='empty',action='store',type=str, help='Merge multpile PDF files into one file' )
my_parser.add_argument('-r','--right',metavar='page', action='store',default='0',type=int,help='Rotate specified page # to the right 90 degrees')
my_parser.add_argument('-l','--left',metavar='page', action='store',default='0',type=int,help='Rotate specified page # to the left 90 degrees')
my_parser.add_argument('-d','--remove', metavar='page', action='store',default='0',type=int,help='Remove specified page from the PDF file')

# Get Arguments
arglist= my_parser.parse_args()	


KeepGoing = True 	# bool used to determine if the files or list of files are valid


# Check files to see if they have the pdf extension and if they are a valid file on the system
for p in arglist.file:
	if '.pdf' in p or '.PDF' in p:	
		if os.path.isfile(p) == False:				
			print(p +' is not a valid PDF file')	# Notify user that the file is not valid and set KeepGoing to false so the program won't continue
			KeepGoing=False


if KeepGoing==True:						# bool used to check if PDFs are valid. 

	if arglist.merge != 'empty':				# Check if merge is selected
		outputfile=''
		if '.pdf' in arglist.merge:			# Add extension to end of output file if missing
			outputfile=arglist.merge
		else:
			outputfile=arglist.merge+'.pdf'
		MergePDFs(arglist.file,outputfile)		# Merge the PDFs into one file with the user specified output file name.
		
	if arglist.info == True:				# Output the Metadata for the PDFs if selected
		for pd in arglist.file:
			ExtractInformation(pd)
			
	for pdf in arglist.file:				# iterate through the files and manipulate the pages specified for each PDF		
		if arglist.remove > 0:				# Remove specfied page from the PDF
			RemovePage(pdf, arglist.remove)
		if arglist.left > 0:				# Rotate specified page CCW 90 degrees in the PDF
			RotateLeft(pdf, arglist.left)
		if arglist.right > 0:				# Rotate specified page CW 90 degrees in the PDF
			RotateRight(pdf,arglist.right)

