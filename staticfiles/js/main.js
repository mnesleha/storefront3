// Cart functionality
let cartId = localStorage.getItem('cartId');

// Initialize cart count on page load
document.addEventListener('DOMContentLoaded', function() {
    if (cartId) {
        updateCartCount();
    }
});

// Update cart count badge
async function updateCartCount() {
    if (!cartId) return;
    
    try {
        const response = await fetch(`/store/api/carts/${cartId}/`);
        if (response.ok) {
            const data = await response.json();
            const count = data.items ? data.items.length : 0;
            const badge = document.getElementById('cart-count');
            if (badge) {
                badge.textContent = count;
            }
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

// Add to cart function
async function addToCart(productId, quantity = 1) {
    console.log('Adding to cart:', productId, 'quantity:', quantity);
    
    // Create cart if doesn't exist
    if (!cartId) {
        try {
            const response = await fetch('/store/api/carts/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                const errorData = await response.text();
                console.error('Cart creation failed:', response.status, errorData);
                showNotification('Error creating cart: ' + response.status, 'error');
                return;
            }
            
            const data = await response.json();
            cartId = data.id;
            localStorage.setItem('cartId', cartId);
            console.log('Cart created:', cartId);
        } catch (error) {
            console.error('Error creating cart:', error);
            showNotification('Error creating cart', 'error');
            return;
        }
    }

    // Add item to cart
    try {
        const url = `/store/api/carts/${cartId}/items/`;
        console.log('Adding item to cart URL:', url);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Item added successfully:', data);
            updateCartCount();
            showNotification('Product added to cart!', 'success');
        } else {
            const errorText = await response.text();
            console.error('Add to cart failed:', response.status, errorText);
            try {
                const error = JSON.parse(errorText);
                showNotification(error.detail || error.product_id || 'Error adding to cart', 'error');
            } catch {
                showNotification('Error adding to cart: ' + response.status, 'error');
            }
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showNotification('Error adding to cart', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '80px';
    notification.style.right = '20px';
    notification.style.zIndex = '1000';
    notification.style.minWidth = '300px';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Quantity controls
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('qty-minus')) {
        const input = e.target.nextElementSibling;
        const currentValue = parseInt(input.value);
        if (currentValue > 1) {
            input.value = currentValue - 1;
            updateCartItemQuantity(e.target.dataset.itemId, currentValue - 1);
        }
    }
    
    if (e.target.classList.contains('qty-plus')) {
        const input = e.target.previousElementSibling;
        const currentValue = parseInt(input.value);
        input.value = currentValue + 1;
        updateCartItemQuantity(e.target.dataset.itemId, currentValue + 1);
    }
});

// Update cart item quantity
async function updateCartItemQuantity(itemId, quantity) {
    if (!cartId) return;
    
    try {
        const response = await fetch(`/store/api/carts/${cartId}/items/${itemId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: quantity })
        });

        if (response.ok) {
            updateCartCount();
            location.reload(); // Reload to update totals
        }
    } catch (error) {
        console.error('Error updating quantity:', error);
    }
}

// Remove from cart
async function removeFromCart(itemId) {
    if (!cartId) return;
    
    if (confirm('Are you sure you want to remove this item?')) {
        try {
            const response = await fetch(`/store/api/carts/${cartId}/items/${itemId}/`, {
                method: 'DELETE'
            });

            if (response.ok) {
                updateCartCount();
                location.reload();
            }
        } catch (error) {
            console.error('Error removing from cart:', error);
        }
    }
}

// Get CSRF token for authenticated requests
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

// Add CSRF token to all fetch requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    if (args[1] && (args[1].method === 'POST' || args[1].method === 'PATCH' || args[1].method === 'DELETE')) {
        args[1].headers = args[1].headers || {};
        args[1].headers['X-CSRFToken'] = getCookie('csrftoken');
    }
    return originalFetch.apply(this, args);
};
