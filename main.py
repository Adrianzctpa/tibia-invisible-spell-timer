from pynput import keyboard as kb
import time
from subprocess import call
import tkinter as tk

IS_RUNNING = False
CHOSEN_SPELL = None

SPELLS = {
    'Invisible': 200,
    'Magic Shield': 180,
    'Conjure Wand of Darkness': 900,
    'Test': 30
}

def set_running(val: bool):
    global IS_RUNNING
    IS_RUNNING = val

def set_spell(spell: str):
    global CHOSEN_SPELL
    CHOSEN_SPELL = spell

# You may change your config here
key = '<shift>+r'
exitKey = '<ctrl>+e'
beep = True

# Will be used to warn player before spells runs out
SAFE_TIMER = 20

def play():
    if beep:
        call(['beep', '-f', '5000', '-l', '50', '-r', '2'])
    else:
        call(['aplay', 'sound.wav'])

def main():
    global IS_RUNNING
    global CHOSEN_SPELL

    window = tk.Tk()
    window.title("Timer")
    window.geometry("800x600")
    window.configure(background='lightgray')

    def disable_buttons():
        for child in window.winfo_children():
            if isinstance(child, tk.Button) and child['text'] != 'Stop' and child['text'] != 'Reset':
                child.configure(state='disabled')

    def enable_buttons():
        for child in window.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(state='normal')

    def create_spell_button(window, spell: str):
        button = tk.Button(window, text=spell, command=lambda: on_press(spell))
        button.pack(pady=10)

    def on_press(spell: str):
        disable_buttons()

        set_running(True)
        set_spell(spell)

        seconds = SPELLS[CHOSEN_SPELL]
        countdown(seconds - SAFE_TIMER)
        
        if IS_RUNNING:
            TIME.set("00:00")
            play()

        enable_buttons()

    def on_stop_press():
        set_running(False)
        set_spell(None)

        enable_buttons()

    def on_reset_press():
        TIME.set("00:00")
        on_stop_press()

    def countdown(seconds: int): 
        while seconds:
            if not IS_RUNNING:
                break

            mins, secs = divmod(seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            TIME.set(timeformat)
            window.update()
            time.sleep(1)
            seconds -= 1
    
    TIME = tk.StringVar()
    TIME.set("00:00")

    timer_label = tk.Label(window, textvariable=TIME, font=("Arial Bold", 50), fg="black")
    timer_label.pack(pady=10)

    for spell in SPELLS:
        create_spell_button(window, spell)

    stop_button = tk.Button(window, text="Stop", command=lambda : on_stop_press())
    stop_button.pack(pady=10)

    reset_button = tk.Button(window, text="Reset", command=lambda : on_reset_press())
    reset_button.pack(pady=10)

    window.mainloop()
        
if __name__ == '__main__':
    main()