# Presentation Outline

## Introduction

### Ask 3 questions then move on explaining the NPCs and how they are ignored then arrow in the knee meme

## Research

### Most papers talked about how AI and ML could solve the issue which became the industry started

### Easier in games (0.6 human likness) but harder in other (care about character creation only)

### FSM AI and how research paper say it is dead and mention why (computing power, limited number of states, and how they are repetitive)

## Motivation

### "With this in mind and with everyone talking about AI/ML"

### Talk about how AI/ML approaches will take time and may have ethical and social issues

### Take another look at FSM to make NPCs as human as possible and solve limited states issue

## Terminology

now there are 3 words that will get repeated constantly and may already has, *in slides*

## Technical Aspect

### Trying to represent opposite traits led us to Markov chains

### We take a set of traits from the user, where the first and second are opposites

### They don't have to be opposites, they can be anything, but we treat them as mutually exclusive

### The user chooses a value and depending on that value and some randomness, those traits are chosen

### Those traits serve as base traits or personality traits that will decide the actions of those NPCs

### For now, let's choose 4 base sets of traits: Diligent and Lazy, Gregarious and Shy, Generous and Greedy, Brave and Cowardly

### The creation of this state machine is generic as possible, we do this by essentially creating a meta-class, a state machine template that is made by the environment from the input given and then giving a copy of it to each NPC

### The NPCs aren't alive as their traits and actions have no consequences and as if there is no world to interact with

### More research needed to be done

### History deterministic timed automatas, automatas that their design could be non-deterministic, but through their knowledge of past states that they were in and "clock value" representing a condition, they were, in fact, deterministic

### We started keeping track of states we have been in

### The best way to solve the limited states issue is to change the limit to the user's imagination and their computer's memory. We did this by delegating the task of creating those states to the user themselves

### By using the meta-class or the state machine templatte we created earlier, we allow the user to add specific actions that could depend on previous actions, with the possibility of each action having an effect that could affect the following actions, making them possible and preventing others

### Example

### This means user can make any environment and make their own set of actions that suit their world, game or book. For example we could make something like this, that involves working, getting groceries, cooking, eating and buying clothes

## Project Management

So for code management i exlusively used github, using some githun action like testing to make my life a bit easier and know whether i broke smth, while for time management i created a few gantt charts that are in the appendix, and with the their rough timeline here. So Let's start with term 1. As mentioned before, I don't think I split the project into chunks of research and development that are fully separated. Instead, the first 4 weeks were focused on looking into different state machines and languages with the best modules for them. I used those languages to create state machines, assessed how active the maintainers of said modules are, and tracked how frequently they get updated.

In the next 4 weeks, after implementing the Markov chain implementation we saw previously, I worked on the generic automata implementation that allows us to create the meta-class state machine and also worked on a simple UI interface. This served as the basis for all my work in term 2.

From weeks 8-10, I mostly focused on the progress report, figuring out the timeline for the next term, ways to advance my implementation, and establishing concrete goals for the project more generally.

Starting term 2, I received a few recommendations from my progress report. The first was the possibility of implementing history determinism, and looking at it, it seemed perfect. We followed a similar cycle by starting with researching what that actually is and then trying to create smaller variants of it in code. This allowed me to gauge how easy or hard of a task it would be and explore ways to implement it in my existing framework.

Being comfortable with it and having a concrete way of implementing it, I focused on its implementation while constantly referring back to the notes I took during the research and supervisor meetings to ensure alignment with my understanding. These weeks also included feedback from other students, and most of the complaints I received were about the UI and wanting to add more interactions to the NPCs. I addressed both concerns, focusing more on the latter as I wanted to emphasize the interesting intersection where the theory of the project meets the practical aspects.

In the last two weeks, I am focusing on one allowing those NPCs to interact with each other and not just with the enivronment and the user, as i beleive this will open a new world of possibilities that will be discussed in the next steps.

As part of the progress report, I created a few MOSCOW goals that I wanted to achieve and managed to do so. Let's start with the "Must-haves."

### Must-haves

1. We successfully generated the character's personality using the Markov chain at the start. This depended on user input and a random value to try and make it feel more alive.

2. We allowed the user not only to interact with the NPC but also with the environment. The user literally creates the environment and can change everything in it.

And for the "Should-haves."

### Should-haves

1. We implemented the first by using history determinism, as explained before. The states that we went to matter and are stored, and according to the path we took previously, we will choose the next path.

2. Regarding the second "should-have," we couldn't directly do it, but we do have all our NPC and environment data in JSON format. This makes it easier to use if someone decides that they want to do something with it.

## Limitations

There are three main limitations here

1. The first is computing power, that means process speed and memory which were ones of the main limitations in the FSM AI papers I read. This is something that was out of the scope of my project to solve.

2. The second point is that NPCs don't interact with each other; instead, they interact with the user and the environment. Making the NPCs interact with each other will go a long way in increasing immersion. For example, having a limited pool of money in the environment could mean that getting money involves taking it from someone else, representing trading. This is not hard to implement and could be achieved using the message passing system we have, where NPCs interact with the environment, and the environment reacts to NPCs' interactions with an action that changes other NPCs' traits and values.

3. The third limitation is that we gave the user the power to create their own environment, world, and NPCs. This is great because, as mentioned before, the only limit here is what the user themselves can imagine and is willing to create. So if the user is not willing to work on their world and NPCs, their world will be as limited as they made it out to be.

## Next Steps

As a continuation of the limitations, we have the next steps.

1. I have already mentioned how we can allow the NPCs to interact with each other, which will add a lot of immersion and allow complex human systems to develop, like trade, for example.

2. Another thing I could envision is a type of AI or ML algorithm that could take and process what the user said, and change it to the format of the application here to create the state machines. I could see this as a new way of making text-based games and as a backend for bigger titles. If we can represent complex human societies as a state machine, we could use this power to enable users to create their own simple sandbox games with whatever features they want, possibly in days or even hours.

3. The third is a new, more interactive way to create those machines by replacing the current format and the parser I have. Making the user literally drag and drop different states will make the whole process much easier and much more user-friendly.

## Conclusion

We created a program that can generate a sandbox world, whether it's a city, town, or a galaxy, with the user having the power to create this world, its people, and the actions that those people undertake. This will assist book writers and Dungeon Masters (DMs) in not only keeping track of their NPCs and adjusting their actions based on the environment but also in creating scenarios for any world they want to build.

We found a solution to the problem of limited and repetitive states in games by enabling users to create and add their own states and actions into this world. The number of states is limited only by the time the user invests in creating them.

## Demo

## Questions
