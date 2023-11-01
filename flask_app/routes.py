import datetime
import pprint
from flask_app import app, db
from flask import render_template, request, jsonify, redirect, url_for
from bson import ObjectId


@app.route("/")
def index():
    pipeline = [
        {
            "$group": {
                "_id": "$name",  # Group by name
                "average_value": {"$avg": "$reviewsRating"},
                "hotel_info": {
                    "$first": {
                        "city": "$city",
                        "address": "$address",
                        "province": "$province",
                        "postalCode": "$postalCode",
                    }
                },
            },
        },
        {
            "$sort": {"average_value": -1},  # descending
        },
    ]

    aggregated_data = db.review.aggregate(pipeline)

    return render_template("index.html", hotels=aggregated_data)


@app.route("/reviews/<string:hotel_name>")
def show_reviews(hotel_name):
    reviews = db.review.find({"name": hotel_name}).sort("reviewsDate", -1)
    return render_template("reviews.html", reviews=reviews)


@app.route("/search")
def search():
    search_attr = request.args.get("search_attr")
    sort_order = int(request.args.get("sort_order"))
    query = request.args.get("query")  # La query di ricerca inviata dalla search bar

    pipeline = [
        {
            "$match": {
                search_attr: {
                    "$regex": query,  # L'operatore $regex cerca la lettera nel campo specificato
                    "$options": "i",  # 'i' indica una corrispondenza insensibile alle maiuscole/minuscole
                }
            }
        },
        {
            "$group": {
                "_id": "$name",
                "average_value": {"$avg": "$reviewsRating"},
                "hotel_info": {
                    "$first": {
                        "city": "$city",
                        "address": "$address",
                        "province": "$province",
                        "postalCode": "$postalCode",
                    }
                },
            },
        },
        {
            "$sort": {"average_value": sort_order},
        },
    ]

    risultati = list(db.review.aggregate(pipeline))
    return jsonify(risultati)


@app.route("/add/<string:hotel_name>", methods=["POST", "GET"])
def add_review(hotel_name):
    review = db.review.find_one({"name": hotel_name})
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        rating = int(request.form["rating"])
        # Ottieni la data corrente
        current_date = datetime.datetime.now()
        # Formatta la data nel formato "anno-mese-giorno"
        formatted_date = current_date.strftime("%Y-%m-%d")

        db.review.insert_one(
            {
                "name": review["name"],
                "city": review["city"],
                "address": review["address"],
                "postalCode": review["postalCode"],
                "province": review["province"],
                "reviewsTitle": title,
                "reviewsText": text,
                "reviewsRating": rating,
                "reviewsUsername": "user_test",
                "reviewsDate": formatted_date,
            }
        )

        return redirect(url_for("index"))

    return render_template("add_review.html", review=review)


@app.route("/myreviews")
def my_reviews():
    reviews = db.review.find({"reviewsUsername": "user_test"}).sort("reviewsDate", -1)
    return render_template("myreviews.html", reviews=reviews)


@app.route("/delete/<string:hotel_id>")
def delete_review(hotel_id):
    hotel_id = ObjectId(hotel_id)
    db.review.delete_one({"_id": hotel_id})
    return redirect(url_for("my_reviews"))


@app.route("/update/<string:hotel_id>", methods=["POST", "GET"])
def update_review(hotel_id):
    if request.method == "GET":
        hotel_id = ObjectId(hotel_id)
        review = db.review.find_one({"_id": hotel_id})
        return render_template("update_review.html", review=review)
    else:
        title = request.form["title"]
        text = request.form["text"]
        rating = int(request.form["rating"])
        # Ottieni la data corrente
        current_date = datetime.datetime.now()
        # Formatta la data nel formato "anno-mese-giorno"
        formatted_date = current_date.strftime("%Y-%m-%d")
        hotel_id = ObjectId(hotel_id)
        review = db.review.update_one(
            {"_id": hotel_id},
            {
                "$set": {
                    "reviewsTitle": title,
                    "reviewsText": text,
                    "reviewsRating": rating,
                    "reviewsDate": formatted_date,
                }
            },
        )
        return redirect(url_for("my_reviews"))
