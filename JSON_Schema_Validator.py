
from object_validator import *


def validate_schema(json_data : dict,
                    schema : dict,
                    schema_integrity_file = {}
                   ) -> bool:
    """
    param : json_data: json file which needs validation
    typ : dict
    param : schema: schema for verification of json
    type dict
    param : schema_integrity_file: for checking 
            integrity of schema file
    type : dict
    """
    if("object" not in schema["type"]):
        return typecheck(schema, json_data)
    else:
        return object_validator(json_data, schema)