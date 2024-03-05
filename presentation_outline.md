# Introduction

## Some questions

- Has anyone here read a fantasy book?
- Played a story-driven computer game?
- Or maybe even played something like Dungeons and Dragons?

Something common in all of those is main characters, whether they are the players in DnD, protagonists in a book, or the character you play in a game. They have other characters around them, some more developed than others. Those characters are called NPCs, and they help set the tone of the game and flesh out the world and its story.

Sadly, those characters are usually neglected, with them having repeated dialogue options. The most popular phrase is 'I took an arrow to the knee' in Skyrim, which became a meme and somehow found its way to mean getting married. In books, characters are sidelined, and in other cases, they feel like filler and static characters in TTRPGs.

# Research

Through my research into it, most of the papers I saw and read were about how to use machine learning to solve this and how to use AI to partially treat the problem. Of course, a lot of AI methods are already used in games, some of them are relatively successful, being the industry standard nowadays, with the topmost being Reinforcement learning, which achieved around 0.6 human likeness. This is very promising, of course, but still far from being human-like. Other alternatives for writers, storytellers, or DMs running TTRPG games are only for creating said NPCs and never about how their life continues or how they are affected by their environment or the player's actions. Some research papers focused more on a finite state machine AI and how, so far, they have been standard when creating games, but some research papers are particularly vocal about how they are on the dying end due to their limitations, one of them being that they have a limited size with each game. As much as its developers try, they will always have a set number of paths, which means that there is bound to be repeated characters in whatever media they are used in.

# Motivation

With this in mind and with everyone looking at ML to solve those issues, something that might take years and even then its actions are unpredictable, where it can still do something it is not supposed to do which may cause ethical and social issues. I wanted to take another look at finite state machines and try to make the NPCs as human as possible, all the while solving one of the major problems that the FSM AI has, the number of limited states they need to have by definition.

# Terminology

now there are 3 words that will get repeated constantly and may already has, *in slides*

# Methodology

I would like to think the project itself was split up almost equally between research and development, and they weren't split up in chunks. For example, the first 4 months for research and the second 4 months for research; they mostly happened together where I needed to research further to be able to improve the state machine I had. For example, we started with a Markov chain, which is something like the following state machine and had to find and develop a better method of representing those NPCs using a state machine. We started by allowing the user to choose two sets of traits. Those traits were supposed to be opposites, for example, hardworking and lazy, generous and greedy, friendly and shy, or tall and short. Those sets of traits could be anything the user chose; they could be grandma and cousin, which are not opposites, but we would treat them as mutually exclusive for the purpose of our Markov chains. Those traits will serve as base traits or personality traits that will decide the actions of those NPCs.

For now, let's choose 4 base sets of traits: Diligent and Lazy, Gregarious and Shy, Generous and Greedy, Brave and Cowardly. As you can see between each set of states, there is a middle state that serves as an epsilon transition from the first set to the next set. Those personality traits are chosen by a value that the user chooses in addition to some randomness to make the environment feel more alive.

Now the generation of this machine is as generic as it gets; the user passes on the traits, and depending on these traits, we create a state machine template that belongs to the environment. Then, this environment gives a copy of this template to every NPC.

Now, those NPCs were only alive in the sense that they have personality traits, but there were no consequences and there was nothing for them to do, almost as if their choices and traits did nothing, almost as if there is no world to interact with. So, to advance the implementation further, more research needed to be done.

This research led to finding about History deterministic timed automatas, automatas that their design could be non-deterministic, but through their knowledge of past states that they were in and "clock value" representing a condition, they were, in fact, deterministic.

Knowing this, we decided to do a few things. The first is keeping track of the states we have been into. For example, if our machine chose "brave" as a personality trait, we started keeping track of it. The second is how we decided to solve the problem of having limited states in games, with the us changing that limit to literally being the user's imagination and their computer computing power. We did this by delegating the task of creating those states to the user. By using the meta-class we created earlier, we allow the user to add specific actions with the possibility of each action having an effect that could affect the following actions, making them possible and preventing others. For example, let's assume that you have been in the 'work' state that gives 'money,' and then you chose to go to the 'groceries' state, which takes 'money' away and adds 'food,' for example. But if you have a state called 'clothes' that also needs 'money,' you won't be able to go to it because you don't have the required condition. Instead, you will have to get 'money' again using the state called 'work,' for example.

Now, this means that the user can essentially make whatever machine they want for the actions they want the NPCs to take. For example, we could make something like this, and again, this is completely customizable by the user.

# Project Management

So how did I manage this project? Let's start with term 1. As mentioned before, I don't think I split the project into chunks of research and development that are fully separated. Instead, the first 4 weeks were focused on looking into different state machines and languages with the best modules for them. I used those languages to create state machines, assessed how active the maintainers of said modules are, and tracked how frequently they get updated.

In the next 4 weeks, after implementing the Markov chain implementation we saw previously, I worked on the generic automata implementation that allows us to create the meta-class state machine and also worked on a simple UI interface. This served as the basis for all my work in term 2.

From weeks 8-10, I mostly focused on the progress report, figuring out the timeline for the next term, ways to advance my implementation, and establishing concrete goals for the project more generally.

Starting term 2, I received a few recommendations from my progress report. The first was the possibility of implementing history determinism, and looking at it, it seemed perfect. We followed a similar cycle by starting with researching what that actually is and then trying to create smaller variants of it in code. This allowed me to gauge how easy or hard of a task it would be and explore ways to implement it in my existing framework.

Being comfortable with it and having a concrete way of implementing it, I focused on its implementation while constantly referring back to the notes I took during the research and supervisor meetings to ensure alignment with my understanding. These weeks also included feedback from other students, and most of the complaints I received were about the UI and wanting to add more interactions to the NPCs. I addressed both concerns, focusing more on the latter as I wanted to emphasize the interesting intersection where the theory of the project meets the practical aspects.

In the last two weeks, I have been concentrating on my presentation, and you will be the judge of how that's going.

As part of the progress report, I had a few goals that I wanted to achieve and managed to do so. Let's start with the "Must-haves."

## Must-haves

1. We successfully generated the character's personality using the Markov chain at the start. This depended on user input and a random value to try and make it feel more alive.

2. We allowed the user not only to interact with the NPC but also with the environment. The user literally creates the environment and can change everything in it.

And for the "Should-haves."

## Should-haves

1. We implemented the first by using history determinism, as explained before. The states that we went to matter and are stored, and according to the path we took previously, we will choose the next path.

2. Regarding the second "should-have," we couldn't directly do it, but we do have all our NPC and environment data in JSON format. This makes it easier to use if someone decides that they want to do something with it.


# Limitations

There are three main limitations here

1. The first is computing power, which was one of the main limitations in the FSM AI papers I read. This is something that was out of the scope of my project to solve.

2. The second point is that NPCs don't interact with each other; instead, they interact with the user and the environment. Making the NPCs interact with each other will go a long way in increasing immersion. For example, having a limited pool of money in the environment could mean that getting money involves taking it from someone else, representing trading. This is not hard to implement and could be achieved using the message passing system we have, where NPCs interact with the environment, and the environment reacts to NPCs' interactions with an action that changes other NPCs' traits and values.

3. The third limitation is that we gave the user the power to create their own environment, world, and NPCs. This is great because, as mentioned before, the only limit here is what the user themselves can imagine and is willing to create. So if the user is not willing to work on their world and NPCs, their world will be as limited as they made it out to be.

# Next Steps

As a continuation of the limitations, we have the next steps.

1. I have already mentioned how we can allow the NPCs to interact with each other, which will add a lot of immersion and allow complex human systems to develop, like trade, for example.

2. Another thing I could envision is a type of AI or ML algorithm that could take and process what the user said, and change it to the format of the application here to create the state machines. I could see this as a new way of making text-based games and as a backend for bigger titles. If we can represent complex human societies as a state machine, we could use this power to enable users to create their own simple sandbox games with whatever features they want, possibly in days or even hours.

3. The third is a new, more interactive way to create those machines by replacing the current format and the parser I have. Making the user literally drag and drop different states will make the whole process much easier and much more user-friendly.

# Conclusion

We created a program that can generate a sandbox world, whether it's a city, town, or a galaxy, with the user having the power to create this world, its people, and the actions that those people undertake. This will assist book writers and Dungeon Masters (DMs) in not only keeping track of their NPCs and adjusting their actions based on the environment but also in creating scenarios for any world they want to build.

Additionally, we found a solution to the problem of limited and repetitive states in games by enabling users to create and add their own states and actions into this world. The number of states is limited only by the time the user invests in creating them.

# Demo

# Questions
