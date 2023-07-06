import random
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import requests



class Worker_List:

    # Creating and uploading data to Workers collection on firebase

    def __init__(self):

        self.worker_list = []

        self.skills_list = []

        self.experience_list = []

        self.start_date = None

        self.end_date = None

        self.start_date_list = []

        self.end_date_list = []

        self.pincode_list = [
            '110001',   # Delhi
            '400001',   # Mumbai
            '700001',   # Kolkata
        ]
        """
            '600001',   # Chennai
            '560001',   # Bangalore
            '411001',   # Pune
            '380001',   # Ahmedabad
            '500001',   # Hyderabad
            '302001',   # Jaipur
            '800001',   # Patna
            '560066',   # Electronic City, Bangalore
            '400086',   # Andheri, Mumbai
            '600040',   # T. Nagar, Chennai
            '411014',   # Hinjewadi, Pune
            '500081',   # Gachibowli, Hyderabad
            '560008',   # Malleshwaram, Bangalore
            '380009',   # Navrangpura, Ahmedabad
            '700091',   # Salt Lake City, Kolkata
            '110020',   # Hauz Khas, Delhi
            '302017'    # Malviya Nagar, Jaipur
            # Add more PIN codes here...
        ]
        """


        self.first_names = [
            "Aarav",
            "Aditi",
            "Akash",
            "Amrita",
            "Anaya",
            "Anika",
            "Arjun",
            "Avni",
            "Chaitanya",
            "Devika",
            "Divya",
            "Gaurav",
            "Isha",
            "Kabir",
            "Kavya",
            "Manisha",
            "Mehul",
            "Neha",
            "Nikhil",
            "Pooja",
            "Pranav",
            "Radha",
            "Rahul",
            "Riya",
            "Rohan",
            "Shreya",
            "Siddharth",
            "Tanvi",
            "Varun",
            "Yash",
            "Zara"
        ]

        self.last_names = [
            "Agarwal",
            "Bajaj",
            "Chopra",
            "Deshmukh",
            "Gupta",
            "Jain",
            "Kapoor",
            "Kumar",
            "Mahajan",
            "Malhotra",
            "Mehta",
            "Mishra",
            "Nair",
            "Patel",
            "Puri",
            "Rajput",
            "Rao",
            "Reddy",
            "Sethi",
            "Shah",
            "Sharma",
            "Singh",
            "Soni",
            "Srivastava",
            "Tiwari",
            "Trivedi",
            "Verma",
            "Yadav",
            "Zaveri",
            "Zoshi"
        ]

        self.primary_skills = [
            "Construction Laborer",
            "Agricultural Worker",
            "Mason",
            "Carpenter",
            "Painter",
            "Plumber",
        ]
        """
            "Electrician",
            "Welder",
            "Loader/Unloader",
            "Housekeeper",
            "Janitor",
            "Cleaner",
            "Gardener",
            "Security Guard",
            "Factory Worker",
            "Packaging Worker",
            "Helper",
            "Driver",
            "Delivery Person",
            "Garbage Collector",
            "Street Vendor",
            "Farm Laborer",
            "Brick Maker",
            "Road Sweeper",
            "Tea Picker",
            "Textile Worker",
            "Fisherman",
            "Construction Site Watchman",
            "Cycle Rickshaw Puller",
            "Auto Rickshaw Driver"
        ]
        """

        self.secondary_skills = [
            "Construction Laborer",
            "Agricultural Worker",
            "Mason",
        ]
        """
            "Carpenter",
            "Painter",
            "Plumber",
            "Electrician",
            "Welder",
            "Loader/Unloader",
            "Housekeeper",
            "Janitor",
            "Cleaner",
            "Gardener",
            "Security Guard",
            "Factory Worker",
            "Packaging Worker",
            "Helper",
            "Driver",
            "Delivery Person",
            "Garbage Collector",
            "Street Vendor",
            "Farm Laborer",
            "Brick Maker",
            "Road Sweeper",
            "Tea Picker",
            "Textile Worker",
            "Fisherman",
            "Construction Site Watchman",
            "Cycle Rickshaw Puller",
            "Auto Rickshaw Driver"
        """


        self.qualifications = [
            'Primary Education',
            'Secondary Education',
            'Higher Secondary Education',
            'Diploma/Certificate Programs',
            "Bachelor's Degree (BSc)",
        ]

        self.company_names = [
            "Shramik Solutions",
            "Kamgar Staffing",
            "Kaushal Labor Co."
        ]
        """
            "Naukari Services",
            "Mazdoor Manpower",
            "SkillKart Staffing",
            "Kadambari Labor Solutions",
            "Saksham Labor Providers",
            "Kushal LaborForce",
            "Samarth Skilled Staffing",
            "Shram Sangathan Agency",
            "KaamChakra Labor Co.",
            "Rozgar Staffing",
            "Hunar Labor Solutions",
            "Sangharsh Labor Providers",
            "Sambhav Labor Group",
            "Yashasvi Labor Agency",
            "Kausalya Skilled Staffing",
            "KadamKadam Labor Solutions",
            "Karigar Staffing",
            "Kausal Labor Co.",
            "Samarpan Labor Providers",
            "Pragati Skilled Staffing",
            "Sambandh Labor Solutions",
            "Karyarat Labor Agency",
            "KaamSevak Staffing",
            "Kushalta Labor Group",
            "Samarthak Labor Solutions",
            "Sashakt Labor Agency",
            "Nirmaan Staffing",
            "KarmaYogi Labor Co."
        ]
        """

        self.job_titles = [
            "Laborer",
            "Janitor",
            "Warehouse Worker"
        ]
        """
            "Production Worker",
            "Cleaner",
            "Farm Worker",
            "Construction Helper",
            "Kitchen Staff",
            "Landscaping Laborer",
            "Housekeeper",
            "Packer",
            "Delivery Driver",
            "Assembler",
            "Dishwasher",
            "Retail Associate",
            "Security Guard",
            "Valet Parking Attendant",
            "Car Wash Attendant",
            "Food Service Worker",
            "Stock Clerk",
            "Cashier",
            "Laundry Attendant",
            "Gardener",
            "Garbage Collector",
            "Mover",
            "Security Officer",
            "General Maintenance Worker",
            "Data Entry Clerk",
            "Groundskeeper",
            "Production Operator"
        """
        
    
    def location_api(self):

        self.pincode = random.choice(self.pincode_list)

        api = requests.get('https://api.postalpincode.in/pincode/' + self.pincode)

        response = api.json()

        
        data = response[0]['PostOffice'][0]
        self.area = data['Region']
        self.district = data['District']
        self.state = data['State']

    def firebase(self):
        cred = credentials.Certificate('jansakti-andrew-firebase-adminsdk.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        return self.db

    def generate_random_date_of_birth(self, start_date, end_date):

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        total_days = (end_date - start_date).days

        random_days = random.randint(0, total_days)

        random_date = start_date + timedelta(days=random_days)

        formatted_date = random_date.strftime("%Y-%m-%d")

        return formatted_date

    def generate_dates(self):

        current_date = datetime.now()

        start_date_offset = random.randint(1, 1900)

        self.start_date = current_date - timedelta(days=start_date_offset)

        end_date_offset = random.randint(1, start_date_offset)

        self.end_date = self.start_date + timedelta(days=end_date_offset)
        
    def generate_worker_data(self):

        self.location_api()
        
        worker = {
            'full_name': random.choice(self.first_names) + ' ' + random.choice(self.last_names),
            'gender': random.choice(['Male', 'Female']),
            'highest_qualification': random.choice(self.qualifications),
            'dob': self.generate_random_date_of_birth(start_date='1960-01-01', end_date='2002-01-01'),
            'employment_status': random.randint(0, 1),
            'state': self.state,
            'district': self.district,
            'area': self.area,
            'pincode': self.pincode,
            'created_date': datetime.now()
        }

        self.worker_list.append(worker)

        return self.worker_list
    
    def randomise(self):

        self.worker_list = []  

        random_worker = pd.DataFrame(self.generate_worker_data())
        return random_worker

    
    def upload_data(self):

        pd.set_option('display.max_columns', None)

        df = self.randomise().transpose()

        dic = df.to_dict()

        for idx in range(0, len(dic)):

            self.db.collection('Workers').add(dic[idx])
       
    # Creating and uploading data to subcollections 'Skills' and 'Experience' and adding them to individual records

    def generate_skills_data(self):

        self.skills_list = []

        skills = {
            'skill_name': random.choice(self.primary_skills),
            'experience': random.randint(1, 5),
            'is_primary': random.choice([True, False]),
        }

        self.skills_list.append(skills)
        

        return self.skills_list
    
    def generate_experience_dates(self):

        current_date = datetime.today()
        start_date_offset = random.randint(1, 1900)
        self.start_date = current_date - timedelta(days=start_date_offset)
        end_date_offset = random.randint(1, start_date_offset)
        self.end_date = self.start_date + timedelta(days=end_date_offset)

    def generate_experience_data(self):

        self.experience_list = []

        self.generate_experience_dates()

        experience = {
            'company_name': random.choice(self.company_names),
            'job_title': random.choice(self.job_titles),
            'primary_skill': random.choice(self.primary_skills),
            'start_date': self.start_date.strftime("%d/%m/%y"),
            'end_date': self.end_date.strftime("%d/%m/%y"),
        }

        self.experience_list.append(experience)

        return self.experience_list
     
    def randomise_subcollection_data(self):

        random_skill_choice = random.randint(1,5)

        random_experience_choice = random.randint(1,5)


        for i in range(random_skill_choice):

            self.random_skills_data = pd.DataFrame(self.generate_skills_data())

        for i in range(random_experience_choice):

            self.random_experience_data = pd.DataFrame(self.generate_experience_data())

    def upload_subcollection_data(self):

        self.randomise_subcollection_data()

        collection_ref = self.db.collection('Workers')
        query = collection_ref.order_by('created_date', direction=firestore.Query.DESCENDING).limit(1)
        documents = query.get()

        for parent_doc in documents:
            parent_doc_id = parent_doc.id
            parent_doc_ref = collection_ref.document(parent_doc_id)

            skills_subcollection_ref = parent_doc_ref.collection('Skills')
            experience_subcollection_ref = parent_doc_ref.collection('Experience')

            for _, skill_row in self.random_skills_data.iterrows():
                
                skills_subcollection_ref.add(skill_row.to_dict())

            for _, experience_row in self.random_experience_data.iterrows():
                
                experience_subcollection_ref.add(experience_row.to_dict())

        self.random_skills_data.drop(self.random_skills_data.index)
        
        self.random_experience_data.drop(self.random_experience_data.index)

        
wl = Worker_List()

wl.firebase()

for _ in range(50):
    
    wl.upload_data()
    wl.upload_subcollection_data()
    