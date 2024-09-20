print("ciao mondo")
from jsonschema import validate

# A sample schema, like what we'd get from json.load()
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

# If no exception is raised by validate(), the instance is valid.
assert validate_wrapper(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == False

'''validate(
    instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema,
)'''    

def validate_wrapper(instance, schema):
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        reutrn False

