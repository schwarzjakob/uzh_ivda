from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Company
from flask import request
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

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
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)
        # If the user specified category is "All" we retrieve all companies
        if args["category"] == "All":
            cursor = companies.find()
        # In any other case, we only return the companies where
        # the category applies
        else:
            cursor = companies.find(args)
        # we return all companies as json
        return [Company(**doc).to_json() for doc in cursor]


class Companies(Resource):
    def get(self, id):
        # search for the company by ID
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        # retrieve args
        args = request.args.to_dict()

        # Set default is_predicted flag to False for all real data
        for entry in company.profit:
            entry["is_predicted"] = False

        # Check if 'algorithm' is in args to avoid KeyError
        if "algorithm" in args:
            if args["algorithm"] == "random":
                # retrieve the profit value from 2021 (hardcoded here, but it could be dynamic)
                prediction_value = int(company.profit[-1]["value"])
                # add the predicted value for 2022
                company.profit.insert(
                    0, {"year": 2022, "value": prediction_value, "is_predicted": True}
                )

            elif args["algorithm"] == "regression":
                # create model
                profit_df = pd.DataFrame(company.profit).iloc[
                    ::-1
                ]  # Create DataFrame to fit model
                model_ag = AutoReg(
                    endog=profit_df["value"],
                    lags=1,
                    trend="c",
                    seasonal=False,
                    exog=None,
                    hold_back=None,
                    period=None,
                    missing="none",
                )
                # train the model
                fit_ag = model_ag.fit()
                # predict for 2022 based on the profit data
                prediction_value = fit_ag.predict(
                    start=len(profit_df), end=len(profit_df), dynamic=False
                ).values[0]
                # add the predicted value for 2022
                company.profit.insert(
                    0, {"year": 2022, "value": prediction_value, "is_predicted": True}
                )

        # return data as json
        return company.to_json()


api.add_resource(CompaniesList, "/companies")
api.add_resource(Companies, "/companies/<int:id>")
