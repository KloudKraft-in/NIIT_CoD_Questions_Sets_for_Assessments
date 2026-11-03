import copy

class MergeConflictError(Exception):
    def __init__(self, message):
        # TODO: Initialize with message
        pass

class ConfigMerger:
    def __init__(self, initial_data: dict):
        # TODO: Store a deep copy of initial_data in self.base_config
        pass

    def recursive_merge(self, current: dict, update: dict) -> dict:
        # TODO: Iterate through update.items()
        # Case 1: Key exists and both are dicts -> calls recursive_merge
        # Case 2: One is dict, other is not -> raise MergeConflictError
        # Case 3: Otherwise, update current[key] with value
        # Return current
        pass

    def apply_update(self, update_data: dict) -> str:
        # TODO: Call recursive_merge and return "Update Applied Successfully"
        # TODO: Catch MergeConflictError and return its message string
        pass

    def get_config(self) -> dict:
        # TODO: Return a shallow copy of the base_config
        pass
