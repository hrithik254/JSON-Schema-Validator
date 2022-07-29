from typechecker import *

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