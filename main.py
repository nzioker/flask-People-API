from flask import Flask, jsonify, redirect, url_for
from createcontact import create_new_contact
from deletecontact import delete_contacts_with_resourceName
from updatecontact import update_contact_information
from flask import request

from firebaseConfig import config
import pyrebase


firebase = pyrebase.initialize_app(config)
auth = firebase.auth() 

app = Flask(__name__)

@app.route('/create_contact', methods=['POST'])
def create_contact():
    user_data = request.get_json()
    first_name = user_data["first_name"]
    phone= user_data["phone"]
    job_title = user_data["job_title"]
    company = user_data["company"]
    email = user_data["email"]
    city = user_data["city"]
    primaryNumberCC = user_data["countryCode"]
 
    create_new_contact(first_name, phone, job_title, company, email, city, primaryNumberCC) 
    return "User has been creatd succesfully" 


@app.route('/delete_contact')
def delete_user_contact():
    delete_contacts_with_resourceName(2)
    return "Deleted"

@app.route('/update_contact', methods=['POST'])
def update_user_contact():
    user_data = request.get_json()
    current_name = user_data['current_name']
    new_name = user_data['new_name']
    phone_number = user_data['phone_number']
    update_contact_information(current_name, new_name, phone_number)
    return "Updated"


if __name__ == '__main__':
    app.run()
            