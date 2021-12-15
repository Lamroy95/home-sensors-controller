from dataclasses import dataclass
from typing import Callable

from miio.airpurifier import OperationMode


@dataclass
class Method:
    name: str
    process_param: Callable


commands_methods_map = {
    "set_level": Method(
        name="set_favorite_level",
        process_param=lambda x: int(x)
    ),
    "set_auto": Method(
        name="set_mode",
        process_param=lambda x: OperationMode.Auto if x in [1, "1"] else OperationMode.Favorite
    )
}


class Command:
    def __init__(self, command_name, param):
        self.method = commands_methods_map.get(command_name)
        if not self.method:
            raise ValueError(f"Invalid command `{command_name}`")

        self.param = self.method.process_param(param)
