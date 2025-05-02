// Cart JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    initCartFunctionality();
    updateCartHeader();
    updateFloatingCart();
});

/**
 * Initialize cart functionality
 */
function initCartFunctionality() {
    // Add to Cart buttons on product pages
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    if (addToCartForms) {
        addToCartForms.forEach(form => {
            form.addEventListener('submit', handleAddToCart);
        });
    }

    // Quantity update forms in cart
    const quantityForms = document.querySelectorAll('.quantity-form');
    if (quantityForms) {
        quantityForms.forEach(form => {
            form.addEventListener('submit', handleQuantityUpdate);
        });
    }

    // Remove from cart buttons
    const removeButtons = document.querySelectorAll('.product-remove form');
    if (removeButtons) {
        removeButtons.forEach(form => {
            form.addEventListener('submit', handleRemoveItem);
        });
    }
}

/**
 * Handle adding item to cart
 * @param {Event} e - Submit event
 */
function handleAddToCart(e) {
    e.preventDefault();

    const form = e.target;
    const url = form.action;
    const formData = new FormData(form);

    // Get CSRF token
    const csrfToken = getCsrfToken();

    // Send AJAX request
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count in header
            updateCartHeader();

            // Update floating cart
            updateFloatingCart();

            // Show notification that item was added to cart
            showNotification('Товар добавлен в корзину', 'success');

            // Add animation to floating cart icon
            animateFloatingCart();
        }
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
        showNotification('Ошибка при добавлении в корзину', 'error');
    });
}

/**
 * Handle quantity update in cart
 * @param {Event} e - Submit event
 */
function handleQuantityUpdate(e) {
    e.preventDefault();

    const form = e.target;
    const url = form.action;
    const formData = new FormData(form);
    const productRow = form.closest('.cart-item');
    const productId = productRow.dataset.productId;

    // Get CSRF token
    const csrfToken = getCsrfToken();

    // Send AJAX request
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count in header
            updateCartHeader();

            // Update floating cart
            updateFloatingCart();

            // Update the total price for this item
            const totalCell = productRow.querySelector('.product-total');
            if (totalCell) {
                totalCell.textContent = `${data.item_total} руб.`;
            }

            // Update the cart total
            const totalAmount = document.querySelector('.total-amount');
            if (totalAmount) {
                totalAmount.textContent = `${data.cart_total} руб.`;
            }

            // Show success message
            showNotification('Корзина обновлена', 'success');
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
        showNotification('Ошибка при обновлении корзины', 'error');
    });
}

/**
 * Handle removing item from cart
 * @param {Event} e - Submit event
 */
function handleRemoveItem(e) {
    e.preventDefault();

    const form = e.target;
    const url = form.action;
    const formData = new FormData(form);
    const productRow = form.closest('.cart-item');

    // Get CSRF token
    const csrfToken = getCsrfToken();

    // Send AJAX request
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the row from the table
            productRow.remove();

            // Update cart count in header
            updateCartHeader();

            // Update floating cart
            updateFloatingCart();

            // Update the cart total
            const totalAmount = document.querySelector('.total-amount');
            if (totalAmount) {
                totalAmount.textContent = `${data.cart_total} руб.`;
            }

            // If cart is empty, reload the page to show empty cart message
            if (data.cart_count === 0) {
                window.location.reload();
            }

            // Show success message
            showNotification('Товар удален из корзины', 'success');
        }
    })
    .catch(error => {
        console.error('Error removing item from cart:', error);
        showNotification('Ошибка при удалении товара из корзины', 'error');
    });
}

/**
 * Update cart information in header
 */
function updateCartHeader() {
    fetch('/cart/summary/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data) return;

        // Update cart count
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = data.count;

            // Show/hide cart count based on whether there are items
            if (data.count > 0) {
                cartCount.style.display = 'flex';
            } else {
                cartCount.style.display = 'none';
            }
        }

        // Update cart total
        const cartTotal = document.querySelector('.cart-total-price');
        if (cartTotal && data.count > 0) {
            cartTotal.textContent = `${data.total} руб.`;
            cartTotal.style.display = 'block';
        } else if (cartTotal) {
            cartTotal.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error updating cart header:', error);
    });
}

/**
 * Update floating cart and popup cart
 */
function updateFloatingCart() {
    fetch('/cart/summary/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data) return;

        // Update floating cart count
        const floatingCartCount = document.querySelector('.floating-cart-count');
        if (floatingCartCount) {
            floatingCartCount.textContent = data.count;
        }

        // Show/hide floating cart based on whether there are items
        const floatingCart = document.getElementById('floating-cart');
        if (floatingCart) {
            if (data.count > 0) {
                // Показываем с анимацией если корзина еще не отображается
                if (floatingCart.style.display !== 'block') {
                    showFloatingCart();
                }
            } else {
                // Убираем класс анимации и скрываем
                floatingCart.classList.remove('show');
                floatingCart.style.display = 'none';
            }
        }
    })
    .catch(error => {
        console.error('Error updating floating cart:', error);
    });
}

/**
 * Animate floating cart icon
 */
function animateFloatingCart() {
    const floatingCartIcon = document.querySelector('.floating-cart-icon');
    if (floatingCartIcon) {
        floatingCartIcon.classList.add('cart-pulse');

        // Remove class after animation ends
        setTimeout(() => {
            floatingCartIcon.classList.remove('cart-pulse');
        }, 600);
    }
}

/**
 * Get CSRF token from cookie
 * @returns {string} CSRF token
 */
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

/**
 * Show notification message
 * @param {string} message - Message to display
 * @param {string} type - Notification type (success, error)
 */
function showNotification(message, type) {
    // Check if notification container exists, create if not
    let notificationContainer = document.getElementById('notification-container');
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        document.body.appendChild(notificationContainer);

        // Add styles
        notificationContainer.style.position = 'fixed';
        notificationContainer.style.top = '20px';
        notificationContainer.style.right = '20px';
        notificationContainer.style.zIndex = '9999';
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Style notification
    notification.style.backgroundColor = type === 'success' ? '#d4edda' : '#f8d7da';
    notification.style.color = type === 'success' ? '#155724' : '#721c24';
    notification.style.padding = '15px 20px';
    notification.style.marginBottom = '10px';
    notification.style.borderRadius = '5px';
    notification.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    notification.style.opacity = '0';
    notification.style.transition = 'opacity 0.3s ease';

    // Append to container
    notificationContainer.appendChild(notification);

    // Fade in
    setTimeout(() => {
        notification.style.opacity = '1';
    }, 10);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Show floating cart with animation
 */
function showFloatingCart() {
    const floatingCart = document.getElementById('floating-cart');
    if (floatingCart) {
        // Сначала показываем элемент
        floatingCart.style.display = 'block';

        // Затем добавляем класс для анимации
        setTimeout(() => {
            floatingCart.classList.add('show');
        }, 10);
    }
}