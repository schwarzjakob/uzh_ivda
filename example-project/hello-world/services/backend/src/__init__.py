from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Company
from .llm.groq_llm import GroqClient
from flask import request
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
import os

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

# Initialize GroqClient
groq_client = GroqClient()


class CompaniesList(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)
        # If the user specified category is "All" we retrieve all companies
        if args.get("category") == "All":
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


# New endpoint for generating a poem
@app.route("/llm/groq/poem/<int:id>", methods=["GET"])
def get_poem(id):
    # Get the company name based on id
    company_doc = companies.find_one({"id": id})
    if not company_doc:
        return jsonify({"error": "Company not found"}), 404
    company_name = company_doc["name"]

    # Path to the prompt file
    prompt_file_path = os.path.join(
        os.path.dirname(__file__), "llm", "prompts", "groq_api_poem.json"
    )

    # Generate the poem
    poem = groq_client.generate_poem(company_name, prompt_file_path)

    # Debugging: Print the generated poem
    print(f"Generated poem: {poem}")

    # Check if the poem contains the placeholder (indicating replacement failure)
    if "{company}" in poem:
        return jsonify(
            {
                "poem": f"I'd be happy to! Unfortunately, I wasn't able to find specific information about the company \"{company_name}\". Could you please provide more context or details about the company you're interested in?"
            }
        )

    return jsonify({"poem": poem})


# New endpoint for generating additional information
@app.route("/llm/groq/additional_information/<int:id>", methods=["GET"])
def get_additional_information(id):
    # Get the company details based on id
    company_doc = companies.find_one({"id": id})
    if not company_doc:
        return jsonify({"error": "Company not found"}), 404

    company_name = company_doc.get("name")
    founding_year = company_doc.get("founding_year")
    employees = company_doc.get("employees")

    # Path to the new prompt file
    prompt_file_path = os.path.join(
        os.path.dirname(__file__),
        "llm",
        "prompts",
        "groq_api_additional_information.json",
    )

    # Generate the additional information
    additional_info = groq_client.generate_additional_information(
        company_name, founding_year, employees, prompt_file_path
    )

    # Debugging: Print the generated additional information
    print(f"Generated additional information: {additional_info}")

    # Check if placeholders are still present
    if (
        "{company}" in additional_info
        or "{founding_year}" in additional_info
        or "{employees}" in additional_info
    ):
        return jsonify(
            {
                "additional_information": f"I'd be happy to! Unfortunately, I couldn't retrieve detailed information about the company \"{company_name}\". Could you please provide more specific details or check the company data?"
            }
        )

    return jsonify({"additional_information": additional_info})


@app.route("/industry_standard/<string:category>", methods=["GET"])
def get_industry_standard(category):
    # Find all companies in the same category
    cursor = companies.find({"category": category})
    all_companies = [Company(**doc) for doc in cursor]

    # Dictionary to store the cumulative profit and employee count for each year
    industry_data = {}

    # Loop through all companies in the category
    for company in all_companies:
        for profit_entry in company.profit:
            year = profit_entry["year"]
            profit_per_employee = profit_entry["value"] / company.employees

            if year not in industry_data:
                industry_data[year] = {
                    "total_profit": 0,
                    "total_employees": 0,
                    "company_count": 0,
                }

            # Accumulate the profit per employee for that year
            industry_data[year]["total_profit"] += profit_per_employee
            industry_data[year]["company_count"] += 1

    # Calculate the average profit per employee for each year
    avg_profit_per_employee = [
        {"year": year, "value": data["total_profit"] / data["company_count"]}
        for year, data in industry_data.items()
    ]

    return jsonify(avg_profit_per_employee)
