
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Hotel Booking Bill Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            text-align: center;
        }

        .container {
            width: 500px;
            margin: 30px auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
        }

        input, select {
            width: 90%;
            padding: 10px;
            margin: 8px;
        }

        button {
            background-color: blue;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
        }

        .bill {
            margin-top: 20px;
            padding: 15px;
            background-color: #e9f7ef;
            text-align: left;
        }
    </style>
</head>

<body>

<div class="container">

<h1>Hotel Booking Bill Generator</h1>

<form method="POST">

<input type="text" name="customer_name"
placeholder="Customer Name" required>

<select name="room_type" required>
    <option value="">Select Room Type</option>
    <option value="Standard">Standard</option>
    <option value="Deluxe">Deluxe</option>
    <option value="Suite">Suite</option>
</select>

<input type="number" name="nights"
placeholder="Number of Nights" required min="1">

<input type="number" name="guests"
placeholder="Number of Guests" required min="1">

<input type="number" name="price"
placeholder="Price per Night" required min="1">

<input type="number" name="service"
placeholder="Additional Service Charges" required min="0">

<br><br>

<button type="submit">Generate Bill</button>

</form>

{% if bill %}

<div class="bill">

<h2>Booking Bill</h2>

<p><b>Customer Name:</b> {{ bill.name }}</p>
<p><b>Room Type:</b> {{ bill.room }}</p>
<p><b>Number of Nights:</b> {{ bill.nights }}</p>
<p><b>Number of Guests:</b> {{ bill.guests }}</p>

<hr>

<p><b>Room Charges:</b> ₹{{ bill.room_charges }}</p>
<p><b>Service Charges:</b> ₹{{ bill.service }}</p>
<p><b>Tax Amount (10%):</b> ₹{{ bill.tax }}</p>
<p><b>Total Bill:</b> ₹{{ bill.total }}</p>
<p><b>Cost per Guest:</b> ₹{{ bill.cost_per_guest }}</p>
<p><b>Booking Category:</b> {{ bill.category }}</p>

</div>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    bill = None

    if request.method == "POST":

        name = request.form["customer_name"]
        room = request.form["room_type"]
        nights = int(request.form["nights"])
        guests = int(request.form["guests"])
        price = float(request.form["price"])
        service = float(request.form["service"])

        room_charges = nights * price
        subtotal = room_charges + service
        tax = subtotal * 0.10
        total = subtotal + tax
        cost_per_guest = total / guests

        if total >= 20000:
            category = "Luxury Booking"

        elif total >= 10000:
            category = "Premium Booking"

        else:
            category = "Standard Booking"

        bill = {
            "name": name,
            "room": room,
            "nights": nights,
            "guests": guests,
            "room_charges": round(room_charges, 2),
            "service": round(service, 2),
            "tax": round(tax, 2),
            "total": round(total, 2),
            "cost_per_guest": round(cost_per_guest, 2),
            "category": category
        }

    return render_template_string(HTML, bill=bill)


if __name__ == "__main__":
    app.run(debug=True)
