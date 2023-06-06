from Worker_List import Worker_List
from Job_List import Job_List
import json

class test:

    def load_config(self, filename):
        with open(filename, 'r') as f:
            config = json.load(f)
        return config

    def __init__(self):

        wl = Worker_List()
        self.worker_list = wl.generate_worker()
        jl = Job_List()
        self.job_list = jl.generate_job()
        self.recommendations = {}  
        self.config = self.load_config('Config.json')
        self.preference = self.config['preference']
        self.adjustable_job_years_experience = self.config['adjustable_job_years_experience']
  
    


    def calculation(self):

        for worker in self.worker_list:
            
            worker_id = worker['worker_id']
            worker_location = worker['location']
            worker_primary_skill = worker['primary_skills']
            worker_secondary_skills = worker['secondary_skills']
            worker_name = worker['name']
            worker_gender = worker['gender']
            worker_experience = int(worker['years_of_experience'])

            for job in self.job_list:
                job_id = job['job_id']
                job_location = job['location']
                job_primary_skill = job['primary_skills']
                job_secondary_skills = job['secondary_skills']
                job_name = job['job_names']
                job_gender = job['gender']
                job_experience = int(job['years_of_experience'])

                
                match self.preference:
                    case 'best scenario':
                        config = worker_location == job_location and (worker_gender == job_gender or job_gender == 'Neutral') and worker_primary_skill == job_primary_skill and any(skill in worker_secondary_skills for skill in job_secondary_skills) and worker_experience >= job_experience
                        if config:
                            self.recommendations.append(job_id)

                    case 'adjustable years of experience':
                        config = worker_location == job_location and (worker_gender == job_gender or job_gender == 'Neutral') and worker_primary_skill == job_primary_skill and any(skill in worker_secondary_skills for skill in job_secondary_skills) and worker_experience >= job_experience - self.adjustable_job_years_experience
                        if config:
                            self.recommendations.append(job_id)

                    case 'secondary skills not taken into account + adjustable years of experience':
                        config = worker_location == job_location and (worker_gender == job_gender or job_gender == 'Neutral') and worker_primary_skill == job_primary_skill and worker_experience >= job_experience - self.adjustable_job_years_experience
                        if config:
                            self.recommendations.append(job_id)

                    case 'primary job skill is a worker secondary skill + adjustable years of experience':
                        config = worker_location == job_location and (worker_gender == job_gender or job_gender == 'Neutral') and job_primary_skill in worker_secondary_skills and worker_experience >= job_experience - self.adjustable_job_years_experience
                        if config:
                            self.recommendations.append(job_name)

                
            self.recommendations[worker_name] = self.recommendations

        print(self.recommendations)

re = test()
re.calculation()
