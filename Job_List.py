import random

class Job_List:

    def __init__(self):

        self.job_list = []

    def generate_job(self):
        organisation_names = ['Google', 'Facebook', 'IBM', 'Dell', 'KPMG', 'Deloitte', 'Microsoft', 'Apple']
        job_names = ['Software Engineer', 'Tester', 'Project Manager', 'Director', 'Intern', 'Analyst', 'Consultant', 'Partner']
        primary_skills = ['Python', 'Java', 'JavaScript', 'C++', 'Data Analysis', 'Machine Learning']
        secondary_skills = ['Python', 'Java', 'JavaScript', 'C++', 'Data Analysis', 'Machine Learning']
        locations = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Edinburgh', 'Liverpool']

        for i in range(0, 20):

            job = {
                'job_id': random.randint(1000, 9999),
                'organisation_names': random.choice(organisation_names),
                'job_names': random.choice(job_names),
                'gender': random.choice(['Male', 'Female', 'Neutral']),
                'primary_skills': random.sample(primary_skills, random.randint(1, 1)),
                'secondary_skills': random.sample(secondary_skills, random.randint(1, 3)),
                'years_of_experience': random.randint(1, 5),
                'location': random.choice(locations) + ', Britain'
            }

            self.job_list.append(job)

        return self.job_list
    
jl = Job_List()

#for i in jl.generate_job():
#    print(i)
