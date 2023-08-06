from pynput import keyboard as kb
import time
from subprocess import call
import os

# You may change your config here
key = '<shift>+r'
exitKey = '<ctrl>+e'
seconds = 180
beep = True

def countdown(seconds): 
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1

def play():
    if beep:
        call(['beep', '-f', '5000', '-l', '50', '-r', '2'])
    else:
        call(['aplay', 'sound.wav'])

def main():
    os.system('clear')
    print('Press ' + key + ' to run timer and ' + exitKey + ' to exit.')

    def on_activate():
        countdown(seconds)
        play()
        main()
    
    def on_activate_close():
        listener.stop()
        exit()

    with kb.GlobalHotKeys({
            key: on_activate,
            exitKey: on_activate_close}) as listener:
        listener.join()
        
if __name__ == '__main__':
    main()