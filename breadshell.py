# breadshell development build

# detect if running on wsl
try:
    with open('/proc/version', 'r') as f:
        if 'microsoft' in f.read().lower() or 'wsl' in f.read().lower():
            WSL = True
        else:
            WSL = False
except:
    WSL = False

failed_imports = []

# IMPORT ALL DEPENDENCIES --initial

# built-in libraries
import os
try:
    import curses
except:
    failed_imports.append('curses')
import time
import sys
import threading
import base64
import datetime
import random
import subprocess
import getpass
import socket
import re

# the point of this code is to install the modules if the user doesn't already have them installed

DISABLE_COLORS = False
DEFAULT_SETTINGS = False
LEGACY_PROMPT = False # just uses prompt() which was used in every version before 1.0

# import colorama
try:
    import colorama
except:
    try:
        os.system('pip install colorama --break-system-packages')
        import colorama
    except:
        DISABLE_COLORS = True
        failed_imports.append('colorama')

# import playsound (for beeper utility)
try:
    from playsound import playsound
except:
    try:
        os.system('pip install playsound --break-system-packages')
        from playsound import playsound
    except:
        failed_imports.append('playsound')

# import distro (issue #1 https://github.com/wheatbread2056/breadshell/issues/1)
try:
    import distro
except:
    try:
        os.system('pip install playsound --break-system-packages')
        import distro
    except:
        failed_imports.append('distro')

# import getkey - required for autocompletion + command history
try:
    from getkey import getkey, keys
except:
    try:
        os.system('pip install getkey --break-system-packages')
        from getkey import getkey, keys
    except:
        failed_imports.append('getkey')
        LEGACY_PROMPT = True


# makes sure that bash shell is used
os.environ['SHELL'] = '/bin/bash'

# version number and other information --version
version = '1.0-dev5-prev4'
versiontype = 3 # 1 = release, 2 = prerelease, 3 = development, 4 = early development
versiontext = '' # add for stuff like "bugtesting preview" or "private beta", appended to version in parentheses. example: 1.1-pre7c (Private Beta)
devnote = ''

# define colors --customization
if DISABLE_COLORS == True:
    # empty classes so there's no undefined "c.red undefined" errors
    class c:
        red = ''
        yellow = ''
        green = ''
        blue = ''
        magenta = ''
        cyan = ''
        white = ''
        black = ''
        r = ''

    class bc:
        red = ''
        yellow = ''
        green = ''
        blue = ''
        magenta = ''
        cyan = ''
        white = ''
        black = ''
        r = ''

else:
    # foreground colors
    class c:
        red = colorama.Fore.RED
        yellow = colorama.Fore.YELLOW
        green = colorama.Fore.GREEN
        blue = colorama.Fore.BLUE
        magenta = colorama.Fore.MAGENTA
        cyan = colorama.Fore.CYAN
        white = colorama.Fore.WHITE
        black = colorama.Fore.BLACK
        b = '\033[1m' # bold
        i = '\033[3m' # italic
        u = '\033[4m' # underline
        e = '\033[0m' # end
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

# color customization
class cc:
    login = c.blue
    dir = c.green
    text = c.r
    pointer = c.r

if not 'colorama' in failed_imports:
    colorama.init(autoreset=True) # fix weird command output color bug idk

# used for networktest utility
def ping_ip(ip_address):
    try:
        pingOutput = subprocess.check_output(['ping', '-c', '1', ip_address]).decode('utf-8')
        
        timeMatch = re.search(r'time=([\d.]+) ms', pingOutput)
        if timeMatch:
            responseTime = float(timeMatch.group(1))
            return responseTime
        else:
            return None
        
    except subprocess.CalledProcessError:
        # Handle if the ping command fails
        return None
    
user = getpass.getuser()
    
# now time to load settings --settings
try:
    settingsdir = f'/home/{user}/.config/breadshell'
except:
    settingsdir = '/home/user/.config/breadshell'
settingspath = settingsdir+'/settings.ini'
# read the settings and return all key/value pairs
def read_settings():
    global DEFAULT_SETTINGS
    config = {}
    # create the file if it doesn't already exist
    try:
        with open(settingspath, 'a') as file:
            file.close()
    except:
        try:
            os.mkdir(settingsdir)
        except:
            DEFAULT_SETTINGS = True
        try:
            with open(settingspath, 'a') as file:
                file.close()
        except:
            DEFAULT_SETTINGS = True
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'r') as file:
            for line in file:
                # skip empty lines and comment lines
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=',1)
                    # remove quotes
                    value = value.strip('"').strip("'")
                    config[key] = value
            file.close()
        return config

if DEFAULT_SETTINGS == False:
    settings = read_settings()

# overwrite the settings and add new values
def add_settings(key, value):
    settings[key] = value
    # write to the file
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'w') as file:
            for key, value in settings.items():
                file.write(f'{key}={value}\n')
            file.close()

# remove a setting (broken idk why)
def remove_settings(key1):
    # write to the file
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'w') as file:
            for key, value in settings.items():
                if not key1 == key:
                    file.write(f'{key}={value}\n')
            file.close()

# generate default settings
defaultSettings = {
    'loginColor': 'blue',
    'dirColor': 'green',
    'textColor': 'r',
    'pointerColor': 'r',
    'pointerChar': '>',
    'showLogin': 'True',
    'showDir': 'True',
    'showPointer': 'True',
    'showHost': 'True',
    'clearOnBoot': 'True',
    'shortenDir': 'True',
    'dirType': '0',
}
temp1494861 = 0
# checks for settings (kinda sucks but it works)
if DEFAULT_SETTINGS == False:
    for setting in defaultSettings:
        try:
            temp1494861 = settings[setting]
        except:
            add_settings(setting,defaultSettings[setting])
else:
    settings = defaultSettings.copy()

# settings friendly names
friendlySettings = {
    'loginColor': 'Username Color',
    'dirColor': 'Directory Color',
    'textColor': 'Text Color',
    'pointerColor': 'Pointer Color',
    'pointerChar': 'Pointer Character',
    'showLogin': 'Show Current User',
    'showDir': 'Show Current Directory',
    'showPointer': 'Show Pointer',
    'showHost': 'Show Hostname',
    'clearOnBoot': 'Clear On Boot',
    'shortenDir': 'Shorten User Directory',
    'dirType': 'not implemented', # add this later
    'h_version': 'Installed Version',
}

# clear console
if settings['clearOnBoot'] == 'True':
    os.system('clear')

# change colors depending on settings
exec(f"cc.login = c.{settings['loginColor']}")
exec(f"cc.dir = c.{settings['dirColor']}")
exec(f"cc.text = c.{settings['textColor']}")
exec(f"cc.pointer = c.{settings['pointerColor']}")

# check if breadshell is installed --installcheck
try:
    currentdir = os.getcwd()
    scriptdir = os.path.dirname(__file__)

    # if this doesn't work, it will give an error, which is how this works
    os.chdir('/usr/src/breadshell')
    os.chdir(currentdir)
    
    if scriptdir == '/usr/src/breadshell':
        installed = True
        runfrominstall = True

    else:
        print(f'{c.red}you are running breadshell from a file, even though breadshell is installed{c.r}')
        installed = True
        runfrominstall = False

    # change back to the previous directory
    os.chdir(currentdir)

except:
    print(f'{c.red}breadshell is not installed, or an error has occured when loading{c.r}')
    installed = False
    runfrominstall = False

# set version if installed
if runfrominstall == True:
    add_settings('h_version', version)

# basic functions
    
# returns yellow error
def throwerror(msg='An unknown error has occured'):
    print(f'{c.yellow}{msg}{c.r}')

# returns red error and exits to prevent corruption or something
def fatalerror(msg='A fatal error has occured, exiting immediately',force_exit=1):
    print(f'{c.red}{msg}{c.r}')
    if force_exit == 1:
        exit()

# game scripts --games
    
def startg_rpg_test():
    rpgversion = '0.2'
    print('What is your name? (leave blank for PLAYER)')
    name = input()
    if name == '':
        name = 'PLAYER'
    print('What is your gender? (leave blank for random)')
    gender = input()
    if gender == '':
        genders = ['male','female'] # there are only two genders
        gender = genders[random.randint(0,1)]
    stats = {
        'level': 1,
        'xptolvl': 100,
        'xp': 0,
        'maxhp': 100,
        'hp': 'UNDEFINED',
        'gender': gender,
        'regenspd': 1,
        'name': name,
    }
    chunkdata = {}
    data = {
        'x': 16,
        'y': 8,
        'xc': 0,
        'yc': 0,
    }
    # set hp to maxhp
    stats['hp'] = stats['maxhp']
    inventory = {
        'gold': 0,
        'weapon': 'nuclear bomb',
        'armor': 'NONE',
    }

    # world gen
    def genchunk():
        try:
            if chunkdata[f"chunk{data['xc']}_{data['yc']}"] == []:
                for i in range(16):
                    buffer = ''
                    for i in range(32):
                        possibleChars = [' ',' ',' ',' ',' ','C','.']
                        buffer = buffer + possibleChars[random.randint(0,len(possibleChars)-1)]
                    chunkdata[f"chunk{data['xc']}_{data['yc']}"].append(buffer)
        except KeyError:
            chunkdata[f"chunk{data['xc']}_{data['yc']}"] = []
            for i in range(16):
                buffer = ''
                for i in range(32):
                    possibleChars = [' ',' ',' ',' ',' ','C','.']
                    buffer = buffer + possibleChars[random.randint(0,len(possibleChars)-1)]
                chunkdata[f"chunk{data['xc']}_{data['yc']}"].append(buffer)
    genchunk()

    def regenchunk():
        del chunkdata[f"chunk{data['xc']}_{data['yc']}"]
        genchunk()

    def main(stdscr):
        tips = ['press E for inventory','press - to exit','press ENTER to attack','press SHIFT to use']
        current_tip = tips[random.randint(0,len(tips)-1)]
        tip_delay = 150 # 150 frames tip delay (5s)

        DEBUG_MODE = False

        curses.curs_set(0)  # Hide the cursor

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)

        stdscr.nodelay(1)

        while True:
            prevxy = [data['x'],data['y']]
            curchunk = chunkdata[f"chunk{data['xc']}_{data['yc']}"]
            origchunk = chunkdata["chunk0_0"]

            max_y, max_x = stdscr.getmaxyx()

            # user input

            key = stdscr.getch()

            # arrow keys
            if key == curses.KEY_LEFT or key == ord('a'):
                data['x']-=1
            if key == curses.KEY_RIGHT or key == ord('d'):
                data['x']+=1
            if key == curses.KEY_UP or key == ord('w'):
                data['y']+=1
            if key == curses.KEY_DOWN or key == ord('s'):
                data['y']-=1

            # other keys
            if key == ord('p'): # toggle debug
                if DEBUG_MODE == False:
                    DEBUG_MODE = True
                else:
                    DEBUG_MODE = False
            if key == ord('-'): # exit
                break

            # debug mode ONLY
            if DEBUG_MODE == True:
                if key == ord('q'): # regen chunk
                    regenchunk()
                if key == ord('z'): # go to chunk 0,0
                    data['xc'],data['yc'] = 0,0
                if key == ord('x'): # increment gold
                    inventory['gold']+=1
                if key == ord('c'): # decrement gold
                    inventory['gold']-=1

            # player collision
            '''
            if curchunk[data['y']][data['x']] == 'C': # coin collision
                inventory['gold']+=1
                tempVariable1 = list(curchunk[data['y']])  
                tempVariable1[data['x']] = ' '
                ''.join(tempVariable1)
                chunkdata[f"chunk{data['xc']}_{data['yc']}"][data['y']] = ''
                chunkdata[f"chunk{data['xc']}_{data['yc']}"][data['y']] = tempVariable1
            '''

            # for RIGHT border
            if data['x'] >= 32:
                data['x']-=32
                data['xc']+=1
                genchunk()
            # for LEFT border
            if data['x'] < 0:
                data['x']+=32
                data['xc']-=1
                genchunk()
            # for TOP border
            if data['y'] >= 16:
                data['y']-=16
                data['yc']+=1
                genchunk()
            # for BOTTOM border
            if data['y'] < 0:
                data['y']+=16
                data['yc']-=1
                genchunk()

            stdscr.clear()
            str1 = f"❤️  {stats['hp']}/{stats['maxhp']}"
            str2 = f"💰 ${inventory['gold']}"
            str3 = f"LVL {stats['level']} ({stats['xp']}/{stats['xptolvl']} xp)"
            str1a = f"x: {data['x']+data['xc']*32}, y: {data['y']+data['yc']*16}"
            str1b = current_tip
            str1c = f"selected weapon: {inventory['weapon']}"
            # activated with debug mode
            dstr1 = f"[CHUNK] x: {data['xc']}, y: {data['yc']}"
            dstr2 = f"[POS IN CHUNK] x: {data['x']}, y: {data['y']}"
            dstr3 = "(q) regenerate chunk"
            dstr4 = "(z) return to chunk 0,0"
            dstr5 = "(x) increment gold"
            dstr6 = "(c) decrement gold"

            # add strings to the screen

            try:
                # world rendering

                stdscr.addstr(5, int(max_x/2) - int(len(origchunk[0])/2)-1, '0'*len(origchunk[0])+'0'*2)
                for i in range(len(curchunk)):
                    stdscr.addstr(i + 6, int(max_x/2) - int(len(curchunk[i])/2)-1, '0'+curchunk[i]+'0')
                stdscr.addstr(22, int(max_x/2) - int(len(origchunk[0])/2)-1, '0'*len(origchunk[0])+'0'*2)

                # player rendering

                stdscr.addstr(21-data['y'],int(max_x/2) - int(len(origchunk[i])/2)+data['x'],'&', curses.color_pair(1))

                # bottom gui

                stdscr.addstr(max_y - 1, 0, str1)
                stdscr.addstr(max_y - 1, max_x - 3 - len(str2), str2)
                stdscr.addstr(max_y - 1, int(max_x/2) - int(len(str3)/2), str3)

                # top gui

                stdscr.addstr(0, 0, str1a)
                stdscr.addstr(0, int(max_x/2) - int(len(str1b)/2), str1b)

                # debug mode gui

                if DEBUG_MODE == True:
                    for i in range(6):
                        exec(f'stdscr.addstr(i+1,0,dstr{i+1})')
            except:
                throwerror('A larger terminal is required to play rpg_test, please enlarge it and come back')
                break

            stdscr.refresh()
            tip_delay-=1
            if tip_delay <= 0:
                current_tip = tips[random.randint(0,len(tips)-1)]
                tip_delay = 150
            time.sleep(1/30) # 30 fps

    curses.wrapper(main)

# utility scripts --utilities

def startu_colortester():
    # random colors+chars for 256 characters
    chars = '`1234567890-=~!@#$%^&*()_+qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    str = ''
    for i in range(4096):
        a = random.randint(0,len(chars)-1)
        char = chars[a]

        # define colors by lists instead of classes
        foregroundColors = [c.red,c.yellow,c.green,c.blue,c.cyan,c.magenta,c.white,c.black,c.r]
        backgroundColors = [bc.red,bc.yellow,bc.green,bc.blue,bc.cyan,bc.magenta,bc.white,bc.black,bc.r]
        # get random item in the lists
        b = foregroundColors[random.randint(0,len(foregroundColors)-1)]
        # used _c here since c is already used for the main colors class
        _c = backgroundColors[random.randint(0,len(foregroundColors)-1)]

        # add it to the main string
        str=str+b+_c+char

    # +c.r+bc.r is needed to reset the colors
    print(str+c.r+bc.r)

def startu_calculator():
    while True:
        # command (meant to be an expression)
        cmd = input(f'{c.cyan}calculator{c.r} {settings["pointerChar"]} ')
        if cmd == 'exit':
            utillauncher()
        # funny easter egg
        elif cmd == '9+10':
            print(21)
        # as of 0.5-pre1d the user can no longer execute any command in the calculator
        elif cmd.startswith('exec') or cmd.startswith('os') or cmd.startswith('subprocess') or cmd.startswith('start') or cmd.startswith('main') or cmd.startswith('utillauncher') or cmd.startswith('games'):
            throwerror()
        elif cmd == '':
            pass
        else:
            try:
                # print() is needed because simply executing 1+1 does not display 2
                exec(f'print({cmd})')
            except:
                throwerror()

def startu_python():
    while True:
        # command
        cmd = input(f'{c.cyan}python{c.r} {settings["pointerChar"]} ')

        if cmd == 'exit':
            utillauncher()
        else:
            try:
                exec(cmd)
            except:
                throwerror()

def startu_networktest():
    print(f'network tester v0.3')
    disabled = 0
    if ping_ip('8.8.8.8') == None:
        throwerror('Run this utility as the superuser and try again.')
        disabled = 1
    if disabled == 0:
        print('How many pings per IP?')
        pcount = int(input('> '))
        print(f'testing google ping ({pcount}+{pcount}x):')
        initialms = 0
        for i in range(pcount):
            rt = ping_ip('8.8.8.8')
            initialms+=int(rt)
        print(f'{round(initialms/pcount,2)}ms on 8.8.8.8')

        initialms = 0
        for i in range(pcount):
            rt = ping_ip('8.8.4.4')
            initialms+=int(rt)
        print(f'{round(initialms/pcount,2)}ms on 8.8.4.4')

        print(f'testing cloudflare ping ({pcount}x):')

        initialms = 0
        for i in range(pcount):
            rt = ping_ip('1.1.1.1')
            initialms+=int(rt)
        print(f'{round(initialms/pcount,2)}ms on 1.1.1.1')

def startu_assistant():
    '''
    POSSIBLE MOODS
    neutral = white message, 35ms char delay
    happy = green (lime) message, 30ms char delay
    sad = blue message, 60ms char delay
    empathy = light blue (cyan) message, 40ms char delay
    angry = red message, 25ms char delay
    uncomfortable = yellow message, 45ms char delay
    love = pink (magenta) message, 40ms char delay
    '''
    errors = [
        'what do you mean?',
        "i don't know what you mean by that...",
        "what the hell do you mean?",
        'stop talking nonsense...',
        "i'm sorry, can you say that again?",
        "i couldn't hear you...",
        "huh?",
        "what?"
    ]
    blankerrors = [
        "don't be shy, say something...",
        "are you going to say something?",
        "please talk to me...",
        "hey... wake up...",
        "WAKE UP!!!",
    ]
    responses = {
        "im good": ['glad to hear that!', 'happy'],
        "im doing good": ['glad to hear that!', 'happy'],
        "good": ['good!', 'happy'],
        "im not doing good": ["is everything okay?", 'empathy'],
        "im doing bad": ['is everything okay?', 'empathy'],
        "im not good": ['is everything okay?', 'empathy'],
        "bad": ['is everything good?', 'empathy'],
        "im hungry": ["why?"],
        "kill yourself": ["why?"],
        "because": ["because what?"],
        "because you know": ["just tell me already", 'angry'],
        "i will never tell you": ["kill yourself!!!", 'angry'],
        "you suck": ["oh... i'm sorry if i didn't make you happy...", 'sad']
    }
    def ms(a): # milliseconds
        return a/1000
    def formatinput(str):
        return str.replace('"','').replace("'",'').replace('!','').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace(',','').replace('.','')
    def botmessage(str,mood='neutral'):
        if mood == 'neutral':
            m = ''
            b = 35
        elif mood == 'happy':
            m = c.green
            b = 30
        elif mood == 'sad':
            m = c.blue
            b = 60
        elif mood == 'empathy':
            m = c.cyan
            b = 40
        elif mood == 'angry':
            m = c.red
            b = 25
        elif mood == 'uncomfortable':
            m = c.yellow
            b = 45
        elif mood == 'love':
            m = c.magenta
            b = 40
        else:
            m = ''
        writtenchars = ''
        for i in range(len(str)):
            writtenchars+=str[i]
            print(m+writtenchars+c.r,end='\r')
            time.sleep(ms(b)) # 35 ms delay per char, realistic talking speed
        print() # new line
        time.sleep(ms(500))
    botmessage("hi! i'm iris, your personal assistant.")
    botmessage('how are you?')
    while True:
        userinput = input(f'{c.cyan}assistant{c.r} {settings["pointerChar"]} ')
        if userinput == 'exit':
            utillauncher()
        elif userinput == '':
            botmessage(blankerrors[random.randint(0,len(blankerrors)-1)])
        else:
            try:
                botmessage(responses[formatinput(userinput.lower())][0],responses[formatinput(userinput.lower())][1])
            except KeyError:
                botmessage(errors[random.randint(0,len(errors)-1)])
            except IndexError:
                botmessage(responses[formatinput(userinput.lower())][0])


# game launcher
def games():
    globalversion = '0.3.1'
    # list amount of games here
    games = ['rpg_test']
    versions = ['0.2']

    print(f'breadshell game launcher version {globalversion}')
    print(f'please select the game you would like to start ({len(games)} found):')

    i = 1
    for game in games:
        print(f'{c.yellow}{i} - {game} {c.cyan}{versions[i-1]}{c.r}')
        i += 1
    
    print(f'{c.yellow}exit - exit')

    # fixes crashing bug (major) - added in 1.0-dev1a
    def selection(games):
        game = input(f'{c.cyan}bgames{c.r} {settings["pointerChar"]} ')

        if game == 'exit':
            main()
        try:
            if games[int(game)-1] in games:
                print(f'Loading {games[int(game)-1]}...')
                exec(f'startg_{games[int(game)-1]}()')
        except:
            throwerror('Invalid game.')
            selection(games)
    selection(games)

# utility launcher (totally not just modified game launcher)

def utillauncher():
    globalversion = '0.3.2'
    # list amount of games here
    #------------------- NOTE: add 'networktest' utility when finished -------------
    utilities = ['colortester','calculator','python','assistant','networktest']
    versions = ['1.1','1.1','1.0','0.1.1','0.3']

    print(f'breadshell utilities {globalversion}')
    print(f'please select the utility you would like to start ({len(utilities)} found):')

    i = 1
    for utility in utilities:
        print(f'{c.yellow}{i} - {utility} {c.cyan}{versions[i-1]}{c.r}')
        i += 1

    print(f'{c.yellow}exit - exit')

    # fixes crashing bug (major) - added in 1.0-dev1a, fixed in 1.0-dev1b (another minor bug appeared)
    def selection(utilities):
        try:
            utility = input(f'{c.cyan}butils{c.r} {settings["pointerChar"]} ')
        except:
            pass
        try:
            if utility == 'exit':
                main()
            else:
                try:
                    if utilities[int(utility)-1] in utilities:
                        print(f'Starting {utilities[int(utility)-1]}...')
                        exec(f'startu_{utilities[int(utility)-1]}()')
                except:
                    if utility == None or utility == '' or utility.lower == 'exit':
                        pass
                    else:
                        throwerror('Invalid utility.')
        except:
            pass
    selection(utilities)

badStart = False

def reportBadStart(a): # legacy fix introduced around 0.4 to prevent wsl from instantly crashing
    global badStart
    if not badStart:
        throwerror(f'an error occurred: {a}')
        throwerror('username will default to \'user\' to fix compatibility issues')
        badStart = True

if WSL == 1:
    throwerror('Note: Bold and italic text effects are not supported when using the Windows Terminal. Use real Linux or an X Server when possible.')

if DEFAULT_SETTINGS == True:
    throwerror(f'{settingspath.replace(f"/home/{user}", "~")} couldn\'t be generated, default settings will be used. Settings will not save.')

# start of program, shown when opening the file
if not versiontext == '' and not versiontext == None:
    vt = f' ({c.cyan}{versiontext}{c.r})'
else:
    vt = ''

cmdhistory = []
historycur = -2

print(f'version {c.cyan}{version}{c.r}{vt}, latest login {c.magenta}{datetime.datetime.now()}{c.r}')
print(f'type {c.yellow}bhelp{c.r} for a list of custom commands.')
# main loop
def main():
    global cmdhistory
    while True:
        # generate the line

        tempcmd = ""
        if settings['showLogin'] == 'True':
            try:
                tempcmd += f"{cc.login}{user}@{socket.gethostname()}{c.r} "
                if not settings['showHost'] == 'True':
                    tempcmd = tempcmd.split('@')[0]+f'{c.r} '
            except Exception as e:
                reportBadStart(e)
                tempcmd += f"{cc.login}user@{socket.gethostname()}{c.r} "
                if not settings['showHost'] == 'True':
                    tempcmd = tempcmd.split('@')[0]+f'{c.r} '

        if settings['showDir'] == 'True':
            if settings['shortenDir'] == 'True':
                tempcmd += f"{cc.dir}{os.getcwd()}{c.r} ".replace(f'/home/{user}', '~')
            else:
                tempcmd += f"{cc.dir}{os.getcwd()}{c.r} "

        if settings['showPointer'] == 'True':
            tempcmd += f"{cc.pointer}{settings['pointerChar']} {c.r}"

        tempcmd += cc.text

        # main input (user@hostname path/to/directory > command typed in) --main
        if LEGACY_PROMPT == True: # pre 1.0, only used as fallback
            try:
                cmd = input(tempcmd)
            except Exception as e:
                fatalerror('An error has occured: '+str(e))
        else:
            buffer = ''
            print(tempcmd, end='')
            while True:
                key = getkey()
                if key == keys.ENTER:
                    break
                elif key == keys.UP: # previous command in the history
                    try:
                        # if historycur = -1, that's the end of the history
                        prevbuffer = buffer
                        if historycur == -2:
                            historycur = len(cmdhistory)
                        if historycur > 0:
                            historycur -= 1
                            buffer = cmdhistory[historycur]
                            print('\b \b' * len(prevbuffer), end='')
                            print(buffer,end='')
                    except:
                        pass
                elif key == keys.DOWN: # next command in the history
                    try:
                        prevbuffer = buffer
                        if historycur == -2:
                            historycur = len(cmdhistory)-1
                        if historycur < len(cmdhistory)-1:
                            historycur += 1
                            buffer = cmdhistory[historycur]
                            print('\b \b' * len(prevbuffer), end='')
                            print(buffer,end='')
                    except:
                        pass
                elif key == keys.BACKSPACE: # handle backspace
                    try:
                        if len(buffer) > 0:
                            buffer = buffer[:len(buffer)-1]
                            print('\b \b', end='')
                    except:
                        pass
                else:
                    buffer += str(key)
                    print(key, end='')
            print()
            cmd = buffer
            try: # make sure that empty and duplicate commands don't get added to the command history
                if not cmd.replace(' ','') == '' and not cmd == cmdhistory[len(cmdhistory)-1]:
                    cmdhistory.append(cmd)
            except:
                if not cmd.replace(' ','') == '':
                    cmdhistory.append(cmd)

            historycur = -2
        
        print(c.r + c.e,end='') # attempt to stop command output from using the set text color
        cmdargs = cmd.split(' ') # get command arguments

        # for special commands
            
        # change directory (cd)
        if cmdargs[0] == ('cd'):
            try:
                os.chdir(cmd.split(' ')[1])
            except:
                throwerror('Invalid directory, or a directory was not specified')

        # breadhelp (bhelp)
        elif cmdargs[0] == ('bhelp'):
            print(f'''
    breadshell version {c.cyan}{version}{c.r}

    --- CUSTOM COMMANDS ---

    {c.yellow}bhelp{c.r} - open this page
    {c.yellow}inst{c.r} {c.cyan}<package-name>{c.r} - easy way to install packages
    {c.yellow}uninst{c.r} {c.cyan}<package-name>{c.r} - easy way to uninstall packages
    {c.yellow}bpkgs{c.r} {c.cyan}<query>{c.r} - search packages
    {c.yellow}bgames{c.r} - start game launcher
    {c.yellow}butils{c.r} - start utility launcher
    {c.yellow}version{c.r} - displays version information
    {c.yellow}settings{c.r} - change your breadshell settings
    {c.yellow}scedit{c.r} - edit, view, and create breadshell shortcuts
    {c.red}exit{c.r} - exits breadshell
    ''')
            
        # breadfetch (bfetch)
        elif cmdargs[0] == ('bfetch'):
            print('making this later, for now just have neofetch')
            subprocess.run(['bash','-c','neofetch'])

        # breadinstall (inst)
        elif cmdargs[0] == ('inst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt install {cmd.split(" ")[1]} -y'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breaduninstall (uninst)
        elif cmdargs[0] == ('uninst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt remove {cmd.split(" ")[1]} -y'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breadpackages (bpkgs)
        elif cmdargs[0] == ('bpkgs'):
            try:
                subprocess.run(['bash','-c',f'apt search {cmd.split(" ")[1]}'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # exit... self explanatory
        elif cmdargs[0] == ('exit'):
            exit()

        # "developer commands"
            
        # throw a generic error
        elif cmdargs[0] == ('dev-generic-error'):
            throwerror()
            
        # throw a FATAL generic error, which is red...
        elif cmdargs[0] == ('dev-generic-fatalerror'):
            fatalerror()

        # set background color to a random color
        elif cmdargs[0] == ('dev-randombg'):
            quickColors = [bc.red,bc.yellow,bc.green,bc.blue,bc.magenta]
            print(quickColors[random.randint(0,len(quickColors)-1)])
            os.system('clear')
        
        # reset the background color
        elif cmdargs[0] == ('dev-resetbg'):
            print(bc.r)
            os.system('clear')
        
        # colortest 1024 times... for some reason
        elif cmdargs[0] == ('dev-explosionofcolors'):
            for i in range(1024):
                startu_colortester()

        # actually useful, directly execute code from breadshell.py
        # able to execute multiple commands at a time without semicolon seperators
        elif cmdargs[0] == ('dev-exec'):
            try:
                exec(' '.join(cmdargs[1:]))
            except Exception as e:
                throwerror('(Python) '+str(e))

        elif cmdargs[0] == ('dev-text-effects-demo'):
            print(f'''
{c.b}this text should be bold{c.e} and this text is normal
{c.i}this should be italic{c.e}
{c.u}this should be underlined{c.e}
''')

        elif cmdargs[0] == ('dev-clear-history'):
            try:
                cmdhistory = []
            except Exception as e:
                throwerror(f'Failed to clear command history ({e})')

        # launch games
        elif cmdargs[0] == ('bgames'):
            games()

        # launch utilities
        elif cmdargs[0] == ('butils'):
            utillauncher()

        # display version info
        elif cmdargs[0] == ('version'):
            print(f'breadshell version {c.cyan}{version}{c.r}{vt}')                

            # display version type
            if versiontype == 1:
                print(f'this is a {c.green}release{c.r} of breadshell')
            elif versiontype == 2:
                print(f'this is a {c.yellow}prerelease{c.r} of breadshell. \nsome bugs may occur')
            elif versiontype == 3:
                print(f'this is a {c.magenta}development{c.r} version of breadshell. \nsome bugs or unfinished features may occur')
            elif versiontype == 4:
                print(f'this is an {c.cyan}early development{c.r} version of breadshell. \nmany bugs or unfinished features may occur')
            else:
                print(f'this is an {c.red}unknown {c.r}or {c.red}unofficial{c.r} version of breadshell')

            # display installation status
            if installed == True:
                if DEFAULT_SETTINGS == False:
                    print(f'breadshell is {c.green}installed{c.r} (version {c.cyan}{settings["h_version"]}{c.r})')
                else:
                    print(f'breadshell is {c.green}installed{c.r} (version {c.red}unknown{c.r})')
            else:
                print(f'breadshell is {c.red}not installed{c.r}')

            # running from file or not
            if runfrominstall == True:
                print(f'running from {c.green}install{c.r}')
            else:
                print(f'running from {c.red}file{c.r}')

            print(f'source code on {c.blue}github.com/wheatbread2056/breadshell{c.r}')

            if not devnote == """""" and not devnote == '' and not devnote == None:
                print('Note from the developer:')
                print(devnote)

        # edit settings --editsettings
        elif cmdargs[0] == ('settings'):
            if settings == {}:
                throwerror(f'No settings were found, or there was an error reading settings.ini ({settingspath})')
                main()
            else:
                tm0 = 0
                reflist = []
                for key, value in settings.items():
                    if not key.startswith('h_') and not key.startswith('s_'):
                        if key in friendlySettings:
                            if settings[key] == 'False':
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.red}{value}{c.r}")
                            elif settings[key] == 'True':
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.green}{value}{c.r}")
                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.cyan}{value}{c.r}")

                        else:
                            print(f"({c.yellow}{tm0}{c.r}) {c.yellow}{key}{c.r} - {c.cyan}{value}{c.r}") # if there is no friendly name for the setting
                        reflist.append(key)
                        tm0 += 1

            print('Type the number of the setting you would like to change, or list to list settings, or exit to leave')

            while True:
                setting = input(f'{c.cyan}settings{c.r} {settings["pointerChar"]} ')
                completed = False

                # legacy (pre-1.0) settings, this means typing the non-friendly name of the setting and changing it that way still works
                if setting in settings and not setting.startswith('h_') and not setting.startswith('s_'):
                    throwerror('Note: Using non-friendly settings names is obsolete and may be removed in 1.1.')
                    print('Enter a new value:')
                    newValue = input(f'{c.green}{setting}{c.r} {settings["pointerChar"]} ')
                    if newValue.lower() == 'true':
                        try:
                            add_settings(setting,True)
                            print(f'Successfully updated the setting {c.green}{setting}{c.r}.')
                        except:
                            throwerror(f'Failed to update the setting {c.green}{setting}{c.r}')

                    elif newValue.lower() == 'false':
                        try:
                            add_settings(setting,False)
                            print(f'Successfully updated the setting {c.green}{setting}{c.r}.')
                        except:
                            throwerror(f'Failed to update the setting {c.green}{setting}{c.r}')

                    elif newValue.lower() == 'exit':
                        pass

                    else:
                        try:
                            add_settings(setting,newValue)
                            print(f'Successfully updated the setting {c.green}{setting}{c.r}.')
                        except:
                            throwerror(f'Failed to update the setting {c.green}{setting}{c.r}')
                    completed = True

                # new (1.0+) settings, number-based selection
                try:
                    if int(setting) < len(reflist):
                        print('Enter a new value:')
                        newValue = input(f'{c.green}{reflist[int(setting)]}{c.r} {settings["pointerChar"]} ')
                        if newValue.lower() == 'true':
                            try:
                                add_settings(reflist[int(setting)],True)
                                print(f'Successfully updated the setting {c.green}{reflist[int(setting)]}{c.r}.')
                            except:
                                throwerror(f'Failed to update the setting {c.green}{reflist[int(setting)]}{c.r}')

                        elif newValue.lower() == 'false':
                            try:
                                add_settings(reflist[int(setting)],False)
                                print(f'Successfully updated the setting {c.green}{reflist[int(setting)]}{c.r}.')
                            except:
                                throwerror(f'Failed to update the setting {c.green}{reflist[int(setting)]}{c.r}')

                        elif newValue.lower() == 'exit':
                            pass

                        else:
                            try:
                                add_settings(reflist[int(setting)],newValue)
                                print(f'Successfully updated the setting {c.green}{reflist[int(setting)]}{c.r}.')
                            except:
                                throwerror(f'Failed to update the setting {c.green}{reflist[int(setting)]}{c.r}')

                        completed = True
                except:
                    pass

                if setting.lower() == 'list':
                    tm0 = 0
                    reflist = []
                    for key, value in settings.items():
                        if not key.startswith('h_') and not key.startswith('s_'):
                            if key in friendlySettings:
                                if settings[key] == 'False':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.red}{value}{c.r}")
                                elif settings[key] == 'True':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.green}{value}{c.r}")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.cyan}{value}{c.r}")

                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {c.yellow}{key}{c.r} - {c.cyan}{value}{c.r}") # if there is no friendly name for the setting
                            reflist.append(key)
                            tm0 += 1

                elif setting.lower() == 'dev-list':
                    tm0 = 0
                    reflist = []
                    for key, value in settings.items():
                        if not key.startswith('h_') and not key.startswith('s_'):
                            if key in friendlySettings:
                                if settings[key] == 'False':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.red}{value}{c.r} .b")
                                elif settings[key] == 'True':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.green}{value}{c.r} .b")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.cyan}{value}{c.r} .s")
                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {key} - {c.cyan}{value}{c.r} .s")
                            tm0 += 1
                        else:
                            if key in friendlySettings:
                                if settings[key] == 'False':
                                    print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.red}{value}{c.r} {c.u}HIDDEN{c.e} .b")
                                elif settings[key] == 'True':
                                    print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.green}{value}{c.r} {c.u}HIDDEN{c.e} .b")
                                else:
                                    print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.cyan}{value}{c.r} {c.u}HIDDEN{c.e} .s")
                            else:
                                print(f"({c.red}X{c.r}) {c.red}{key}{c.r} - {c.cyan}{value}{c.r} {c.u}HIDDEN{c.e} .s")

                elif setting.lower() == 'exit':
                    break

                elif completed == True: # variable added to stop throwing errors when nothing went wrong
                    pass

                else:
                    throwerror('Invalid setting')

        # edit shortcuts (totally not just modified settings)
        elif cmdargs[0] == ('scedit'):
            if settings == {}:
                throwerror(f'No shortcuts were found, or there was an error reading settings.ini ({settingspath})')
                main()
            else:
                for key, value in settings.items():
                    if key.startswith('s_'):
                        print(f"{key[2:]} - {c.cyan}{value}{c.r}")

            print('which shortcut would you like to change? alternatively, you can type exit, list, remove, or add.')
            
            while True:
                setting = input(f'{c.cyan}scedit{c.r} {settings["pointerChar"]} ')
                
                if 's_'+setting in settings:
                    print('Enter a new command for this shortcut:')
                    newValue = input(f'{c.cyan}{setting}{c.r} {settings["pointerChar"]} ')
                    add_settings('s_'+setting,newValue)

                elif setting == 'exit':
                    break

                elif setting == 'add':
                    print('what would you like to type to activate the shortcut?')
                    newshortcutname = input(f'{c.cyan}new shortcut{c.r} {settings["pointerChar"]} ')
                    print('what command would you like to run for this shortcut?')
                    newshortcutcmd = input(f'{c.cyan}{newshortcutname}{c.r} {settings["pointerChar"]} ')
                    add_settings('s_'+newshortcutname,newshortcutcmd)

                elif setting == 'remove':
                    print('which shortcut would you like to remove?')
                    delshortcut = input(f'{c.cyan}scedit{c.r} {settings["pointerChar"]} ')
                    if 's_'+delshortcut in settings:
                        remove_settings('s_'+delshortcut)
                    else:
                        throwerror('Invalid shortcut.')

                elif setting == 'list':
                    for key, value in settings.items():
                        if key.startswith('s_'):
                            print(f"{key[2:]} - {c.cyan}{value}{c.r}")

                else:
                    throwerror('Invalid shortcut.')

        elif cmdargs[0] == ('kill yourself'):
            print('Ok, closing in 5 seconds...')
            time.sleep(5)
            exit()

        # shortcuts (added in 0.5-pre4h)
        elif 's_'+cmd in settings:
            subprocess.run(['bash','-c',settings['s_'+cmd]]) 

        # if none of the above commands were selected, it will run this (run any command inside the input)
            
        else:
            try:
                subprocess.run(['bash','-c',cmd])
            except Exception as e:
                fatalerror('An error has occured: '+e)
            
# run main function (moved from while loop to function in 0.3 so the user can be returned back to the shell in case anything goes wrong)
main()