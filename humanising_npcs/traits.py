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
    middle_state_3 = State('Middle State 3')
    brave = State('Brave')
    cowardly = State('Cowardly')
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
    # generous and greedy to middle state 3
    generous_to_middle_state_3 = generous.to(middle_state_3)
    greedy_to_middle_state_3 = greedy.to(middle_state_3)
    # middle state 3 to brave and cowardly
    middle_state_3_to_brave = middle_state_3.to(brave)
    middle_state_3_to_cowardly = middle_state_3.to(cowardly)
    # brave and cowardly to end
    brave_to_end = brave.to(end)
    cowardly_to_end = cowardly.to(end)
    
    
    
    
    

    # print the state machine
    def on_enter_diligent(self):
        # print("I am diligent")
        pass
    def on_enter_lazy(self):
        # print("I am lazy")
        pass
    def on_enter_gregarious(self):
        # print("I am gregarious")
        pass
    def on_enter_shy(self):
        # print("I am shy")
        pass
    def on_enter_generous(self):
        # print("I am generous")
        pass
    def on_enter_greedy(self):
        # print("I am greedy")
        pass
    def on_enter_brave(self):
        # print("I am brave")
        pass
    def on_enter_cowardly(self):
        # print("I am cowardly")
        pass
    
    # print the state machine
    def on_exit_diligent(self):
        # print("I am no longer diligent")
        pass
    def on_exit_lazy(self):
        # print("I am no longer lazy")
        pass
    def on_exit_gregarious(self):
        # print("I am no longer gregarious")
        pass
    def on_exit_shy(self):
        # print("I am no longer shy")
        pass
    def on_exit_generous(self):
        # print("I am no longer generous")
        pass
    def on_exit_greedy(self):
        # print("I am no longer greedy")
        pass
    def on_exit_brave(self):
        # print("I am no longer brave")
        pass
    def on_exit_cowardly(self):
        # print("I am no longer cowardly")
        pass
        
    def before_cycle(self, event: str, source: State, target: State, message: str = ""):
        print(f"Before cycle: {event} from {source} to {target} because {message}")
        
def main():
    sm = Traits()
    
if __name__ == "__main__":
    main()

    
    