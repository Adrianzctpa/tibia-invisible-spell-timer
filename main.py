from pynput import keyboard as kb
import time
from subprocess import call

# You may change your config here
key = '<shift>+r'
exitKey = '<ctrl>+e'
seconds = 180

def countdown(seconds): 
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1

def main():
    print('Press ' + key + ' to run timer and ' + exitKey + ' to exit.')

    def on_activate():
        countdown(seconds)
        call(['aplay', 'sound.wav'])
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