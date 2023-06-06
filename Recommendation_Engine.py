from Worker_List import Worker_List
from Job_List import Job_List
import json

class Recommendation_Engine:

    

    def __init__(self):

        wl = Worker_List()
        self.worker_list = wl.generate_worker()
        jl = Job_List()
        self.job_list = jl.generate_job()
        self.recommendations = {}  
        self.config = self.load_config('Config.json')
        self.preference = self.config['preference']

    def load_config(self, filename):
        with open(filename, 'r') as f:
            config = json.load(f)
        return config
  
    
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

                
                if self.preference == 'config1':
                    config = worker_location == job_location and (worker_gender == job_gender or job_gender == 'Neutral') and any(skill in worker_skills for skill in job_skills) and worker_experience >= job_experience
                       # self.recommendations.append(job_id)

                elif self.preference == 'config2':
                    config = worker_location == job_location and (worker_gender == job_gender or job_gender == 'Neutral') and any(skill in worker_skills for skill in job_skills) and worker_experience >= job_experience

                
                    






            self.recommendations[worker_id] = recommendations

        print(self.recommendations)

re = Recommendation_Engine()
re.calculation()
