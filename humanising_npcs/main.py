# make a GUI to take input for the state machine and then display image produced of the machine
# it should take the input as a number between 1 and -1 as a slider
from tkinter import Image, Scale, Tk


def main():
    # create a window
    window = Tk()
    # set the title
    window.title("Humanising NPCs")
    # set the window size
    window.geometry("800x600")
    # set the window background color
    window.config(background="white")
    # read the slider value
    slider_value = -2
    # update the slider value
    def update_slider_value(value):
        nonlocal slider_value
        slider_value = value
    # add a slider to the window between 1 and -1
    window.slider = Scale(window, from_=1, to=-1, orient="horizontal", label="Goodness of NPC", length=600, tickinterval=0.1, resolution=0.1, showvalue=True, command=update_slider_value)
    # add the slider to the window
    window.slider.pack()
    # display the window
    window.mainloop()
    
    print(slider_value)

    
    
if __name__ == "__main__":
    main()
    
    