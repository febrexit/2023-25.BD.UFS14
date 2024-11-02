import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Funzione per calcolare l'età in base alla data di nascita
def calculate_age(birth_date: str) -> str:
    birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.datetime.now()
    
    age_years = today.year - birth_date.year
    age_months = today.month - birth_date.month
    age_days = today.day - birth_date.day

    if age_days < 0:
        age_months -= 1
        age_days += (birth_date.replace(month=birth_date.month + 1) - birth_date).day

    if age_months < 0:
        age_years -= 1
        age_months += 12

    return f"Hai esattamente {age_years} anni, {age_months} mesi e {age_days} giorni."


# Trigger della funzione con route e autenticazione anonima
@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

    if name:
        response = {
            "message": f"Hello, {name} {surname}." if surname else f"Hello, {name}."
        }
        if birth_date:
            try:
                age = calculate_age(birth_date)
                response["age"] = age
                response["today"] = datetime.datetime.now().strftime('%Y-%m-%d')
            except ValueError:
                response["error"] = "Invalid date format. Please use YYYY-MM-DD."

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
