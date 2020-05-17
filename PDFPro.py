import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path

def ExtractInformation(pdfpath):
	with open(pdfpath,'rb') as f:
		pdf=PdfFileReader(f)
		information= pdf.getDocumentInfo()
		number_of_pages = pdf.getNumPages()
		
	txt=f"""
	Information about {pdfpath}:
	
	Author: {information.author}
	Creator: {information.creator}
	Producer: {information.producer}
	Subject: {information.subject}
	Title: {information.title}
	Number of Pages: {number_of_pages}
	"""
	print(txt)
	return information

def Merge_PDFs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def RotateRight(PDFPath,RotatePage):
    pdfwriter = PdfFileWriter()
    pdfreader = PdfFileReader(PDFPath)
    
    for PageNum in range(pdfreader.getNumPages()):
    	if PageNum == RotatePage-1:
    		pdfwriter.addPage(pdfreader.getPage(PageNum).rotateClockwise(90))
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
    	else:
    		pdfwriter.addPage(pdfreader.getPage(PageNum))


    with open(PDFPath, 'wb') as fh:
        pdfwriter.write(fh)

# Create the Help Menu
my_parser = argparse.ArgumentParser(prog='python3 PDFPro.py',usage='%(prog)s [options] PDF', description='Manipulates PDF files. Merge PDF files. View metadata. Rotate pages')

# Create and Add Arguments to the Help Menu
my_parser.add_argument('file', metavar='PDF', type=str,nargs='+', help='the path to PDF files')	# Add the URL argument
#my_parser.add_argument('-s','--split',metavar='page',action='store', default='0',type=int, help='Split PDF at Specified Page')
my_parser.add_argument('-d','--data',action='store_true',help='View metadata from the PDF File')
my_parser.add_argument('-m','--merge',metavar='[Output File]',default='empty',action='store',type=str, help='Merge multpile PDF files into one file' )
my_parser.add_argument('-r','--right',metavar='page', action='store',default='0',type=int,help='Rotate specified page # to the right 90 degrees')
my_parser.add_argument('-l','--left',metavar='page', action='store',default='0',type=int,help='Rotate specified page # to the left 90 degrees')

# Get Arguments
arglist= my_parser.parse_args()	

# bool used to determine if the files or list of files are valid
KeepGoing = True

# Check files to see if they have the pdf extension and if they are a valid file on the system
for p in arglist.file:
	if '.pdf' in p or '.PDF' in p:	
		if os.path.isfile(p) == False:				
		# Notify user that the file is not valid and set KeepGoing to false so the program won't continue
			print(p +' is not a valid PDF file')
			KeepGoing=False

if KeepGoing==True:
	if arglist.merge != 'empty':
		outputfile=''
		if '.pdf' in arglist.merge:
			outputfile=arglist.merge
		else:
			outputfile=arglist.merge+'.pdf'
			
		MergePDFs(arglist.file,outputfile)
		
	if arglist.data == True:
		for pd in arglist.file:
			ExtractInformation(pd)
	#if arglist.split > 0:
	#	print('Change Page')
	
	if arglist.left > 0:
		RotateLeft(arglist.file[0], arglist.left)

	if arglist.right > 0:
		RotateRight(arglist.file[0],arglist.right)


