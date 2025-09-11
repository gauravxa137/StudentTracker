// Combined JavaScript for Flask Student Tracker

// Global variables
let refreshTimer;
let refreshCount = 0;
const maxRefreshes = 3;

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    initializeBootstrapComponents();
    
    // Setup auto-refresh
    setupAutoRefresh();
    
    // Setup form enhancements
    setupFormEnhancements();
    
    // Setup table enhancements
    setupTableEnhancements();
    
    // Setup notification auto-hide
    setupNotificationAutoHide();
});

// Bootstrap Components Initialization
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
}

// Auto-refresh functionality
function setupAutoRefresh() {
    const autoRefresh = setInterval(function() {
        refreshCount++;
        console.log(`Student Tracker auto-refresh ${refreshCount}/${maxRefreshes}`);
        
        if (refreshCount >= maxRefreshes) {
            clearInterval(autoRefresh);
            console.log('Auto-refresh completed');
            return;
        }
        
        // Show notification
        showRefreshNotification();
        
        // Refresh after delay
        setTimeout(() => window.location.reload(), 2000);
    }, 240000); // 4 minutes
}

function showRefreshNotification() {
    const alert = document.createElement('div');
    alert.className = 'alert alert-info position-fixed top-0 end-0 m-3 alert-dismissible fade show';
    alert.style.zIndex = '1060';
    alert.innerHTML = `
        <i class="bi bi-arrow-clockwise me-2"></i>
        Refreshing for latest data...
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(alert);
}

// Statistics Modal Handler
function loadStats() {
    const modal = new bootstrap.Modal(document.getElementById('statsModal'));
    modal.show();
    
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            document.getElementById('statsContent').innerHTML = `
                <div class="row text-center">
                    <div class="col-4">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h4 class="text-primary mb-1">${data.total_students}</h4>
                                <small class="text-muted">Total Students</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h4 class="text-success mb-1">${data.total_grades}</h4>
                                <small class="text-muted">Total Grades</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h4 class="text-info mb-1">${data.overall_average}</h4>
                                <small class="text-muted">Avg Grade</small>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mt-3 text-center">
                    <small class="text-muted">
                        <i class="bi bi-info-circle me-1"></i>
                        Real-time statistics powered by Flask API
                    </small>
                </div>
            `;
        })
        .catch(error => {
            console.error('Stats loading error:', error);
            document.getElementById('statsContent').innerHTML = `
                <div class="alert alert-warning">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    Statistics temporarily unavailable. Please try again later.
                </div>
            `;
        });
}

// Form Enhancement Functions
function setupFormEnhancements() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
                submitBtn.disabled = true;
                form.classList.add('loading');
            }
        });
    });
    
    // Setup form validation
    setupFormValidation();
}

function setupFormValidation() {
    // Real-time validation for student form
    const nameInput = document.getElementById('name');
    const rollNumberInput = document.getElementById('roll_number');
    const gradeInput = document.getElementById('grade');
    const subjectInput = document.getElementById('subject');
    
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            validateName(this);
        });
    }
    
    if (rollNumberInput) {
        rollNumberInput.addEventListener('input', function() {
            validateRollNumber(this);
        });
    }
    
    if (gradeInput) {
        gradeInput.addEventListener('input', function() {
            const grade = parseFloat(this.value) || 0;
            updateGradeIndicator(grade);
            validateGrade(this);
        });
    }
    
    if (subjectInput) {
        subjectInput.addEventListener('input', function() {
            validateSubject(this);
        });
    }
}

// Validation Functions
function validateName(input) {
    const value = input.value.trim();
    const isValid = value.length >= 2 && value.length <= 100;
    
    updateValidationState(input, isValid);
    return isValid;
}

function validateRollNumber(input) {
    const value = input.value.trim();
    const pattern = /^[A-Za-z0-9\-_]+$/;
    const isValid = value.length >= 1 && value.length <= 20 && pattern.test(value);
    
    updateValidationState(input, isValid);
    return isValid;
}

function validateGrade(input) {
    const value = parseFloat(input.value);
    const isValid = !isNaN(value) && value >= 0 && value <= 100;
    
    updateValidationState(input, isValid);
    return isValid;
}

function validateSubject(input) {
    const value = input.value.trim();
    const isValid = value.length >= 2 && value.length <= 50;
    
    updateValidationState(input, isValid);
    return isValid;
}

function updateValidationState(input, isValid) {
    if (isValid) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
    }
}

// Grade Visual Indicator
function updateGradeIndicator(grade) {
    const gradeProgress = document.getElementById('gradeProgress');
    const gradeLabel = document.getElementById('gradeLabel');
    
    if (!gradeProgress || !gradeLabel) return;
    
    const percentage = Math.min(100, Math.max(0, grade));
    gradeProgress.style.width = percentage + '%';
    
    let label, className;
    if (grade >= 90) {
        label = 'Excellent (A+)';
        className = 'bg-success';
    } else if (grade >= 80) {
        label = 'Very Good (A)';
        className = 'bg-info';
    } else if (grade >= 70) {
        label = 'Good (B)';
        className = 'bg-primary';
    } else if (grade >= 60) {
        label = 'Satisfactory (C)';
        className = 'bg-warning';
    } else if (grade >= 50) {
        label = 'Pass (D)';
        className = 'bg-warning';
    } else if (grade > 0) {
        label = 'Fail (F)';
        className = 'bg-danger';
    } else {
        label = 'Enter a grade to see performance level';
        className = 'bg-secondary';
    }
    
    gradeProgress.className = `progress-bar ${className}`;
    gradeLabel.textContent = label;
    gradeLabel.className = grade > 0 ? 'text-dark fw-medium' : 'text-muted';
}

// Table Enhancement Functions
function setupTableEnhancements() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const performanceFilter = document.getElementById('performanceFilter');
    
    if (searchInput) {
        searchInput.addEventListener('input', filterStudents);
    }
    
    if (performanceFilter) {
        performanceFilter.addEventListener('change', filterStudents);
    }
    
    // View toggle functionality
    const tableView = document.getElementById('tableView');
    const cardView = document.getElementById('cardView');
    
    if (tableView && cardView) {
        tableView.addEventListener('click', showTableView);
        cardView.addEventListener('click', showCardView);
    }
    
    // Sorting functionality
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', function() {
            sortTable(this.dataset.sort);
        });
    });
}

// Student Filtering
function filterStudents() {
    const searchInput = document.getElementById('searchInput');
    const performanceFilter = document.getElementById('performanceFilter');
    const noResults = document.getElementById('noResults');
    
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const performanceLevel = performanceFilter ? performanceFilter.value : '';
    
    const rows = document.querySelectorAll('.student-row');
    const cards = document.querySelectorAll('.student-card');
    let visibleCount = 0;
    
    // Filter table rows
    rows.forEach(row => {
        const name = row.dataset.name || '';
        const roll = row.dataset.roll || '';
        const average = parseFloat(row.dataset.average) || 0;
        
        const matchesSearch = name.includes(searchTerm) || roll.includes(searchTerm);
        const matchesPerformance = checkPerformanceMatch(average, performanceLevel);
        
        if (matchesSearch && matchesPerformance) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Filter cards
    cards.forEach(card => {
        const name = card.dataset.name || '';
        const roll = card.dataset.roll || '';
        const average = parseFloat(card.dataset.average) || 0;
        
        const matchesSearch = name.includes(searchTerm) || roll.includes(searchTerm);
        const matchesPerformance = checkPerformanceMatch(average, performanceLevel);
        
        if (matchesSearch && matchesPerformance) {
            card.parentElement.style.display = '';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
    
    // Show/hide no results message
    if (noResults) {
        noResults.classList.toggle('d-none', visibleCount > 0);
    }
}

function checkPerformanceMatch(average, level) {
    if (!level) return true;
    
    switch (level) {
        case 'excellent': return average >= 90;
        case 'very-good': return average >= 80 && average < 90;
        case 'good': return average >= 70 && average < 80;
        case 'satisfactory': return average >= 60 && average < 70;
        case 'needs-improvement': return average > 0 && average < 60;
        case 'no-grades': return average === 0;
        default: return true;
    }
}

// View Toggle Functions
function showTableView() {
    const tableView = document.getElementById('tableView');
    const cardView = document.getElementById('cardView');
    const tableContent = document.getElementById('tableViewContent');
    const cardContent = document.getElementById('cardViewContent');
    
    tableView.classList.add('active');
    cardView.classList.remove('active');
    tableContent.classList.remove('d-none');
    cardContent.classList.add('d-none');
}

function showCardView() {
    const tableView = document.getElementById('tableView');
    const cardView = document.getElementById('cardView');
    const tableContent = document.getElementById('tableViewContent');
    const cardContent = document.getElementById('cardViewContent');
    
    cardView.classList.add('active');
    tableView.classList.remove('active');
    cardContent.classList.remove('d-none');
    tableContent.classList.add('d-none');
}

// Table Sorting
function sortTable(column) {
    const table = document.getElementById('studentsTable');
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        let aVal, bVal;
        
        switch (column) {
            case 'name':
                aVal = a.dataset.name;
                bVal = b.dataset.name;
                break;
            case 'roll':
                aVal = a.dataset.roll;
                bVal = b.dataset.roll;
                break;
            case 'average':
                aVal = parseFloat(a.dataset.average) || 0;
                bVal = parseFloat(b.dataset.average) || 0;
                return bVal - aVal; // Descending for averages
            case 'subjects':
                aVal = parseInt(a.querySelector('.badge').textContent) || 0;
                bVal = parseInt(b.querySelector('.badge').textContent) || 0;
                return bVal - aVal; // Descending for subject count
            default:
                return 0;
        }
        
        if (typeof aVal === 'string') {
            return aVal.localeCompare(bVal);
        }
        return aVal - bVal;
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Notification Auto-hide
function setupNotificationAutoHide() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Print Report Function
function printReport() {
    const printWindow = window.open('', '_blank');
    const studentName = document.querySelector('h4.card-title')?.textContent?.trim() || 'Student';
    
    let reportContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Report - ${studentName}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 20px; }
                .info { margin-bottom: 20px; }
                .grades-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                .grades-table th, .grades-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                .grades-table th { background-color: #f2f2f2; }
                .average { font-size: 1.2em; font-weight: bold; margin-top: 20px; }
                .footer { margin-top: 40px; text-align: center; color: #666; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Student Performance Report</h1>
                <p>Generated on ${new Date().toLocaleDateString()}</p>
            </div>
            
            <div class="info">
                <h2>Student Information</h2>
                <p><strong>Name:</strong> ${studentName}</p>
            </div>
            
            <div class="footer">
                <p>Student Performance Tracker - Academic Report</p>
            </div>
        </body>
        </html>
    `;
    
    printWindow.document.write(reportContent);
    printWindow.document.close();
    printWindow.print();
}

// Clear Filters Function
function clearFilters() {
    const searchInput = document.getElementById('searchInput');
    const performanceFilter = document.getElementById('performanceFilter');
    
    if (searchInput) searchInput.value = '';
    if (performanceFilter) performanceFilter.value = '';
    
    filterStudents();
}

// Utility Functions
function showSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-overlay';
    spinner.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    document.body.appendChild(spinner);
    return spinner;
}

function hideSpinner(spinner) {
    if (spinner && spinner.parentNode) {
        spinner.parentNode.removeChild(spinner);
    }
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

// Export functions for global access
window.loadStats = loadStats;
window.printReport = printReport;
window.clearFilters = clearFilters;
window.showTableView = showTableView;
window.showCardView = showCardView;
