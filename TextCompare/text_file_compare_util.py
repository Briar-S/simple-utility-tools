import PySimpleGUI as sg
import os
class TextCompareUtility():
    sg.theme('Light Grey 6')

    def CreateWindow(self):#creates layout and draws window for use when reading events
        form_rows = [[sg.Text('Enter 2 files to comare')],
                     [sg.Text('Checks if file 1 contains lines that file 2 does not')],
                     [sg.HorizontalSeparator()],
                        [sg.Text('File 1', size=(10, 1)), sg.InputText(key='-file1-'), sg.FileBrowse()],
                        [sg.Text('File 2', size=(10, 1)), sg.InputText(key='-file2-'), sg.FileBrowse(target='-file2-')],
                        [sg.Text('Output', size=(10, 1)), sg.InputText(key='-file3-'), sg.FileBrowse(target='-file3-')],
                     [sg.HorizontalSeparator()],
                        [sg.Text('Options')],
                        [sg.Checkbox('Swap comparison direction?', default=False, key="-swap-"), sg.VerticalSeparator(), sg.Checkbox('Add Text seperators? (useful for append)', default=True, key="-titlecard-")],
                        [sg.Radio('Append', "RADIO1", default=True)],
                        [sg.Radio('Overwrite', "RADIO1", default=False, key="-overwrite-")],
                     [sg.HorizontalSeparator()],
                     [sg.Submit(), sg.Cancel()]]
        return sg.Window('File Compare', form_rows, resizable=True, finalize=True)

    def OpenFixRead(self, f1, f2): #appends a /n, then reads. weird python read quirk workaround
        curFile = open(f1,'r').readlines()
        curFile[-1:] = [str(curFile[-1])+'\n']

        oldFile = open(f2,'r').readlines()
        oldFile[-1:] = [str(oldFile[-1])+'\n']

        return curFile, oldFile

    def CompareFiles(self, f1, f2, f3, swap, owrite, tCard): #Compares Files, obviously

        curFile, oldFile = self.OpenFixRead(f1,f2) if swap else self.OpenFixRead(f2,f1) #swaps files on flag

        outF = open(f3, "w") if owrite else open(f3, "a") #overwrite flag determines whether file is appended or rewritten

        if(tCard): #titlecard flag puts in aesthetic text
            outF.write("=================\nFollowing lines exist in " + (f2 if swap else f1) + " but not in " + (f1 if swap else f2) + "\n-----------------\n")

        for line in oldFile: #actual comparison and write
            if (curFile.count(line) == 0 and line != '' and line != None and line != ' ' and line !='\n'): #only if line is not blank essentially
                outF.write(line)
        outF.close()

    def Functionality(self): #essentially main(), but eff keywords even if it doesnt matter here
        window = self.CreateWindow()

        while True:
            event, values = window.read() #Reads the window object values stored when interacting with the window

            if any((event == 'Cancel', event == "Exit", event == sg.WIN_CLOSED)): #if X, or cancel pressed, break loop (closes window)
                break

            elif any((event != 'Submit', values['-file1-'] == '', values['-file2-'] == '', values['-file3-'] == '')): #if a path isnt filled out, toss an error message (Dont close window)
                sg.popup_error('Error, likely missing a file path in selection')

            elif(event == 'Submit' and values['-file1-'] != '' and values['-file2-'] != '' and values['-file3-'] != ''): #if all is well, compare and write
                self.CompareFiles(values['-file1-'], values['-file2-'], values['-file3-'], values['-swap-'], values['-overwrite-'], values['-titlecard-'])
                sg.popup('Files Compared Successfully')

        window.close()
        exit(0)

TextCompareUtility().Functionality() #main call of the program which allows this file to be ran from another project easily