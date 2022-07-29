def typecheck(object_property_keyword : dict,
              json_literal : dict
             ) -> bool:
    """
    Checks if json value is of the type described in schema
    param : object_property_keyword : keyword in properties of schema object
    type : dict
    param json_literal : json value corresponsding to keyword decscribed in schema object properties
    type : any type valid in python
    """
    j_type = type(json_literal)
#     print("type of value in json = ",j_type) # for debugging 
#     print("type as described in schema ",object_property_keyword["type"]) #for debugging
    try:
        schema_type = object_property_keyword["type"]
        if(schema_type == "number"):
            if(j_type is int or j_type is float): 
#                 print("Numerical type found in json")  #for debugging
                return True
            else:
                return False
        elif(schema_type == "string"):
#             print("type in schema is :",schema_type) #for debugging
            if(j_type == str):
#                 print("String type found in json")   #for debugging
                return True
            else:
                return False
        elif(schema_type == "array"):
            if(j_type == list):
#                 print("Array type found in json") #for debugging
                return True
            else:
                return False
        elif(schema_type == "boolean"):
            if(j_type == bool):
#                 print("Bool type found in json") #for debugging
                return True
            else:
                return False
        elif(schema_type == "null"):
            if(j_type == None):
#                 print("None type found in json") #for debugging
                return True
            else:
                return False
        elif(schema_type == "object"):
            if(j_type == dict):
#                 print("Object type found in json") #for debugging
                return True
            else:
                return False
    except KeyError as e:
#         print("Key Error Occured in type check fuction, checking for enum, exception = ",e) #for debugging
        try:
            enum = object_property_keyword["enum"]
            if(json_literal in enum):
#                 print("enum found in json") #for debugging
                return True
        except KeyError as e:
#             print("Key Error has occured in typecheck function in enum, exception = ",e) #for debugging
            return False



def object_validator(json_object : dict,
                     schema_object : dict
                    ) -> bool:
    """
    Validates json object (dict in python) against its 
    description of schema object
    
    param : json_object: dictionary in json 
    type : dict
    param : schema_object : object(dictionary in python terminology) 
                            in schema, describing json_object content
                            type
    type: dict
    
    """
#     if(schema_object["type"] == "object"):
    if("oneof" in schema_object):
        count = 0
        for schemas in schema_object["oneof"]:
            if(object_validator(json_object, schemas)):
                count += 1
        if(count!= 1):
            return False
        else:
            return True
    elif("anyof" in schema_object):
        for schemas in schema_object["anyof"]:
            if(object_validator(json_object, schemas)):
                return True
            else:
                return False
    try:
        for keyword in schema_object["required"]:
#             print("schema_object['required']= ",keyword) #for debugging
            try: 
                json_object[keyword]
                if(schema_object["properties"][keyword]["type"] == "object"):
                    object_validator(json_object[keyword],schema_object["properties"][keyword])
                if(typecheck(schema_object["properties"][keyword], json_object[keyword])):
                    continue
            except KeyError as e:
#                 print("exception has occured in jsonchecker json has no keyword '{keyword}' ", "exception = ",e) #for debugging
                return False

            try:
                schema_object[keyword]["enum"]
                if(typecheck(schema_object["properties"][keyword],json_object[keyword])):
                    continue
                else:
                    return False
            except KeyError as e:
#                 print("Exception occured, {schema_object[keyword]} has no key as 'enum', excep is ",e)  #for debugging
                return False

    except KeyError as e:
#         print("Exception occured in jsonchecker, 'required' keyword not in schema_object exception is ",e)  #for debugging
        for keyword in schema_object["properties"]:
#             print("schema_object['properties']= ",keyword)  #for debugging
            try: 
                json_object[keyword]
#                 print("json_object[keyword] = ",json_object[keyword])  #for debugging
                if(schema_object["properties"][keyword]["type"] == "object"):
#                     print("nested object detected, entering recursive loop")   #for debugging
                    object_validator(json_object[keyword],schema_object[keyword])
                if(typecheck(schema_object["properties"][keyword], json_object[keyword])):
                    continue
                else:
                    return False
            except KeyError as e:
#                 print("KeyError Occured, ",keyword)  #for debugging
                return False
            if("enum" in schema_object[keyword]):
                if(typecheck(schema_object["properties"][keyword],json_object[keyword])):
                    continue
                else:
                    return False

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