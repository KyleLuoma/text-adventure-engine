# from .scene import Scene

class Path:

    requirement_types = ['visible', 'passable']

    def __init__(
            self, 
            direction_strict: str,
            goes_to: str,
            direction_description: str,
            description: str,
            scene_fixtures = None,
            requirements = None
            ):
        self.direction_strict = direction_strict
        self.goes_to = goes_to
        self.direction_description = direction_description
        self.description = description
        self.requirements = requirements
        self.scene_fixtures = self.make_fixture_lookup_dict(scene_fixtures)
        self.states = self.determine_states()

    def refresh_states(self) -> None:
        self.states = self.determine_states()

    def make_fixture_lookup_dict(self, fixtures) -> dict:
        fixture_dict = {}
        if fixtures == None:
            return fixture_dict
        for f in fixtures:
            fixture_dict[f['title']] = f
        return fixture_dict

    def determine_states(self) -> bool:
        req_states = {}

        if self.requirements == None:
            for req_type in Path.requirement_types:
                req_states[req_type] = True
            return req_states
        
        for req_type in Path.requirement_types:
            req_states[req_type] = True
            for requirement in self.requirements:
                if requirement['type'] == req_type:
                    req_fixture = requirement['fixture']
                    req_state = requirement['state']
                    state = self.scene_fixtures[req_fixture]['state']
                    req_states[req_type] = state == req_state

        return req_states