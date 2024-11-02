import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Funzione per calcolare l'età in base alla data di nascita
def calculate_age(birth_date: str) -> int:
    birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Trigger della funzione con route e autenticazione anonima
@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Ricezione dei parametri 'name', 'surname' e 'birthdate' dalla query o dal body della richiesta
    name = req.params.get('name')
    surname = req.params.get('surname')
    birth_date = req.params.get('birthdate')

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            surname = req_body.get('surname')
            birth_date = req_body.get('birthdate')

    # Creazione della risposta
    if name:
        response = {
            "message": f"Hello, {name} {surname}." if surname else f"Hello, {name}."
        }
        # Calcolo dell'età se è presente la data di nascita
        if birth_date:
            try:
                age = calculate_age(birth_date)
                response["age"] = age
            except ValueError:
                response["error"] = "Invalid date format. Please use YYYY-MM-DD."

        # Restituzione della risposta JSON
        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            json.dumps({
                "message": "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."
            }),
            mimetype="application/json",
            status_code=200
        )