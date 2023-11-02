# make a GUI to take input for the state machine and then display image produced of the machine
# it should take the input as a number between 1 and -1 as a slider
import time
from tkinter import Button, Label, Scale, Tk
from PIL import ImageTk, Image
from random import uniform as randomuniform

from traits import Traits


def main():
    # create a window
    window = Tk()
    # set the title
    window.title("Humanising NPCs")
    # set the window size
    window.geometry("1600x900")
    # set the window background color
    window.config(background="white")
    # read the slider value
    slider_value = -2
    # update the slider value
    def update_slider_value(value):
        nonlocal slider_value
        slider_value = float(value)
    # add a slider to the window between 1 and -1
    window.slider = Scale(window, from_=1, to=-1, orient="horizontal", label="Goodness of NPC", length=600, tickinterval=0.1, resolution=0.1, showvalue=True, command=update_slider_value)
    # add the slider to the window
    window.slider.pack()
    # add a submit button to the window to update the slider value
    def submit():     
        sm = Traits()
        img_path = "./readme_trafficlightmachine_" + time.strftime("%Y%m%d-%H%M%S") + ".png"
        sm._graph().write_png(img_path)
        mode = -1 if slider_value > 0 else 1
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('start_to_lazy')
            print("Lazy")
            sm.send('lazy_to_middle_state_1')
        else:
            sm.send('start_to_diligent')
            print("Diligent")
            sm.send('diligent_to_middle_state_1')
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('middle_state_1_to_shy')
            print("Shy")
            sm.send('shy_to_middle_state_2')
        else:
            sm.send('middle_state_1_to_gregarious')
            print("Gregarious")
            sm.send('gregarious_to_middle_state_2')
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('middle_state_2_to_greedy')
            print("Greedy")
            sm.send('greedy_to_middle_state_3') 
        else:
            sm.send('middle_state_2_to_generous')
            print("Generous")
            sm.send('generous_to_middle_state_3')
        if slider_value+(mode*randomuniform(0,1)) < 0:
            sm.send('middle_state_3_to_cowardly')
            print("Cowardly")
            sm.send('cowardly_to_end')
        else:
            sm.send('middle_state_3_to_brave')
            print("Brave")
            sm.send('brave_to_end')
        print(sm.current_state)
    window.submit = Button(window, text="Submit", command=submit)
    window.submit.pack()
    # display the image
    img = ImageTk.PhotoImage(Image.open("./readme_trafficlightmachine_20231102-124203.png"))
    panel = Label(window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    # display the window
    window.mainloop()
    

    
    
if __name__ == "__main__":
    main()
    
    