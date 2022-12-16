from typing import List, Any

""" This module is made of utility function used to build serializers
"""

def create_instance(Class: Any, data: dict[str, str], object_name: str) -> Any:
    """create a single instance of a Class from an object, using a serializers's validated_data"""
    object_data = data.pop(object_name)
    created_object, created = Class.objects.get_or_create(**object_name)
    return created_object


def create_mutiple_instances(Class: Any, data: dict[str, str], object_name: str) -> List[Any]:
    """create multiple instances of a Class from an object, using a serializers's validated_data"""
    result = []
    object_data = data.pop(object_name)
    for o in object_data:
        created_object, created = Class.objects.get_or_create(**object_name)
        result.append(created_object)
    return result
