import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Funzione per calcolare età dettagliata
def calculate_age(birth_date: str) -> dict:
    try:
        birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    except ValueError:
        logging.error("Formato data non valido")
        raise ValueError("Formato data non valido")
    
    today = datetime.datetime.now()

    # Calcolare l'età in anni, mesi, e giorni
    age_years = today.year - birth_date.year
    age_months = today.month - birth_date.month
    age_days = today.day - birth_date.day

    # Gestire il caso di giorni e mesi negativi
    if age_days < 0:
        age_months -= 1
        age_days += (birth_date.replace(month=(birth_date.month % 12) + 1) - birth_date).days
    if age_months < 0:
        age_years -= 1
        age_months += 12

    # Calcolare l'età in settimane e giorni totali
    total_days = (today - birth_date).days
    total_weeks = total_days // 7

    # Calcolare giorni mancanti per il prossimo compleanno
    next_birthday = birth_date.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_until_birthday = (next_birthday - today).days

    # Determinare il segno zodiacale
    zodiac_sign = get_zodiac_sign(birth_date)

    return {
        "age_years": age_years,
        "age_months": age_months,
        "age_days": age_days,
        "total_days": total_days,
        "total_weeks": total_weeks,
        "next_birthday_in_days": days_until_birthday,
        "zodiac_sign": zodiac_sign,
        "birth_date": birth_date.strftime('%d-%m-%Y'),
    }

# Funzione per ottenere il segno zodiacale
def get_zodiac_sign(birth_date):
    zodiacs = [
        (120, "Capricorno"), (218, "Acquario"), (320, "Pesci"), (420, "Ariete"),
        (521, "Toro"), (621, "Gemelli"), (723, "Cancro"), (823, "Leone"),
        (923, "Vergine"), (1023, "Bilancia"), (1122, "Scorpione"), (1222, "Sagittario")
    ]
    
    birth_day_of_year = birth_date.timetuple().tm_yday
    
    for date, sign in zodiacs:
        if birth_day_of_year <= date:
            return sign
    return "Capricorno"  # Default per chi nasce il 31 dicembre

# Funzione per generare la pagina HTML
def generate_html_form():
    return """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calcolatore di Età</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                width: 300px;
                text-align: center;
            }
            h1 {
                font-size: 24px;
                color: #333;
            }
            input {
                margin: 10px 0;
                padding: 8px;
                width: 80%;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Calcolatore di Età</h1>
            <form action="/api/MyHttpTrigger" method="post">
                <input type="text" name="name" placeholder="Inserisci il tuo nome" required><br>
                <input type="date" name="birthdate" required><br>
                <button type="submit">Calcola Età</button>
            </form>
        </div>
    </body>
    </html>
    """

# Trigger della funzione
@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST"])
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == "GET":
        # Mostra il form HTML
        return func.HttpResponse(generate_html_form(), mimetype="text/html", status_code=200)

    # Gestisci il POST (quando l'utente invia il form)
    name = req.form.get('name')
    birth_date = req.form.get('birthdate')

    # Se il nome è presente
    if name:
        response = {
            "message": f"Ciao {name}!",
            "description": "Ecco alcune informazioni dettagliate sulla tua età.",
        }
        
        # Se la data di nascita è presente
        if birth_date:
            try:
                age_details = calculate_age(birth_date)
                response["age_details"] = f"Hai esattamente {age_details['age_years']} anni, {age_details['age_months']} mesi e {age_details['age_days']} giorni."
                response["total_days"] = f"Totale giorni vissuti: {age_details['total_days']} giorni."
                response["total_weeks"] = f"Totale settimane vissute: {age_details['total_weeks']} settimane."
                response["next_birthday_in_days"] = f"Il tuo prossimo compleanno è tra {age_details['next_birthday_in_days']} giorni."
                response["zodiac_sign"] = f"Il tuo segno zodiacale è {age_details['zodiac_sign']}."
                response["birth_date"] = f"La tua data di nascita è: {age_details['birth_date']}."
                response["today"] = datetime.datetime.now().strftime('%Y-%m-%d')
            except ValueError as e:
                logging.error(f"Errore nel calcolo dell'età: {e}")
                response["error"] = str(e)
        else:
            response["message"] += " Ma non hai inserito una data di nascita. Per favore, prova di nuovo!"

        # Mostra il risultato
        return func.HttpResponse(
            json.dumps(response, indent=4, ensure_ascii=False),
            mimetype="application/json",
            status_code=200
        )
    else:
        # Se il nome non è fornito, guida l'utente
        return func.HttpResponse(
            json.dumps({
                "message": "Benvenuto nel calcolatore di età!",
                "instructions": "Per calcolare la tua età, inserisci il nome e la data di nascita nel modulo qui sopra.",
            }, indent=4, ensure_ascii=False),
            mimetype="application/json",
            status_code=400
        )
