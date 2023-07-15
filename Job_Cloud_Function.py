import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import datetime

attribute_weights = {
    'primary_skills': 256,
    'years_of_experience': 128,
    'job_title': 64,
    'location': 32,
    'age': 16,
    'gender': 8,
    'secondary_skills': 4,
    'min_qualification': 2,
    'organisation_name': 1,
}

qualifications = [
    '8th Pass',
    '10th Pass',
    '12th Pass',
    'Graduation',
    "Post graduation",
]


def dict_values_to_list(dictionary):
    return list(dictionary.values())


attribute_weights_array = dict_values_to_list(attribute_weights)


def firebase():
    cred = credentials.Certificate('jansakti-andrew-firebase-adminsdk.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def retrieve_worker_data(db):
    workers_ref = db.collection('Workers')
    workers_snapshot = workers_ref.get()
    worker_data = _prepare_data(workers_snapshot)
    retrieve_worker_skills(db, worker_data)
    retrieve_worker_experience(db, worker_data)
    return worker_data


def retrieve_worker_skills(db, worker_data):
    for worker_id, worker in worker_data.items():
        skills_ref = db.collection('Workers').document(worker_id).collection('Skills')
        skills_snapshot = skills_ref.get()
        skills_data = _prepare_data(skills_snapshot)

        primary_skills = [data['skill_name'] for data in skills_data.values() if 'skill_name' in data and data.get('is_primary', False) == True]
        secondary_skills = [data['skill_name'] for data in skills_data.values() if 'skill_name' in data and data.get('is_primary', False) == False]
        experience = [data['experience'] for data in skills_data.values()]

        if primary_skills:
            worker['primary_skills'] = primary_skills[0]

        if secondary_skills:
            worker['secondary_skills'] = secondary_skills[0]

        if experience:
            worker['experience'] = experience[0]


def retrieve_worker_experience(db, worker_data):
    for worker_id, worker in worker_data.items():
        experience_ref = db.collection('Workers').document(worker_id).collection('Experience')
        experience_snapshot = experience_ref.get()
        experience_data = _prepare_data(experience_snapshot)

        total_years = 0
        company_names = []
        job_titles = []

        for experience in experience_data.values():
            start_date = experience['start_date']
            end_date = experience['end_date']
            company_name = experience['company_name']
            job_title = experience['job_title']

            start_date_obj = datetime.datetime.strptime(start_date, '%d/%m/%y')
            end_date_obj = datetime.datetime.strptime(end_date, '%d/%m/%y')

            start_year = start_date_obj.year
            end_year = end_date_obj.year

            total_years += end_year - start_year

        worker['years_of_company_experience'] = total_years
        worker['company_name'] = company_name
        worker['job_title'] = job_title


def calculate_worker_age(worker_data):
    for worker_id, worker in worker_data.items():
        dob = worker.get('dob', '')
        if dob:
            dob_datetime = datetime.datetime.strptime(dob, '%Y-%m-%d')
            age = datetime.datetime.now().year - dob_datetime.year
            worker['age'] = int(age)


def score_qualification(worker_data, job_data):
    worker_scores = {}
    job_scores = {}

    qualifications = [
        '8th Pass',
        '10th Pass',
        '12th Pass',
        'Graduation',
        "Post graduation",
    ]

    for worker_id, worker_info in worker_data.items():
        if 'highest_qualification' in worker_info:
            worker_qualification = worker_info['highest_qualification']
            for index, item in enumerate(qualifications):
                if item == worker_qualification:
                    worker_scores[worker_id] = index
                    break

    for job_id, job_info in job_data.items():
        if 'min_qualification' in job_info:
            job_qualification = job_info['min_qualification']
            for index, item in enumerate(qualifications):
                if item == job_qualification:
                    job_scores[job_id] = index
                    break

    return worker_scores, job_scores


def retrieve_organisation_data(db):
    organisations_ref = db.collection('Organisations')
    organisations_snapshot = organisations_ref.get()
    organisation_data = _prepare_data(organisations_snapshot)
    return organisation_data


def retrieve_job_data(db, organisation_data):
    job_data = {}
    for org_id, org in organisation_data.items():
        job_ref = db.collection('Organisations').document(org_id).collection('Jobs')
        job_snapshot = job_ref.get()
        jobs_data = _prepare_data(job_snapshot)
        job_data.update(jobs_data)
    return job_data


def _prepare_data(snapshot):
    data = {}
    for doc in snapshot:
        data[doc.id] = doc.to_dict()
    return data


def calculate_score(worker_id, job_id, worker_data, job_data, worker_scores, job_scores):
    score = 0
    worker = worker_data.get(worker_id)
    job = job_data.get(job_id)

    if worker and job:
        for attribute, weight in attribute_weights.items():
            if attribute in worker and attribute in job and worker[attribute] == job[attribute]:
                score += weight

            qualification_score = worker_scores.get(worker_id, 0)
            min_qualification = job_scores.get(job_id, 0)
            if qualification_score >= min_qualification:
                score += attribute_weights['min_qualification']

            if 'min_age' in job and 'max_age' in job and 'age' in worker and job['min_age'] <= worker['age'] <= job['max_age']:
                score += attribute_weights['age']

            if worker['gender'] == job['gender'] or job['gender'] == 'Gender Neutral':
                score += attribute_weights['gender']

            if 'primary_skills' in worker and 'secondary_skills' in job:
                if worker['primary_skills'] in job['secondary_skills']:
                    score += attribute_weights['secondary_skills']
            elif 'secondary_skills' in worker and 'secondary_skills' in job:
                if worker['secondary_skills'] in job['secondary_skills']:
                    score += attribute_weights['secondary_skills']

            if 'area' in worker and 'area' in job:
                if worker['area'] == job['area'] and worker['district'] == job['district'] and worker['state'] == job['state']:
                    score += attribute_weights['location']
                elif worker['area'] != job['area'] and worker['district'] == job['district'] and worker['state'] == job['state']:
                    score += attribute_weights['location']
                elif worker['area'] != job['area'] and worker['district'] != job['district'] and worker['state'] == job['state']:
                    score += attribute_weights['location']

            if 'experience' in worker and 'years_of_experience' in job and worker['experience'] >= job['years_of_experience']:
                score += attribute_weights['years_of_experience']

            if 'company_name' in worker and 'organisation_name' in job and worker['company_name'] == job['organisation_name']:
                score += attribute_weights['organisation_name']

            if 'job_title' in worker and 'job_title' in job and worker['job_title'] == job['job_title']:
                score += attribute_weights['job_title']

        return score


def matching_algorithm(worker_data, job_data, attribute_weights_array, attribute_weights):
    workers = list(worker_data.keys())
    num_workers = len(workers)
    job_scores = {}
    worker_scores = {}
    worker_list = []
    job_list = []
    job_recommendations = {}

    jobs = list(job_data.keys())
    num_jobs = len(jobs)

    for worker_id in workers:
        worker = worker_data[worker_id]
        jobs = list(job_data.keys())
        num_jobs = len(jobs)

        job_matrix = np.zeros((num_jobs, len(attribute_weights_array)))

        for i in range(num_jobs):
            job_id = jobs[i]
            job = job_data[job_id]
            for j, attribute in enumerate(attribute_weights.keys()):
                if attribute == 'primary_skills':
                    if attribute in worker and attribute in job and job[attribute] in worker[attribute]:
                        job_matrix[i, j] = 1
                elif attribute == 'min_qualification':
                    qualification_score = worker_scores.get(worker_id, 0)
                    min_qualification = job_scores.get(job_id, 0)
                    if qualification_score >= min_qualification:
                        job_matrix[i, j] = 1
                elif attribute == 'age':
                    if 'min_age' in job and 'max_age' in job and 'age' in worker and job['min_age'] <= worker['age'] <= job['max_age']:
                        job_matrix[i, j] = 1
                elif attribute == 'gender':
                    if 'gender' in worker and 'gender' in job and (worker['gender'] == job['gender'] or job['gender'] == 'Gender Neutral'):
                        job_matrix[i, j] = 1
                elif attribute == 'secondary_skills':
                    if 'primary_skills' in worker and 'secondary_skills' in job:
                        if worker['primary_skills'] in job['secondary_skills']:
                            job_matrix[i, j] = 0.75
                    elif 'secondary_skills' in worker and 'secondary_skills' in job:
                        if worker['secondary_skills'] in job['secondary_skills']:
                            job_matrix[i, j] = 0.5
                elif attribute == 'location':
                    if 'area' in worker and 'area' in job:
                        if worker['area'] == job['area'] and worker['district'] == job['district'] and worker['state'] == job['state']:
                            job_matrix[i, j] = 1
                        elif worker['area'] != job['area'] and worker['district'] == job['district'] and worker['state'] == job['state']:
                            job_matrix[i, j] = 0.75
                        elif worker['area'] != job['area'] and worker['district'] != job['district'] and worker['state'] == job['state']:
                            job_matrix[i, j] = 0.5
                elif attribute == 'years_of_experience':
                    if 'experience' in worker and 'years_of_experience' in job:
                        if worker['experience'] >= job['years_of_experience']:
                            job_matrix[i, j] = 1
                elif attribute == 'organisation_name':
                    if 'company_name' in worker and 'organisation_name' in job:
                        if worker['company_name'] == job['organisation_name']:
                            job_matrix[i, j] = 1
                elif attribute == 'job_title':
                    if 'job_title' in worker and 'job_title' in job:
                        if worker['job_title'] == job['job_title']:
                            job_matrix[i, j] = 1
                else:
                    if attribute in worker and attribute in job and worker[attribute] == job[attribute]:
                        job_matrix[i, j] = 1

        job_weighted_matrix = job_matrix * attribute_weights_array
        job_score_vector = np.sum(job_weighted_matrix, axis=1)

        # Pair each worker with their score
        job_scores.update(dict(zip(jobs, job_score_vector)))

        # Sort the workers' indices based on their scores in descending order
        job_sorted_indices = np.argsort(job_score_vector)[::-1]
        sorted_jobs = [jobs[idx] for idx in job_sorted_indices]
        job_sorted_scores = job_score_vector[job_sorted_indices]

        job_recommendations[worker_id] = sorted_jobs  # Store job-score pairs

    return job_recommendations


def main():
    db = firebase()
    worker_data = retrieve_worker_data(db)
    calculate_worker_age(worker_data)
    organisation_data = retrieve_organisation_data(db)
    job_data = retrieve_job_data(db, organisation_data)

    matching_algorithm(worker_data, job_data, attribute_weights_array, attribute_weights)
    
main()