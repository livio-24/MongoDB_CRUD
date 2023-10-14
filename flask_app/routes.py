import pprint
from flask_app import app, db
from flask import render_template, request, jsonify


@app.route("/")
def index():
    pipeline = [
        {
            "$group": {
                "_id": "$name",  # Group by this attribute
                "average_value": {
                    "$avg": "$reviewsRating"
                },  # Calculate the average of this attribute
                "hotel_info": {
                    "$first": {
                        "city": "$city",
                        "address": "$address",
                        "province": "$province",
                        "postalCode": "$postalCode",
                    }
                },
            },
        }
    ]

    aggregated_data = list(db.review.aggregate(pipeline))

    return render_template("index.html", hotels=aggregated_data)


@app.route("/reviews/<string:hotel_id>")
def show_reviews(hotel_id):
    reviews = list(db.review.find({"name": hotel_id}))
    return render_template("reviews.html", reviews=reviews)


@app.route("/search")
def search():
    search_attr = request.args.get("search_attr")
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
                "_id": "$name",  # Group by this attribute
                "average_value": {
                    "$avg": "$reviewsRating"
                },  # Calculate the average of this attribute
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
    ]

    risultati = list(db.review.aggregate(pipeline))
    # risultati = list(db.review.find({"name": {"$regex": query, "$options": "i"}}))
    return jsonify(risultati)
