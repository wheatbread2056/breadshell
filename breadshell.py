# os library is NEEDED for this to run
import os

# IMPORT ALL DEPENDENCIES

# import time
try:
    import time
except:
    print('time not installed, installing now')
    os.system('sudo apt install python3-time -y')
    import time

# import datetime
try:
    import datetime
except:
    print('datetime not installed, installing now')
    os.system('sudo apt install python3-datetime -y')
    import datetime

# import random
try:
    import random
except:
    print('random not installed, installing now')
    os.system('sudo apt install python3-random -y')
    import random

# import colorama
try:
    import colorama
except:
    print('colorama not installed, installing now')
    os.system('sudo apt install python3-colorama -y')
    import colorama

# import subprocess
try:
    import subprocess
except:
    print('subprocess not installed, installing now')
    os.system('sudo apt install python3-subprocess -y')
    import subprocess

# import socket
try:
    import socket
except:
    print('socket not installed, installing now')
    os.system('sudo apt install python3-socket -y')
    import socket

# makes sure that bash shell is used
os.environ['SHELL'] = '/bin/bash'

# version number and other information
version = '0.5-dev4'
versiontype = 3 # 1 = release, 2 = prerelease, 3 = development build

# define colors
class c:
    red = colorama.Fore.RED
    yellow = colorama.Fore.YELLOW
    green = colorama.Fore.GREEN
    blue = colorama.Fore.BLUE
    magenta = colorama.Fore.MAGENTA
    cyan = colorama.Fore.CYAN
    white = colorama.Fore.WHITE
    black = colorama.Fore.BLACK
    r = colorama.Fore.RESET # resets color to default

# background colors
class bc:
    red = colorama.Back.RED
    yellow = colorama.Back.YELLOW
    green = colorama.Back.GREEN
    blue = colorama.Back.BLUE
    magenta = colorama.Back.MAGENTA
    cyan = colorama.Back.CYAN
    white = colorama.Back.WHITE
    black = colorama.Back.BLACK
    r = colorama.Back.RESET # resets color to default

# check if breadshell is installed
try:
    currentdir = os.getcwd()
    scriptdir = os.path.dirname(__file__)

    # if this doesn't work, it will give an error, which is how this works
    os.chdir('/usr/src/breadshell')
    if scriptdir == '/usr/src/breadshell':
        installed = True
        runfrominstall = True
    else:
        print(f'{c.red}breadshell is installed, but you are running it from a file instead{c.r}')
        installed = True
        runfrominstall = False

    # change back to the previous directory
    os.chdir(currentdir)

except:
    print(f'{c.red}breadshell is not installed, install it for more functionality{c.r}')
    installed = False
    runfrominstall = False

# basic functions
    
# returns yellow error
def throwerror(msg='An unknown error has occured'):
    print(f'{c.yellow}{msg}{c.r}')

# returns red error and exits to prevent corruption or something
def fatalerror(msg='A fatal error has occured, exiting immediately'):
    print(f'{c.red}{msg}{c.r}')
    exit()

# game scripts

# utility scripts

def startu_colortester():
    # random colors+chars for 256 characters
    chars = '`1234567890-=~!@#$%^&*()_+qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    str = ''
    for i in range(4096):
        a = random.randint(0,len(chars)-1)
        char = chars[a]
        b = random.randint(1,9)

        # wow this code is inefficient

        # skipping d since c is used for foreground colors
        if b == 1:
            d = c.red
        elif b == 2:
            d = c.yellow
        elif b == 3:
            d = c.green
        elif b == 4:
            d = c.blue
        elif b == 5:
            d = c.cyan
        elif b == 6:
            d = c.magenta
        elif b == 7:
            d = c.white
        elif b == 8:
            d = c.black
        elif b == 9:
            d = c.r

        # reroll colors to be used for background
        b = random.randint(1,9)

        if b == 1:
            e = bc.red
        elif b == 2:
            e = bc.yellow
        elif b == 3:
            e = bc.green
        elif b == 4:
            e = bc.blue
        elif b == 5:
            e = bc.cyan
        elif b == 6:
            e = bc.magenta
        elif b == 7:
            e = bc.white
        elif b == 8:
            e = bc.black
        elif b == 9:
            e = bc.r

        # add it to the main string
        str=str+d+e+char

    # +c.r+bc.r is needed to reset the colors
    print(str+c.r+bc.r)

def startu_calculator():
    while True:
        # command (meant to be an expression)
        cmd = input(f'{c.cyan}calculator{c.r} > ')
        if cmd == 'exit':
            utillauncher()
        # funny easter egg
        elif cmd == '9+10':
            print(21)
        else:
            try:
                # print() is needed because simply executing 1+1 does not display 2
                exec(f'print({cmd})')
            except:
                throwerror()

def startu_python():
    while True:
        # command
        cmd = input(f'{c.cyan}python{c.r} > ')

        if cmd == 'exit':
            utillauncher()
        else:
            try:
                exec(cmd)
            except:
                throwerror()


# game launcher
def games():
    globalversion = '0.2'
    # list amount of games here
    games = ['GAMES COMING SOON']

    print(f'bread games version {globalversion}')
    print(f'please select the game you would like to start ({len(games)} found):')

    i = 1
    for game in games:
        print(f'{c.yellow}{i} - {game}')
        i += 1
    
    print(f'{c.yellow}exit - exit')

    game = input(f'{c.cyan}breadgames{c.r} > ')

    if game == 'exit':
        main()
    if games[int(game)-1] in games:
        print(f'Loading {games[int(game)-1]}...')
        exec(f'startg_{games[int(game)-1]}()')

# utility launcher (totally not just modified game launcher)
def utillauncher():
    globalversion = '0.2'
    # list amount of games here
    utilities = ['colortester','calculator','python']

    print(f'bread utilities version {globalversion}')
    print(f'please select the utility you would like to start ({len(utilities)} found):')

    i = 1
    for utility in utilities:
        print(f'{c.yellow}{i} - {utility}')
        i += 1

    print(f'{c.yellow}exit - exit')

    utility = input(f'{c.cyan}breadutils{c.r} > ')

    if utility == 'exit':
        main()
    if utilities[int(utility)-1] in utilities:
        print(f'Loading {utilities[int(utility)-1]}...')
        exec(f'startu_{utilities[int(utility)-1]}()')

# start of program, shown when opening the file
print(f'version {c.cyan}{version}{c.r}, latest login {c.magenta}{datetime.datetime.now()}{c.r}')
print(f'type {c.yellow}bhelp{c.r} for a list of custom commands')
# main loop
def main():
    while True:
        # main input (user@hostname path/to/directory > command typed in)
        try:
            cmd = input(f"{c.blue}{os.getlogin()}@{socket.gethostname()} {c.green}{os.getcwd()}{c.r} > ")
        except:
            fatalerror()

        # for special commands
            
        # change directory (cd)
        if cmd.startswith('cd'):
            try:
                os.chdir(cmd.split(' ')[1])
            except:
                throwerror('Invalid directory, or a directory was not specified')

        # breadhelp (bhelp)
        elif cmd.startswith('bhelp'):
            print(f'''
    breadshell version {c.cyan}{version}{c.r}

    --- CUSTOM COMMANDS ---

    {c.yellow}bhelp{c.r} - open this page
    {c.yellow}bfetch{c.r} - get system information
    {c.yellow}inst{c.r} {c.cyan}<package-name>{c.r} - easy way to install packages
    {c.yellow}uninst{c.r} {c.cyan}<package-name>{c.r} - easy way to uninstall packages
    {c.yellow}bpkgs{c.r} {c.cyan}<query>{c.r} - search packages
    {c.yellow}bgames{c.r} - start game launcher
    {c.yellow}butils{c.r} - start utility launcher
    {c.yellow}version{c.r} - displays version information
    {c.red}exit{c.r} - exits breadshell
    ''')
            
        # breadfetch (bfetch)
        elif cmd.startswith('bfetch'):
            print('making this later, for now just have neofetch')
            subprocess.run(['bash','-c','neofetch'])

        # breadinstall (inst)
        elif cmd.startswith('inst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt install {cmd.split(" ")[1]} -y'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breaduninstall (uninst)
        elif cmd.startswith('uninst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt remove {cmd.split(" ")[1]} -y'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breadpackages (bpkgs)
        elif cmd.startswith('bpkgs'):
            try:
                subprocess.run(['bash','-c',f'apt search {cmd.split(" ")[1]}'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # exit... self explanatory
        elif cmd.startswith('exit'):
            exit()

        # "developer commands"
            
        # throw a generic error
        elif cmd.startswith('dev-generic-error'):
            throwerror()
            
        # throw a FATAL generic error, which is red...
        elif cmd.startswith('dev-generic-fatalerror'):
            fatalerror()

        # launch games
        elif cmd.startswith('bgames'):
            games()

        # launch utilities
        elif cmd.startswith('butils'):
            utillauncher()

        # display version info
        elif cmd.startswith('version'):
            print(f'breadshell version {c.cyan}{version}{c.r}')

            # display version type
            if versiontype == 1:
                print(f'this is a {c.green}release{c.r} build of breadshell')
            elif versiontype == 2:
                print(f'this is a {c.yellow}prerelease{c.r} build of breadshell')
            elif versiontype == 3:
                print(f'this is a {c.magenta}development{c.r} build of breadshell')
            else:
                print(f'this is an {c.red}unknown{c.r} build of breadshell')

            # display installation status
            if installed == True:
                print(f'breadshell is {c.green}installed{c.r}')
            else:
                print(f'breadshell is {c.red}not installed{c.r}')

            # running from file or not
            if runfrominstall == True:
                print(f'running from {c.green}install{c.r}')
            else:
                print(f'running from {c.red}file{c.r}')

            print(f'made by {c.blue}wheatbread2056{c.r} on github')
            
        # if none of the above commands were selected, it will run this (run any command inside the input)
            
        else:
            try:
                subprocess.run(['bash','-c',cmd])
            except:
                fatalerror()
            
# run main function (moved from while loop to function in 0.3 so the user can be returned back to the shell in case anything goes wrong)
main()