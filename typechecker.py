def typecheck(object_property_keyword : dict,
              json_literal : dict
             ) -> bool:
    """
    Checks if json value is of the type described in schema
    json_literal refers to the json being validated
    object_property_keyword is defined in the json schema

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