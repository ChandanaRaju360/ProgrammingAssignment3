from datetime import datetime
import csv
import sys
import random

class Patient:
    def __init__(self, patient_id, visit_id, visit_time, visit_department, race, gender, ethnicity, age, zip_code, insurance, chief_complaint, note_id, note_type):
        self.patient_id = patient_id
        self.visits = {visit_id: Visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)}
        self.info = {
            'Race': race,
            'Gender': gender,
            'Ethnicity': ethnicity,
            'Age': age,
            'Zip_code': zip_code,
            'Insurance': insurance
        }
    
    def add_visit(self, visit_id, visit_time, visit_department, chief_complaint, note_id, note_type):
        self.visits[visit_id] = Visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)

class Visit:
    def __init__(self, visit_id, visit_time, visit_department, chief_complaint, note_id, note_type):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.visit_department = visit_department
        self.chief_complaint = chief_complaint
        self.note_id = note_id
        self.note_type = note_type

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Hospital:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient_id, visit_id, visit_time, visit_department, race, gender, ethnicity, age, zip_code, insurance, chief_complaint, note_id, note_type):
        patient = Patient(patient_id, visit_id, visit_time, visit_department, race, gender, ethnicity, age, zip_code, insurance, chief_complaint, note_id, note_type)
        self.patients[patient_id] = patient
        return patient

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            print("Patient removed successfully.")
        else:
            print("Patient ID not found.")

    def retrieve_patient(self, patient_id):
        if patient_id in self.patients:
            print("Patient Information:")
            print("Patient ID:", self.patients[patient_id].patient_id)
            print("Patient Info:", self.patients[patient_id].info)
            print("Visits:")
            for visit_id, visit in self.patients[patient_id].visits.items():
                print("Visit ID:", visit_id)
                print("Visit Time:", visit.visit_time)
                print("Visit Department:", visit.visit_department)
                print("Chief Complaint:", visit.chief_complaint)
                print("Note ID:", visit.note_id)
                print("Note Type:", visit.note_type)
                print()
        else:
            print("Patient ID not found.")

    def count_visits(self, date):
        count = 0
        input_date = datetime.strptime(date, '%Y-%m-%d').date()
        for patient in self.patients.values():
            for visit in patient.visits.values():
                if visit.visit_time == input_date:
                    count += 1
        print("Total visits on", date, ":", count)

    def generate_unique_visit_id(self, patient_id):
        visit_id = f"{patient_id}_{random.randint(100000, 999999)}"
        while visit_id in self.patients[patient_id].visits:
            visit_id = f"{patient_id}_{random.randint(100000, 999999)}"
        return visit_id

def load_credentials(file_path):
    users = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append(User(row['username'], row['password'], row['role']))
    return users

def load_data(file_path):
    hospital = Hospital()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert visit_time to datetime.date object
            visit_time = datetime.strptime(row['Visit_time'], '%Y-%m-%d').date()
            hospital.add_patient(row['Patient_ID'], row['Visit_ID'], visit_time, row['Visit_department'], row['Race'], row['Gender'], row['Ethnicity'], row['Age'], row['Zip_code'], row['Insurance'], row['Chief_complaint'], row['Note_ID'], row['Note_type'])
    return hospital

def main():
    if len(sys.argv) != 3:
        print("Usage: python Program_Name.py Credential_file_path Patient_file_path")
        return

    credential_file_path = sys.argv[1]
    patient_file_path = sys.argv[2]

    users = load_credentials(credential_file_path)
    hospital = load_data(patient_file_path)

    # User Authentication
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = None
    for u in users:
        if u.username == username and u.password == password:
            user = u
            break

    if user is None:
        print("Invalid username or password.")
        return

    # Role-based Access Control
    if user.role == "management":
        # Generate statistics
        generate_statistics(hospital)
    elif user.role == "admin":
        # Count visits
        date = input("Enter date (yyyy-mm-dd): ")
        hospital.count_visits(date)
    elif user.role in ["clinician", "nurse"]:
        # Allow user interactions
        while True:
            action = input("Choose an action (Add_patient, Remove_patient, Retrieve_patient, Count_visits) or type 'Stop' to exit: ")
            if action == 'Stop':
                break
            elif action == 'Add_patient':
                patient_id = input("Enter Patient_ID: ")
                if patient_id in hospital.patients:
                    visit_time_str = input("Enter Visit_time (YYYY-MM-DD): ")
                    visit_time = datetime.strptime(visit_time_str, '%Y-%m-%d').date()
                    patient = hospital.patients[patient_id]
                    visit_id = hospital.generate_unique_visit_id(patient_id)
                    visit_department = input("Enter Visit_department: ")
                    chief_complaint = input("Enter Chief_complaint: ")
                    note_id = input("Enter Note ID: ")
                    note_type = input("Enter Note Type: ")
                    visit = Visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)
                    patient.add_visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)
                else:
                    race = input("Enter Race: ")
                    gender = input("Enter Gender: ")
                    ethnicity = input("Enter Ethnicity: ")
                    age = int(input("Enter Age: "))
                    zip_code = input("Enter Zip Code: ")
                    insurance = input("Enter Insurance: ")
                    patient = hospital.add_patient(patient_id, 'None', 'None', 'None', race, gender, ethnicity, age, zip_code, insurance, 'None', 'None', 'None')
                    visit_id = hospital.generate_unique_visit_id(patient_id)
                    visit_time_str = input("Enter Visit_time (YYYY-MM-DD): ")
                    visit_time = datetime.strptime(visit_time_str, '%Y-%m-%d').date()
                    visit_department = input("Enter Visit_department: ")
                    chief_complaint = input("Enter Chief_complaint: ")
                    note_id = input("Enter Note ID: ")
                    note_type = input("Enter Note Type: ")
                    visit = Visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)
                    patient.add_visit(visit_id, visit_time, visit_department, chief_complaint, note_id, note_type)
            elif action == 'Remove_patient':
                patient_id = input("Enter Patient ID: ")
                hospital.remove_patient(patient_id)
            elif action == 'Retrieve_patient':
                patient_id = input("Enter Patient ID: ")
                hospital.retrieve_patient(patient_id)
            elif action == 'Count_visits':
                date = input("Enter date (yyyy-mm-dd): ")
                hospital.count_visits(date)
            else:
                print("Invalid action.")
    else:
        print("Invalid user role.")

def generate_statistics(hospital):
    print("Generating key statistics report...")
    # 1. Temporal trend of the number of patients who visited the hospital.
    print("Temporal trend of the number of patients who visited the hospital:")
    patient_counts = {}
    for patient in hospital.patients.values():
        for visit_id, visit in patient.visits.items():
            visit_date = visit.visit_time.strftime('%Y-%m-%d')
            if visit_date in patient_counts:
                patient_counts[visit_date] += 1
            else:
                patient_counts[visit_date] = 1
    
    sorted_dates = sorted(patient_counts.keys())
    for date in sorted_dates:
        print(f"{date}: {patient_counts[date]}")

    # 2. Temporal trend of the number of patients who visited the hospital with different types of insurances.
    print("\nTemporal trend of the number of patients who visited the hospital with different types of insurances:")
    insurance_counts = {}
    for patient in hospital.patients.values():
            insurance_type = patient.info['Insurance']
            if insurance_type in insurance_counts:
                insurance_counts[insurance_type] += 1
            else:
                insurance_counts[insurance_type] = 1

    for insurance, count in insurance_counts.items():
        print(f"{insurance}: {count}")

    # 3. Temporal trend of the number of patients who visited the hospital in different demographics groups (e.g., age, race, gender, ethnicity).
    print("\nTemporal trend of the number of patients who visited the hospital in different demographics groups:")
    demographics_counts = {'Age': {}, 'Race': {}, 'Gender': {}, 'Ethnicity': {}}
    for patient in hospital.patients.values():
        for visit_id, visit in patient.visits.items():
            # Age
            age_group = int(patient.info['Age']) // 10 * 10  # Convert age to integer
            if age_group in demographics_counts['Age']:
                demographics_counts['Age'][age_group] += 1
            else:
                demographics_counts['Age'][age_group] = 1
            # Race
            race = patient.info['Race']  # Assuming race is stored in patient's information
            if race in demographics_counts['Race']:
                demographics_counts['Race'][race] += 1
            else:
                demographics_counts['Race'][race] = 1
            # Gender
            gender = patient.info['Gender']  # Assuming gender is stored in patient's information
            if gender in demographics_counts['Gender']:
                demographics_counts['Gender'][gender] += 1
            else:
                demographics_counts['Gender'][gender] = 1
            # Ethnicity
            ethnicity = patient.info['Ethnicity']  # Assuming ethnicity is stored in patient's information
            if ethnicity in demographics_counts['Ethnicity']:
                demographics_counts['Ethnicity'][ethnicity] += 1
            else:
                demographics_counts['Ethnicity'][ethnicity] = 1

    for category, counts in demographics_counts.items():
        print(f"\n{category}:")
        for item, count in counts.items():
            print(f"{item}: {count}")



if __name__ == "__main__":
    main()
