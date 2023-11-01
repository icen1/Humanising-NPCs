from statemachine import StateMachine, State

class Traits(StateMachine):
    """ A state machine for the traits of a character. """
    start = State('Start', initial=True)
    traits  =["diligent","lazy","gregarious","shy","generous","greedy"]
    # make states for each trait
    diligent = State('Diligent')
    lazy = State('Lazy')
    middle_state_1 = State('Middle State 1')
    gregarious = State('Gregarious')
    shy = State('Shy')
    middle_state_2 = State('Middle State 2')
    generous = State('Generous')
    greedy = State('Greedy')
    end = State('End')
    
    # add transitions
    # start to diligent
    start_to_diligent = start.to(diligent)
    # start to lazy
    start_to_lazy = start.to(lazy)
    # diligen and lazy to middle state 1
    diligent_to_middle_state_1 = diligent.to(middle_state_1)
    lazy_to_middle_state_1 = lazy.to(middle_state_1)
    # middle state 1 to gregarious and shy
    middle_state_1_to_gregarious = middle_state_1.to(gregarious)
    middle_state_1_to_shy = middle_state_1.to(shy)
    # gregarious and shy to middle state 2
    gregarious_to_middle_state_2 = gregarious.to(middle_state_2)
    shy_to_middle_state_2 = shy.to(middle_state_2)
    # middle state 2 to generous and greedy
    middle_state_2_to_generous = middle_state_2.to(generous)
    middle_state_2_to_greedy = middle_state_2.to(greedy)
    # generous and greedy to end
    generous_to_end = generous.to(end)
    greedy_to_end = greedy.to(end)
    
    
    
    
    

    # print the state machine
    def on_enter_diligent(self):
        print("I am diligent")
    def on_enter_lazy(self):
        print("I am lazy")
    def on_enter_gregarious(self):
        print("I am gregarious")
    def on_enter_shy(self):
        print("I am shy")
    def on_enter_generous(self):
        print("I am generous")
    def on_enter_greedy(self):
        print("I am greedy")
    
    # print the state machine
    def on_exit_diligent(self):
        print("I am no longer diligent")
    def on_exit_lazy(self):
        print("I am no longer lazy")
    def on_exit_gregarious(self):
        print("I am no longer gregarious")
    def on_exit_shy(self):
        print("I am no longer shy")
    def on_exit_generous(self):
        print("I am no longer generous")
    def on_exit_greedy(self):
        print("I am no longer greedy")
        
    def before_cycle(self, event: str, source: State, target: State, message: str = ""):
        print(f"Before cycle: {event} from {source} to {target} because {message}")

    
    