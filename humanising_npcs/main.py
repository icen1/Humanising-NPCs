# make a GUI to take input for the state machine and then display image produced of the machine
# it should take the input as a number between 1 and -1 as a slider

import multiprocessing
import tempfile
import time
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from random import uniform as randomuniform
import os
import logging
import customtkinter as ctk

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='w')


os.environ['HUMANISING_NPCS_TRAITS'] = "diligent-lazy,gregarious-shy,generous-greedy,brave-cowardly"
os.environ['HUMANISING_NPCS_ENVIRONMENT'] = "forest,city"

from generic_automata import Automata
from environment import Environment
from HDT import HDT

# add a few examples on how a character with each combinations of traits would behave
# Generate examples for all combinations of traits
# def generate_examples(combinations):
#     for i in range(1, len(combinations) + 1):
#         examples = []
#         if "lazy" in combinations:
#             examples.append("I will only work when I have to")
#         if "diligent" in combinations:
#             examples.append("I will work hard and be dedicated")
#         if "shy" in combinations:
#             examples.append("I will be reserved and prefer solitude")
#         if "gregarious" in combinations:
#             examples.append("I will be outgoing and enjoy socializing")
#         if "greedy" in combinations:
#             examples.append("I will prioritize my own interests and seek personal gain")
#         if "generous" in combinations:
#             examples.append("I will be generous and willing to help others")
#         if "cowardly" in combinations:
#             examples.append("I will avoid risks and prioritize my safety")
#         if "brave" in combinations:
#             examples.append("I will be courageous and face challenges head-on")
#     return examples


def main():
    npc_labels = {}
    HDT_instance = HDT()
    
    current_env = None
        
    HDT_instance.add_environment("desert_city_environment")
    environment = HDT_instance.get_environment("desert_city_environment")
    
    
    # create root window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    root.title("Humanising NPCs")
    root.geometry("1080x720")
    
    # scrollbar = ctk.CTkScrollbar(root)
    # scrollbar.pack(side=RIGHT, fill=Y)
    
    
    
    # read the slider value
    slider_value = -2
    # update the slider value
    def update_slider_value(value):
        nonlocal slider_value
        slider_value = float(value)
        
    def change_env(environment,name):
        nonlocal current_env
        current_env = environment
        for npc in environment.get_NPCS_names():
            label = ctk.CTkLabel(environments_frame.tab(name), text=npc)
            label.pack()
            
    # Create environment table
    # take all width and height of the window
    environments_frame = ctk.CTkTabview(root, width=1080, height=720)
    
    # def switch_tab(tab_name):
    #     # Select the tab
    #     environments_frame.select(tab_name)

    #     # Hide all widgets in non-active tabs
    #     for tab in environments_frame.tabs():
    #         if tab != tab_name:
    #             for child in environments_frame.tab(tab).winfo_children():
    #                 child.pack_forget()
    
    environments_frame.pack()
    environments_frame.add("World")
    environments_frame.add("Environments")
    
    environment_buttons = {}
    
    # fill out environment tab 
    # add a npc traits text box, environment trait text box, an environment name text box, and a button to add a new environment
    npc_trait_input = ctk.CTkEntry(environments_frame.tab("Environments"), placeholder_text="NPC Traits.")
    npc_trait_input_help = ctk.CTkLabel(environments_frame.tab("Environments"), text="Eneeds to be in the form of trait1-trait2,trait3-trait4 where trait1 and trait2 are opposites and trait3 and trait4 are opposites.")
    environment_trait_input = ctk.CTkEntry(environments_frame.tab("Environments"), placeholder_text="Environment Traits")
    environment_trait_input_help = ctk.CTkLabel(environments_frame.tab("Environments"), text="Comma separated traits. If the traits don't match any NPC traits those will have no effect.")
    environment_name_input = ctk.CTkEntry(environments_frame.tab("Environments"), placeholder_text="Environment Name")
    environment_name_input.pack(pady=3)
    environment_trait_input.pack(pady=3)
    environment_trait_input_help.pack(pady=3)
    npc_trait_input.pack(pady=3)
    npc_trait_input_help.pack(pady=3)
    
    environment_scrollable_frame = ctk.CTkScrollableFrame(environments_frame.tab("World"), width=1080, height=300)
    environment_scrollable_frame.pack(pady=3)
    
    

    def add_environment():
        npc_traits = npc_trait_input.get()
        environment_traits = environment_trait_input.get()
        environment_name = environment_name_input.get()
        # file_names = []
        # # add enviroment traits and npc traits to a tempfile that starts with the environment name
        # with tempfile.NamedTemporaryFile(mode='w', prefix=f"{environment_name}_HUMANISING_NPCS_ENVIRONMENT", suffix=".json", delete=False) as f:
        #     f.write(f'{{"{environment_name}": {environment_traits}}}')
        #     file_names.append(f.name)
        #     f.close()
        # with tempfile.NamedTemporaryFile(mode='w', prefix=f"{environment_name}_HUMANISING_NPCS_TRAITS", suffix=".json", delete=False) as f:
        #     f.write(f'{{"{environment_name}": {npc_traits}}}')
        #     file_names.append(f.name)
        #     f.close()
        os.environ['HUMANISING_NPCS_TRAITS'] = npc_traits
        os.environ['HUMANISING_NPCS_ENVIRONMENT'] = environment_traits
        HDT_instance.add_environment(environment_name)
        for environment in HDT_instance.get_environment_names():
            # Check if the button already exists
            if environment in environment_buttons:
                # If the button exists, configure it
                environment_buttons[environment].configure(text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
            else:
                # If the button doesn't exist, create it
                environment_buttons[environment] = ctk.CTkButton(environment_scrollable_frame, text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
                environment_buttons[environment].pack(pady=3)

        logging.info(f"Environment: {environment_name} added with traits: {environment_traits} and NPC traits: {npc_traits}")
    
    environment_button = ctk.CTkButton(environments_frame.tab("Environments"), text="Add Environment", command=add_environment)    
    environment_button.pack(pady=3)


    
    # for environment in HDT_instance.get_environment_names():
    #     environment_buttons[f"{environment}_env"] = environment
    #     environment_buttons[f"{environment}_env"] = ctk.CTkButton(environment_scrollable_frame, text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
    #     environment_buttons[f"{environment}_env"].pack(pady=3)
    
    
    
    # Create slider
    slider = ctk.CTkSlider(environments_frame.tab("World"), from_=-1, to=1, command=update_slider_value)
    slider.pack()
    npc_counter = 0
    label_frame = ctk.CTkScrollableFrame(environments_frame.tab("World"), width=1080, height=300)
    
    npc_labels = {}
        

    # add a submit button to the window to update the slider value
    def submit(environment):
        if environment is None:
            # break out of the function
            return
        nonlocal npc_counter
        environment.add_NPC(f"NPC {npc_counter}",slider_value)
        sm = environment.get_NPC(f"NPC {npc_counter}")
        logging.info(f"Environment: {sm.get_environment()}")
        # logging.info(f"Transition names: {sm.get_transitions()}")
        chosen_traits = environment.get_NPC_traits(f"NPC {npc_counter}")
        logging.log(logging.INFO, f"Chosen traits: {chosen_traits}")
        # examples = generate_examples(chosen_traits)
        # Create labels
        label1 = ctk.CTkLabel(label_frame, text=f"Traits of NPC {npc_counter}: " + ", ".join(chosen_traits))
        label2 = ctk.CTkLabel(label_frame, text="----Examples: " + ", ".join('examples'))
        npc_labels[f"NPC {npc_counter}"] = label1
        label1.pack()
        label2.pack()
        npc_counter += 1
    # Create button
    button = ctk.CTkButton(environments_frame.tab("World"), text="Submit", command=lambda: submit(current_env))
    button.pack()
    current_env = HDT_instance.get_environment(environment_name=environment.get_name())

    # Go through all NPCs in current enviroment and add them to npc_labels as keys
    # Go through all NPCs in the current environment
    for npc_name in current_env.get_NPCS_names():
        # Add the NPC to npc_labels as a key
        npc_labels[npc_name] = ctk.CTkLabel(label_frame)
        npc_labels[npc_name].pack()

    label_frame.pack()

    def update_traits():
        for environment_name in HDT_instance.get_environment_names():
            environment = HDT_instance.get_environment(environment_name)
            for npc_name in environment.get_NPCS_names():
                # Update the text of the label for this NPC
                # # stop the NPC
                # environment.remove_NPC(npc_name)
                if npc_name in npc_labels:
                    traits = environment.get_NPC_traits(npc_name)
                    if traits == []:
                        pass
                    else:
                        npc_labels[npc_name].configure(text=f"Traits of {npc_name}: " + ", ".join(traits))
                else:
                    # If this NPC doesn't have a label yet, create one
                    traits = environment.get_NPC_traits(npc_name)
                    if traits == []:
                        pass
                    else:
                        npc_labels[npc_name].configure(text=f"Traits of {npc_name}: " + ", ".join(traits))
                        npc_labels[npc_name].pack()
    # Create a button to update the traits at the top right of the window with the picture as refresh
    update_button = ctk.CTkButton(environments_frame, text="Update Traits", command=update_traits)
    update_button.grid(row=6, column=0)

    
    
    
    root.mainloop()
    

    
    
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