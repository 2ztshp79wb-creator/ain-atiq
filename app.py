from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from database import db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this'  # Change this!

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
        
        # Check credentials
        user = db.get_doctor_by_credentials(int(doctor_id), password)
        
        if user:
            session['doctor_id'] = user['doctor_id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    stats = db.get_patient_statistics()
    patients_by_doctor = db.get_patients_by_doctor()
    age_groups = db.get_patients_by_age_group()
    visits = db.get_visits_distribution()
    
    return render_template('dashboard.html', 
                         stats=stats[0] if stats else None,
                         patients_by_doctor=patients_by_doctor,
                         age_groups=age_groups,
                         visits=visits)

@app.route('/about')
def about():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/statistics')
def statistics():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    
    stats = db.get_patient_statistics()
    patients_by_doctor = db.get_patients_by_doctor()
    age_groups = db.get_patients_by_age_group()
    visits = db.get_visits_distribution()
    patients_by_specialty = db.get_patients_by_specialty()
    
    return render_template('statistics.html',
                         stats=stats[0] if stats else None,
                         patients_by_doctor=json.dumps(patients_by_doctor),
                         age_groups=json.dumps(age_groups),
                         visits=json.dumps(visits),
                         patients_by_specialty=json.dumps(patients_by_specialty))

@app.route('/api/patients/filter', methods=['POST'])
def filter_patients():
    if 'doctor_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    
    
    
    
    data = request.json
    specialty = data.get('specialty')
    age_min = data.get('age_min')
    age_max = data.get('age_max')
    sexe = data.get('sexe')
    
    patients = db.filter_patients(specialty, age_min, age_max, sexe)
    return jsonify(patients)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)