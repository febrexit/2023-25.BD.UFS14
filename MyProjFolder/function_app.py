import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Funzione per calcolare il segno zodiacale
def zodiac_sign(day: int, month: int) -> str:
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Ariete"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Toro"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemelli"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancro"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leone"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Vergine"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Bilancia"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpione"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittario"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorno"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Acquario"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pesci"
    return ""

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
    sign = zodiac_sign(birth_date.day, birth_date.month)

    # Curiosità sulla data di nascita (se il compleanno è vicino a una festività)
    holiday_closest = ""
    if birth_date.month == 12 and birth_date.day == 25:
        holiday_closest = "Il tuo compleanno è vicino al Natale!"
    elif birth_date.month == 1 and birth_date.day == 1:
        holiday_closest = "Il tuo compleanno è vicino al Capodanno!"
    
    return {
        "age_years": age_years,
        "age_months": age_months,
        "age_days": age_days,
        "total_days": total_days,
        "total_weeks": total_weeks,
        "next_birthday_in_days": days_until_birthday,
        "birth_date": birth_date.strftime('%d-%m-%Y'),
        "sign": sign,
        "holiday_closest": holiday_closest
    }

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
                background-color: #f0f8ff;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                flex-direction: column;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                text-align: center;
                max-width: 400px;
                width: 90%;
            }
            h1 {
                color: #4CAF50;
            }
            p {
                font-size: 1rem;
                color: #666;
            }
            input, button {
                margin: 10px 0;
                padding: 10px;
                width: 90%;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1rem;
            }
            button {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>Benvenuto nel Calcolatore di Età!</h1>
        <p>Scopri dettagli sulla tua età, il tuo segno zodiacale e altre curiosità su di te!</p>
        <div class="container">
            <form action="/api/MyHttpTrigger" method="post">
                <input type="text" name="name" placeholder="Inserisci il tuo nome" required><br>
                <input type="date" name="birthdate" required><br>
                <button type="submit">Calcola Età</button>
            </form>
        </div>
    </body>
    </html>
    """

# Funzione per generare la risposta HTML con i dettagli dell'età e del segno zodiacale
def generate_html_result(response_data):
    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Risultati Calcolatore di Età</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                flex-direction: column;
            }}
            .container {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                text-align: left;
                max-width: 600px;
                width: 90%;
                margin-top: 20px;
            }}
            h1 {{
                color: #4CAF50;
                font-size: 28px;
            }}
            .result {{
                margin-bottom: 15px;
                font-size: 1.1rem;
                color: #444;
            }}
            .result span {{
                font-weight: bold;
                color: #4CAF50;
            }}
        </style>
    </head>
    <body>
        <h1>Risultati del Calcolatore di Età</h1>
        <div class="container">
            <div class="result">Ciao <span>{response_data['name']}</span>!</div>
            <div class="result">Hai esattamente <span>{response_data['age_years']} anni</span>, <span>{response_data['age_months']} mesi</span> e <span>{response_data['age_days']} giorni</span>.</div>
            <div class="result">Hai vissuto <span>{response_data['total_days']} giorni</span> in totale, che equivalgono a <span>{response_data['total_weeks']} settimane</span>.</div>
            <div class="result">Il tuo prossimo compleanno è tra <span>{response_data['next_birthday_in_days']} giorni</span>.</div>
            <div class="result">La tua data di nascita è: <span>{response_data['birth_date']}</span>.</div>
            <div class="result">Il tuo segno zodiacale è: <span>{response_data['sign']}</span>.</div>
            <div class="result">{response_data['holiday_closest']}</div>
        </div>
    </body>
    </html>
    """

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST"])
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == "GET":
        return func.HttpResponse(generate_html_form(), mimetype="text/html", status_code=200)

    # Gestisci il POST (quando l'utente invia il form)
    name = req.form.get('name')
    birth_date = req.form.get('birthdate')

    if name and birth_date:
        try:
            age_details = calculate_age(birth_date)
            response = {
                'name': name,
                'age_years': age_details['age_years'],
                'age_months': age_details['age_months'],
                'age_days': age_details['age_days'],
                'total_days': age_details['total_days'],
                'total_weeks': age_details['total_weeks'],
                'next_birthday_in_days': age_details['next_birthday_in_days'],
                'birth_date': age_details['birth_date'],
                'sign': age_details['sign'],
                'holiday_closest': age_details['holiday_closest'],
            }
            return func.HttpResponse(generate_html_result(response), mimetype="text/html", status_code=200)
        except ValueError as e:
            return func.HttpResponse(f"Errore: {str(e)}", mimetype="text/html", status_code=400)
    else:
        return func.HttpResponse("Nome e data di nascita sono richiesti.", mimetype="text/html", status_code=400)
