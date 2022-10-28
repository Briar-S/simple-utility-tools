import PySimpleGUI as sg
import os
class TextCompareUtility():
    sg.theme('Light Grey 6')

    def TxtCompLayout():
        #This creates the basic layout of the window using pysimpleGUI and returns a window value
        form_rows = [[sg.Text('Enter 2 files to comare')],
             [sg.Text('Checks if file 2 contains lines that file 1 does not')],
             [sg.HorizontalSeparator()],
                [sg.Text('File 1', size=(10, 1)), sg.InputText(key='-file1-'), sg.FileBrowse()],
                [sg.Text('File 2', size=(10, 1)), sg.InputText(key='-file2-'), sg.FileBrowse(target='-file2-')],
                [sg.Text('Output', size=(10, 1)), sg.InputText(key='-file3-'), sg.FileBrowse(target='-file3-')],
             [sg.HorizontalSeparator()],
             [sg.Text('Options')],
                [sg.Checkbox('Swap comparison direction?', default=False, key="-swap-")],
                [sg.Radio('Append', "RADIO1", default=True)],
                [sg.Radio('Overwrite', "RADIO1", default=False, key="-overwrite-")],
             [sg.HorizontalSeparator()],
             [sg.Submit(), sg.Cancel()]]

        return sg.Window('File Compare', form_rows, resizable=True, finalize=True)

    def CompareFiles(f1, f2, f3, swap, owrite):
        with open(f1,'a+') as fone:
            fone.write('\n')
        with open(f2,'a+') as ftwo:
            ftwo.write('\n')
        
        curF = open(f1, "r")
        curFile = curF.readlines()
        curF.close()

        oldF = open(f2, "r")
        oldFile = oldF.readlines()
        oldF.close()        

        with open(f1, 'rb+') as filehandle:
            filehandle.seek(-2, os.SEEK_END)
            filehandle.truncate()

        with open(f2, 'rb+') as filehandle:
            filehandle.seek(-2, os.SEEK_END)
            filehandle.truncate()

        if(owrite == True):
            outF = open(f3, "w")
        else:
            outF = open(f3, "a")

        outF.write("\n=================\n")
        if(swap == True):
            outF.write("Following lines exist in " + f1 + " but not in " + f2)
            curFile, oldFile = oldFile, curFile
        else:
            outF.write("Following lines exist in " + f2 + " but not in " + f1)

        outF.write("\n=================\n")
        for line in oldFile:
            if (curFile.count(line) == 0 and line != '' and line != None and line != ' ' and line !='\n'):
                outF.write(line)

        outF.close()
    

    while True:

        button, values = TxtCompLayout.read() #Reads the window object values stored when interacting with the window

        f1, f2, f3 = values['-file1-'], values['-file2-'], values['-file3-'] #stores file paths gotten from the window

        if any((button == 'Cancel', button == "Exit", button == sg.WIN_CLOSED)): #if X, or cancel pressed, break loop (closes window)
            break

        if any((button != 'Submit', f1 == '', f2 == '', f3 == '')): #if a path isnt filled out, toss an error message (Dont close window)
            sg.popup_error('Error, likely missing a file path in selection')

        if(button == 'Submit' and f1 != '' and f2 != '' and f3 != ''):
            CompareFiles(f1, f2, f3, values['-swap-'], values['-overwrite-'])
            sg.popup('Files Compared Successfully')

    window.close()