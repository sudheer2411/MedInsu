from flask import Flask, jsonify, request, render_template
import pymongo
import config
from src.utils import MedicalInsurance
medical_insurance_obj = MedicalInsurance()

app = Flask(__name__)

# mongo_client = pymongo.MongoClient(config.MONGO_URL)
# db = mongo_client[config.db_name]
# user_collection = db[config.user_collection_name]

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/register", methods = ["POST"])
# def register():
#     user_data = request.form
#     user_name = user_data['user_name']
#     password = user_data['password']
#     email_id = user_data['email_id']
#     contact_number = user_data['contact_number']
#     dob = user_data['dob']

#     response = user_collection.find_one({"email_id": email_id})
#     if not response:
#         user_collection.insert_one({
#             "user_name": user_name,
#             "password": password,
#             "email_id": email_id,
#             "contact_number": contact_number,
#             "dob": dob
#             })
#         return jsonify({"message":"User Registered Successfully"})
    
#     else:
#         return jsonify({"message": "User Already Exists"})

# @app.route("/login", methods = ["POST"])
# def login():
#     user_data = request.form
#     user_name = user_data['user_name']
#     password = user_data['password']
#     response = user_collection.find_one({"user_name": user_name, "password": password})
#     if response:
#         return jsonify({"message": "Login Successful"})
#     else:
#         return jsonify({"message": "Invalid Credentials"})

@app.route("/gender_options")
def gender_options():
    col_data = medical_insurance_obj.load_column_data()
    gender_values = list(col_data['gender'].keys())
    return jsonify(gender_values)

@app.route("/smoker_options")
def smoker_options():
    col_data = medical_insurance_obj.load_column_data()
    smoker_values = list(col_data['smoker'].keys())
    return jsonify(smoker_values)

@app.route("/region_options")
def region_options():
    col_data = medical_insurance_obj.load_column_data()
    region_values = [feature.replace("region_", "") for feature in col_data['colName'] if "region_" in feature]
    return jsonify(region_values)

@app.route("/predict_charges", methods = ["POST"])
def predict_charges():
    user_input_data = request.form

    prediction = medical_insurance_obj.predict_charges(user_input_data)
    return jsonify({"Predicted Charges": prediction[0]})

if __name__ == "__main__":
    app.run(host = config.FLASK_HOST, port = config.FLASK_PORT,debug = True)

