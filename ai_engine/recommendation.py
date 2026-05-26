import re

def recommend_cars(user_input, cars):

    user_input = user_input.lower()

    budget = None

    # =====================================
    # BUDGET
    # =====================================

    budget_match = re.search(r'(\d+)', user_input)

    if budget_match:

        budget = int(
            budget_match.group(1)
        ) * 100000

    wants_automatic = (
        "automatic" in user_input
        or "amt" in user_input
    )

    wants_petrol = "petrol" in user_input

    wants_diesel = "diesel" in user_input

    wants_suv = "suv" in user_input

    # =====================================
    # FILTERING
    # =====================================

    filtered = []

    for car in cars:

        car = dict(car)

        # BUDGET

        if budget:

            if car['price'] > budget:
                continue

        # AUTOMATIC

        if wants_automatic:

            transmission = (
                car['transmission']
                .strip()
                .lower()
            )

            if transmission not in [
                'automatic',
                'amt',
                'cvt',
                'dct'
            ]:
                continue

        # PETROL

        if wants_petrol:

            if (
                car['fuel']
                .strip()
                .lower()
                != 'petrol'
            ):
                continue

        # DIESEL

        if wants_diesel:

            if (
                car['fuel']
                .strip()
                .lower()
                != 'diesel'
            ):
                continue

        # SUV

        if wants_suv:

            if (
                car['body_type']
                .strip()
                .lower()
                != 'suv'
            ):
                continue

        # =====================================
        # AI SCORE
        # =====================================

        score = 0

        # Mileage

        if car['mileage'] >= 20:
            score += 5

        # Safety

        if "5" in car['safety']:
            score += 5

        # Automatic

        if (
            car['transmission']
            .lower()
            in ['amt', 'automatic']
        ):
            score += 3

        # ADAS

        if car['adas'] == 'Yes':
            score += 3

        car['score'] = score

        filtered.append(car)

    # =====================================
    # SORTING
    # =====================================

    filtered = sorted(

        filtered,

        key=lambda x: x['score'],

        reverse=True

    )

    # =====================================
    # NO RESULT
    # =====================================

    if not filtered:

        return {
            "reply":
            "❌ No matching cars found."
        }

    # =====================================
    # RESPONSE
    # =====================================

    result = "🚗 Top Recommended Cars\n\n"

    for car in filtered[:5]:

        result += f"""

{car['brand']} {car['model']}

🚘 Variant: {car['variant']}

💰 Price: ₹{car['price']:,}

📈 Mileage: {car['mileage']} kmpl

⛽ Fuel: {car['fuel']}

🔄 Transmission: {car['transmission']}

🛡️ Safety: {car['safety']}

🚙 Body Type: {car['body_type']}

🤖 ADAS: {car['adas']}

⭐ AI Score: {car['score']}

--------------------------------

"""

    return {
        "reply": result
    }