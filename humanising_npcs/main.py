# make a GUI to take input for the state machine and then display image produced of the machine
# it should take the input as a number between 1 and -1 as a slider

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from random import uniform as randomuniform

from traits import Traits


# add a few examples on how a character with each combinations of traits would behave
# Generate examples for all combinations of traits
def generate_examples(combinations):
    for i in range(1, len(combinations) + 1):
        examples = []
        if "Lazy" in combinations:
            examples.append("I will only work when I have to")
        if "Diligent" in combinations:
            examples.append("I will work hard and be dedicated")
        if "Shy" in combinations:
            examples.append("I will be reserved and prefer solitude")
        if "Gregarious" in combinations:
            examples.append("I will be outgoing and enjoy socializing")
        if "Greedy" in combinations:
            examples.append("I will prioritize my own interests and seek personal gain")
        if "Generous" in combinations:
            examples.append("I will be generous and willing to help others")
        if "Cowardly" in combinations:
            examples.append("I will avoid risks and prioritize my safety")
        if "Brave" in combinations:
            examples.append("I will be courageous and face challenges head-on")
    return examples


def main():
    # create a window
    window = ttk.window.Window(title="Humanising NPCs",themename="lumen")
    
    sf = ScrolledFrame(window, autohide=True, width=1080)
    sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    

    # Create style object
    style = ttk.style.Style(theme='lumen')  # You can choose a different theme

    # Apply the style to the window window
    style.configure(style,window)
    style.configure(style,sf)


    # read the slider value
    slider_value = -2
    # update the slider value
    def update_slider_value(value):
        nonlocal slider_value
        slider_value = float(value)
        print(slider_value)
    # Create slider
    slider = ttk.Scale(sf,from_=-1, to=1, value=0,command=update_slider_value)
    slider.pack()
    counter = 0
    # add a submit button to the window to update the slider value
    def submit():
        nonlocal counter
        counter += 1 
        sm = Traits()
        chosen_traits = []
        mode = -1 if slider_value > 0 else 1
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('start_to_lazy')
            chosen_traits.append("Lazy")
            sm.send('lazy_to_middle_state_1')
        else:
            sm.send('start_to_diligent')
            chosen_traits.append("Diligent")
            sm.send('diligent_to_middle_state_1')
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('middle_state_1_to_shy')
            chosen_traits.append("Shy")
            sm.send('shy_to_middle_state_2')
        else:
            sm.send('middle_state_1_to_gregarious')
            chosen_traits.append("Gregarious")
            sm.send('gregarious_to_middle_state_2')
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('middle_state_2_to_greedy')
            chosen_traits.append("Greedy")
            sm.send('greedy_to_middle_state_3') 
        else:
            sm.send('middle_state_2_to_generous')
            chosen_traits.append("Generous")
            sm.send('generous_to_middle_state_3')
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('middle_state_3_to_cowardly')
            chosen_traits.append("Cowardly")
            sm.send('cowardly_to_end')
        else:
            sm.send('middle_state_3_to_brave')
            chosen_traits.append("Brave")
            sm.send('brave_to_end')
        # on submit, display the list of traits
        examples = generate_examples(chosen_traits)
        # Create labels
        label1 = ttk.Label(sf, text=f"Traits of NPC {counter}: " + ", ".join(chosen_traits), padding="5")
        label2 = ttk.Label(sf, text="----Examples: " + ", ".join(examples), padding="5")
        label1.pack()
        label2.pack()
        style.configure(style,label1)
        style.configure(style,label2)
    # Create button
    button = ttk.Button(sf, text="Submit", command=submit, bootstyle=OUTLINE)
    button.pack()
    window.mainloop()
    

    
    
if __name__ == "__main__":
    main()
    

""" 
# Create style object
style = Style(theme='lumen')  # You can choose a different theme

# Apply the style to the window window
style.configure(window)

# Create and configure frames
frame = ttk.Frame(window, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
style.configure(frame)

# Create labels
label1 = ttk.Label(frame, text=f"Traits of NPC {counter}: " + ", ".join(chosen_traits), padding="5")
label1.grid(row=0, column=0, sticky=tk.W)
style.configure(label1)

label2 = ttk.Label(frame, text="----Examples: " + ", ".join(examples), padding="5")
label2.grid(row=1, column=0, sticky=tk.W)
style.configure(label2)

label_value = ttk.Label(frame, text="Slider Value: 0", padding="5")
label_value.grid(row=2, column=0, columnspan=2, sticky=tk.W)
style.configure(label_value)

label_result = ttk.Label(frame, text="", padding="5")
label_result.grid(row=3, column=0, columnspan=2, sticky=tk.W)
style.configure(label_result)

# Create slider
slider = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=True, command=update_slider_value)
slider.grid(row=2, column=1, sticky=(tk.W, tk.E))
style.configure(slider)

# Create button
button = ttk.Button(frame, text="Submit", command=osubmit)
button.grid(row=3, column=1, sticky=(tk.W, tk.E))
style.configure(button)
"""