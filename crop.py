from PyPDF2 import PdfFileWriter, PdfFileReader
import os

input_file = "Book1.pdf"
output_file = "Book1c.pdf"

os.system('gswin32c.exe -q -sDEVICE=bbox -dNOPAUSE -dBATCH "%s" 2> bbox.txt' % input_file)

with open("bbox.txt", "r") as f:
	bbox_lines = f.readlines()

bbox = None
for l in bbox_lines:
	if l.startswith("%%BoundingBox: "):
		bbox = [ int(b) for b in l[len("%%BoundingBox: "):].split(" ") ]
if bbox is None:
	raise Exception("Could not determine bounding box.")
print bbox

f = open(input_file, "rb")
g = open(output_file, "wb")

input1 = PdfFileReader(f)
output = PdfFileWriter()

numPages = input1.getNumPages()
print "document has %s pages." % numPages


for i in range(numPages):
	page = input1.getPage(i)
	print page.mediaBox
	print page.trimBox
	print page.cropBox
	print page.artBox
	page.trimBox.lowerLeft = (bbox[0], bbox[1])
	page.trimBox.upperRight = (bbox[2], bbox[3])
	page.cropBox.lowerLeft = (bbox[0], bbox[1])
	page.cropBox.upperRight = (bbox[2], bbox[3])
	output.addPage(page)

output.write(g)
