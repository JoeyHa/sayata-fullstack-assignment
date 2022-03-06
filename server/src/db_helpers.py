"""
This file contains all function for database, 
The solution uses a CSV file as a mock up data.
"""
import csv
import random  
from flask import Blueprint,current_app
from submission import Submission

blueprint = Blueprint('api', __name__, url_prefix='/api')
CSV_DATABASE_PATH=r"C:\Users\JOE\Documents\GitHub\sayata-fullstack-assignment\server\mock_data_csv.csv"



def read_data_from_file_db():
    """This function reads all submissions from file and returns it .
        :return: The submissions from mock up db(file)
        :rtype: dict
    """
    current_app.logger.info('START: read_data_from_file_db')
    data = {}
    with open(CSV_DATABASE_PATH,encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        data = list(csvReader)
    current_app.logger.info('END: read_data_from_file_db - Success!')
    return data
    
    """
    response:
    [
        {
            "annual_revenue": "82001",
            "company_name": "Whirlpool",
            "physical_address": "411 Majil Place",
            "status": "New",
            "submission_id": "32395"
        },
        {
            "annual_revenue": "35649",
            "company_name": "Intercosmos Media Group inc",
            "physical_address": "1926 Ehnub Loop",
            "status": "New",
            "submission_id": "92566"
        },
        {
            "annual_revenue": "96806",
            "company_name": "Public Service Enterprise Group",
            "physical_address": "941 Cunuz Place",
            "status": "Bound",
            "submission_id": "27214"
        },
        {
            "annual_revenue": "67404",
            "company_name": "PacifiCare Health Systems",
            "physical_address": "649 Dutmaj Manor",
            "status": "New",
            "submission_id": "97750"
        },
        {
            "annual_revenue": "88828",
            "company_name": "Emarkmonitor Inc. Dba markmonitor",
            "physical_address": "1237 Kezuj Center",
            "status": "Bound",
            "submission_id": "88943"
        }
    ]
    """

def write_sumbission_to_file_db(sumission_object):
    current_app.logger.info('START: write_sumbission_to_file_db for submission ID: {}'.format(sumission_object.submission_id))
    with open(CSV_DATABASE_PATH,'a', newline='') as f:
        writer = csv.writer(f)
        row = [sumission_object.submission_id,sumission_object.company_name,
                        sumission_object.physical_address,sumission_object.annual_revenue,
                        sumission_object.status]
        writer.writerow(row)
        current_app.logger.info('Insert to DB - Success!')
    return sumission_object.submission_id


def convert_json_to_submission(data):
    current_app.logger.info('START: convert_json_to_submission for: {}'.format(data))
    try:
        #data = json.loads(json_obj)
        submission_id = random.randint(10000, 99999)
        submission_id_uniqe = prevent_not_unique_id(submission_id,get_all_ids_from_db())
        submission = Submission(submission_id=submission_id_uniqe,company_name=data['companyName'],
                                physical_address=data['address'],annual_revenue=data['annualRevenue'],
                                status='New')
        return submission
    except TypeError as e:
        current_app.logger.error(e)

def prevent_not_unique_id(submission_id,id_list):
    """
    prvent even the very small chance to generate the same id for the mock up file db
    """
    current_app.logger.info('START: prevent_not_unique_id')
    if submission_id in id_list:
        submission_id = random.randint(10000, 99999)
        prevent_not_unique_id(submission_id,id_list)
    else:
        return submission_id

def get_all_ids_from_db():
    current_app.logger.info('START: get_all_ids_from_db')
    id_list = []
    with open(CSV_DATABASE_PATH, 'r',encoding='utf-8') as csvf:
        file = csv.DictReader(csvf)
        for col in file:
            id_list.append(col['submission_id'])
    return id_list



