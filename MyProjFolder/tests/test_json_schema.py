import pytest
from jsonschema import validate
from function_app import calculate_age
import json



# Percorso dello schema
schema_path = os.path.join(os.path.dirname(__file__), "response_schema.json")

# Carica lo schema
with open(schema_path, "r") as schema_file:
    response_schema = json.load(schema_file)

# Import the JSON schema from your existing file
from tests import response_schema  # Assuming response_schema.json is in the tests directory

def test_calculate_age_schema():
    # Sample birth date
    birth_date = "2000-01-01"

    # Calculate age
    result = calculate_age(birth_date)

    # Validate against the JSON schema
    validate(result, response_schema)


with open("tests/response_schema.json") as f:
    response_schema = json.load(f)

def calculate_age(birthdate):
    from datetime import datetime
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.now()

    # Calcola gli anni, i mesi e i giorni
    age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    age_months = age_years * 12 + today.month - birth_date.month
    age_days = (today - birth_date).days
    total_weeks = age_days // 7
    next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day) if today > birth_date else birth_date

    return {
        "name": "Mario",
        "age_years": age_years,
        "age_months": age_months,
        "age_days": age_days,
        "total_days": age_days,
        "total_weeks": total_weeks,
        "next_birthday_in_days": (next_birthday - today).days,
        "birth_date": birthdate
    }
