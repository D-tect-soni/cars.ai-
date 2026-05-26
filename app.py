from flask import Flask, render_template, request, jsonify
import sqlite3
import requests
import os
app = Flask(__name__)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    'cars.db',
    check_same_thread=False
)

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS cars (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    brand TEXT,
    model TEXT,
    variant TEXT,

    price INTEGER,

    mileage INTEGER,

    fuel TEXT,

    transmission TEXT,

    safety TEXT,

    body_type TEXT,

    adas TEXT

)

""")

conn.commit()

# =====================================================
# INSERT SAMPLE DATA
# =====================================================

cursor.execute("SELECT COUNT(*) FROM cars")

count = cursor.fetchone()[0]

if count == 0:

    cars = [

        (
            'Tata',
            'Punch',
            'Adventure AMT',
            790000,
            20,
            'Petrol',
            'AMT',
            '5-Star',
            'SUV',
            'No'
        ),

        (
            'Hyundai',
            'Exter',
            'SX AMT',
            800000,
            19,
            'Petrol',
            'AMT',
            '4-Star',
            'SUV',
            'No'
        ),

        (
            'Maruti',
            'Celerio',
            'VXI AMT',
            650000,
            26,
            'Petrol',
            'AMT',
            '3-Star',
            'Hatchback',
            'No'
        ),

        (
            'Tata',
            'Nexon',
            'Creative Plus',
            1400000,
            24,
            'Diesel',
            'Manual',
            '5-Star',
            'SUV',
            'Yes'
        ),

        (
            'Mahindra',
            'XUV700',
            'AX7',
            2200000,
            17,
            'Petrol',
            'Automatic',
            '5-Star',
            'SUV',
            'Yes'
        ),

        (
            'Hyundai',
            'Creta',
            'SX(O)',
            1800000,
            19,
            'Petrol',
            'CVT',
            '5-Star',
            'SUV',
            'Yes'
        ),

        (
            'Kia',
            'Seltos',
            'GTX+',
            1900000,
            18,
            'Petrol',
            'DCT',
            '5-Star',
            'SUV',
            'Yes'
        ),

        (
            'Toyota',
            'Innova Hycross',
            'ZX',
            3000000,
            23,
            'Hybrid',
            'Automatic',
            '5-Star',
            'MPV',
            'Yes'
        ),

        (
            'Honda',
            'City',
            'ZX CVT',
            1600000,
            18,
            'Petrol',
            'CVT',
            '5-Star',
            'Sedan',
            'No'
        ),

        (
            'Skoda',
            'Slavia',
            'Style DSG',
            1700000,
            19,
            'Petrol',
            'DCT',
            '5-Star',
            'Sedan',
            'No'
        ),

        (
            'Volkswagen',
            'Virtus',
            'GT Plus',
            1800000,
            18,
            'Petrol',
            'DCT',
            '5-Star',
            'Sedan',
            'No'
        ),

        (
            'MG',
            'ZS EV',
            'Exclusive',
            2500000,
            30,
            'Electric',
            'Automatic',
            '5-Star',
            'SUV',
            'Yes'
        ),

        (
            'Tata',
            'Harrier',
            'Fearless',
            2600000,
            16,
            'Diesel',
            'Automatic',
            '5-Star',
            'SUV',
            'Yes'
        ),

        (
            'Mahindra',
            'Scorpio N',
            'Z8',
            2100000,
            15,
            'Diesel',
            'Automatic',
            '5-Star',
            'SUV',
            'No'
        ),

        (
            'Maruti',
            'Fronx',
            'Alpha Turbo',
            1200000,
            22,
            'Petrol',
            'AMT',
            '4-Star',
            'SUV',
            'No'
        )

    ]

    cursor.executemany("""

    INSERT INTO cars (

        brand,
        model,
        variant,
        price,
        mileage,
        fuel,
        transmission,
        safety,
        body_type,
        adas

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, cars)

    conn.commit()

# =====================================================
# HOME PAGE
# =====================================================

@app.route('/')
def home():

    return render_template('index.html')

# =====================================================
# OLLAMA AI CHATBOT
# =====================================================

# Replace the Ollama request block with:
groq_response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gemma2-9b-it",
        "messages": [{"role": "user", "content": prompt}]
    },
    timeout=30
)
data = groq_response.json()
ai_reply = data["choices"][0]["message"]["content"])

        # =====================================
        # GET CARS
        # =====================================

        cursor.execute("SELECT * FROM cars")

        cars = cursor.fetchall()

        car_data = ""

        for car in cars:

            car_data += f"""

Brand: {car['brand']}
Model: {car['model']}
Price: ₹{car['price']}
Fuel: {car['fuel']}
Transmission: {car['transmission']}
Safety: {car['safety']}

"""

        # =====================================
        # PROMPT
        # =====================================

        prompt = f"""
You are an AI car consultant.

Recommend cars from this database:

{car_data}

User Question:
{user_message}
"""

        # =====================================
        # OLLAMA REQUEST
        # =====================================

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "gemma3",

                "prompt": prompt,

                "stream": False

            },

            timeout=120

        )

        print("STATUS:", response.status_code)

        print("RAW:", response.text)

        data = response.json()

        ai_reply = data.get(
            "response",
            "No response"
        )

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "reply": f"❌ ERROR: {str(e)}"
        })

# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':

    app.run(debug=True)
