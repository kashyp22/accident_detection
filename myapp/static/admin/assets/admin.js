/* Admin Dashboard JavaScript */

// State
let currentPage = 'home';
let currentTheme = localStorage.getItem('theme') || 'dark';

// Mock Data Generators
const mockUsers = [
  { id: 1, name: 'John Doe', email: 'john@example.com', phone: '+1234567890', role: 'User', status: 'active', joined: '2024-01-15' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '+1234567891', role: 'Driver', status: 'active', joined: '2024-02-20' },
  { id: 3, name: 'Mike Johnson', email: 'mike@example.com', phone: '+1234567892', role: 'User', status: 'inactive', joined: '2024-03-10' },
  { id: 4, name: 'Sarah Williams', email: 'sarah@example.com', phone: '+1234567893', role: 'Admin', status: 'active', joined: '2024-01-05' },
  { id: 5, name: 'David Brown', email: 'david@example.com', phone: '+1234567894', role: 'User', status: 'active', joined: '2024-04-12' },
];

const mockRatings = [
  { id: 1, user: 'John Doe', service: 'Ambulance Response', rating: 5, feedback: 'Excellent service, very quick response!', date: '2024-10-01' },
  { id: 2, user: 'Jane Smith', service: 'Hospital Care', rating: 4, feedback: 'Good care but waiting time was long.', date: '2024-10-02' },
  { id: 3, user: 'Mike Johnson', service: 'AI Detection', rating: 5, feedback: 'Accurate detection saved my life!', date: '2024-10-03' },
  { id: 4, user: 'Sarah Williams', service: 'Emergency Alert', rating: 3, feedback: 'Alert was delayed by 2 minutes.', date: '2024-10-03' },
  { id: 5, user: 'David Brown', service: 'Ambulance Response', rating: 5, feedback: 'Professional and caring staff.', date: '2024-10-04' },
];

const mockComplaints = [
  { id: 1, user: 'John Doe', subject: 'Delayed ambulance arrival', priority: 'high', status: 'in-progress', date: '2024-10-02' },
  { id: 2, user: 'Jane Smith', subject: 'App not working properly', priority: 'medium', status: 'pending', date: '2024-10-03' },
  { id: 3, user: 'Mike Johnson', subject: 'False accident detection', priority: 'low', status: 'resolved', date: '2024-09-28' },
  { id: 4, user: 'Sarah Williams', subject: 'Payment issue', priority: 'high', status: 'pending', date: '2024-10-04' },
  { id: 5, user: 'David Brown', subject: 'Wrong hospital location', priority: 'medium', status: 'in-progress', date: '2024-10-01' },
];

const mockHospitals = [
  { id: 1, name: 'City General Hospital', location: 'Downtown, Sector 12', contact: '+1234567800', beds: 45, status: 'verified' },
  { id: 2, name: 'St. Mary Medical Center', location: 'North Avenue, Block A', contact: '+1234567801', beds: 32, status: 'pending' },
  { id: 3, name: 'Emergency Care Hospital', location: 'Highway 45, Exit 7', contact: '+1234567802', beds: 28, status: 'verified' },
  { id: 4, name: 'Metro Health Clinic', location: 'East Side, Plaza 3', contact: '+1234567803', beds: 15, status: 'rejected' },
  { id: 5, name: 'Central Medical Institute', location: 'West End, Street 22', contact: '+1234567804', beds: 52, status: 'pending' },
];

const mockAmbulances = [
  { id: 1, vehicleNo: 'AMB-1234', driver: 'Robert Lee', contact: '+1234567900', hospital: 'City General Hospital', status: 'verified' },
  { id: 2, vehicleNo: 'AMB-5678', driver: 'Emily Davis', contact: '+1234567901', hospital: 'St. Mary Medical Center', status: 'pending' },
  { id: 3, vehicleNo: 'AMB-9012', driver: 'Michael Chen', contact: '+1234567902', hospital: 'Emergency Care Hospital', status: 'verified' },
  { id: 4, vehicleNo: 'AMB-3456', driver: 'Lisa Anderson', contact: '+1234567903', hospital: 'Metro Health Clinic', status: 'rejected' },
  { id: 5, vehicleNo: 'AMB-7890', driver: 'James Wilson', contact: '+1234567904', hospital: 'Central Medical Institute', status: 'pending' },
];

// Initialize
function init() {
  // Set theme
  document.body.setAttribute('data-theme', currentTheme);

  // Event Listeners
  document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);
  document.getElementById('menu-toggle')?.addEventListener('click', toggleSidebar);
  document.getElementById('btn-logout')?.addEventListener('click', handleLogout);
  document.getElementById('btn-change-password')?.addEventListener('click', () => openModal('modal-change-password'));

  // Navigation
  document.querySelectorAll('.nav-item[data-page]').forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const page = item.getAttribute('data-page');
      navigateTo(page);
    });
  });

  // Modal close buttons
  document.querySelectorAll('[data-modal]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modalId = btn.getAttribute('data-modal');
      closeModal(modalId);
    });
  });

  // Form submissions
  document.getElementById('form-change-password')?.addEventListener('submit', handleChangePassword);

  // Load initial data
  loadPageData('home');
}

// Theme Toggle
function toggleTheme() {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.body.setAttribute('data-theme', currentTheme);
  localStorage.setItem('theme', currentTheme);
}

// Sidebar Toggle (Mobile)
function toggleSidebar() {
  document.getElementById('sidebar')?.classList.toggle('active');
}

// Navigation
function navigateTo(page) {
  currentPage = page;

  // Update active nav item
  document.querySelectorAll('.nav-item[data-page]').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-page') === page);
  });

  // Show active page
  document.querySelectorAll('.page').forEach(p => {
    p.classList.toggle('active', p.id === `page-${page}`);
  });

  // Load page data
  loadPageData(page);

  // Close sidebar on mobile
  if (window.innerWidth <= 1024) {
    document.getElementById('sidebar')?.classList.remove('active');
  }
}

// Load Page Data
function loadPageData(page) {
  switch (page) {
    case 'users':
      renderUsersTable();
      break;
    case 'ratings':
      renderRatingsTable();
      break;
    case 'complaints':
      renderComplaintsTable();
      break;
    case 'verify-hospital':
      renderHospitalsTable();
      break;
    case 'verify-ambulance':
      renderAmbulancesTable();
      break;
  }
}

// Render Users Table
function renderUsersTable() {
  const tbody = document.querySelector('#users-table tbody');
  if (!tbody) return;

  tbody.innerHTML = mockUsers.map(user => `
    <tr>
      <td>${user.id}</td>
      <td>${user.name}</td>
      <td>${user.email}</td>
      <td>${user.phone}</td>
      <td>${user.role}</td>
      <td><span class="badge ${user.status}">${user.status}</span></td>
      <td>${user.joined}</td>
      <td>
        <div class="action-buttons">
          <button class="btn btn-sm btn-primary" onclick="editUser(${user.id})">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="deleteUser(${user.id})">Delete</button>
        </div>
      </td>
    </tr>
  `).join('');
}

// Render Ratings Table
function renderRatingsTable() {
  const tbody = document.querySelector('#ratings-table tbody');
  if (!tbody) return;

  tbody.innerHTML = mockRatings.map(rating => `
    <tr>
      <td>${rating.id}</td>
      <td>${rating.user}</td>
      <td>${rating.service}</td>
      <td><span class="stars">${'★'.repeat(rating.rating)}${'☆'.repeat(5 - rating.rating)}</span></td>
      <td>${rating.feedback}</td>
      <td>${rating.date}</td>
      <td>
        <div class="action-buttons">
          <button class="btn btn-sm btn-primary" onclick="viewRating(${rating.id})">View</button>
          <button class="btn btn-sm btn-danger" onclick="deleteRating(${rating.id})">Delete</button>
        </div>
      </td>
    </tr>
  `).join('');
}

// Render Complaints Table
function renderComplaintsTable() {
  const tbody = document.querySelector('#complaints-table tbody');
  if (!tbody) return;

  tbody.innerHTML = mockComplaints.map(complaint => `
    <tr>
      <td>${complaint.id}</td>
      <td>${complaint.user}</td>
      <td>${complaint.subject}</td>
      <td><span class="badge ${complaint.priority}">${complaint.priority}</span></td>
      <td><span class="badge ${complaint.status}">${complaint.status}</span></td>
      <td>${complaint.date}</td>
      <td>
        <div class="action-buttons">
          <button class="btn btn-sm btn-primary" onclick="viewComplaint(${complaint.id})">View</button>
          <button class="btn btn-sm btn-success" onclick="resolveComplaint(${complaint.id})">Resolve</button>
        </div>
      </td>
    </tr>
  `).join('');
}

// Render Hospitals Table
function renderHospitalsTable() {
  const tbody = document.querySelector('#hospitals-table tbody');
  if (!tbody) return;

  tbody.innerHTML = mockHospitals.map(hospital => `
    <tr>
      <td>${hospital.id}</td>
      <td>${hospital.name}</td>
      <td>${hospital.location}</td>
      <td>${hospital.contact}</td>
      <td>${hospital.beds}</td>
      <td><span class="badge ${hospital.status}">${hospital.status}</span></td>
      <td>
        <div class="action-buttons">
          ${hospital.status === 'pending' ? `
            <button class="btn btn-sm btn-success" onclick="verifyHospital(${hospital.id}, 'verified')">Verify</button>
            <button class="btn btn-sm btn-danger" onclick="verifyHospital(${hospital.id}, 'rejected')">Reject</button>
          ` : `
            <button class="btn btn-sm btn-primary" onclick="viewHospital(${hospital.id})">View</button>
          `}
        </div>
      </td>
    </tr>
  `).join('');
}

// Render Ambulances Table
function renderAmbulancesTable() {
  const tbody = document.querySelector('#ambulances-table tbody');
  if (!tbody) return;

  tbody.innerHTML = mockAmbulances.map(ambulance => `
    <tr>
      <td>${ambulance.id}</td>
      <td>${ambulance.vehicleNo}</td>
      <td>${ambulance.driver}</td>
      <td>${ambulance.contact}</td>
      <td>${ambulance.hospital}</td>
      <td><span class="badge ${ambulance.status}">${ambulance.status}</span></td>
      <td>
        <div class="action-buttons">
          ${ambulance.status === 'pending' ? `
            <button class="btn btn-sm btn-success" onclick="verifyAmbulance(${ambulance.id}, 'verified')">Verify</button>
            <button class="btn btn-sm btn-danger" onclick="verifyAmbulance(${ambulance.id}, 'rejected')">Reject</button>
          ` : `
            <button class="btn btn-sm btn-primary" onclick="viewAmbulance(${ambulance.id})">View</button>
          `}
        </div>
      </td>
    </tr>
  `).join('');
}

// Action Handlers (TODO: Replace with actual API calls)
function editUser(id) {
  showToast(`Edit user ${id} - TODO: Implement edit functionality`, 'info');
}

function deleteUser(id) {
  if (confirm('Are you sure you want to delete this user?')) {
    showToast(`User ${id} deleted successfully`, 'success');
    // TODO: Call API to delete user
  }
}

function viewRating(id) {
  showToast(`View rating ${id} - TODO: Implement view functionality`, 'info');
}

function deleteRating(id) {
  if (confirm('Are you sure you want to delete this rating?')) {
    showToast(`Rating ${id} deleted successfully`, 'success');
    // TODO: Call API to delete rating
  }
}

function viewComplaint(id) {
  showToast(`View complaint ${id} - TODO: Implement view functionality`, 'info');
}

function resolveComplaint(id) {
  if (confirm('Mark this complaint as resolved?')) {
    showToast(`Complaint ${id} marked as resolved`, 'success');
    // TODO: Call API to update complaint status
    setTimeout(() => renderComplaintsTable(), 1000);
  }
}

function verifyHospital(id, status) {
  const action = status === 'verified' ? 'verified' : 'rejected';
  if (confirm(`Are you sure you want to ${action} this hospital?`)) {
    showToast(`Hospital ${id} ${action} successfully`, 'success');
    // TODO: Call API to update hospital status
    setTimeout(() => renderHospitalsTable(), 1000);
  }
}

function viewHospital(id) {
  showToast(`View hospital ${id} - TODO: Implement view functionality`, 'info');
}

function verifyAmbulance(id, status) {
  const action = status === 'verified' ? 'verified' : 'rejected';
  if (confirm(`Are you sure you want to ${action} this ambulance?`)) {
    showToast(`Ambulance ${id} ${action} successfully`, 'success');
    // TODO: Call API to update ambulance status
    setTimeout(() => renderAmbulancesTable(), 1000);
  }
}

function viewAmbulance(id) {
  showToast(`View ambulance ${id} - TODO: Implement view functionality`, 'info');
}

// Modal Functions
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
  }
}

// Handle Change Password
function handleChangePassword(e) {
  e.preventDefault();
  const form = e.target;
  const inputs = form.querySelectorAll('input');
  const [current, newPass, confirm] = Array.from(inputs).map(i => i.value);

  if (newPass !== confirm) {
    showToast('Passwords do not match!', 'error');
    return;
  }

  if (newPass.length < 6) {
    showToast('Password must be at least 6 characters!', 'error');
    return;
  }

  // TODO: Call API to change password
  showToast('Password changed successfully!', 'success');
  closeModal('modal-change-password');
  form.reset();
}

// Handle Logout
function handleLogout() {
  if (confirm('Are you sure you want to logout?')) {
    showToast('Logging out...', 'info');
    setTimeout(() => {
      // TODO: Clear session and redirect to login
      window.location.href = 'index.html';
    }, 1500);
  }
}

// Toast Notification
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  if (!toast) return;

  toast.textContent = message;
  toast.className = `toast ${type} show`;

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// Search Functionality (Basic)
document.getElementById('search-users')?.addEventListener('input', (e) => {
  // TODO: Implement search filter
  console.log('Search users:', e.target.value);
});

document.getElementById('search-ratings')?.addEventListener('input', (e) => {
  // TODO: Implement search filter
  console.log('Search ratings:', e.target.value);
});

document.getElementById('search-complaints')?.addEventListener('input', (e) => {
  // TODO: Implement search filter
  console.log('Search complaints:', e.target.value);
});

document.getElementById('search-hospitals')?.addEventListener('input', (e) => {
  // TODO: Implement search filter
  console.log('Search hospitals:', e.target.value);
});

document.getElementById('search-ambulances')?.addEventListener('input', (e) => {
  // TODO: Implement search filter
  console.log('Search ambulances:', e.target.value);
});

// Initialize on DOM load
window.addEventListener('DOMContentLoaded', init);

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
  const sidebar = document.getElementById('sidebar');
  const menuToggle = document.getElementById('menu-toggle');
  
  if (window.innerWidth <= 1024 && 
      sidebar?.classList.contains('active') && 
      !sidebar.contains(e.target) && 
      !menuToggle?.contains(e.target)) {
    sidebar.classList.remove('active');
  }
});

// Close modal when clicking outside
document.querySelectorAll('.modal').forEach(modal => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('active');
    }
  });
});
