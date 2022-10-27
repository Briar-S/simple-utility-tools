import PySimpleGUI as sg
sg.theme('Light Grey 6')

def CompareFiles(f1, f2, f3, swap, owrite):
    curF = open(f1, "r")
    curFile = curF.readlines()
    curF.close()

    oldF = open(f2, "r")
    oldFile = oldF.readlines()
    oldF.close()

    if(owrite == True):
        outF = open(f3, "w")
    else:
        outF = open(f3, "a")

    if(swap == True):
        outF.write("Following lines exist in " + f1 + " but not in " + f2)
        curFile, oldFile = oldFile, curFile
    else:
        outF.write("Following lines exist in " + f2 + " but not in " + f1)

    outF.write("\n=================\n")
    for line in oldFile:
        if (curFile.count(line) == 0):
            outF.write(line)
    outF.write("\n=================\n")
    oldF.close()

form_rows = [[sg.Text('Enter 2 files to comare')],
             [sg.Text('Checks if file 2 contains lines that file 1 does not')],
             [sg.HorizontalSeparator()],
             [sg.Text('File 1', size=(10, 1)),
                sg.InputText(key='-file1-'), sg.FileBrowse()],
             [sg.Text('File 2', size=(10, 1)), sg.InputText(key='-file2-'),
              sg.FileBrowse(target='-file2-')],
             [sg.Text('Output', size=(10, 1)), sg.InputText(key='-file3-'),
              sg.FileBrowse(target='-file3-')],
             [sg.HorizontalSeparator()],
             [sg.Text('Options')],
             [sg.Checkbox('Swap comparison direction?', default=False, key="-swap-")],
             [sg.Radio('Append', "RADIO1", default=True)],
             [sg.Radio('Overwrite', "RADIO1", default=False, key="-overwrite-")],
             [sg.Submit(), sg.Cancel()]]
             
window = sg.Window('File Compare', form_rows, resizable=True, finalize=True)

while True:
    button, values = window.read()

    f1, f2, f3 = values['-file1-'], values['-file2-'], values['-file3-']

    if any((button == 'Cancel', button == "Exit", button == sg.WIN_CLOSED)):
        break

    if any((button != 'Submit', f1 == '', f2 == '', f3 == '')):
        sg.popup_error('Error, likely missing a file path in selection')

    if(f1 != '' and f2 != '' and f3 != ''):
        CompareFiles(f1, f2, f3, values['-swap-'], values['-overwrite-'])
        sg.popup('Files Compared Successfully')
window.close()