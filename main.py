from pynput import keyboard as kb
import time
from subprocess import call

# You may change your config here
key = '<shift>+r'
exitKey = '<ctrl>+e'
seconds = 180

def main():
    print('Press ' + key + ' to run timer again and ' + exitKey + ' to exit.')

    def on_activate():
        print('Running...')
        time.sleep(seconds)
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