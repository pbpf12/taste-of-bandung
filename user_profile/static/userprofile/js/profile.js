async function getUser() {
    try {
        const response = await fetch(showJsonUrl);
        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching user data:', error);
        showAlert('Failed to fetch user data', 'error');
        return null;
    }
}

async function getUserHistory(filter) {
    try {
        const url = filter ? `${showHistoryUrl}?filter=${filter}` : showHistoryUrl;
        const response = await fetch(url);
        
        if (!response.ok) {
            showAlert('Failed to fetch user history', 'error');
        }
        return await response.json();
    }
    catch (error) {
        console.error('Error fetching user history:', error);
        showAlert('Failed to fetch user history', 'error');
        return null;
    }
}

async function refreshHistory(filter) {
    const history = await getUserHistory(filter);
    const historyContainer = document.getElementById('user_history');

    if (history && history.history && history.history.length > 0) {
        historyContainer.innerHTML = ''; // Clear existing history
        
        // Create a container for all history items
        const historyList = document.createElement('div');
        historyList.className = 'space-y-4';

        history.history.forEach(item => {
            // Create card for each history item
            const card = document.createElement('div');
            card.className = 'bg-white p-4 rounded-lg shadow-md w-full md:w-1/2 lg:w-full';

            // Create flex container for image and details
            const flexContainer = document.createElement('div');
            flexContainer.className = 'flex flex-col sm:flex-row gap-4';

            // Image section
            const imageSection = document.createElement('div');
            imageSection.className = 'w-full sm:w-24 h-24 flex-shrink-0';
            const img = document.createElement('img');
            img.src = item.dish.image;
            img.className = 'w-full h-full object-cover rounded-md';
            img.alt = item.dish.name;
            imageSection.appendChild(img);

            // Details section
            const details = document.createElement('div');
            details.className = 'flex flex-col flex-grow';

            // Dish name and restaurant
            const nameRestaurant = document.createElement('div');
            nameRestaurant.className = 'flex justify-between items-start mb-2';

            const dishName = document.createElement('h3');
            dishName.className = 'text-lg font-semibold text-stone-800';
            dishName.textContent = item.dish.name;

            const restaurant = document.createElement('p');
            restaurant.className = 'text-sm text-stone-600';
            restaurant.textContent = item.dish.restaurant;

            nameRestaurant.appendChild(dishName);
            nameRestaurant.appendChild(restaurant);

            // Price and date
            const priceDate = document.createElement('div');
            priceDate.className = 'flex justify-between items-end mt-auto';

            const price = document.createElement('p');
            price.className = 'text-stone-800 font-medium';
            price.textContent = `$${parseFloat(item.dish.price).toFixed(2)}`;

            const date = document.createElement('p');
            date.className = 'text-sm text-stone-500';
            date.textContent = new Date(item.created_at).toLocaleDateString();

            priceDate.appendChild(price);
            priceDate.appendChild(date);

            // Assemble the details section
            details.appendChild(nameRestaurant);
            details.appendChild(priceDate);

            // Assemble the flex container
            flexContainer.appendChild(imageSection);
            flexContainer.appendChild(details);

            // Add flex container to card
            card.appendChild(flexContainer);

            // Add card to history list
            historyList.appendChild(card);
        });
        
        // Add the history list to the container
        historyContainer.appendChild(historyList);
    } else {
        historyContainer.innerHTML = `
            <div class="text-center py-8 text-stone-600">
                <p>No history available</p>
            </div>
        `;
    }
}

async function refreshProfile() {
    try {
        const response = await fetch(showJsonUrl);
        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }
        const user = await response.json();
    
        // Log the received data to check what we're getting
        console.log('Received user data:', user);

        // Update profile information if the data exists
        if (user) {
            // Sanitize the user data
            first_name = DOMPurify.sanitize(user.first_name);
            last_name = DOMPurify.sanitize(user.last_name);
            email = DOMPurify.sanitize(user.email);

            // Update profile fields
            document.getElementById('profile-first-name').textContent = first_name || 'Not Provided';
            document.getElementById('profile-last-name').textContent = last_name || 'Not Provided';
            document.getElementById('profile-email').textContent = email || 'Not Provided';
            
            // Update full name in the profile picture section
            const fullName = [first_name, last_name].filter(Boolean).join(' ') || 'Not Provided';
            document.getElementById('user-full-name').textContent = fullName;

            // Toggle incomplete profile alert
            const alertElement = document.getElementById('incomplete-profile-alert');
            if (first_name && last_name && email) {
                alertElement.classList.add('hidden');
            } else {
                alertElement.classList.remove('hidden');
            }

            // Update form fields
            document.getElementById('first_name').value = first_name || '';
            document.getElementById('last_name').value = last_name || '';
            document.getElementById('email').value = email || '';
        }
        
        await refreshHistory();
    } catch (error) {
        console.error('Error refreshing profile:', error);
        showAlert('Failed to refresh profile data', 'error');
    }
}

function showModal() {
    const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');
    
    modal.classList.remove('hidden');
    setTimeout(() => {
        modalContent.classList.remove('opacity-0', 'scale-95');
        modalContent.classList.add('opacity-100', 'scale-100');
    }, 50);
}

function hideModal() {
    const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');
    
    modalContent.classList.remove('opacity-100', 'scale-100');
    modalContent.classList.add('opacity-0', 'scale-95');
    
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
}

async function edit_profile(e) {
    e.preventDefault();
    try {
        const form = document.getElementById('userForm');
        const formData = new FormData(form);
        
        const response = await fetch(editProfileUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData,
            credentials: 'same-origin'  // This ensures cookies are sent
        });

        const data = await response.json();  // Get the response data

        if (!response.ok) {
            throw new Error(data.message || 'Failed to update profile');
        }

        // Refresh the profile data immediately
        await refreshProfile();
        document.getElementById('userForm').reset();
        hideModal();
        showAlert('Profile updated successfully', 'success');
    } catch (error) {
        console.error('Error updating profile:', error);
        showAlert(error.message || 'Failed to update profile', 'error');
    }
}

// Add this function to make sure form data is being collected correctly
function getFormData() {
    const form = document.getElementById('userForm');
    const formData = new FormData(form);
    
    // Log the form data to check what's being sent
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }
    
return formData;
}

function showAlert(message, type) {
    // Check if the current page is the profile page
    if (!document.getElementById('profile-page')) {
        return; // Exit if not on the profile page
    }

    var alertBox = document.createElement('div');
    alertBox.textContent = message;

    alertBox.className = 'fixed bottom-5 right-5 px-4 py-2 rounded shadow-lg text-white z-50';
    if (type === 'success') {
        alertBox.classList.add('bg-green-500');
    } else if (type === 'error') {
        alertBox.classList.add('bg-red-500');
    } else {
        alertBox.classList.add('bg-blue-500');
    }

    document.body.appendChild(alertBox);

    setTimeout(function() {
        alertBox.remove();
    }, 3000);

    document.addEventListener('DOMContentLoaded', refreshProfile);
}

function clearHistory() {
    // Get CSRF token from cookie
    function getCsrfToken() {
        const name = 'csrftoken';
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

    if (confirm('Clear history? This action cannot be undone.')) {
        fetch(clearHistoryUrl, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload page after successful deletion
            } else {
                console.error('Failed to clear history');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', (event) => {
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }

    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', showModal);
    }

    const closeModalBtn = document.getElementById('closeModalBtn');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', hideModal);
    }

    const cancelButton = document.getElementById('cancelButton');
    if (cancelButton) {
        cancelButton.addEventListener('click', hideModal);
    }

    const userForm = document.getElementById('userForm');
    if (userForm) {
        userForm.addEventListener('submit', edit_profile);
    }

    var filter = null;
    const sortByNameButton = document.getElementById('sortByNameBtn');
    if (sortByNameButton) {
        sortByNameButton.addEventListener('click', async function() {
            if (filter === 'dish_asc') {
                filter = 'dish_desc';
                await refreshHistory(filter);
            } else if (filter === 'dish_desc') {
                filter = 'dish_asc';
                await refreshHistory(filter);
            } else {
                filter = 'dish_asc';
                await refreshHistory(filter);
            }
        });
    }
});

// Initialize profile on page load
refreshProfile();

// Delete account functionality
document.addEventListener('DOMContentLoaded', (event) => {
    const deleteAccountBtn = document.getElementById('delete-account-btn');
    // Get the CSRF token from the hidden input field
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
                fetch(deleteUserUrl, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        showAlert('Account deleted successfully.', 'success');
                        setTimeout(() => {
                            window.location.href = loginUrl;
                        }, 500);
                    } else {
                        showAlert('Failed to delete account.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('An error occurred. Please try again.', 'error');
                });
            }
        });
    }
});