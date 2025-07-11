from pm4py.objects.petri_net.obj import PetriNet


class Arc:
    def __init__(self, place, transition):
        self.place = place
        self.transition = transition