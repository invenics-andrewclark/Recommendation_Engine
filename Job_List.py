import random
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import requests



class Job_List:

    # Creating and uploading data to Workers collection on firebase

    def __init__(self):

        self.job_list = []

        self.organisation_list = []

        self.skills_list = None

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
            "Mason"
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
            '8th Pass',
            '10th Pass',
            '12th Pass',
            'Graduation',
            "Post graduation",
        ]

        self.company_names = [
            "Shramik Solutions",
            "Kamgar Staffing",
            "Kaushal Labor Co.",
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
        """

        self.job_titles = [
            "Laborer",
            "Janitor",
            "Warehouse Worker",
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
        self.skill_level = [
            'Less than 1 year',
            '1 to 10 years',
            'More than 10 years'
        ]
    
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

    def generate_dates(self):

        current_date = datetime.now()

        start_date_offset = random.randint(1, 30)

        self.start_date = current_date + timedelta(days=start_date_offset)

        end_date_offset = random.randint(1, start_date_offset)

        self.end_date = self.start_date + timedelta(days=end_date_offset)

    def generate_max_age(self):

        min_age = 18

        max_age = min_age + 30 + random.randint(1,17)

        return max_age
    
    def generate_organisation_data(self):
        self.location_api()
        organisation = {
            'area': self.area,
            'district': self.district,
            'state': self.state,
            'created_on': datetime.now(),
            'organisation_name': random.choice(self.company_names)
        }

        self.organisation_list.append(organisation)

        return self.organisation_list
    
    def randomise(self):

        self.organisation_list = []  

        random_organisation = pd.DataFrame(self.generate_organisation_data())
        return random_organisation
    
    def upload_data(self):

        pd.set_option('display.max_columns', None)

        df = self.randomise().transpose()

        dic = df.to_dict()

        for idx in range(0, len(dic)):

            self.db.collection('Organisations').add(dic[idx])
        
    def generate_job_data(self):

        self.location_api()
        self.generate_dates()
        
        job = {
            'organisation_name': random.choice(self.company_names),
            'job_title': random.choice(self.job_titles),
            'gender': random.choice(['Male', 'Female', 'Gender Neutral']),
            'min_qualification': random.choice(self.qualifications),
            'primary_skills': random.choice(self.primary_skills),
            'secondary_skills': random.sample(self.secondary_skills, random.randint(1, 3)),
            'skill_level': random.choice(self.skill_level),
            'state': self.state,
            'district': self.district,
            'area': self.area,
            'pincode': self.pincode,
            'min_age': 18,
            'max_age': self.generate_max_age(),
            'start_date': self.start_date.strftime("%d/%m/%y"),
            'end_date': self.end_date.strftime("%d/%m/%y"),
            'filled': random.randint(0, 20),
            'number_of_vacancies': random.randint(0,20),
        }

        self.job_list.append(job)

        return self.job_list
    
    def randomise_subcollection_data(self):

        random_job_choice = random.randint(1,5)

        for _ in range(random_job_choice):

            self.random_job_data = pd.DataFrame(self.generate_job_data())

    def upload_subcollection_data(self):

        self.randomise_subcollection_data()

        collection_ref = self.db.collection('Organisations')
        query = collection_ref.order_by('created_on', direction=firestore.Query.DESCENDING).limit(1)
        documents = query.get()

        for parent_doc in documents:
            parent_doc_id = parent_doc.id
            parent_doc_ref = collection_ref.document(parent_doc_id)

            jobs_subcollection_ref = parent_doc_ref.collection('Jobs')

            for _, job_row in self.random_job_data.iterrows():
                
                jobs_subcollection_ref.add(job_row.to_dict())

        self.random_job_data.drop(self.random_job_data.index)

        
jl = Job_List()

jl.firebase()

for _ in range(10):
    jl.upload_data()
    jl.upload_subcollection_data()
