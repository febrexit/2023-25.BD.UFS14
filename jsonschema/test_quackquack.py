print("ciao mondo")
from jsonschema import validate
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}
# content of text tample.py
def func(x):
    return x +1

def test_answer():
    assert func(3) == 4

def test_jsonschema_invalid():
    # If no exception is raised by validate(), the instance is valid.
    assert validate_wrapper(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == True

def validate_wrapper(instance, schema):
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        return False
