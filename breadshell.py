# os library is NEEDED for this to run
import os

# import time
try:
    import time
except:
    print('time not installed, installing now')
    os.system('sudo apt install python3-time -y')
    import time

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

# version number...
version = '0.3'

# define colors
class c:
    red = colorama.Fore.RED
    yellow = colorama.Fore.YELLOW
    green = colorama.Fore.GREEN
    blue = colorama.Fore.BLUE
    magenta = colorama.Fore.MAGENTA
    cyan = colorama.Fore.CYAN
    r = colorama.Fore.RESET # resets color to default

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
    
def start_calculator():
    while True:
        cmd = input(f'{c.cyan}calculator{c.r} > ')
        if cmd == 'exit':
            utillauncher()
        else:
            exec(f'print({cmd})')

def start_python():
    cmd = input(f'{c.cyan}python{c.r} > ')
    while True:
        if cmd == 'exit':
            utillauncher()
        else:
            exec(cmd)


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
        exec(f'start_{games[int(game)-1]}()')

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
        exec(f'start_{utilities[int(utility)-1]}()')

# start of program, shown when opening the file
print(f'version {version}')
print('type bhelp for a list of custom commands')

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
    breadshell version {version}

    --- CUSTOM COMMANDS ---

    bhelp - open this page
    bfetch - get system information
    binst <package-name> - easy way to install packages
    buninst <package-name> - easy way to uninstall packages
    bpkgs <query> - search packages
    bgames - start game launcher
    butils - start utility launcher
    exit - exits breadshell
    ''')
            
        # breadfetch (bfetch)
        elif cmd.startswith('bfetch'):
            print('making this later, for now just have neofetch')
            subprocess.run(['bash','-c','neofetch'])

        # breadinstall (binst)
        elif cmd.startswith('binst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt install {cmd.split(" ")[1]}'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breaduninstall (buninst)
        elif cmd.startswith('buninst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt remove {cmd.split(" ")[1]}'])
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
            
        # if none of the above commands were selected, it will run this (run any command inside the input)
            
        else:
            try:
                subprocess.run(['bash','-c',cmd])
            except:
                fatalerror()
main()