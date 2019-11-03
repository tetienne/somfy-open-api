from typing import Dict, Union, List, Optional


class Site:
    __slots__ = "id", "label"

    def __init__(self, json: Dict[str, str]):
        self.id = json.get("id")
        self.label = json.get("label")


class Device:
    __slots__ = "id", "name", "type", "site_id", "states", "capabilities", "categories"

    def __init__(
        self,
        *,
        id: str,
        type: str,
        site_id: str,
        categories: List[str],
        states: List[Dict[str, str]],
        capabilities: List[Dict[str, str]],
        name: Optional[str] = None,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.type = type
        self.site_id = site_id
        self.categories = categories
        self.states = [State(**s) for s in states]
        self.capabilities = [Capability(**c) for c in capabilities]


class State:
    __slots__ = "name", "value", "type"

    def __init__(self, name: str, value: Union[str, int], type: str):
        self.name = name
        self.value = value
        self.type = type


class Capability:
    __slots__ = "name", "parameters"

    def __init__(self, name: str, parameters: List[Dict[str, str]]):
        self.name = name
        self.parameters = [ParameterDescription(**p) for p in parameters]


class ParameterDescription:
    __slots__ = "name", "type"

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


class Parameter(dict):
    __slots__ = "name", "value"

    def __init__(self, name: str, value: Union[str, int]):
        self.name = name
        self.value = value
        dict.__init__(self, name=name, value=value)


class Command(dict):
    __slots__ = "name", "parameters"

    def __init__(self, name: str, parameters: Union[List[Parameter], Parameter] = None):
        if parameters is None:
            parameters = []
        if not isinstance(parameters, list):
            parameters = [parameters]
        self.name = name
        self.parameters = parameters
        dict.__init__(self, name=name, parameters=parameters)
