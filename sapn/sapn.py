from Place import Place
from Transition import Transition
from Arc import Arc
import xml.etree.ElementTree as ET

class StructuralAdaptivePN:
    def __init__(self):
        self.places = {}
        self.transitions = {}

    def add_place(self, place_id, tokens=0):
        if place_id not in self.places:
            self.places[place_id] = Place(place_id, tokens)

    def add_transition(self, transition_id, input_place_ids=None, output_place_ids=None):
        input_places = [self.places[pid] for pid in input_place_ids] if input_place_ids else []
        output_places = [self.places[pid] for pid in output_place_ids] if output_place_ids else []
        self.transitions[transition_id] = Transition(transition_id, input_places, output_places)

    def modify_place(self, place_id, tokens=None):
        if place_id in self.places:
            if tokens is not None:
                self.places[place_id].tokens = tokens
        else:
            raise ValueError("Place does not exist")

    def remove_place(self, place_id):
        if place_id in self.places:
            del self.places[place_id]
            # Additional logic to remove or update affected transitions may be required
        else:
            raise ValueError("Place does not exist")

    # Additional methods for adding, removing, and modifying transitions and arcs
    
    def import_from_pnml(self, pnml_file_path):
        tree = ET.parse(pnml_file_path)
        root = tree.getroot()
        
        # Assuming a simple PNML structure. Adjust as necessary.
        for place in root.findall(".//place"):
            place_id = place.attrib.get('id')
            tokens = int(place.find(".//initialMarking/value").text) if place.find(".//initialMarking/value") is not None else 0
            self.add_place(place_id, tokens)
        
        for transition in root.findall(".//transition"):
            transition_id = transition.attrib.get('id')
            input_places = [arc.attrib.get('source') for arc in root.findall(f".//arc[@target='{transition_id}']")]
            output_places = [arc.attrib.get('target') for arc in root.findall(f".//arc[@source='{transition_id}']")]
            self.add_transition(transition_id, input_places, output_places)    

    def export_to_pnml(self, pnml_file_path):
        net = ET.Element("pnml")
        net.attrib = {"type": "http://www.pnml.org/version-2009/grammar/pnmlcoremodel"}
        page = ET.SubElement(net, "page", id="page0")

        for place_id, place in self.places.items():
            place_element = ET.SubElement(page, "place", id=place_id)
            tokens_element = ET.SubElement(place_element, "initialMarking")
            value_element = ET.SubElement(tokens_element, "value")
            value_element.text = str(place.tokens)

        for transition_id, transition in self.transitions.items():
            transition_element = ET.SubElement(page, "transition", id=transition_id)
            for input_place in transition.input_places:
                ET.SubElement(page, "arc", id=f"a{input_place.identifier}to{transition_id}", source=input_place.identifier, target=transition_id)
            for output_place in transition.output_places:
                ET.SubElement(page, "arc", id=f"a{transition_id}to{output_place.identifier}", source=transition_id, target=output_place.identifier)

        tree = ET.ElementTree(net)
        tree.write(pnml_file_path, encoding='utf-8', xml_declaration=True)

    def __repr__(self):
        return f"StructuralAdaptivePetriNet(Places: {list(self.places.keys())}, Transitions: {list(self.transitions.keys())})"