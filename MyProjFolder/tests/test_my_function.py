import pytest
from datetime import datetime
from unittest.mock import MagicMock
import json
from jsonschema import validate
from function_app import MyHttpTrigger, calculate_age  # Assicura che `function_app` sia nel PYTHONPATH
import sys
import os

# Aggiungi il percorso al PYTHONPATH se necessario
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test per il calcolo dell'età
def test_calculate_age():
    # Input di esempio
    birth_date = "2000-01-01"  # Compleanno: 1 gennaio 2000

    # Esegui la funzione
    result = calculate_age(birth_date)

    # Data di oggi
    today = datetime.now()

    # Verifica degli anni
    assert result['age_years'] == today.year - 2000
    assert result['birth_date'] == "01-01-2000"

    # Altri controlli
    assert result['total_days'] > 0  # Almeno 1 giorno deve essere trascorso
    assert result['total_weeks'] == result['total_days'] // 7


# Test per l'endpoint HTTP con POST
def test_my_http_trigger_post():
    # Mock della richiesta HTTP
    req = MagicMock()
    req.method = "POST"
    req.get_json = MagicMock(return_value={
        "name": "Mario",
        "birthdate": "1990-05-15"
    })

    # Esegui la funzione
    response = MyHttpTrigger(req)

    # Controlla il risultato
    assert response is not None, "La funzione ha restituito None"
    assert response.status_code == 200
    body = response.get_body().decode()
    assert "Mario" in body
    assert "1990" in body
    assert "Hai esattamente" in body


# Test per l'endpoint HTTP con GET
def test_my_http_trigger_get():
    # Mock della richiesta HTTP GET
    req = MagicMock()
    req.method = "GET"

    # Esegui la funzione
    response = MyHttpTrigger(req)

    # Controlla il risultato
    assert response is not None, "La funzione ha restituito None"
    assert response.status_code == 200
    assert "Benvenuto nel Calcolatore di Età!" in response.get_body().decode()


# Test per validare la risposta con JSON Schema
def test_response_schema():
    # Carica lo schema JSON dal file
    with open("tests/snapshots/response_schema.json", "r") as schema_file:
        schema = json.load(schema_file)

    # Mock della richiesta HTTP POST con dati di esempio
    req = MagicMock()
    req.method = "POST"
    req.get_json = MagicMock(return_value={
        "name": "Luca",
        "birthdate": "1995-06-10"
    })

    # Ottieni la risposta
    response = MyHttpTrigger(req)

    # Verifica lo status code
    assert response is not None, "La funzione ha restituito None"
    assert response.status_code == 200

    # Converte la risposta in un dizionario Python
    response_data = json.loads(response.get_body().decode())

    # Valida la risposta contro il JSON Schema
    validate(instance=response_data, schema=schema)


# Test per il confronto della risposta con uno snapshot
def test_snapshot(snapshot):
    # Mock della richiesta HTTP POST
    req = MagicMock()
    req.method = "POST"
    req.get_json = MagicMock(return_value={
        "name": "Giulia",
        "birthdate": "1988-03-25"
    })

    # Ottieni la risposta
    response = MyHttpTrigger(req)

    # Verifica che la funzione non restituisca None
    assert response is not None, "La funzione ha restituito None"
    assert response.status_code == 200, "Il codice di stato non è 200"

    # Aggiungi il contenuto della risposta al confronto con lo snapshot
    snapshot.assert_match(response.get_body().decode())
