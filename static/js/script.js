// ============================================
// AIN ATIQ HEALTH DEPARTMENT - MAIN JAVASCRIPT
// Complete functionality for all pages
// ============================================

// ============================================
// 1. LOGIN PAGE BEHAVIOR
// ============================================

// Toggle password visibility
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? '👁️' : '🙈';
    });
}

// Login form validation and loading state
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
        
        // Show loading state
        if (loginBtn) {
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline';
            loginBtn.disabled = true;
        }
    });
}

// Show error function
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.innerHTML = `<span class="error-icon">⚠️</span> ${message}`;
        errorDiv.style.display = 'flex';
        errorDiv.style.opacity = '1';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.transition = 'opacity 0.5s ease';
            errorDiv.style.opacity = '0';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 500);
        }, 5000);
    } else {
        alert(message);
    }
}

// Remember me functionality
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

// ============================================
// 2. DASHBOARD CHARTS
// ============================================

// Helper to get color palette
function getColors(count) {
    const colors = [
        '#006A4E', '#00856A', '#00A38A', '#4CAF50', 
        '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9',
        '#2E7D32', '#388E3C', '#43A047', '#4CAF50',
        '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9'
    ];
    return colors.slice(0, count);
}

// Helper to get random colors for charts
function getRandomColors(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        const hue = Math.floor(Math.random() * 360);
        colors.push(`hsl(${hue}, 70%, 55%)`);
    }
    return colors;
}

// ============================================
// DOCTOR CHART
// ============================================
const doctorChartEl = document.getElementById('doctorChart');
if (doctorChartEl && typeof patientsByDoctor !== 'undefined' && patientsByDoctor && patientsByDoctor.length > 0) {
    const labels = patientsByDoctor.map(d => {
        const firstName = d.doctor_first || '';
        const lastName = d.doctor_last || '';
        return `${firstName} ${lastName}`.trim() || 'Unassigned';
    });
    const data = patientsByDoctor.map(d => d.patient_count || 0);
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
                barPercentage: 0.7
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
                    ticks: { stepSize: 1 },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        maxRotation: 45,
                        minRotation: 30,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}

// ============================================
// AGE GROUP CHART
// ============================================
const ageChartEl = document.getElementById('ageChart');
if (ageChartEl && typeof ageGroups !== 'undefined' && ageGroups && ageGroups.length > 0) {
    const labels = ageGroups.map(g => g.age_group || 'Unknown');
    const data = ageGroups.map(g => g.count || 0);
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
                        pointStyle: 'circle',
                        font: { size: 11 }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

// ============================================
// VISIT CHART
// ============================================
const visitChartEl = document.getElementById('visitChart');
if (visitChartEl && typeof visits !== 'undefined' && visits && visits.length > 0) {
    const labels = visits.map(v => v.visits_2_years || 0);
    const data = visits.map(v => v.count || 0);
    
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
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2
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
                        text: 'Visits (2 years)',
                        font: { weight: 'bold' }
                    },
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Patients',
                        font: { weight: 'bold' }
                    },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                }
            }
        }
    });
}

// ============================================
// SPECIALTY CHART
// ============================================
const specialtyChartEl = document.getElementById('specialtyChart');
if (specialtyChartEl && typeof patientsBySpecialty !== 'undefined' && patientsBySpecialty && patientsBySpecialty.length > 0) {
    const labels = patientsBySpecialty.map(s => s.specialty || 'Unknown');
    const data = patientsBySpecialty.map(s => s.patient_count || 0);
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
                barPercentage: 0.7
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
                    ticks: { stepSize: 1 },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                y: {
                    grid: { display: false },
                    ticks: { font: { size: 10 } }
                }
            }
        }
    });
}

// ============================================
// 3. PATIENTS PAGE - FILTER FUNCTIONALITY
// ============================================

// Toggle filters visibility
function toggleFilters() {
    const grid = document.querySelector('.filter-grid');
    const btn = document.querySelector('.toggle-filters');
    if (grid) {
        if (grid.style.display === 'none') {
            grid.style.display = 'grid';
            if (btn) btn.textContent = '▲ Hide Filters';
        } else {
            grid.style.display = 'none';
            if (btn) btn.textContent = '▼ Show Filters';
        }
    }
}

// Remove a specific filter
function removeFilter(label) {
    const paramMap = {
        'Name Search': 'search_name',
        'Phone Search': 'search_phone',
        'Email Search': 'search_email',
        'Address Search': 'search_address',
        'Doctor ID': 'doctor_id',
        'Specialty': 'specialty',
        'Doctor Gender': 'doctor_sexe',
        'Doctor Min Age': 'doctor_age_min',
        'Doctor Max Age': 'doctor_age_max',
        'Min Age': 'age_min',
        'Max Age': 'age_max',
        'Gender': 'sexe',
        'Birth From': 'dob_from',
        'Birth To': 'dob_to',
        'Min Visits': 'visits_min',
        'Max Visits': 'visits_max',
        'Admission From': 'admission_date_from',
        'Admission To': 'admission_date_to',
        'Status': 'status',
        'Has Appointment': 'has_appointment',
        'High Risk': 'is_high_risk'
    };
    
    const param = paramMap[label];
    if (param) {
        const url = new URL(window.location.href);
        url.searchParams.delete(param);
        window.location.href = url.toString();
    }
}

// Apply filter preset
const filterPresets = {
    'high_risk': {
        label: 'High Risk Patients',
        params: {
            is_high_risk: 'true',
            sort_by: 'age',
            sort_direction: 'DESC'
        }
    },
    'frequent_visitors': {
        label: 'Frequent Visitors',
        params: {
            visits_min: '10',
            sort_by: 'visits_2_years',
            sort_direction: 'DESC'
        }
    },
    'senior_patients': {
        label: 'Senior Patients (65+)',
        params: {
            age_min: '65',
            sort_by: 'age',
            sort_direction: 'DESC'
        }
    },
    'no_appointments': {
        label: 'Patients with No Appointments',
        params: {
            has_appointment: 'false'
        }
    },
    'active_patients': {
        label: 'Active Patients',
        params: {
            status: 'active'
        }
    },
    'inactive_patients': {
        label: 'Inactive Patients',
        params: {
            status: 'inactive'
        }
    },
    'female_patients': {
        label: 'Female Patients',
        params: {
            sexe: 'F'
        }
    },
    'male_patients': {
        label: 'Male Patients',
        params: {
            sexe: 'M'
        }
    }
};

function applyPreset(presetName) {
    const preset = filterPresets[presetName];
    if (!preset) return;
    
    const url = new URL(window.location.href);
    Object.keys(preset.params).forEach(key => {
        url.searchParams.set(key, preset.params[key]);
    });
    window.location.href = url.toString();
}

// ============================================
// 4. AJAX FILTERS - Real-time filtering
// ============================================

const applyFilterBtn = document.getElementById('applyFilterBtn');
if (applyFilterBtn) {
    applyFilterBtn.addEventListener('click', async function(e) {
        e.preventDefault();
        
        const specialty = document.getElementById('filterSpecialty')?.value || '';
        const ageMin = document.getElementById('filterAgeMin')?.value || '';
        const ageMax = document.getElementById('filterAgeMax')?.value || '';
        const sexe = document.getElementById('filterSexe')?.value || '';
        
        const filterData = { 
            specialty, 
            age_min: ageMin, 
            age_max: ageMax, 
            sexe 
        };
        
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
            showError('Error applying filters. Please try again.');
        }
    });
}

// Display filter results in a table
function displayFilterResults(patients) {
    const container = document.getElementById('patientTableContainer');
    const resultsDiv = document.getElementById('filterResults');
    
    if (!container || !resultsDiv) return;
    
    if (!patients || patients.length === 0) {
        resultsDiv.style.display = 'block';
        container.innerHTML = `<div class="no-results">
            <span class="no-results-icon">🔍</span>
            <h3>No patients found</h3>
            <p>Try adjusting your filters or search criteria</p>
        </div>`;
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
                <td>${p.patient_id || 'N/A'}</td>
                <td>${p.first_name || 'N/A'}</td>
                <td>${p.last_name || 'N/A'}</td>
                <td>${p.age || 'N/A'}</td>
                <td>${p.sexe || 'N/A'}</td>
                <td>
                    <span class="visit-badge ${p.visits_2_years > 10 ? 'high' : p.visits_2_years > 5 ? 'medium' : 'low'}">
                        ${p.visits_2_years || 0}
                    </span>
                </td>
                <td>${p.doctor_first || ''} ${p.doctor_last || ''}</td>
                <td>${p.specialty || 'N/A'}</td>
            </tr>
        `;
    });
    
    tableHTML += `</tbody></table>`;
    tableHTML += `<p style="margin-top:12px;color:#6b8a7a;font-size:14px;">Showing ${patients.length} patient(s)</p>`;
    
    container.innerHTML = tableHTML;
    resultsDiv.style.display = 'block';
}

// ============================================
// 5. EXPORT FUNCTIONALITY
// ============================================

function exportData() {
    const currentUrl = new URL(window.location.href);
    const exportUrl = '/export/patients' + currentUrl.search;
    window.location.href = exportUrl;
}

function printResults() {
    window.print();
}

// ============================================
// 6. KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', function(e) {
    // Ctrl + F to focus on search (Patients page)
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        const searchInput = document.querySelector('input[name="search_name"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
    }
    
    // Ctrl + R to reset filters
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        const pathname = window.location.pathname;
        if (pathname === '/patients' || pathname === '/patients/') {
            e.preventDefault();
            window.location.href = window.location.pathname;
        }
    }
    
    // Ctrl + Enter to submit login
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            e.preventDefault();
            loginForm.dispatchEvent(new Event('submit'));
        }
    }
});

// ============================================
// 7. AUTO-SUBMIT FOR FILTERS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        // Auto-submit on select changes (except text inputs)
        const selects = filterForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', function() {
                if (this.name === 'sort_by' || this.name === 'sort_direction' || this.name === 'limit') {
                    filterForm.submit();
                }
            });
        });
        
        // Submit on Enter key (except text inputs)
        const inputs = filterForm.querySelectorAll('input');
        inputs.forEach(input => {
            if (input.type !== 'text') {
                input.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        filterForm.submit();
                    }
                });
            }
        });
    }
});

// ============================================
// 8. STATISTICS PAGE - ADDITIONAL CHARTS
// ============================================

// Create a chart for doctor performance
const performanceChartEl = document.getElementById('performanceChart');
if (performanceChartEl && typeof doctorPerformance !== 'undefined' && doctorPerformance && doctorPerformance.length > 0) {
    const labels = doctorPerformance.map(d => `${d.first_name || ''} ${d.last_name || ''}`.trim());
    const data = doctorPerformance.map(d => d.total_patients || 0);
    const colors = getColors(data.length);
    
    new Chart(performanceChartEl, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Patients',
                data: data,
                backgroundColor: colors,
                borderRadius: 6,
                borderSkipped: false
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
                    ticks: { stepSize: 1 },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        maxRotation: 45,
                        minRotation: 30,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}

// ============================================
// 9. TOOLTIP FUNCTIONALITY
// ============================================

function showTooltip(element, message) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = message;
    
    const rect = element.getBoundingClientRect();
    tooltip.style.position = 'fixed';
    tooltip.style.top = (rect.top - 40) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2 - 60) + 'px';
    tooltip.style.background = '#1a2a2a';
    tooltip.style.color = 'white';
    tooltip.style.padding = '6px 12px';
    tooltip.style.borderRadius = '6px';
    tooltip.style.fontSize = '12px';
    tooltip.style.zIndex = '1000';
    tooltip.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    tooltip.style.pointerEvents = 'none';
    
    document.body.appendChild(tooltip);
    
    setTimeout(() => {
        tooltip.remove();
    }, 2000);
}

// ============================================
// 10. CONSOLE WELCOME MESSAGE
// ============================================

console.log('🏥 =========================================');
console.log('🏥  Ain Atiq Health Department');
console.log('🏥  Version 2.0');
console.log('🏥  © 2024 All Rights Reserved');
console.log('🏥 =========================================');
console.log('📊 Connected to hospital database');
console.log('🔐 Secure session management active');

// ============================================
// 11. RESPONSIVE TABLE HANDLING
// ============================================

function handleResponsiveTables() {
    const tables = document.querySelectorAll('.patient-table');
    const isMobile = window.innerWidth < 768;
    
    tables.forEach(table => {
        if (isMobile) {
            table.classList.add('mobile-table');
        } else {
            table.classList.remove('mobile-table');
        }
    });
}

window.addEventListener('resize', handleResponsiveTables);
document.addEventListener('DOMContentLoaded', handleResponsiveTables);

// ============================================
// 12. TOAST NOTIFICATIONS
// ============================================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;
    
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: ${type === 'success' ? '#006A4E' : type === 'error' ? '#dc2626' : '#1a2a2a'};
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        max-width: 400px;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ============================================
// 13. CONFIRM DIALOG
// ============================================

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// ============================================
// 14. LOADING SPINNER
// ============================================

function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    overlay.innerHTML = `
        <div style="text-align:center;">
            <div style="width:50px;height:50px;border:4px solid #e8efec;border-top-color:#006A4E;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto;"></div>
            <p style="margin-top:16px;color:#1a2a2a;font-weight:600;">Loading...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// ============================================
// 15. ADD CSS ANIMATIONS
// ============================================

const styleSheet = document.createElement("style");
styleSheet.textContent = `
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .animate-pulse {
        animation: pulse 2s infinite;
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease;
    }
`;

document.head.appendChild(styleSheet);

// ============================================
// 16. DARK MODE TOGGLE (Optional)
// ============================================

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    
    const btn = document.getElementById('darkModeToggle');
    if (btn) {
        btn.textContent = isDark ? '☀️' : '🌙';
    }
}

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// ============================================
// 17. DATE HELPER FUNCTIONS
// ============================================

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateFull(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getAgeFromDOB(dob) {
    if (!dob) return null;
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

// ============================================
// 18. SEARCH HIGHLIGHTING
// ============================================

function highlightText(text, searchTerm) {
    if (!searchTerm || !text) return text;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark class="highlight">$1</mark>');
}

// ============================================
// 19. SMOOTH SCROLLING
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ============================================
// 20. INITIALIZATION
// ============================================

console.log('✅ All scripts loaded successfully');
console.log('📅 Current time:', new Date().toLocaleString());