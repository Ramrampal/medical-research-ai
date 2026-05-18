import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

CORS(app, origins="*")

# MongoDB Connection

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)

db = client["medical_research_ai"]

users_collection = db["users"]

favorites_collection = db["favorites"]

analytics_collection = db["analytics"]

print("MongoDB Connected Successfully")


# Home Route

@app.route('/')
def home():

    return jsonify({
        "message": "Medical Research AI Backend Running"
    })


# Analyze API

@app.route('/api/analyze', methods=['POST'])
def analyze_research():

    try:

        data = request.get_json()

        text = data.get("text", "")

        analysis = {

            "data_quality": {

                "accuracy": 0.88,

                "completeness": 0.85,

                "consistency": 0.90,

                "overall_quality": 0.88

            },

            "key_insights": [

                {

                    "insight": f"Research topic focuses on: {text[:50]}",

                    "confidence": 0.92,

                    "source": "AI Analysis"

                },

                {

                    "insight": "Potential breakthrough opportunities identified",

                    "confidence": 0.87,

                    "source": "Machine Learning"

                },

                {

                    "insight": "Strong publication potential detected",

                    "confidence": 0.89,

                    "source": "Research Model"

                }

            ],

            "recommendations": [

                "Focus on high-impact journals for publication",

                "Collaborate with leading research institutions",

                "Invest in multi-center trials for validation",

                "Utilize open-access platforms for maximum reach"

            ]

        }

        return jsonify({

            "analysis": analysis

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# Signup API

@app.route('/api/signup', methods=['POST'])
def signup():

    try:

        data = request.get_json()

        user = {

            "name": data.get("name"),

            "email": data.get("email"),

            "password": data.get("password")

        }

        existing_user = users_collection.find_one({
            "email": user["email"]
        })

        if existing_user:

            return jsonify({
                "error": "User already exists"
            }), 400

        users_collection.insert_one(user)

        return jsonify({
            "message": "Signup successful"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# Login API

@app.route('/api/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        email = data.get("email")

        password = data.get("password")

        user = users_collection.find_one({
            "email": email
        })

        if not user:

            return jsonify({
                "error": "User not found"
            }), 404

        if user["password"] != password:

            return jsonify({
                "error": "Invalid password"
            }), 401

        return jsonify({

            "message": "Login successful",

            "user": {

                "name": user["name"],

                "email": user["email"]

            }

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# Favorites APIs

@app.route('/api/favorites', methods=['POST'])
def save_favorite():

    try:

        data = request.get_json()

        favorites_collection.insert_one(data)

        return jsonify({
            "message": "Favorite saved"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/favorites', methods=['GET'])
def get_favorites():

    try:

        favorites = list(

            favorites_collection.find(
                {},
                {"_id": 0}
            )

        )

        return jsonify(favorites)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# Search Analytics APIs

@app.route('/api/analytics/search', methods=['POST'])
def update_search_count():

    try:

        analytics_collection.update_one(

            {"type": "searches"},

            {"$inc": {"count": 1}},

            upsert=True

        )

        return jsonify({
            "message": "Search count updated"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/analytics/search', methods=['GET'])
def get_search_count():

    try:

        data = analytics_collection.find_one({
            "type": "searches"
        })

        count = data["count"] if data else 0

        return jsonify({
            "count": count
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# Search API

@app.route('/api/search/combined', methods=['POST'])
def search_combined():

    try:

        data = request.get_json()

        query = data.get("query", "")

        sample_results = [

            {

                "display_name":
                f"Research Paper on {query}",

                "abstract":
                "This study explores important medical findings and AI-driven healthcare analysis.",

                "publication_year": 2026,

                "cited_by_count": 120

            },

            {

                "display_name":
                f"Advanced {query} Treatment Study",

                "abstract":
                "Clinical trials and modern AI approaches for medical improvement.",

                "publication_year": 2025,

                "cited_by_count": 89

            }

        ]

        return jsonify({

            "query": query,

            "results": {

                "openalex": {

                    "works": sample_results

                }

            }

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':

    port = int(
        os.getenv('PYTHON_PORT', 5001)
    )

    app.run(
        debug=False,
        host='0.0.0.0',
        port=port
    )