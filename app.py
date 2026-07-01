from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
from datetime import datetime, timedelta
from database import db
from audit import AuditLogger

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'

audit = AuditLogger(db)

# ============================================
# HOME & LOGIN ROUTES
# ============================================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        password = request.form.get('password')
        
        if not doctor_id or not password:
            return render_template('login.html', error='Please enter both ID and password')
        
        user = db.get_doctor_by_credentials(int(doctor_id), password)
        
        if user:
            session['doctor_id'] = user['doctor_id']
            session['role'] = user['role']
            session['name'] = user.get('first_name', 'Doctor')
            
            audit.log_login(doctor_id, True, request.remote_addr, request.headers.get('User-Agent'))
            return redirect(url_for('dashboard'))
        else:
            audit.log_login(doctor_id, False, request.remote_addr, request.headers.get('User-Agent'))
            return render_template('login.html', error='Invalid credentials. Please try again.')
    
    return render_template('login.html')


# ============================================
# DASHBOARD ROUTE
# ============================================

import json

@app.route('/dashboard')
def dashboard():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    # Get statistics for the dashboard
    stats = db.get_patient_statistics()
    patients_by_doctor = db.get_patients_by_doctor()
    age_groups = db.get_patients_by_age_group()
    visits = db.get_visits_distribution()
    
    # Ensure data is not None
    if patients_by_doctor is None:
        patients_by_doctor = []
    if age_groups is None:
        age_groups = []
    if visits is None:
        visits = []
    
    return render_template('dashboard.html', 
                         stats=stats[0] if stats else None,
                         patients_by_doctor=json.dumps(patients_by_doctor),
                         age_groups=json.dumps(age_groups),
                         visits=json.dumps(visits))


# ============================================
# PATIENTS LIST WITH 20 FILTERS
# ============================================

@app.route('/patients')
def patients():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    # ALL 20 FILTERS - Captured from URL
    filters = {
        # 1. BASIC SEARCH
        'search_name': request.args.get('search_name', ''),
        'search_phone': request.args.get('search_phone', ''),
        'search_email': request.args.get('search_email', ''),
        'search_address': request.args.get('search_address', ''),
        
        # 2. DOCTOR & SPECIALTY
        'doctor_id': request.args.get('doctor_id'),
        'specialty': request.args.get('specialty'),
        'doctor_sexe': request.args.get('doctor_sexe'),
        'doctor_age_min': request.args.get('doctor_age_min'),
        'doctor_age_max': request.args.get('doctor_age_max'),
        
        # 3. PATIENT DEMOGRAPHICS
        'age_min': request.args.get('age_min'),
        'age_max': request.args.get('age_max'),
        'sexe': request.args.get('sexe'),
        'dob_from': request.args.get('dob_from'),
        'dob_to': request.args.get('dob_to'),
        
        # 4. PATIENT ACTIVITY
        'visits_min': request.args.get('visits_min'),
        'visits_max': request.args.get('visits_max'),
        'admission_date_from': request.args.get('admission_date_from'),
        'admission_date_to': request.args.get('admission_date_to'),
        'status': request.args.get('status'),
        
        # 5. ADVANCED METRICS
        'has_appointment': request.args.get('has_appointment'),
        'is_high_risk': request.args.get('is_high_risk'),
        
        # 6. SORTING & PAGINATION
        'sort_by': request.args.get('sort_by', 'last_name'),
        'sort_direction': request.args.get('sort_direction', 'ASC'),
        'limit': request.args.get('limit', 100),
        'page': request.args.get('page', 1)
    }
    
    # Get filtered patients
    patients = db.filter_patients_20_filters(filters)
    
    # Get all doctors for filter dropdown
    all_doctors = db.get_all_doctors()
    all_specialties = db.get_all_specialties()
    
    # Get filter stats
    filter_summary = db.get_filter_summary(filters)
    
    # Ensure data is not None
    if patients is None:
        patients = []
    if all_doctors is None:
        all_doctors = []
    if all_specialties is None:
        all_specialties = []
    
    return render_template('patients.html',
                         patients=patients,
                         all_doctors=all_doctors,
                         all_specialties=all_specialties,
                         filters=filters,
                         filter_summary=filter_summary)


# ============================================
# PATIENT DETAIL ROUTE
# ============================================

@app.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    patient = db.get_patient_by_id(patient_id)
    if not patient:
        return "Patient not found", 404
    
    audit.log_view(session['doctor_id'], 'patients', patient_id, 
                   request.remote_addr, request.headers.get('User-Agent'))
    
    return render_template('patient_detail.html', patient=patient)


# ============================================
# STATISTICS ROUTE
# ============================================

@app.route('/statistics')
def statistics():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    stats = db.get_patient_statistics()
    patients_by_doctor = db.get_patients_by_doctor()
    age_groups = db.get_patients_by_age_group()
    visits = db.get_visits_distribution()
    patients_by_specialty = db.get_patients_by_specialty()
    demographics = db.get_complete_demographics()
    doctor_performance = db.get_doctor_performance()
    
    # Ensure data is not None
    if patients_by_doctor is None:
        patients_by_doctor = []
    if age_groups is None:
        age_groups = []
    if visits is None:
        visits = []
    if patients_by_specialty is None:
        patients_by_specialty = []
    if doctor_performance is None:
        doctor_performance = []
    
    return render_template('statistics.html',
                         stats=stats[0] if stats else None,
                         patients_by_doctor=json.dumps(patients_by_doctor),
                         age_groups=json.dumps(age_groups),
                         visits=json.dumps(visits),
                         patients_by_specialty=json.dumps(patients_by_specialty),
                         demographics=demographics[0] if demographics else None,
                         doctor_performance=doctor_performance)


# ============================================
# ABOUT ROUTE
# ============================================

@app.route('/about')
def about():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')


# ============================================
# LOGOUT ROUTE
# ============================================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ============================================
# API ROUTES FOR AJAX FILTERS
# ============================================

@app.route('/api/patients/filter', methods=['POST'])
def api_filter_patients():
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    filters = {
        'search_name': data.get('search_name', ''),
        'search_phone': data.get('search_phone', ''),
        'search_email': data.get('search_email', ''),
        'search_address': data.get('search_address', ''),
        'doctor_id': data.get('doctor_id'),
        'specialty': data.get('specialty'),
        'doctor_sexe': data.get('doctor_sexe'),
        'doctor_age_min': data.get('doctor_age_min'),
        'doctor_age_max': data.get('doctor_age_max'),
        'age_min': data.get('age_min'),
        'age_max': data.get('age_max'),
        'sexe': data.get('sexe'),
        'dob_from': data.get('dob_from'),
        'dob_to': data.get('dob_to'),
        'visits_min': data.get('visits_min'),
        'visits_max': data.get('visits_max'),
        'admission_date_from': data.get('admission_date_from'),
        'admission_date_to': data.get('admission_date_to'),
        'status': data.get('status'),
        'has_appointment': data.get('has_appointment'),
        'is_high_risk': data.get('is_high_risk'),
        'sort_by': data.get('sort_by', 'last_name'),
        'sort_direction': data.get('sort_direction', 'ASC'),
        'limit': data.get('limit', 100),
        'page': data.get('page', 1)
    }
    
    patients = db.filter_patients_20_filters(filters)
    
    # Ensure data is not None
    if patients is None:
        patients = []
    
    audit.log(session['doctor_id'], 'FILTER_APPLIED', 'patients',
              ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'))
    
    return jsonify(patients)


# ============================================
# AUDIT LOGS ROUTE (CEO Only)
# ============================================

@app.route('/audit_logs')
def audit_logs():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    user = db.execute_query(
        "SELECT role FROM doctor_credentials WHERE doctor_id = %s", 
        (session['doctor_id'],)
    )
    
    if not user or user[0]['role'] != 'ceo':
        return "Access Denied", 403
    
    action = request.args.get('action')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    doctor_id = request.args.get('doctor_id')
    
    logs = audit.get_logs(
        doctor_id=doctor_id,
        action=action,
        from_date=from_date,
        to_date=to_date,
        limit=200
    )
    
    # Ensure data is not None
    if logs is None:
        logs = []
    
    return render_template('audit_logs.html', logs=logs)


# ============================================
# EXPORT FILTERED DATA (CEO Only)
# ============================================

@app.route('/export/patients')
def export_patients():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    user = db.execute_query(
        "SELECT role FROM doctor_credentials WHERE doctor_id = %s", 
        (session['doctor_id'],)
    )
    
    if not user or user[0]['role'] != 'ceo':
        return "Access Denied", 403
    
    # Get all filters from URL
    filters = {
        'search_name': request.args.get('search_name', ''),
        'search_phone': request.args.get('search_phone', ''),
        'search_email': request.args.get('search_email', ''),
        'search_address': request.args.get('search_address', ''),
        'doctor_id': request.args.get('doctor_id'),
        'specialty': request.args.get('specialty'),
        'age_min': request.args.get('age_min'),
        'age_max': request.args.get('age_max'),
        'sexe': request.args.get('sexe'),
        'visits_min': request.args.get('visits_min'),
        'visits_max': request.args.get('visits_max'),
        'dob_from': request.args.get('dob_from'),
        'dob_to': request.args.get('dob_to'),
        'status': request.args.get('status'),
    }
    
    patients = db.filter_patients_20_filters(filters, limit=10000)
    
    # Ensure data is not None
    if patients is None:
        patients = []
    
    # Generate CSV
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['ID', 'First Name', 'Last Name', 'Age', 'Sexe', 'Phone', 'Email', 
                     'Address', 'Visits (2 Years)', 'Doctor', 'Specialty'])
    
    for p in patients:
        writer.writerow([
            p['patient_id'], p['first_name'], p['last_name'], 
            p['age'], p['sexe'], p['phone'], p['email'],
            p['address'], p['visits_2_years'],
            f"{p.get('doctor_first', '')} {p.get('doctor_last', '')}",
            p.get('specialty', '')
        ])
    
    output.seek(0)
    
    response = app.response_class(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=patients_export.csv'}
    )
    
    audit.log(session['doctor_id'], 'EXPORT_DATA', 'patients',
              ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'))
    
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)