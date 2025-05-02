/**
 * Mobile-friendly enhancements for checkout process
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile checkout features
    initMobileCheckout();

    // Initialize form validation with helpful mobile feedback
    initMobileFormValidation();

    // Initialize sticky checkout button
    initStickyCheckoutButton();

    // Add autofill helper for address
    initAddressHelper();
});

/**
 * Initialize mobile checkout features
 */
function initMobileCheckout() {
    // Check if we're on mobile
    if (window.innerWidth > 768) return;

    // Add mobile-specific styles and behaviors
    const checkoutForm = document.querySelector('.checkout-form');
    if (!checkoutForm) return;

    // Enhance form inputs for mobile
    enhanceFormInputs();

    // Add progress indicator
    addProgressIndicator();

    // Add delivery time estimate
    addDeliveryEstimate();
}

/**
 * Enhance form inputs for mobile devices
 */
function enhanceFormInputs() {
    // Add appropriate input types for mobile
    const phoneInput = document.querySelector('input[name="customer_phone"]');
    if (phoneInput) {
        phoneInput.setAttribute('type', 'tel');
        phoneInput.setAttribute('pattern', '[+]?[0-9]{10,15}');
        phoneInput.setAttribute('autocomplete', 'tel');
    }

    const emailInput = document.querySelector('input[name="customer_email"]');
    if (emailInput) {
        emailInput.setAttribute('type', 'email');
        emailInput.setAttribute('autocomplete', 'email');
    }

    const nameInput = document.querySelector('input[name="customer_name"]');
    if (nameInput) {
        nameInput.setAttribute('autocomplete', 'name');
    }

    const cityInput = document.querySelector('input[name="city"]');
    if (cityInput) {
        cityInput.setAttribute('autocomplete', 'address-level2');
    }

    const addressInput = document.querySelector('textarea[name="shipping_address"]');
    if (addressInput) {
        addressInput.setAttribute('autocomplete', 'street-address');
    }
}

/**
 * Add progress indicator for checkout process
 */
function addProgressIndicator() {
    const checkoutContainer = document.querySelector('.checkout-container');
    if (!checkoutContainer) return;

    // Create progress indicator
    const progressIndicator = document.createElement('div');
    progressIndicator.className = 'checkout-progress';
    progressIndicator.innerHTML = `
        <div class="progress-steps">
            <div class="progress-step active">
                <div class="step-number">1</div>
                <div class="step-label">Корзина</div>
            </div>
            <div class="progress-line"></div>
            <div class="progress-step active">
                <div class="step-number">2</div>
                <div class="step-label">Оформление</div>
            </div>
            <div class="progress-line"></div>
            <div class="progress-step">
                <div class="step-number">3</div>
                <div class="step-label">Готово</div>
            </div>
        </div>
    `;

    // Style the progress indicator
    progressIndicator.style.marginBottom = '20px';

    const steps = progressIndicator.querySelectorAll('.progress-step');
    steps.forEach(step => {
        step.style.display = 'flex';
        step.style.flexDirection = 'column';
        step.style.alignItems = 'center';
        step.style.position = 'relative';
        step.style.width = '33.333%';
    });

    const stepNumbers = progressIndicator.querySelectorAll('.step-number');
    stepNumbers.forEach(number => {
        number.style.width = '30px';
        number.style.height = '30px';
        number.style.borderRadius = '50%';
        number.style.backgroundColor = '#f0f0f0';
        number.style.display = 'flex';
        number.style.alignItems = 'center';
        number.style.justifyContent = 'center';
        number.style.marginBottom = '5px';
        number.style.fontWeight = 'bold';
        number.style.color = '#666';
    });

    const activeSteps = progressIndicator.querySelectorAll('.progress-step.active');
    activeSteps.forEach(step => {
        const number = step.querySelector('.step-number');
        if (number) {
            number.style.backgroundColor = '#3698D4';
            number.style.color = 'white';
        }
    });

    const stepLabels = progressIndicator.querySelectorAll('.step-label');
    stepLabels.forEach(label => {
        label.style.fontSize = '0.8rem';
        label.style.color = '#666';
    });

    const progressLines = progressIndicator.querySelectorAll('.progress-line');
    progressLines.forEach(line => {
        line.style.height = '2px';
        line.style.backgroundColor = '#e0e0e0';
        line.style.flex = '1';
        line.style.margin = '0 5px';
        line.style.alignSelf = 'center';
    });

    // Add the progress steps before the title
    const title = checkoutContainer.querySelector('.checkout-title');
    if (title) {
        checkoutContainer.insertBefore(progressIndicator, title);
    }
}

/**
 * Add delivery time estimate
 */
function addDeliveryEstimate() {
    const orderTotals = document.querySelector('.order-totals');
    if (!orderTotals) return;

    // Create delivery estimate element
    const deliveryEstimate = document.createElement('div');
    deliveryEstimate.className = 'delivery-estimate';

    // Calculate estimated delivery date (3-5 business days from now)
    const today = new Date();
    const estimatedDelivery = new Date(today);
    estimatedDelivery.setDate(today.getDate() + 3); // Minimum 3 days

    // Format date to Russian format
    const options = { day: 'numeric', month: 'long' };
    const estimatedDateStr = estimatedDelivery.toLocaleDateString('ru-RU', options);

    // Add 5 days for maximum
    const maxDelivery = new Date(today);
    maxDelivery.setDate(today.getDate() + 5);
    const maxDateStr = maxDelivery.toLocaleDateString('ru-RU', options);

    deliveryEstimate.innerHTML = `
        <div class="estimate-header">Ориентировочная доставка:</div>
        <div class="estimate-dates">${estimatedDateStr} - ${maxDateStr}</div>
    `;

    // Style the estimate
    deliveryEstimate.style.marginTop = '15px';
    deliveryEstimate.style.padding = '10px 15px';
    deliveryEstimate.style.backgroundColor = '#f0f7ff';
    deliveryEstimate.style.borderRadius = '8px';
    deliveryEstimate.style.fontSize = '0.9rem';

    // Add to DOM
    orderTotals.appendChild(deliveryEstimate);
}

/**
 * Initialize form validation with mobile-friendly feedback
 */
function initMobileFormValidation() {
    const form = document.querySelector('.checkout-form');
    if (!form) return;

    // Add novalidate to use custom validation
    form.setAttribute('novalidate', 'true');

    // Validate on submit
    form.addEventListener('submit', function(e) {
        if (!validateForm(form)) {
            e.preventDefault();

            // Scroll to first error
            const firstError = form.querySelector('.form-error:not(.hidden)');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

    // Add validation on blur for each field
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(input);
        });
    });
}

/**
 * Validate form fields
 * @param {HTMLFormElement} form - The form to validate
 * @returns {boolean} - True if form is valid
 */
function validateForm(form) {
    let isValid = true;

    // Validate all fields
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });

    return isValid;
}

/**
 * Validate a single form field
 * @param {HTMLElement} field - The field to validate
 * @returns {boolean} - True if field is valid
 */
function validateField(field) {
    // Get field's parent form group
    const formGroup = field.closest('.form-group');
    if (!formGroup) return true;

    // Get or create error element
    let errorElement = formGroup.querySelector('.form-error');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'form-error hidden';
        formGroup.appendChild(errorElement);
    }

    // Reset error
    errorElement.classList.add('hidden');
    field.classList.remove('is-invalid');

    // Skip validation for non-required fields if empty
    if (!field.hasAttribute('required') && !field.value.trim()) {
        return true;
    }

    // Check for required fields
    if (field.hasAttribute('required') && !field.value.trim()) {
        errorElement.textContent = 'Это поле обязательно для заполнения';
        errorElement.classList.remove('hidden');
        field.classList.add('is-invalid');
        return false;
    }

    // Check email format
    if (field.type === 'email' && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value.trim())) {
            errorElement.textContent = 'Введите корректный email адрес';
            errorElement.classList.remove('hidden');
            field.classList.add('is-invalid');
            return false;
        }
    }

    // Check phone format
    if (field.name === 'customer_phone' && field.value.trim()) {
        const phoneRegex = /^[+]?[0-9]{10,15}$/;
        if (!phoneRegex.test(field.value.trim())) {
            errorElement.textContent = 'Введите корректный номер телефона';
            errorElement.classList.remove('hidden');
            field.classList.add('is-invalid');
            return false;
        }
    }

    // Check for agreement to terms
    if (field.type === 'checkbox' && field.name === 'agree_to_terms' && !field.checked) {
        errorElement.textContent = 'Необходимо согласиться с условиями';
        errorElement.classList.remove('hidden');
        field.classList.add('is-invalid');
        return false;
    }

    return true;
}

/**
 * Initialize sticky checkout button
 */
function initStickyCheckoutButton() {
    // Check if we're on mobile
    if (window.innerWidth > 768) return;

    const checkoutForm = document.querySelector('.checkout-form');
    if (!checkoutForm) return;

    // Get total amount
    const totalAmount = document.querySelector('.total-value');
    if (!totalAmount) return;

    // Create sticky button container
    const stickyContainer = document.createElement('div');
    stickyContainer.className = 'sticky-checkout-footer';
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
    priceDisplay.className = 'sticky-order-price';
    priceDisplay.style.fontWeight = 'bold';
    priceDisplay.style.fontSize = '1.1rem';
    priceDisplay.style.color = '#113E71';
    priceDisplay.textContent = totalAmount.textContent;

    // Create submit button
    const submitBtn = document.createElement('button');
    submitBtn.type = 'button';
    submitBtn.className = 'sticky-order-btn';
    submitBtn.textContent = 'Оформить заказ';
    submitBtn.style.backgroundColor = '#3698D4';
    submitBtn.style.color = 'white';
    submitBtn.style.padding = '10px 20px';
    submitBtn.style.borderRadius = '50px';
    submitBtn.style.border = 'none';
    submitBtn.style.fontWeight = '600';
    submitBtn.style.cursor = 'pointer';

    // Add elements to container
    stickyContainer.appendChild(priceDisplay);
    stickyContainer.appendChild(submitBtn);

    // Add to DOM
    document.body.appendChild(stickyContainer);

    // Add padding to bottom of document to account for sticky footer
    const footerHeight = stickyContainer.offsetHeight;
    document.body.style.paddingBottom = `${footerHeight + 20}px`;

    // Handle the button click - submit the form
    submitBtn.addEventListener('click', function() {
        // Validate form before submission
        if (validateForm(checkoutForm)) {
            checkoutForm.submit();
        } else {
            // Scroll to first error
            const firstError = checkoutForm.querySelector('.form-error:not(.hidden)');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

    // Hide the sticky footer when form is visible in viewport
    window.addEventListener('scroll', function() {
        const formRect = checkoutForm.getBoundingClientRect();
        // If form is visible
        if (formRect.top < window.innerHeight * 0.7 && formRect.bottom > 0) {
            stickyContainer.style.transform = 'translateY(100%)';
            stickyContainer.style.opacity = '0';
        } else {
            stickyContainer.style.transform = 'translateY(0)';
            stickyContainer.style.opacity = '1';
        }
    });
}