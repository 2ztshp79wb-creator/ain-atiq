import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='fekra',
                user='root',
                password='password',
                port=3306
            )
            print("Connected to MySQL database successfully")
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def execute_query(self, query, params=None):
        cursor = None
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    # ============================================
    # AUTHENTICATION METHODS
    # ============================================
    
    def get_doctor_by_credentials(self, doctor_id, password):
        query = "SELECT * FROM doctor_credentials WHERE doctor_id = %s AND password = %s"
        result = self.execute_query(query, (doctor_id, password))
        return result[0] if result else None
    
    def get_all_doctors(self):
        query = "SELECT doctor_id, first_name, last_name, specialty FROM doctors ORDER BY first_name"
        return self.execute_query(query)
    
    def get_all_specialties(self):
        query = "SELECT DISTINCT specialty FROM doctors ORDER BY specialty"
        return self.execute_query(query)

    # ============================================
    # 20 FILTERS - COMPLETE IMPLEMENTATION
    # ============================================
    
    def filter_patients_20_filters(self, filters, limit=None):
        """
        20 Advanced Filters for Patient Data
        
        FILTERS:
        1. search_name      - Search by patient name
        2. search_phone     - Search by phone number
        3. search_email     - Search by email
        4. search_address   - Search by address
        5. doctor_id        - Filter by specific doctor
        6. specialty        - Filter by doctor specialty
        7. doctor_sexe      - Filter by doctor gender
        8. doctor_age_min   - Filter by doctor minimum age
        9. doctor_age_max   - Filter by doctor maximum age
        10. age_min         - Filter by patient minimum age
        11. age_max         - Filter by patient maximum age
        12. sexe            - Filter by patient gender
        13. dob_from        - Filter by date of birth range (start)
        14. dob_to          - Filter by date of birth range (end)
        15. visits_min      - Filter by minimum visits
        16. visits_max      - Filter by maximum visits
        17. admission_date_from - Filter by admission date (start)
        18. admission_date_to   - Filter by admission date (end)
        19. status          - Filter by patient status (active/inactive)
        20. has_appointment - Filter patients with/without appointments
        21. is_high_risk    - Filter high-risk patients (age 65+ OR visits>20)
        """
        
        query = """
            SELECT 
                p.patient_id,
                p.first_name,
                p.last_name,
                p.age,
                p.sexe,
                p.date_of_birth,
                p.phone,
                p.email,
                p.address,
                p.visits_2_years,
                p.admission_date,
                p.status,
                d.doctor_id,
                d.first_name as doctor_first,
                d.last_name as doctor_last,
                d.specialty,
                d.age as doctor_age,
                d.sexe as doctor_sexe,
                (SELECT COUNT(*) FROM appointments WHERE patient_id = p.patient_id AND status = 'scheduled') as upcoming_appointments,
                (SELECT COUNT(*) FROM appointments WHERE patient_id = p.patient_id AND status = 'completed') as completed_appointments
            FROM patients p
            LEFT JOIN doctors d ON p.doctor_id = d.doctor_id
            WHERE 1=1
        """
        params = []
        
        # ============================================
        # FILTER 1: SEARCH BY NAME
        # ============================================
        if filters.get('search_name'):
            search = f"%{filters['search_name']}%"
            query += " AND (p.first_name LIKE %s OR p.last_name LIKE %s)"
            params.extend([search, search])
        
        # ============================================
        # FILTER 2: SEARCH BY PHONE
        # ============================================
        
        # ============================================
        # FILTER 3: SEARCH BY EMAIL
        # ============================================

        
        # ============================================
        # FILTER 4: SEARCH BY ADDRESS
        # ============================================

        
        # ============================================
        # FILTER 5: DOCTOR ID (EXACT MATCH)
        # ============================================
        if filters.get('doctor_id'):
            query += " AND p.doctor_id = %s"
            params.append(filters['doctor_id'])
        
        # ============================================
        # FILTER 6: SPECIALTY
        # ============================================
        if filters.get('specialty'):
            query += " AND d.specialty = %s"
            params.append(filters['specialty'])
        
        # ============================================
        # FILTER 7: DOCTOR GENDER
        # ============================================

        # ============================================
        # FILTER 8-9: DOCTOR AGE RANGE
        # ============================================

        
        # ============================================
        # FILTER 10-11: PATIENT AGE RANGE
        # ============================================
        if filters.get('age_min'):
            query += " AND p.age >= %s"
            params.append(int(filters['age_min']))
        if filters.get('age_max'):
            query += " AND p.age <= %s"
            params.append(int(filters['age_max']))
        
        # ============================================
        # FILTER 12: PATIENT GENDER
        # ============================================
        if filters.get('sexe'):
            query += " AND p.sexe = %s"
            params.append(filters['sexe'])
        
        # ============================================
        # FILTER 13-14: DATE OF BIRTH RANGE
        # ============================================

        
        # ============================================
        # FILTER 15-16: VISIT COUNT RANGE
        # ============================================
        if filters.get('visits_min'):
            query += " AND p.visits_2_years >= %s"
            params.append(int(filters['visits_min']))
        if filters.get('visits_max'):
            query += " AND p.visits_2_years <= %s"
            params.append(int(filters['visits_max']))
        
        # ============================================
        # FILTER 17-18: ADMISSION DATE RANGE
        # ============================================

        
        # ============================================
        # FILTER 19: STATUS
        # ============================================

        
        # ============================================
        # FILTER 20: HAS APPOINTMENT
        # ============================================
        if filters.get('has_appointment') is not None:
            if filters['has_appointment'] == 'true':
                query += " AND EXISTS (SELECT 1 FROM appointments WHERE patient_id = p.patient_id)"
            elif filters['has_appointment'] == 'false':
                query += " AND NOT EXISTS (SELECT 1 FROM appointments WHERE patient_id = p.patient_id)"
        
        # ============================================
        # FILTER 21: HIGH RISK PATIENTS (EXTRA)
        # ============================================
        if filters.get('is_high_risk') == 'true':
            query += " AND (p.age >= 65 OR p.visits_2_years >= 20)"
        
        # ============================================
        # SORTING
        # ============================================
        allowed_sort_columns = [
            'patient_id', 'first_name', 'last_name', 'age', 
            'sexe', 'visits_2_years', 'date_of_birth', 
            'specialty', 'doctor_first', 'doctor_last',
            'admission_date', 'status'
        ]
        sort_by = filters.get('sort_by', 'last_name')
        sort_direction = filters.get('sort_direction', 'ASC').upper()
        
        if sort_by in allowed_sort_columns:
            if sort_by == 'doctor_first':
                sort_by = 'd.first_name'
            elif sort_by == 'doctor_last':
                sort_by = 'd.last_name'
            elif sort_by == 'specialty':
                sort_by = 'd.specialty'
            else:
                sort_by = f"p.{sort_by}"
            
            if sort_direction in ['ASC', 'DESC']:
                query += f" ORDER BY {sort_by} {sort_direction}"
        else:
            query += " ORDER BY p.last_name, p.first_name"
        
        # ============================================
        # LIMIT & PAGINATION
        # ============================================
        limit_value = limit or filters.get('limit', 100)
        page = int(filters.get('page', 1))
        offset = (page - 1) * limit_value
        
        query += " LIMIT %s OFFSET %s"
        params.extend([int(limit_value), offset])
        
        return self.execute_query(query, params)
    
    def get_filter_summary(self, filters):
        """Get a summary of applied filters"""
        summary = {
            'total_filters_applied': 0,
            'active_filters': []
        }
        
        filter_map = {
            'search_name': ('Name Search', filters.get('search_name')),
            'doctor_id': ('Doctor ID', filters.get('doctor_id')),
            'specialty': ('Specialty', filters.get('specialty')),
            'age_min': ('Min Age', filters.get('age_min')),
            'age_max': ('Max Age', filters.get('age_max')),
            'sexe': ('Gender', filters.get('sexe')),
            'visits_min': ('Min Visits', filters.get('visits_min')),
            'visits_max': ('Max Visits', filters.get('visits_max')),
            'has_appointment': ('Has Appointment', filters.get('has_appointment')),
            'is_high_risk': ('High Risk', filters.get('is_high_risk'))
        }
        
        for key, (label, value) in filter_map.items():
            if value and str(value).strip():
                summary['total_filters_applied'] += 1
                summary['active_filters'].append({
                    'label': label,
                    'value': value
                })
        
        return summary
    
    # ============================================
    # STATISTICS METHODS
    # ============================================
    
    def get_patient_statistics(self):
        query = """
            SELECT 
                COUNT(*) as total_patients,
                AVG(age) as avg_age,
                COUNT(CASE WHEN sexe = 'M' THEN 1 END) as male_count,
                COUNT(CASE WHEN sexe = 'F' THEN 1 END) as female_count,
                SUM(visits_2_years) as total_visits,
                AVG(visits_2_years) as avg_visits
            FROM patients
        """
        return self.execute_query(query)
    
    def get_patients_by_doctor(self):
        query = """
            SELECT 
                d.doctor_id,
                d.first_name as doctor_first,
                d.last_name as doctor_last,
                d.specialty,
                COUNT(p.patient_id) as patient_count
            FROM doctors d
            LEFT JOIN patients p ON d.doctor_id = p.doctor_id
            GROUP BY d.doctor_id
            ORDER BY patient_count DESC
        """
        return self.execute_query(query)
    
    def get_patients_by_age_group(self):
        query = """
            SELECT 
                CASE 
                    WHEN age < 18 THEN '0-17'
                    WHEN age BETWEEN 18 AND 30 THEN '18-30'
                    WHEN age BETWEEN 31 AND 50 THEN '31-50'
                    WHEN age BETWEEN 51 AND 65 THEN '51-65'
                    ELSE '65+'
                END as age_group,
                COUNT(*) as count
            FROM patients
            GROUP BY age_group
            ORDER BY MIN(age)
        """
        return self.execute_query(query)
    
    def get_visits_distribution(self):
        query = """
            SELECT 
                visits_2_years,
                COUNT(*) as count
            FROM patients
            GROUP BY visits_2_years
            ORDER BY visits_2_years
        """
        return self.execute_query(query)
    
    def get_patients_by_specialty(self):
        query = """
            SELECT 
                d.specialty,
                COUNT(p.patient_id) as patient_count
            FROM doctors d
            LEFT JOIN patients p ON d.doctor_id = p.doctor_id
            GROUP BY d.specialty
            ORDER BY patient_count DESC
        """
        return self.execute_query(query)
    
    def get_complete_demographics(self):
        query = """
            SELECT 
                COUNT(*) as total_patients,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age,
                SUM(CASE WHEN sexe = 'M' THEN 1 ELSE 0 END) as male_patients,
                SUM(CASE WHEN sexe = 'F' THEN 1 ELSE 0 END) as female_patients,
                SUM(visits_2_years) as total_visits,
                AVG(visits_2_years) as avg_visits,
                MAX(visits_2_years) as max_visits,
                COUNT(DISTINCT doctor_id) as active_doctors
            FROM patients
        """
        return self.execute_query(query)
    
    def get_doctor_performance(self):
        query = """
            SELECT 
                d.doctor_id,
                d.first_name,
                d.last_name,
                d.specialty,
                COUNT(p.patient_id) as total_patients,
                AVG(p.visits_2_years) as avg_visits_per_patient,
                MIN(p.age) as youngest_patient,
                MAX(p.age) as oldest_patient,
                AVG(p.age) as avg_patient_age,
                SUM(p.visits_2_years) as total_visits
            FROM doctors d
            LEFT JOIN patients p ON d.doctor_id = p.doctor_id
            GROUP BY d.doctor_id
            ORDER BY total_patients DESC
        """
        return self.execute_query(query)
    
    def get_patient_by_id(self, patient_id):
        query = """
            SELECT 
                p.*,
                d.first_name as doctor_first,
                d.last_name as doctor_last,
                d.specialty
            FROM patients p
            LEFT JOIN doctors d ON p.doctor_id = d.doctor_id
            WHERE p.patient_id = %s
        """
        result = self.execute_query(query, (patient_id,))
        return result[0] if result else None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

# ============================================
# GRAPH DATA METHODS
# ============================================

    def get_age_distribution(self):
        """Age distribution histogram data"""
        query = """
            SELECT 
                CASE 
                    WHEN age < 18 THEN '0-17'
                    WHEN age BETWEEN 18 AND 30 THEN '18-30'
                    WHEN age BETWEEN 31 AND 50 THEN '31-50'
                    WHEN age BETWEEN 51 AND 65 THEN '51-65'
                    ELSE '65+'
                END as age_group,
                COUNT(*) as count
            FROM patients
            GROUP BY age_group
            ORDER BY MIN(age)
        """
        return self.execute_query(query)

    def get_gender_distribution(self):
        """Gender distribution pie chart data"""
        query = """
            SELECT 
                sexe,
                COUNT(*) as count
            FROM patients
            GROUP BY sexe
        """
        return self.execute_query(query)

    def get_age_gender_stacked(self):
        """Age vs Gender stacked bar chart data"""
        query = """
            SELECT 
                CASE 
                    WHEN age < 18 THEN '0-17'
                    WHEN age BETWEEN 18 AND 30 THEN '18-30'
                    WHEN age BETWEEN 31 AND 50 THEN '31-50'
                    WHEN age BETWEEN 51 AND 65 THEN '51-65'
                    ELSE '65+'
                END as age_group,
                SUM(CASE WHEN sexe = 'M' THEN 1 ELSE 0 END) as male,
                SUM(CASE WHEN sexe = 'F' THEN 1 ELSE 0 END) as female
            FROM patients
            GROUP BY age_group
            ORDER BY MIN(age)
        """
        return self.execute_query(query)

    def get_patients_by_doctor(self):
        """Patients by doctor bar chart data"""
        query = """
            SELECT 
                d.doctor_id,
                d.first_name,
                d.last_name,
                COUNT(p.patient_id) as patient_count
            FROM doctors d
            LEFT JOIN patients p ON d.doctor_id = p.doctor_id
            GROUP BY d.doctor_id
            ORDER BY patient_count DESC
        """
        return self.execute_query(query)

    def get_patients_by_specialty(self):
        """Patients by specialty bar chart data"""
        query = """
            SELECT 
                d.specialty,
                COUNT(p.patient_id) as patient_count
            FROM doctors d
            LEFT JOIN patients p ON d.doctor_id = p.doctor_id
            GROUP BY d.specialty
            ORDER BY patient_count DESC
        """
        return self.execute_query(query)

    def get_visit_distribution(self):
        """Visit distribution histogram data"""
        query = """
            SELECT 
                visits_2_years,
                COUNT(*) as count
            FROM patients
            GROUP BY visits_2_years
            ORDER BY visits_2_years
        """
        return self.execute_query(query)

    def get_high_risk_distribution(self):
        """High risk vs normal patients donut chart data"""
        query = """
            SELECT 
                CASE 
                    WHEN age >= 65 OR visits_2_years >= 20 THEN 'High Risk'
                    ELSE 'Normal'
                END as risk_category,
                COUNT(*) as count
            FROM patients
            GROUP BY risk_category
        """
        return self.execute_query(query)

    def get_visits_by_age_group(self):
        """Average visits per age group line chart data"""
        query = """
            SELECT 
                CASE 
                    WHEN age < 18 THEN '0-17'
                    WHEN age BETWEEN 18 AND 30 THEN '18-30'
                    WHEN age BETWEEN 31 AND 50 THEN '31-50'
                    WHEN age BETWEEN 51 AND 65 THEN '51-65'
                    ELSE '65+'
                END as age_group,
                AVG(visits_2_years) as avg_visits
            FROM patients
            GROUP BY age_group
            ORDER BY MIN(age)
        """
        return self.execute_query(query)

    def get_appointment_status(self):
        """Appointment status pie chart data"""
        query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM appointments
            GROUP BY status
        """
        return self.execute_query(query)

    def get_appointments_by_doctor(self):
        """Appointments by doctor bar chart data"""
        query = """
            SELECT 
                d.first_name,
                d.last_name,
                COUNT(a.appointment_id) as appointment_count
            FROM doctors d
            LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id
            ORDER BY appointment_count DESC
        """
        return self.execute_query(query)

    def get_appointments_by_month(self):
        """Appointments by month line chart data"""
        query = """
            SELECT 
                DATE_FORMAT(appointment_date, '%Y-%m') as month,
                COUNT(*) as appointment_count
            FROM appointments
            GROUP BY DATE_FORMAT(appointment_date, '%Y-%m')
            ORDER BY month
        """
        return self.execute_query(query)

    def get_doctor_performance(self):
        """Doctor performance radar chart data"""
        query = """
            SELECT 
                d.first_name,
                d.last_name,
                COUNT(DISTINCT p.patient_id) as total_patients,
                SUM(p.visits_2_years) as total_visits,
                COUNT(a.appointment_id) as total_appointments
            FROM doctors d
            LEFT JOIN patients p ON d.doctor_id = p.doctor_id
            LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id
            ORDER BY total_patients DESC
            LIMIT 5
        """
        return self.execute_query(query)

    def get_patient_summary(self):
        """Patient demographics summary dashboard data"""
        query = """
            SELECT 
                COUNT(*) as total_patients,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age,
                SUM(CASE WHEN sexe = 'M' THEN 1 ELSE 0 END) as male_count,
                SUM(CASE WHEN sexe = 'F' THEN 1 ELSE 0 END) as female_count,
                AVG(visits_2_years) as avg_visits
            FROM patients
        """
        return self.execute_query(query)


# ============================================
# CREATE DATABASE INSTANCE
# ============================================

db = Database()