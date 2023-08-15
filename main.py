import time
from subprocess import call
import tkinter as tk
import math

IS_RUNNING = False
CHOSEN_SPELL = None

SPELLS = {
    'Invisible': 200,
    'Magic Shield': 180,
    'Conjure Wand of Darkness': 900,
}

def set_running(val: bool):
    global IS_RUNNING
    IS_RUNNING = val

def set_spell(spell: str):
    global CHOSEN_SPELL
    CHOSEN_SPELL = spell

### You may change your config here
key = 'Shift+R'
exitKey = 'Esc'
beep = True

# Quick spell for hotkey
QUICK_SPELL = 'Invisible'

# Will be used to warn player before spells runs out
SAFE_TIMER = 20

def play():
    if beep:
        call(['beep', '-f', '5000', '-l', '50', '-r', '2'])
    else:
        call(['aplay', 'sound.wav'])

def calc_magic_shield(level: int, magic_level: int):
    calculation = 300 + (7.6 * level) + (7 * magic_level)
    return math.ceil(calculation)

def main():
    global IS_RUNNING
    global CHOSEN_SPELL

    window = tk.Tk()
    window.title("Timer")
    window.geometry("800x600")

    menu = tk.Menu(window)
    m1 = tk.Menu(menu, tearoff=0)
    m1.add_command(label='Reset', command=lambda: on_reset_press(), accelerator=exitKey)
    m1.add_command(label='Quick Spell', command=lambda: on_press(QUICK_SPELL), accelerator=key)
    menu.add_cascade(label='Options', menu=m1)
    window.config(menu=menu)

    window.bind('<Escape>', lambda e: on_reset_press())
    window.bind('<Shift-R>', lambda e: on_press(QUICK_SPELL))

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
        button.pack(pady=10, padx=10)

    def on_press(spell: str):
        disable_buttons()

        set_running(True)
        set_spell(spell)

        seconds = SPELLS[CHOSEN_SPELL]
        countdown(seconds - SAFE_TIMER)
        
        if IS_RUNNING:
            TIME.set("00:00")
            play()

        on_stop_press()

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

    magic_shield_label = tk.Label(window, text="Magic Shield Capacity: ", font=("Arial Bold", 20), fg="black")
    magic_shield_label.pack(pady=10)

    level_label = tk.Label(window, text="Level: ", fg="black")
    level_label.pack(pady=10)
    
    level_input = tk.Entry(window, width=10)
    level_input.pack(pady=10)

    magic_level_label = tk.Label(window, text="Magic Level: ", fg="black")
    magic_level_label.pack(pady=10)
    
    magic_level_input = tk.Entry(window, width=10)
    magic_level_input.pack(pady=10)

    def on_calc_press():
        level = int(level_input.get())
        magic_level = int(magic_level_input.get())
        magic_shield_label.configure(text="Magic Shield Capacity: " + str(calc_magic_shield(level, magic_level)))

    calc_button = tk.Button(window, text="Calculate", command=lambda : on_calc_press())
    calc_button.pack(pady=10)

    for spell in SPELLS:
        create_spell_button(window, spell)

    stop_button = tk.Button(window, text="Stop", command=lambda : on_stop_press())
    stop_button.pack(pady=10)

    reset_button = tk.Button(window, text="Reset", command=lambda : on_reset_press())
    reset_button.pack(pady=10)
    
    window.mainloop()
    
if __name__ == '__main__':
    main()