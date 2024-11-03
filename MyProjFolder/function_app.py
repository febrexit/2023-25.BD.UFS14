import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Funzione per calcolare età dettagliata
def calculate_age(birth_date: str) -> str:
    try:
        birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    except ValueError:
        logging.error("Formato data non valido")
        raise ValueError("Formato data non valido")
    
    today = datetime.datetime.now()

    age_years = today.year - birth_date.year
    age_months = today.month - birth_date.month
    age_days = today.day - birth_date.day

    if age_days < 0:
        age_months -= 1
        age_days += (birth_date.replace(month=birth_date.month % 12 + 1) - birth_date).days
    if age_months < 0:
        age_years -= 1
        age_months += 12

    return f"Hai esattamente {age_years} anni, {age_months} mesi e {age_days} giorni."

# Trigger della funzione
@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Ottieni parametri
    name = req.params.get('name')
    birth_date = req.params.get('birthdate')

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("Errore nel parsing del JSON")
            pass
        else:
            name = req_body.get('name')
            birth_date = req_body.get('birthdate')

    if name:
        response = {"message": f"Hello, {name}."}
        if birth_date:
            try:
                age_details = calculate_age(birth_date)
                response["age_details"] = age_details
                response["today"] = datetime.datetime.now().strftime('%Y-%m-%d')
            except ValueError as e:
                logging.error(f"Errore nel calcolo dell'età: {e}")
                response["error"] = str(e)

        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            json.dumps({
                "message": "Passa un nome e una data di nascita nel formato YYYY-MM-DD."
            }),
            mimetype="application/json",
            status_code=200
        )
