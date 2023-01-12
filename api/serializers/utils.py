from typing import List, Any

""" This module is made of utility function used to build serializers
"""

def create_instance(ClassSerializer: Any, data: dict[str, str], object_name: str, or_get: bool = False) -> Any:
    """create a single instance of a Class from an object, using a serializers's validated_data"""
    object_data = data.pop(object_name)
    sr = ClassSerializer(data=object_data)
    if sr.is_valid():
        return sr.create(validated_data=object_data)
    else:
        return None


def create_mutiple_instances(ClassSerializer: Any, data: dict[str, str], object_name: str) -> List[Any]:
    """create multiple instances of a Class from an object, using a serializers's validated_data"""
    result = []
    object_data = data.pop(object_name)
    for o in object_data:
        created_object = create_instance(ClassSerializer, o, object_name)
        if created_object is None:
            return None
        result.append(created_object)
    return result
