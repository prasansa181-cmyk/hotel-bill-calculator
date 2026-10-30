
from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Hotel Booking Bill Generator</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #edf2f8;
            margin: 0;
            padding: 35px 15px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 28px;
            border-radius: 15px;
            box-shadow: 0 4px 15px #0002;
        }

        h1 {
            text-align: center;
            color: #28527a;
            font-size: 36px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-top: 15px;
        }

        input, select {
            width: 100%;
            padding: 13px;
            margin-top: 7px;
            box-sizing: border-box;
            font-size: 16px;
        }

        button {
            width: 100%;
            margin-top: 23px;
            padding: 14px;
            background: #28527a;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #173c60;
        }

        .bill {
            background: #e8f5e9;
            padding: 25px;
            margin-top: 25px;
            border-radius: 12px;
        }

        .bill p {
            font-size: 18px;
            margin: 20px 0;
        }

        .total {
            font-weight: bold;
            font-size: 22px !important;
        }

        .back {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #28527a;
        }

        .error {
            color: #c62828;
        }
    </style>
</head>

<body>

<div class="container">

{% if bill %}

    <div class="bill">

        <h1>Hotel Bill</h1>

        <p><b>Customer:</b> {{ bill.name }}</p>
        <p><b>Room Type:</b> {{ bill.room }}</p>
        <p><b>Nights:</b> {{ bill.nights }}</p>
        <p><b>Guests:</b> {{ bill.guests }}</p>

        <hr>

        <p>Room Charges: ₹{{ "%.2f"|format(bill.room_charge) }}</p>

        <p>Service Charges: ₹{{ "%.2f"|format(bill.service) }}</p>

        <p>Tax Amount (5%): ₹{{ "%.2f"|format(bill.tax) }}</p>

        <p class="total">
            Total Bill: ₹{{ "%.2f"|format(bill.total) }}
        </p>

        <p>Cost per Guest: ₹{{ "%.2f"|format(bill.per_guest) }}</p>

        <p><b>Booking Category:</b> {{ bill.category }}</p>

    </div>

    <a class="back" href="/">← Generate Another Bill</a>

{% else %}

    <h1>Hotel Booking Bill Generator</h1>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    <form method="POST">

        <label>Customer Name</label>
        <input type="text" name="name" required>

        <label>Room Type</label>
        <select name="room" required>
            <option>Standard</option>
            <option>Deluxe</option>
            <option>Suite</option>
        </select>

        <label>Number of Nights</label>
        <input type="number" name="nights" min="1" required>

        <label>Number of Guests</label>
        <input type="number" name="guests" min="1" required>

        <label>Price per Night (₹)</label>
        <input type="number" name="price" min="0" step="0.01" required>

        <label>Additional Service Charges (₹)</label>
        <input type="number" name="service" min="0" step="0.01" value="0" required>

        <button type="submit">Generate Bill</button>

    </form>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            name = request.form["name"].strip()
            room = request.form["room"]

            nights = int(request.form["nights"])
            guests = int(request.form["guests"])
            price = float(request.form["price"])
            service = float(request.form["service"])

            if not name or nights <= 0 or guests <= 0:
                raise ValueError

            if price < 0 or service < 0:
                raise ValueError

            room_charge = nights * price

            tax = (room_charge + service) * 0.05

            total = room_charge + service + tax

            per_guest = total / guests

            if nights <= 2:
                category = "Short Stay"
            elif nights <= 5:
                category = "Medium Stay"
            else:
                category = "Long Stay"

            bill = {
                "name": name,
                "room": room,
                "nights": nights,
                "guests": guests,
                "room_charge": room_charge,
                "service": service,
                "tax": tax,
                "total": total,
                "per_guest": per_guest,
                "category": category
            }

            return render_template_string(html, bill=bill)

        except (ValueError, TypeError):
            return render_template_string(
                html,
                bill=None,
                error="Please enter valid booking details."
            )

    return render_template_string(html, bill=None)


if __name__ == "__main__":
    app.run()
