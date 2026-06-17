
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? '👁️' : '🙈';
    });
}


const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const btnText = document.querySelector('.btn-text');
const btnSpinner = document.querySelector('.btn-spinner');

if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        const doctorId = document.getElementById('doctor_id');
        const password = document.getElementById('password');
        
        if (!doctorId.value.trim() || !password.value.trim()) {
            e.preventDefault();
            showError('Please fill in all fields');
            return;
        }
        
        if (doctorId.value < 1) {
            e.preventDefault();
            showError('Please enter a valid Doctor ID');
            return;
        }
        
        
        if (loginBtn) {
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline';
            loginBtn.disabled = true;
        }
    });
}


function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.innerHTML = `<span class="error-icon">⚠️</span> ${message}`;
        errorDiv.style.display = 'flex';
    } else {
        alert(message);
    }
}


const rememberMe = document.getElementById('rememberMe');
if (rememberMe && localStorage.getItem('rememberedId')) {
    document.getElementById('doctor_id').value = localStorage.getItem('rememberedId');
    rememberMe.checked = true;
}

if (rememberMe) {
    rememberMe.addEventListener('change', function() {
        if (this.checked) {
            const id = document.getElementById('doctor_id').value;
            localStorage.setItem('rememberedId', id);
        } else {
            localStorage.removeItem('rememberedId');
        }
    });
}


function getColors(count) {
    const colors = [
        '#006A4E', '#00856A', '#00A38A', '#4CAF50', 
        '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9'
    ];
    return colors.slice(0, count);
}


const doctorChartEl = document.getElementById('doctorChart');
if (doctorChartEl && typeof patientsByDoctor !== 'undefined' && patientsByDoctor.length > 0) {
    const labels = patientsByDoctor.map(d => `${d.doctor_first} ${d.doctor_last}`);
    const data = patientsByDoctor.map(d => d.patient_count);
    const colors = getColors(data.length);
    
    new Chart(doctorChartEl, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Patients',
                data: data,
                backgroundColor: colors,
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
}


const ageChartEl = document.getElementById('ageChart');
if (ageChartEl && typeof ageGroups !== 'undefined' && ageGroups.length > 0) {
    const labels = ageGroups.map(g => g.age_group);
    const data = ageGroups.map(g => g.count);
    const colors = getColors(data.length);
    
    new Chart(ageChartEl, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 12,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            }
        }
    });
}


const visitChartEl = document.getElementById('visitChart');
if (visitChartEl && typeof visits !== 'undefined' && visits.length > 0) {
    const labels = visits.map(v => v.visits_2_years);
    const data = visits.map(v => v.count);
    
    new Chart(visitChartEl, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Patients',
                data: data,
                borderColor: '#006A4E',
                backgroundColor: 'rgba(0, 106, 78, 0.1)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#006A4E',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Visits (2 years)'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Patients'
                    }
                }
            }
        }
    });
}


const specialtyChartEl = document.getElementById('specialtyChart');
if (specialtyChartEl && typeof patientsBySpecialty !== 'undefined' && patientsBySpecialty.length > 0) {
    const labels = patientsBySpecialty.map(s => s.specialty);
    const data = patientsBySpecialty.map(s => s.patient_count);
    const colors = getColors(data.length);
    
    new Chart(specialtyChartEl, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Patients',
                data: data,
                backgroundColor: colors,
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
}



const applyFilterBtn = document.getElementById('applyFilterBtn');
if (applyFilterBtn) {
    applyFilterBtn.addEventListener('click', async function() {
        const specialty = document.getElementById('filterSpecialty')?.value || '';
        const ageMin = document.getElementById('filterAgeMin')?.value || '';
        const ageMax = document.getElementById('filterAgeMax')?.value || '';
        const sexe = document.getElementById('filterSexe')?.value || '';
        
        const filterData = { specialty, age_min: ageMin, age_max: ageMax, sexe };
        
        try {
            const response = await fetch('/api/patients/filter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(filterData)
            });
            
            const patients = await response.json();
            displayFilterResults(patients);
        } catch (error) {
            console.error('Error filtering patients:', error);
            alert('Error applying filters. Please try again.');
        }
    });
}

function displayFilterResults(patients) {
    const container = document.getElementById('patientTableContainer');
    const resultsDiv = document.getElementById('filterResults');
    
    if (!container || !resultsDiv) return;
    
    if (!patients || patients.length === 0) {
        resultsDiv.style.display = 'block';
        container.innerHTML = '<p style="text-align:center;color:#6b8a7a;padding:20px;">No patients found matching the criteria.</p>';
        return;
    }
    
    let tableHTML = `
        <table class="patient-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Age</th>
                    <th>Sexe</th>
                    <th>Visits</th>
                    <th>Doctor</th>
                    <th>Specialty</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    patients.forEach(p => {
        tableHTML += `
            <tr>
                <td>${p.patient_id}</td>
                <td>${p.first_name}</td>
                <td>${p.last_name}</td>
                <td>${p.age}</td>
                <td>${p.sexe}</td>
                <td>${p.visits_2_years}</td>
                <td>${p.doctor_first} ${p.doctor_last}</td>
                <td>${p.specialty}</td>
            </tr>
        `;
    });
    
    tableHTML += `</tbody></table>`;
    tableHTML += `<p style="margin-top:12px;color:#6b8a7a;font-size:14px;">Showing ${patients.length} patient(s)</p>`;
    
    container.innerHTML = tableHTML;
    resultsDiv.style.display = 'block';
    
  
    const style = document.createElement('style');
    style.textContent = `
        .patient-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            margin-top: 8px;
        }
        .patient-table th {
            background: #f0f7f5;
            color: #1a2a2a;
            font-weight: 600;
            padding: 10px 12px;
            text-align: left;
            border-bottom: 2px solid #d4e8e0;
        }
        .patient-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #eef4f1;
            color: #3d5a4a;
        }
        .patient-table tr:hover {
            background: #f8fbf9;
        }
    `;
    document.head.appendChild(style);
}


const errorMessage = document.getElementById('errorMessage');
if (errorMessage) {
    setTimeout(() => {
        errorMessage.style.transition = 'opacity 0.5s ease';
        errorMessage.style.opacity = '0';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 500);
    }, 5000);
}


document.addEventListener('keydown', function(e) {
    // Ctrl + Enter to submit login
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    }
});

console.log('🏥 Ain Atiq Health Department');
console.log('📊 Connected to hospital database');