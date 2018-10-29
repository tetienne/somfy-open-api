import json

from src.api.model import Parameter, Command


class TestCommand:

    def test_serialization(self):
        command = json.dumps(Command('position', Parameter('position', 10)))
        assert json.loads(command) == {'name': 'position', 'parameters': [{'name': 'position', 'value': 10}]}

        command = json.dumps(Command('position', [Parameter('position', 10), Parameter('speed', 'slow')]))
        assert json.loads(command) == {'name': 'position', 'parameters': [{'name': 'position', 'value': 10},
                                                                          {'name': 'speed', 'value': 'slow'}]}
        command = json.dumps(Command('close'))
        assert json.loads(command) == {'name': 'close', 'parameters': []}
