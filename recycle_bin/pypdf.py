from PyPDF2 import PdfFileWriter,PdfFileReader
input1=PdfFileReader(open("C:\\printer\\winapi.pdf","rb"))
print(input1.getNumPages())