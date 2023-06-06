from Worker_List import Worker_List
from Job_List import Job_List

class Recommendation_Engine:
    def __init__(self):
        wl = Worker_List()
        self.worker_list = wl.generate_worker()
        jl = Job_List()
        self.job_list = jl.generate_job()

        self.worker_id = [worker['worker_id'] for worker in self.worker_list]
        self.worker_name = [worker['name'] for worker in self.worker_list]
        self.worker_gender = [worker['gender'] for worker in self.worker_list]
        self.worker_skills = [worker['skills'] for worker in self.worker_list]
        self.worker_experience = [worker['years_of_experience'] for worker in self.worker_list]
        self.worker_location = [worker['location'] for worker in self.worker_list]

        self.job_id = [job['job_id'] for job in self.job_list]
        self.job_organisation = [job['organisation_names'] for job in self.job_list]
        self.job_name = [job['job_names'] for job in self.job_list]
        self.job_gender = [job['gender'] for job in self.job_list]
        self.job_skills = [job['skills'] for job in self.job_list]
        self.job_experience = [job['years_of_experience'] for job in self.job_list]
        self.job_location = [job['location'] for job in self.job_list]

        self.recommendations = {}  

    def print_worker_ids(self):
        for job_name in self.job_name:
            print(job_name)

    def calculation(self):
        for worker in self.worker_list:
            recommendations = []
            worker_id = worker['worker_id']
            worker_location = worker['location']
            worker_skills = worker['skills']
            worker_name = worker['name']
            worker_gender = worker['gender']
            worker_experience = int(worker['years_of_experience'])

            for job in self.job_list:
                job_id = job['job_id']
                job_location = job['location']
                job_skills = job['skills']
                job_name = job['job_names']
                job_gender = job['gender']
                job_experience = int(job['years_of_experience'])

                # Recommendation logic based on location and skills
                if worker_location == job_location and worker_gender == job_gender and any(skill in worker_skills for skill in job_skills) and worker_experience >= job_experience:
                    recommendations.append(job_id)

            self.recommendations[worker_id] = recommendations

        print(self.recommendations)

re = Recommendation_Engine()
re.calculation()
