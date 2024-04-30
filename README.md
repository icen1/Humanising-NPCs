# Humanising-NPCs/

**Table of Contents**

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)
- [License](#license)

## Requirements

`humanising-npcs/` requires ubuntu 20.04 or later, python 3.8 or later, and the following python packages:

1. pip
2. X11 for graphical representation

The following modules are required but are installed automatically using the process in [Installation](#installation):

1. python-statemachine
2. tkinter
3. customtkinter
4. ttkbootstrap

## Installation

We use pip to install the requirments by found in requirements.txt

```console
python3 -m pip install -r requirements.txt
```

Afterwards the program could be run by using

```console
python3 src/main.py
```

## Usage

The user is expected to start in the enviroment tab and are expected to add their own traits and actions according to the parser discussed in the report. We have a sample enviroment already in the project for the user to be able to try the program without writing their own actions or traits. To access said sample the user has to click on the 'World' tab at the top of the screen.

The sample mentioned has the following data:

- **Name**: `desert_city_enviroment`
- **Traits**: `diligent-lazy,gregarious-shy,generous-greedy,brave-cowardly`
- **Actions**: `connector>no_groceries,no_groceries>[diligent]groceries{Get food}(+hunger;-money),groceries>meat{protein source}(+food;-money),groceries>veg{vitamin source}(+vitamins;-money),groceries>fruits{fiber source}(+healthy;-money),meat>[generous]steak{tasty meat}(+satisfaction;-money),veg>[greedy]salad{healthy meal}(+nutrition;-money),fruits>[healthy]apple{delicious fruit}(+happiness;-money),connector>[diligent]work{earn money}(+money),work>connector,salad>eat,steak>eat,apple>eat,connector>[money]clothes(+tshirt;-money),clothes>connector,eat>connector`

## Notes

1. Currently the program only works on Linux due to the multiprocessing module using `spawn` instead of `fork` which doesn't allow us to pickle classes
2. A demo video is part of the zip file with the name 'demo' in case the above requirments weren't met by the supervisor

## License

`humanising-npcs/` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
