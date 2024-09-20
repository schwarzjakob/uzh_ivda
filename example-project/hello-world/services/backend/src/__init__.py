from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Company

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/companiesdatabase"
pymongo = PyMongo(app)
# Get a reference to the companies collection.
companies: Collection = pymongo.db.companies
api = Api(app)


class CompaniesList(Resource):
    def get(self):
        cursor = companies.find()
        return [Company(**doc).to_json() for doc in cursor]


class Companies(Resource):
    def get(self, id):
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        # do preprocessing, machine learning etc.
        return company.to_json()


api.add_resource(CompaniesList, "/companies")
api.add_resource(Companies, "/companies/<int:id>")
