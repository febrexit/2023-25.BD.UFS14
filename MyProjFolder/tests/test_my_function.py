import pytest
from datetime import datetime
from azure.functions import HttpRequest
from function_app import MyHttpTrigger, calculate_age  # Assicurati che il nome della funzione sia MyHttpTrigger

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
    req = HttpRequest(
        method="POST",
        url="/api/MyHttpTrigger",
        body=None,
        headers={},
        params={},
        form={
            "name": "Mario",
            "birthdate": "1990-05-15"
        },
    )

    # Esegui la funzione
    response = MyHttpTrigger(req)  # Chiamato correttamente la funzione MyHttpTrigger

    # Controlla il risultato
    assert response.status_code == 200
    assert "Mario" in response.get_body().decode()
    assert "1990" in response.get_body().decode()
    assert "Hai esattamente" in response.get_body().decode()

# Test per l'endpoint HTTP con GET
def test_my_http_trigger_get():
    # Mock della richiesta HTTP GET
    req = HttpRequest(
        method="GET",
        url="/api/MyHttpTrigger",
        body=None,
        headers={}
    )

    # Esegui la funzione
    response = MyHttpTrigger(req)  # Chiamato correttamente la funzione MyHttpTrigger

    # Controlla il risultato
    assert response.status_code == 200
    assert "Benvenuto nel Calcolatore di Età!" in response.get_body().decode()

# Test per il confronto della risposta con uno snapshot
def test_snapshot(snapshot):
    # Input di esempio (data di nascita)
    birth_date = "1990-05-15"

    # Esegui la funzione
    response = MyHttpTrigger(birth_date)  # Chiamato correttamente la funzione MyHttpTrigger

    # Aggiungi la risposta a uno snapshot per il confronto
    snapshot.assert_match(response)
