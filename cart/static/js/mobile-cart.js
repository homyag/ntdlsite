/**
 * Проверка на очень маленький экран (320px)
 * и применение соответствующих стилей
 */
function checkVerySmallScreen() {
    if (window.innerWidth <= 320) {
        // Применяем специальные стили для экранов 320px
        document.querySelectorAll('.quantity-form').forEach(form => {
            const select = form.querySelector('select');
            const updateBtn = form.querySelector('.quantity-update-btn');
            const controlsWrapper = form.querySelector('.quantity-controls');

            if (controlsWrapper) {
                // Меняем расположение элементов для ультра-маленьких экранов
                controlsWrapper.style.flexDirection = 'column';

                const decrementBtn = controlsWrapper.querySelector('.quantity-decrement');
                const incrementBtn = controlsWrapper.querySelector('.quantity-increment');

                if (decrementBtn && incrementBtn) {
                    // Создаем обертку для кнопок +/-
                    const buttonsWrapper = document.createElement('div');
                    buttonsWrapper.style.display = 'flex';
                    buttonsWrapper.style.justifyContent = 'center';
                    buttonsWrapper.style.gap = '10px';
                    buttonsWrapper.style.marginBottom = '5px';

                    // Перемещаем кнопки в новую обертку
                    decrementBtn.parentNode.insertBefore(buttonsWrapper, decrementBtn);
                    buttonsWrapper.appendChild(decrementBtn);
                    buttonsWrapper.appendChild(select);
                    buttonsWrapper.appendChild(incrementBtn);
                }

                // Перемещаем кнопку Обновить вниз
                if (updateBtn) {
                    updateBtn.style.width = '100%';
                    updateBtn.style.marginTop = '5px';
                    updateBtn.style.marginLeft = '0';
                }
            }
        });

        // Адаптируем кнопки в итоговом блоке
        const checkoutBtn = document.querySelector('.checkout-btn');
        const continueBtn = document.querySelector('.continue-shopping-btn');

        if (checkoutBtn) {
            checkoutBtn.style.fontSize = '0.9rem';
            checkoutBtn.style.padding = '8px 10px';
        }

        if (continueBtn) {
            continueBtn.style.fontSize = '0.9rem';
            continueBtn.style.padding = '8px 10px';
        }
    }
}

// Вызываем функцию при загрузке и при изменении размера окна
document.addEventListener('DOMContentLoaded', checkVerySmallScreen);
window.addEventListener('resize', checkVerySmallScreen);/**
 * Mobile-friendly cart enhancements
 * This script adds mobile-specific functionality to the shopping cart
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile cart functionality
    initMobileCart();

    // Add swipe to remove functionality for mobile
    initSwipeToRemove();

    // Improve quantity selector for mobile
    enhanceQuantitySelector();

    // Add sticky checkout button on mobile
    initStickyCheckout();

    // Применяем специальные стили для экранов 320px
    checkVerySmallScreen();
});

/**
 * Initialize mobile cart functionality
 */
function initMobileCart() {
    // Add mobile-specific data attributes and classes
    const cartItems = document.querySelectorAll('.cart-item');

    if (!cartItems.length) return;

    cartItems.forEach(item => {
        // Add mobile-specific attributes
        item.setAttribute('data-mobile-cart-item', 'true');

        // Add appropriate aria attributes for accessibility
        item.setAttribute('role', 'article');
        item.setAttribute('aria-label', 'Товар в корзине');

        // Add touch feedback
        item.addEventListener('touchstart', function() {
            this.classList.add('touch-active');
        });

        item.addEventListener('touchend', function() {
            this.classList.remove('touch-active');
        });
    });

    // Show mobile cart summary
    const cartSummary = document.querySelector('.mobile-cart-summary');
    if (cartSummary && window.innerWidth <= 768) {
        cartSummary.style.display = 'block';
    }
}

/**
 * Initialize swipe to remove functionality for mobile devices
 */
function initSwipeToRemove() {
    const cartItems = document.querySelectorAll('.cart-item');
    if (!cartItems.length) return;

    // Only apply on mobile devices
    if (window.innerWidth > 768) return;

    cartItems.forEach(item => {
        let startX, moveX, threshold = 80;
        let isLongTouch = false;
        let touchTimeout;

        // Touch start event
        item.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;

            // Detect long touch
            touchTimeout = setTimeout(() => {
                isLongTouch = true;
                // Add visual cue for deletion
                item.classList.add('delete-ready');
            }, 500);
        });

        // Touch move event
        item.addEventListener('touchmove', function(e) {
            if (!startX) return;

            moveX = e.touches[0].clientX;
            const diff = moveX - startX;

            // If swiping left (to remove)
            if (diff < 0) {
                // Prevent page scrolling when swiping the item
                e.preventDefault();

                // Add visual cue with transform
                const swipePercent = Math.min(Math.abs(diff) / threshold, 1);
                item.style.transform = `translateX(${diff}px)`;
                item.style.opacity = 1 - (swipePercent * 0.5);
            }
        });

        // Touch end event
        item.addEventListener('touchend', function(e) {
            clearTimeout(touchTimeout);

            // Handle swipe to remove
            if (startX && moveX && (startX - moveX > threshold)) {
                const removeButton = item.querySelector('.remove-btn');
                if (removeButton) {
                    // Animate item out
                    item.classList.add('swipe-left');
                    item.style.opacity = '0';

                    // Trigger remove button click after animation
                    setTimeout(() => {
                        removeButton.click();
                    }, 300);
                }
            } else if (isLongTouch) {
                // Show remove confirmation on long touch
                showRemoveConfirmation(item);
            } else {
                // Reset styles
                item.style.transform = '';
                item.style.opacity = '';
            }

            // Reset variables
            startX = null;
            moveX = null;
            isLongTouch = false;
            item.classList.remove('delete-ready');
        });
    });
}

/**
 * Show remove confirmation for long touch
 * @param {HTMLElement} item - Cart item element
 */
function showRemoveConfirmation(item) {
    // Find product info
    const productName = item.querySelector('.product-name')?.textContent || 'этот товар';

    // Create confirmation element
    const confirmation = document.createElement('div');
    confirmation.className = 'remove-confirmation';
    confirmation.innerHTML = `
        <div class="remove-confirmation-content">
            <p>Удалить ${productName} из корзины?</p>
            <div class="confirmation-buttons">
                <button class="confirm-remove">Удалить</button>
                <button class="cancel-remove">Отмена</button>
            </div>
        </div>
    `;

    // Style the confirmation
    confirmation.style.position = 'fixed';
    confirmation.style.top = '0';
    confirmation.style.left = '0';
    confirmation.style.width = '100%';
    confirmation.style.height = '100%';
    confirmation.style.backgroundColor = 'rgba(0,0,0,0.5)';
    confirmation.style.zIndex = '1000';
    confirmation.style.display = 'flex';
    confirmation.style.justifyContent = 'center';
    confirmation.style.alignItems = 'center';

    // Style confirmation content
    const content = confirmation.querySelector('.remove-confirmation-content');
    content.style.backgroundColor = '#fff';
    content.style.padding = '20px';
    content.style.borderRadius = '10px';
    content.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
    content.style.width = '80%';
    content.style.maxWidth = '300px';
    content.style.textAlign = 'center';

    // Style buttons
    const buttons = confirmation.querySelectorAll('button');
    buttons.forEach(button => {
        button.style.padding = '10px 15px';
        button.style.margin = '0 5px';
        button.style.border = 'none';
        button.style.borderRadius = '5px';
        button.style.fontWeight = 'bold';
        button.style.cursor = 'pointer';
    });

    // Style remove button
    const removeBtn = confirmation.querySelector('.confirm-remove');
    removeBtn.style.backgroundColor = '#ff3b30';
    removeBtn.style.color = '#fff';

    // Style cancel button
    const cancelBtn = confirmation.querySelector('.cancel-remove');
    cancelBtn.style.backgroundColor = '#f1f1f1';
    cancelBtn.style.color = '#333';

    // Add to DOM
    document.body.appendChild(confirmation);

    // Add event listeners
    confirmation.querySelector('.confirm-remove').addEventListener('click', function() {
        const removeButton = item.querySelector('.remove-btn');
        if (removeButton) {
            removeButton.click();
        }
        confirmation.remove();
    });

    confirmation.querySelector('.cancel-remove').addEventListener('click', function() {
        confirmation.remove();
    });

    // Close on background click
    confirmation.addEventListener('click', function(e) {
        if (e.target === confirmation) {
            confirmation.remove();
        }
    });
}

/**
 * Enhance quantity selector for mobile devices
 */
function enhanceQuantitySelector() {
    // Check if we're on mobile
    if (window.innerWidth > 768) return;

    const quantityForms = document.querySelectorAll('.quantity-form');
    if (!quantityForms.length) return;

    quantityForms.forEach(form => {
        const select = form.querySelector('select');
        const updateBtn = form.querySelector('.quantity-update-btn');

        if (!select || !updateBtn) return;

        // Create increment/decrement buttons for easier mobile interaction
        const controlsWrapper = document.createElement('div');
        controlsWrapper.className = 'quantity-controls';
        controlsWrapper.style.display = 'flex';
        controlsWrapper.style.alignItems = 'center';
        controlsWrapper.style.justifyContent = 'center';
        controlsWrapper.style.width = '100%';

        // Create decrement button
        const decrementBtn = document.createElement('button');
        decrementBtn.type = 'button';
        decrementBtn.className = 'quantity-btn quantity-decrement';
        decrementBtn.innerHTML = '-';
        decrementBtn.style.width = '28px';
        decrementBtn.style.height = '28px';
        decrementBtn.style.border = '1px solid #ddd';
        decrementBtn.style.borderRadius = '50%';
        decrementBtn.style.backgroundColor = '#f8f9fa';
        decrementBtn.style.fontSize = '16px';
        decrementBtn.style.display = 'flex';
        decrementBtn.style.alignItems = 'center';
        decrementBtn.style.justifyContent = 'center';

        // Create increment button
        const incrementBtn = document.createElement('button');
        incrementBtn.type = 'button';
        incrementBtn.className = 'quantity-btn quantity-increment';
        incrementBtn.innerHTML = '+';
        incrementBtn.style.width = '28px';
        incrementBtn.style.height = '28px';
        incrementBtn.style.border = '1px solid #ddd';
        incrementBtn.style.borderRadius = '50%';
        incrementBtn.style.backgroundColor = '#f8f9fa';
        incrementBtn.style.fontSize = '16px';
        incrementBtn.style.display = 'flex';
        incrementBtn.style.alignItems = 'center';
        incrementBtn.style.justifyContent = 'center';

        // Style select
        select.style.width = '45px';
        select.style.textAlign = 'center';
        select.style.margin = '0 5px';
        select.style.border = '1px solid #ddd';
        select.style.borderRadius = '4px';
        select.style.padding = '4px';

        // Add event listeners
        decrementBtn.addEventListener('click', function() {
            const currentIndex = select.selectedIndex;
            if (currentIndex > 0) {
                select.selectedIndex = currentIndex - 1;
                // Не автоматически обновляем, пользователь должен нажать кнопку Обновить
            }
        });

        incrementBtn.addEventListener('click', function() {
            const currentIndex = select.selectedIndex;
            if (currentIndex < select.options.length - 1) {
                select.selectedIndex = currentIndex + 1;
                // Не автоматически обновляем, пользователь должен нажать кнопку Обновить
            }
        });

        // Replace the form contents
        controlsWrapper.appendChild(decrementBtn);
        controlsWrapper.appendChild(select);
        controlsWrapper.appendChild(incrementBtn);

        // Show the update button inline with other controls
        updateBtn.style.display = 'block';
        updateBtn.style.marginLeft = '5px';
        updateBtn.style.padding = '4px 8px';
        updateBtn.style.fontSize = '0.85rem';

        // Insert quantity controls in place of original elements
        select.parentNode.insertBefore(controlsWrapper, select);
        controlsWrapper.appendChild(select);
    });
}

/**
 * Initialize sticky checkout button on mobile
 */
function initStickyCheckout() {
    // Only apply on mobile
    if (window.innerWidth > 768) return;

    // Check if we're on cart page
    const cartSummary = document.querySelector('.cart-summary');
    if (!cartSummary) return;

    // Get checkout button
    const checkoutBtn = document.querySelector('.checkout-btn');
    if (!checkoutBtn) return;

    // Create sticky button container
    const stickyContainer = document.createElement('div');
    stickyContainer.className = 'sticky-checkout-container';
    stickyContainer.style.position = 'fixed';
    stickyContainer.style.bottom = '0';
    stickyContainer.style.left = '0';
    stickyContainer.style.width = '100%';
    stickyContainer.style.backgroundColor = '#fff';
    stickyContainer.style.padding = '10px 15px';
    stickyContainer.style.boxShadow = '0 -2px 10px rgba(0,0,0,0.1)';
    stickyContainer.style.zIndex = '99';
    stickyContainer.style.display = 'flex';
    stickyContainer.style.justifyContent = 'space-between';
    stickyContainer.style.alignItems = 'center';

    // Create price display
    const priceDisplay = document.createElement('div');
    priceDisplay.className = 'sticky-price-display';
    priceDisplay.style.fontWeight = 'bold';
    priceDisplay.style.fontSize = '1.1rem';
    priceDisplay.style.color = '#113E71';

    // Get total amount
    const totalAmount = document.querySelector('.total-amount');
    if (totalAmount) {
        priceDisplay.textContent = totalAmount.textContent;
    }

    // Clone the checkout button
    const stickyCheckoutBtn = document.createElement('a');
    stickyCheckoutBtn.href = checkoutBtn.href;
    stickyCheckoutBtn.className = 'sticky-checkout-btn';
    stickyCheckoutBtn.textContent = 'Оформить заказ';
    stickyCheckoutBtn.style.backgroundColor = '#3698D4';
    stickyCheckoutBtn.style.color = 'white';
    stickyCheckoutBtn.style.padding = '10px 20px';
    stickyCheckoutBtn.style.borderRadius = '50px';
    stickyCheckoutBtn.style.textDecoration = 'none';
    stickyCheckoutBtn.style.fontWeight = 'bold';

    // Add elements to container
    stickyContainer.appendChild(priceDisplay);
    stickyContainer.appendChild(stickyCheckoutBtn);

    // Add to DOM
    document.body.appendChild(stickyContainer);

    // Add padding to bottom of document to account for sticky footer
    const footerHeight = stickyContainer.offsetHeight;
    document.body.style.paddingBottom = `${footerHeight + 20}px`;

    // Hide the sticky footer when near the actual checkout button
    window.addEventListener('scroll', function() {
        const cartSummaryRect = cartSummary.getBoundingClientRect();
        // If cart summary is visible
        if (cartSummaryRect.top < window.innerHeight && cartSummaryRect.bottom > 0) {
            stickyContainer.style.transform = 'translateY(100%)';
            stickyContainer.style.opacity = '0';
        } else {
            stickyContainer.style.transform = 'translateY(0)';
            stickyContainer.style.opacity = '1';
        }
    });
}