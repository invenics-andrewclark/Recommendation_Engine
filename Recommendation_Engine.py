import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import datetime
import random
import requests


class Recommendation_Engine:

    def __init__(self):
        self.attribute_weights = {
            'primary_skills': 15,
            'years_of_experience': 10,
            'location': 4,
            'min_qualification': 3,
            'age':2,
            'gender': 2,
            'secondary_skills': 4
        }

        self.attribute_weights_array = self.dict_values_to_list(self.attribute_weights)

        self.qualifications = [
            'Primary Education',
            'Secondary Education',
            'Higher Secondary Education',
            'Diploma/Certificate Programs',
            "Bachelor's Degree (BSc)",
        ]

    def dict_values_to_list(self, dictionary):
        return list(dictionary.values())

    def firebase(self):
        cred = credentials.Certificate('jansakti-andrew-firebase-adminsdk.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        return self.db


    def retrieve_worker_data(self):
        workers_ref = self.db.collection('Workers')
        workers_snapshot = workers_ref.get()
        self.worker_data = self._prepare_data(workers_snapshot)
        self.retrieve_worker_skills()
        #self.retrieve_worker_experience()
        return self.worker_data

    def retrieve_worker_skills(self):
        for worker_id, worker in self.worker_data.items():
            skills_ref = self.db.collection('Workers').document(worker_id).collection('Skills')
            skills_snapshot = skills_ref.get()
            skills_data = self._prepare_data(skills_snapshot)
            
            primary_skills = [data['skill_name'] for data in skills_data.values() if 'skill_name' in data and data.get('is_primary', False) == True]
            secondary_skills = [data['skill_name'] for data in skills_data.values() if 'skill_name' in data and data.get('is_primary', False) == False]
            experience = [data['experience'] for data in skills_data.values()]

            if primary_skills:
                worker['primary_skills'] = primary_skills[0]

            if secondary_skills:
                worker['secondary_skills'] = secondary_skills[0]

            if experience:
                worker['experience'] = experience[0]

    """
    def retrieve_worker_experience(self):
        for worker_id, worker in self.worker_data.items():
            experience_ref = self.db.collection('Workers').document(worker_id).collection('Experience')
            experience_snapshot = experience_ref.get()
            experience_data = self._prepare_data(experience_snapshot)

            total_years = 0
            for experience in experience_data.values():
                start_date = experience['start_date']
                end_date = experience['end_date']

                start_date_obj = datetime.datetime.strptime(start_date, '%d/%m/%y')
                end_date_obj = datetime.datetime.strptime(end_date, '%d/%m/%y')

                start_year = start_date_obj.year
                end_year = end_date_obj.year

                total_years += end_year - start_year

            worker['years_of_experience'] = total_years
            """

    def calculate_worker_age(self):
        for worker_id, worker in self.worker_data.items():
            dob = worker.get('dob', '')  
            if dob:
                dob_datetime = datetime.datetime.strptime(dob, '%Y-%m-%d')
                age = datetime.datetime.now().year - dob_datetime.year
                worker['age'] = int(age)
                

    def score_qualification(self):
        worker_scores = {}
        job_scores = {}

        for worker_id, worker_info in self.worker_data.items():
            if 'highest_qualification' in worker_info:
                worker_qualification = worker_info['highest_qualification']
                for index, item in enumerate(self.qualifications):
                    if item == worker_qualification:
                        worker_scores[worker_id] = index
                        break

        for job_id, job_info in self.job_data.items():
            if 'min_qualification' in job_info:
                job_qualification = job_info['min_qualification']
                for index, item in enumerate(self.qualifications):
                    if item == job_qualification:
                        job_scores[job_id] = index
                        break

        self.job_scores = job_scores
        self.worker_scores = worker_scores
        return worker_scores, job_scores

    def retrieve_job_data(self):
        jobs_ref = self.db.collection('Jobs')
        jobs_snapshot = jobs_ref.get()
        self.job_data = self._prepare_data(jobs_snapshot)
        return self.job_data

    @staticmethod
    def _prepare_data(snapshot):
        data = {}
        for doc in snapshot:
            data[doc.id] = doc.to_dict()
        return data

    def calculate_score(self, worker_id, job_id):
        score = 0
        worker = self.worker_data.get(worker_id)
        job = self.job_data.get(job_id)

        if worker and job:

            # Calculates score if string type attributes in jobs and worker are equal 
            for attribute, weight in self.attribute_weights.items():
                if attribute in worker and attribute in job and worker[attribute] == job[attribute]:
                    score += weight

                # Calculates score based on index position comparison of min qual and highest qual (highest qual of worker >= min job qual)
                qualification_score = self.worker_scores.get(worker_id, 0)
                min_qualification = self.job_scores.get(job_id, 0)
                if qualification_score >= min_qualification:
                    score += self.attribute_weights['min_qualification']

                # Calculates score based on worker age falling within job age requirement
                    if job['min_age'] <= worker['age'] <= job['max_age']:
                        score += self.attribute_weights['age'] 

                # Calculates score base on gender
                if worker['gender'] == job['gender'] or job['gender'] == 'Gender Neutral':
                    score += self.attribute_weights['gender']

                # Calculate score based on secondary skills
                if 'primary_skills' in worker and worker['primary_skills'] in job['secondary_skills']:
                    score += self.attribute_weights['secondary_skills']
                elif 'secondary_skills' in worker and worker['secondary_skills'] in job['secondary_skills']:
                    score += self.attribute_weights['secondary_skills']

                # Calculate score based on experience from skills subcollection
                if 'experience' in worker and 'years_of_experience' in job and worker['experience'] >= job['years_of_experience']:
                    score += self.attribute_weights['years_of_experience']


                # Calculate score for proximity of location
                for worker_id, worker in self.worker_data.items():
                    worker_pincode = worker['pincode']

                for job_id, job in self.job_data.items():
                    job_pincode = job['pincode']

                    get_worker_api = requests.get('https://api.postalpincode.in/pincode/' + worker_pincode)

                    get_job_api = requests.get('https://api.postalpincode.in/pincode/' + job_pincode)

                    worker_response = get_worker_api.json()
                    job_response = get_job_api.json()

                    worker_data = worker_response[0]['PostOffice'][0]
                    job_data = job_response[0]['PostOffice'][0]

                    worker_area = worker_data['Region']
                    worker_district = worker_data['District']
                    worker_state = worker_data['State']

                    job_area = job_data['Region']
                    job_district = job_data['District']
                    job_state = job_data['State']

                    if worker_area == job_area and worker_district == job_district and worker_state == job_state:
                        score += self.attribute_weights['location']
                    
                    elif worker_area != job_area and worker_district == job_district and worker_state == job_state:
                        score += self.attribute_weights['location']

                    elif worker_area != job_area and worker_district != job_district and worker_state == job_state:
                        score += self.attribute_weights['location']

                    

            return score

    def matching_algorithm(self):
        worker_data = self.worker_data
        job_data = self.job_data

        jobs = list(job_data.keys())
        num_jobs = len(jobs)

        for job_id in jobs:
            job = job_data[job_id]
            workers = list(worker_data.keys())
            num_workers = len(workers)

            matrix = np.zeros((num_workers, len(self.attribute_weights_array)))

            for i in range(num_workers):
                worker_id = workers[i]
                worker = worker_data[worker_id]
                for j, attribute in enumerate(self.attribute_weights.keys()):
                    if attribute == 'primary_skills':
                        if attribute in worker and attribute in job and job[attribute] in worker[attribute]:
                            matrix[i, j] = 1
                    elif attribute == 'min_qualification':
                        qualification_score = self.worker_scores.get(worker_id, 0)
                        min_qualification = self.job_scores.get(job_id, 0)
                        if qualification_score >= min_qualification:
                            matrix[i, j] = 1
                    elif attribute == 'age':
                        if 'min_age' in job and 'max_age' in job and 'age' in worker and job['min_age'] <= worker['age'] <= job['max_age']:
                            matrix[i, j] = 1
                    elif attribute == 'gender':
                        if 'gender' in worker and 'gender' in job and (worker['gender'] == job['gender'] or job['gender'] == 'Gender Neutral'):
                            matrix[i, j] = 1
                    elif attribute == 'secondary_skills':
                        if 'primary_skills' in worker and 'secondary_skills' in job:
                            if worker['primary_skills'] in job['secondary_skills']:
                                matrix[i, j] = 0.75
                        elif 'secondary_skills' in worker and 'secondary_skills' in job:
                            if worker['secondary_skills'] in job['secondary_skills']:
                                matrix[i, j] = 0.5
                    elif attribute == 'location':
                        if 'area' in worker and 'area' in job:
                            if worker['area'] == job['area'] and worker['district'] == job['district'] and worker['state'] == job['state']:
                                matrix[i, j] = 1
                            elif worker['area'] != job['area'] and worker['district'] == job['district'] and worker['state'] == job['state']:
                                matrix[i, j] = 0.75
                            elif worker['area'] != job['area'] and worker['district'] != job['district'] and worker['state'] == job['state']:
                                matrix[i, j] = 0.5
                    elif attribute == 'years_of_experience':
                        if 'experience' in worker and 'years_of_experience' in job:
                            if worker['experience'] >= job['years_of_experience']:
                                matrix[i, j] = 1
                    
                    else:
                        if attribute in worker and attribute in job and worker[attribute] == job[attribute]:
                            matrix[i, j] = 1


            print(f"Job: {job_id}")
            print(matrix * self.attribute_weights_array)


re = Recommendation_Engine()
db = re.firebase()
re.retrieve_job_data()
re.retrieve_worker_data()
re.score_qualification()
re.calculate_worker_age()
re.matching_algorithm()

