// Consultation Booking Form Handler

const bookingModal = document.getElementById('booking-modal');
const consultationForm = document.getElementById('consultation-form');
let currentStep = 1;
const totalSteps = 3;

// Django Backend Configuration
const DJANGO_API_URL = 'http://localhost:8000/api'; // Update with your Django server URL
const CSRF_TOKEN = getCookie('csrftoken');

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Open Modal
function openBookingModal() {
    bookingModal.classList.add('show');
    document.body.style.overflow = 'hidden';
    resetForm();
}

// Close Modal
function closeBookingModal() {
    bookingModal.classList.remove('show');
    document.body.style.overflow = '';
    setTimeout(() => resetForm(), 300);
}

// Reset Form
function resetForm() {
    currentStep = 1;
    consultationForm.reset();
    updateStep(1);
}

// Update Form Step
function updateStep(step) {
    // Hide all steps
    document.querySelectorAll('.form-step').forEach(stepEl => {
        stepEl.classList.remove('active');
    });
    
    // Show current step
    document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
    
    // Update progress indicator
    document.querySelectorAll('.progress-step').forEach((stepEl, index) => {
        if (index < step) {
            stepEl.classList.add('active', 'completed');
        } else if (index === step - 1) {
            stepEl.classList.add('active');
            stepEl.classList.remove('completed');
        } else {
            stepEl.classList.remove('active', 'completed');
        }
    });
}

// Validate Step
function validateStep(step) {
    const stepElement = document.querySelector(`.form-step[data-step="${step}"]`);
    const inputs = stepElement.querySelectorAll('input[required], select[required], textarea[required]');
    
    for (let input of inputs) {
        if (!input.value.trim()) {
            input.focus();
            showNotification('Please fill in all required fields', 'error');
            return false;
        }
        
        // Email validation
        if (input.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                input.focus();
                showNotification('Please enter a valid email address', 'error');
                return false;
            }
        }
        
        // Phone validation
        if (input.type === 'tel') {
            const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
            if (!phoneRegex.test(input.value)) {
                input.focus();
                showNotification('Please enter a valid phone number', 'error');
                return false;
            }
        }
    }
    
    return true;
}

// Next Step Handler
document.querySelectorAll('.next-step').forEach(btn => {
    btn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            currentStep++;
            updateStep(currentStep);
        }
    });
});

// Previous Step Handler
document.querySelectorAll('.prev-step').forEach(btn => {
    btn.addEventListener('click', () => {
        currentStep--;
        updateStep(currentStep);
    });
});

// Form Submission
consultationForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!validateStep(currentStep)) {
        return;
    }
    
    // Show loading state
    const submitBtn = consultationForm.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    submitBtn.disabled = true;
    
    // Collect form data
    const formData = new FormData(consultationForm);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    try {
        // Send to Django backend
        const response = await fetch(`${DJANGO_API_URL}/consultations/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Failed to book consultation');
        }
        
        const result = await response.json();
        
        // Success
        showNotification('Consultation booked successfully! 🎉 Check your email for confirmation.', 'success');
        closeBookingModal();
        
        // Optional: Send confirmation email
        await sendConfirmationEmail(data);
        
    } catch (error) {
        console.error('Error booking consultation:', error);
        showNotification('Failed to book consultation. Please try again or contact us directly.', 'error');
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        submitBtn.disabled = false;
    }
});

// Send Confirmation Email (Optional)
async function sendConfirmationEmail(data) {
    try {
        await fetch(`${DJANGO_API_URL}/send-confirmation/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify({
                email: data.email,
                full_name: data.full_name,
                date: data.preferred_date,
                time: data.preferred_time
            })
        });
    } catch (error) {
        console.error('Error sending confirmation email:', error);
    }
}

// Modal Event Listeners
document.querySelectorAll('[href="#contact"]').forEach(link => {
    link.addEventListener('click', (e) => {
        if (link.textContent.includes('Book') || link.textContent.includes('consultation')) {
            e.preventDefault();
            openBookingModal();
        }
    });
});

document.querySelector('.modal-close')?.addEventListener('click', closeBookingModal);

bookingModal?.addEventListener('click', (e) => {
    if (e.target === bookingModal) {
        closeBookingModal();
    }
});

// Set minimum date to today
const dateInput = document.getElementById('preferred_date');
if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
}

// Notification System (reuse from script.js or define here)
function showNotification(message, type = 'success') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.classList.add('show'), 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}