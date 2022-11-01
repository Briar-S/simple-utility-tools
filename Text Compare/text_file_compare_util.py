import PySimpleGUI as sg
import os
class TextCompareUtility():
    sg.theme('Light Grey 6')


    def CreateWindow(self):
        #This creates the basic layout of the window using pysimpleGUI and returns a draw created window object
        #Just works. if you know PySimpleGUI go ahead and change it to your desire
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

    def CompareFiles(self, f1, f2, f3, swap, owrite):
        #Compares Files, obviously
        
        #python is stupid and doesnt read the last line properly because it stores \n for some stupid reason instead of truncating it in list storage and smart adding it when writing to a file from a list idk its stupid but i understand it would really just help my particular edge case and hurt other cases but im still mad rahh
        #anyways this snippet below basically does what readlines should do anyway and adds a \n to the end of the last line, but that means at the end you gotta truncate it off if you wanna restore the files to the original but yeah anyways im still mad i thought writing this would make me feel better but really just made me more mad because of how dum that is in a so called "smart language" like wahtever man im over it now. nvm not over it why am i writing this in python i shouldve just done a stupid c# project instead that stuff is less frustrating anyways why am i still typing here. tbh its prob bc its sortve funny and long comments make me laugh. oh well. banana. apple. penguin. words. ight im done now i think.
        with open(f1,'a+') as fone:
            fone.write('\n')
        with open(f2,'a+') as ftwo:
            ftwo.write('\n')
        
        #stores 2 lists based on the files you wanna compare
        curF = open(f1, "r")
        curFile = curF.readlines()
        curF.close()

        oldF = open(f2, "r")
        oldFile = oldF.readlines()
        oldF.close()        

        #heres the truncation code to fix readlines idiocy
        #nope not done.
        #screw this thing man its so dum i had to import another project which i was trying to avoid, i mean i couldlve done this the hard way of actual data changes but thats like really lame and takes too long for something as silly as this project
        #like take the input right, if its reading lines from a file, which is the only thing that readlines() really does cause theres other better ways to read things otherwise, if open from file, store an initial array key meaning its a file, truncate the /n, then when writing the list that is stored with the key, add /n at the end of each write line idk it just seems so tedious to add this for every program that would be reading from a file. like literally on a 3 line string array it would be like [string1\n, string2\n, string 3] like, add a \n to 3 or truncate cause thats stupid as hell. anyways yeah im done now.
        with open(f1, 'rb+') as filehandle:
            filehandle.seek(-2, os.SEEK_END)
            filehandle.truncate()

        with open(f2, 'rb+') as filehandle:
            filehandle.seek(-2, os.SEEK_END)
            filehandle.truncate()

        if(owrite == True): #if overwrite flag, open with write or append capabilities yah know
            outF = open(f3, "w")
        else:
            outF = open(f3, "a")

        outF.write("\n=================\n")
        #swap flag that swaps the list var names basically and prints a title for the output
        #TODO: add a flag that puts title card on comparison happening or not
        if(swap == True):
            outF.write("Following lines exist in " + f1 + " but not in " + f2)
            curFile, oldFile = oldFile, curFile #yay you love to see this actually work which python feels like it rarely does for me which is maybe because python is just annoying to me for some reason idk, screw data scientists for making this language so quick, but so frustrating for complexish things, like literally any other language takes so much longer to setup, and pythong is so quick to setup but python i swear just takes so much longer to write but yeah also why is python so anal about whitespace, like thats so stupid, its just extra storage being taken up. i mean its a minimal amount compared to how bloated python programs end up being anyways
        else:
            outF.write("Following lines exist in " + f2 + " but not in " + f1)
        outF.write("\n=================\n")
        
        #actual comparison is super easy, but getting files setup in python is not, ironically.
        #this just calls count(string) for one of the lists, and sees if its zero, meaning the line in the foreach is unique.
        #also this semantic feels so silly, like just call it foreach, it makes so much more sense and rolls off the tongue
        for line in oldFile: 
            if (curFile.count(line) == 0 and line != '' and line != None and line != ' ' and line !='\n'):
                outF.write(line)

        outF.close()

    def Functionality(self):
        window = self.CreateWindow()
        while True:
            button, values = window.read()#Reads the window object values stored when interacting with the window

            f1, f2, f3 = values['-file1-'], values['-file2-'], values['-file3-'] #stores file paths gotten from the window

            if any((button == 'Cancel', button == "Exit", button == sg.WIN_CLOSED)): #if X, or cancel pressed, break loop (closes window)
                break

            elif any((button != 'Submit', f1 == '', f2 == '', f3 == '')): #if a path isnt filled out, toss an error message (Dont close window)
                sg.popup_error('Error, likely missing a file path in selection')

            elif(button == 'Submit' and f1 != '' and f2 != '' and f3 != ''):
                self.CompareFiles(f1, f2, f3, values['-swap-'], values['-overwrite-'])
                sg.popup('Files Compared Successfully')

        window.close()
        exit(0)

TextCompareUtility().Functionality()