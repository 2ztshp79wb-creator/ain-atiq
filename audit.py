import json
from datetime import datetime

class AuditLogger:
    def __init__(self, db):
        self.db = db
    
    def log(self, doctor_id, action, table_name=None, record_id=None, 
            old_value=None, new_value=None, ip_address=None, user_agent=None):
        """Log any action to the audit log"""
        
        if isinstance(old_value, dict):
            old_value = json.dumps(old_value)
        if isinstance(new_value, dict):
            new_value = json.dumps(new_value)
        
        query = """
            INSERT INTO audit_logs 
            (doctor_id, action, table_name, record_id, old_value, new_value, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.db.execute_query(query, (
            doctor_id, action, table_name, record_id, 
            old_value, new_value, ip_address, user_agent
        ))
    
    def log_login(self, doctor_id, success, ip_address, user_agent):
        action = 'LOGIN_SUCCESS' if success else 'LOGIN_FAILED'
        self.log(doctor_id, action, ip_address=ip_address, user_agent=user_agent)
    
    def log_update(self, doctor_id, table_name, record_id, old, new, ip_address, user_agent):
        self.log(doctor_id, 'UPDATE', table_name, record_id, old, new, ip_address, user_agent)
    
    def log_delete(self, doctor_id, table_name, record_id, old_value, ip_address, user_agent):
        self.log(doctor_id, 'DELETE', table_name, record_id, old_value, None, ip_address, user_agent)
    
    def log_view(self, doctor_id, table_name, record_id, ip_address, user_agent):
        self.log(doctor_id, 'VIEW', table_name, record_id, ip_address=ip_address, user_agent=user_agent)
    
    def get_logs(self, doctor_id=None, action=None, from_date=None, to_date=None, limit=100):
        query = """
            SELECT 
                al.log_id,
                al.action,
                al.table_name,
                al.record_id,
                al.old_value,
                al.new_value,
                al.ip_address,
                al.created_at,
                al.user_agent,
                d.first_name as doctor_first,
                d.last_name as doctor_last
            FROM audit_logs al
            LEFT JOIN doctors d ON al.doctor_id = d.doctor_id
            WHERE 1=1
        """
        params = []
        
        if doctor_id:
            query += " AND al.doctor_id = %s"
            params.append(doctor_id)
        
        if action:
            query += " AND al.action = %s"
            params.append(action)
        
        if from_date:
            query += " AND DATE(al.created_at) >= %s"
            params.append(from_date)
        
        if to_date:
            query += " AND DATE(al.created_at) <= %s"
            params.append(to_date)
        
        query += " ORDER BY al.created_at DESC LIMIT %s"
        params.append(limit)
        
        return self.db.execute_query(query, params)