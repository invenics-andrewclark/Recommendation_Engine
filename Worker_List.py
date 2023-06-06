import random

class Worker_List:

    def __init__(self):

        self.worker_list = []

    def generate_worker(self):
        first_names = ['John', 'Alice', 'Michael', 'Emily', 'David', 'Olivia', 'James', 'Sophia']
        last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Wilson', 'Lee', 'Davis', 'Clark']
        skills = ['Python', 'Java', 'JavaScript', 'C++', 'Data Analysis', 'Machine Learning']
        locations = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Edinburgh', 'Liverpool']

        for i in range(0, 250):

            worker = {
                'worker_id': random.randint(1000, 9999),
                'name': random.choice(first_names) + ' ' + random.choice(last_names),
                'gender': random.choice(['Male', 'Female']),
                'skills': random.sample(skills, random.randint(1, 4)),
                'years_of_experience': random.randint(1, 5),
                'location': random.choice(locations) + ', Britain'
            }

            self.worker_list.append(worker)

        return self.worker_list
    
wl = Worker_List()

#for i in wl.generate_worker():
#    print(i)
