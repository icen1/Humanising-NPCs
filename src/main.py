# make a GUI to take input for the state machine and then display image produced of the machine
# it should take the input as a number between 1 and -1 as a slider


from random import uniform as randomuniform
import logging
import customtkinter as ctk
import utils
from functools import partial

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='w')

from generic_automata import Automata
from environment import Environment
from HDT import HDT

# add a few examples on how a character with each combinations of traits would behave
# Generate examples for all combinations of traits
def generate_examples(combinations):
    examples = ['\n']
    if "lazy" in combinations:
        examples.append("I will only work when I have to\n")
    if "diligent" in combinations:
        examples.append("I will work hard and be dedicated\n")
    if "shy" in combinations:
        examples.append("I will be reserved and prefer solitude\n")
    if "gregarious" in combinations:
        examples.append("I will be outgoing and enjoy socializing\n")
    if "greedy" in combinations:
        examples.append("I will prioritize my own interests and seek personal gain\n")
    if "generous" in combinations:
        examples.append("I will be generous and willing to help others\n")
    if "cowardly" in combinations:
        examples.append("I will avoid risks and prioritize my safety\n")
    if "brave" in combinations:
        examples.append("I will be courageous and face challenges head-on\n")
    return examples


def main():
    npc_labels = {}
    HDT_instance = HDT()
    
    current_env = None
    
    
    # create root window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    root.title("Humanising NPCs")
    root.geometry("1080x720")
    
    # scrollbar = ctk.CTkScrollbar(root)
    # scrollbar.pack(side=RIGHT, fill=Y)
    
    
    
    # read the slider value
    slider_value = 0.01
    # update the slider value
    def update_slider_value(value):
        nonlocal slider_value
        slider_value = float(value)
        slider_value_label.configure(text=f"Slider value: {value}")
        
    def change_env(environment, name):
        nonlocal current_env
        current_env = environment

        # Remove all existing labels in the scrollable frame
        for widget in label_frame.winfo_children():
            widget.destroy()

        # Add new labels for the NPCs in the new environment
        for npc in environment.get_NPCS_names():
            label = ctk.CTkLabel(label_frame, text=npc)
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
    npc_trait_input_help = ctk.CTkLabel(environments_frame.tab("Environments"), text="Needs to be in the form of trait1-trait2,trait3-trait4 where trait1 and trait2 are opposites and trait3 and trait4 are opposites.")
    environment_trait_input = ctk.CTkEntry(environments_frame.tab("Environments"), placeholder_text="Environment Actions")
    environment_trait_input_help = ctk.CTkLabel(environments_frame.tab("Environments"), text="Use the format: trait1>[required_trait]trait2{action}(+trait3;-trait4)\n where trait1 is the current trait, required_trait is the required trait, trait2 is the next trait,\n action is the action, trait3 is the trait gained, and trait4 is the trait lost.")
    environment_name_input = ctk.CTkEntry(environments_frame.tab("Environments"), placeholder_text="Environment Name")
    environment_name_input.pack(pady=3)
    environment_trait_input.pack(pady=3)
    environment_trait_input_help.pack(pady=3)
    npc_trait_input.pack(pady=3)
    npc_trait_input_help.pack(pady=3)
    
    environment_scrollable_frame = ctk.CTkScrollableFrame(environments_frame.tab("World"), width=1080, height=300)
    environment_scrollable_frame.pack(pady=3)
    
    

    def add_environment():
        npc_traits = utils.parse_traits(npc_trait_input.get())
        npc_actions = utils.parse_transitions(environment_trait_input.get())
        environment_name = environment_name_input.get()
        HDT_instance.add_environment(environment_name, npc_actions, npc_traits)
        for environment in HDT_instance.get_environment_names():
            # Check if the button already exists
            if environment in environment_buttons:
                # If the button exists, configure it
                environment_buttons[environment].configure(text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
            else:
                # If the button doesn't exist, create it
                environment_buttons[environment] = ctk.CTkButton(environment_scrollable_frame, text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
                environment_buttons[environment].pack(pady=3)

        logging.info(f"Environment: {environment_name} added with actions: {npc_actions} and NPC traits: {npc_traits}")
        
        environments_frame.set("World")

        
    def add_environment_custom(environment_name, npc_actions, npc_traits):
        npc_traits = utils.parse_traits(npc_traits)
        npc_actions = utils.parse_transitions(npc_actions)
        HDT_instance.add_environment(environment_name, npc_actions, npc_traits)
        for environment in HDT_instance.get_environment_names():
            # Check if the button already exists
            if environment in environment_buttons:
                # If the button exists, configure it
                environment_buttons[environment].configure(text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
            else:
                # If the button doesn't exist, create it
                environment_buttons[environment] = ctk.CTkButton(environment_scrollable_frame, text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
                environment_buttons[environment].pack(pady=3)
        logging.info(f"Environment: {environment_name} added with actions: {npc_actions} and NPC traits: {npc_traits}")
    
    environment_button = ctk.CTkButton(environments_frame.tab("Environments"), text="Add Environment", command=add_environment)    
    environment_button.pack(pady=3)

    tmp_npc_actions = "connector>no_groceries,no_groceries>[diligent]groceries{Get food}(+hunger;-money),groceries>meat{protein source}(+food;-money),groceries>veg{vitamin source}(+vitamins;-money),groceries>fruits{fiber source}(+fiber;-money),meat>[generous]steak{tasty meat}(+satisfaction;-money),veg>[greedy]salad{healthy meal}(+nutrition;-money),fruits>[healthy]apple{delicious fruit}(+happiness;-money),connector>[diligent]work{earn money}(+money),work>connector,salad>eat,steak>eat,apple>eat,connector>[money]clothes(+tshirt;-money),clothes>connector,eat>connector"
    add_environment_custom("desert_city_environment", tmp_npc_actions, "diligent-lazy,gregarious-shy,generous-greedy,brave-cowardly")
    environment = HDT_instance.get_environment("desert_city_environment")
    
    # for environment in HDT_instance.get_environment_names():
    #     environment_buttons[f"{environment}_env"] = environment
    #     environment_buttons[f"{environment}_env"] = ctk.CTkButton(environment_scrollable_frame, text=environment, command=lambda: change_env(HDT_instance.get_environment(environment), "World"))
    #     environment_buttons[f"{environment}_env"].pack(pady=3)

        
    
    # Create slider
    slider = ctk.CTkSlider(environments_frame.tab("World"), from_=-1, to=1, command=update_slider_value, number_of_steps=80)
    slider.pack()
    # Create a label to display the slider value
    slider_value_label = ctk.CTkLabel(environments_frame.tab("World"), text=f"Slider value: {slider_value}")
    slider_value_label.pack()
    npc_counter = 0
    label_frame = ctk.CTkScrollableFrame(environments_frame.tab("World"), width=1080, height=300)
    
    npc_labels = {}
    npc_button_frames = {}
    npc_buttons = {}
    # example_labels = {}

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
        chosen_traits = environment.get_Current_NPC_traits(f"NPC {npc_counter}")
        logging.log(logging.INFO, f"Chosen traits: {chosen_traits}")
        examples = generate_examples(chosen_traits)
        # Create labels
        label1 = ctk.CTkLabel(label_frame, text=f"Traits of NPC {npc_counter}: " + ", ".join(chosen_traits))
        # label2 = ctk.CTkLabel(label_frame, text="----Examples: " + " ".join(examples))
        label2 = ctk.CTkLabel(label_frame, text="Possible actions: \n")
        npc_labels[f"NPC {npc_counter}"] = label1
        # example_labels[f"NPC {npc_counter}"] = label2
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
        if current_env.get_name() is not None:
            environment = HDT_instance.get_environment(current_env.get_name())
            for npc_name in environment.get_NPCS_names():
                traits = environment.get_Current_NPC_traits(npc_name)
                if traits:
                    traits_text = f"Traits of {npc_name}: " + ", ".join(traits)
                    examples_text = "----Examples: " + " ".join(generate_examples(traits))

                    if npc_name not in npc_labels:
                        # If this NPC doesn't have a label yet, create one
                        npc_labels[npc_name] = ctk.CTkLabel(label_frame)
                        npc_labels[npc_name].pack()

                    # Update the text of the label for this NPC
                    npc_labels[npc_name].configure(text=traits_text)                        

                    if npc_name not in npc_button_frames:
                        npc_button_frames[npc_name] = ctk.CTkScrollableFrame(label_frame)
                        npc_button_frames[npc_name].pack()

                transitions = environment.get_Current_NPC_Next_Transitions(npc_name)
                # if not transitions and npc_name in npc_labels and npc_name in npc_button_frames:
                #     # If there are no more transitions, remove the label and the button frame for the NPC
                #     npc_labels[npc_name].destroy()
                #     del npc_labels[npc_name]
                #     npc_button_frames[npc_name].destroy()
                #     del npc_button_frames[npc_name]
                # else:
                for i in range(max(len(transitions), len(npc_buttons))):
                    if i < len(transitions):
                        transition = transitions[i]
                        command_func = partial(environment.set_Current_NPC_action, npc_name, transition[1])

                        if f"{npc_name}_{i}" not in npc_buttons:
                            npc_buttons[f"{npc_name}_{i}"] = ctk.CTkButton(npc_button_frames[npc_name], text=transition[0], command=command_func)
                            npc_buttons[f"{npc_name}_{i}"].pack()
                        else:
                            npc_buttons[f"{npc_name}_{i}"].configure(text=transition[0], command=command_func)
                    elif f"{npc_name}_{i}" in npc_buttons:
                        # remove unused button
                        npc_buttons[f"{npc_name}_{i}"].destroy()
                        del npc_buttons[f"{npc_name}_{i}"]
            root.after(200, update_traits)

    
    # start with environment tab
    environments_frame.set("Environments")
    
    update_traits()
    root.mainloop()
    

    
    
if __name__ == "__main__":
    main()
    