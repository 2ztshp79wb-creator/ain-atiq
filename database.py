import mysql.connector
from mysql.connector import Error

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
            print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            cursor.close()
    
    def get_doctor_by_credentials(self, doctor_id, password):
        query = "SELECT * FROM doctor_credentials WHERE doctor_id = %s AND password = %s"
        result = self.execute_query(query, (doctor_id, password))
        return result[0] if result else None
    
    def get_all_doctors(self):
        query = "SELECT * FROM doctor_credentials"
        return self.execute_query(query)
    
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
            d.first_name as doctor_first,
            d.last_name as doctor_last,
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
    
    def filter_patients(self, specialty=None, age_min=None, age_max=None, sexe=None):
        query = """
        SELECT 
            p.patient_id,
            p.first_name,
            p.last_name,
            p.age,
            p.sexe,
            p.visits_2_years,
            d.first_name as doctor_first,
            d.last_name as doctor_last,
            d.specialty
        FROM patients p
        JOIN doctors d ON p.doctor_id = d.doctor_id
        WHERE 1=1
        """
        params = []
        
        if specialty:
            query += " AND d.specialty = %s"
            params.append(specialty)
        if age_min:
            query += " AND p.age >= %s"
            params.append(age_min)
        if age_max:
            query += " AND p.age <= %s"
            params.append(age_max)
        if sexe:
            query += " AND p.sexe = %s"
            params.append(sexe)
        
        return self.execute_query(query, params)

db = Database()