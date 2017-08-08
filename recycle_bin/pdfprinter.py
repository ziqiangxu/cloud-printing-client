import os
def printer():
    #Change the workplace to the documents' directory
    os.chdir("c:\\users\\hyike\\desktop\\print\\pdf\\")
    #The first time get the list of the files
    filelist=os.listdir(".\\")
    num=0
    for i in filelist:
        num=num+1
        os.rename(i,str(num)+".pdf")
    exepath="\"C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe\""
    #Get the list of files again
    filelist=os.listdir(".\\")
    for i in filelist:
        cmd=exepath+" /h /p "+i
        os.system(cmd)
        print(cmd)
