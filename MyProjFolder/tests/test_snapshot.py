import pytest
from azure.functions import HttpRequest
from function_app import MyHttpTrigger
import sys
import os
import json  


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test per il confronto della risposta con uno snapshot
def test_snapshot(snapshot):
    # Crea una richiesta HTTP di esempio con dati validi
    req = HttpRequest(
        method="POST",
        url="/api/MyHttpTrigger",
        headers={},
        params={},
        route_params={},
        body=json.dumps({
            "name": "Mario",
            "birthdate": "1990-05-15"
        }).encode('utf-8')  # Converte il corpo in bytes per HttpRequest
    )

    # Esegui la funzione
    response = MyHttpTrigger(req)

    # Verifica lo stato della risposta
    assert response.status_code == 200  # Verifica che il codice di stato sia 200

    # Aggiungi la risposta decodificata allo snapshot per il confronto
    snapshot.assert_match(response.get_body().decode())
