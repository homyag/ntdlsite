/**
 * Mobile-friendly enhancements for order success page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile order success features
    initMobileOrderSuccess();

    // Make order details collapsible
    makeOrderDetailsCollapsible();

    // Add timeline visualization for steps
    addStepsTimeline();

    // Add order sharing options
    addOrderSharingOptions();

    // Check for very small screens
    checkVerySmallScreen();
});

/**
 * Initialize mobile order success features
 */
function initMobileOrderSuccess() {
    // Check if we're on mobile
    if (window.innerWidth > 768) return;

    // Find the success content container
    const successContent = document.querySelector('.order-success-content');
    if (!successContent) return;

    // Add mobile-specific classes
    successContent.classList.add('mobile-success');

    // Add back to home button at top for easier navigation
    addBackButton(successContent);

    // Transform the order items table for mobile
    transformOrderTable();
}

/**
 * Add a back button for easy navigation
 * @param {HTMLElement} container - The container to add the button to
 */
function addBackButton(container) {
    const backButton = document.createElement('button');
    backButton.className = 'mobile-back-button';
    backButton.innerHTML = '&larr; На главную';
    backButton.style.background = 'none';
    backButton.style.border = 'none';
    backButton.style.color = '#3698D4';
    backButton.style.padding = '10px 0';
    backButton.style.fontSize = '0.9rem';
    backButton.style.fontWeight = '500';
    backButton.style.cursor = 'pointer';
    backButton.style.textAlign = 'left';
    backButton.style.marginBottom = '15px';
    backButton.style.width = '100%';

    // Add click event
    backButton.addEventListener('click', function() {
        window.location.href = '/';
    });

    // Insert at the top of container
    container.insertBefore(backButton, container.firstChild);
}

/**
 * Transform the order items table for better mobile display
 */
function transformOrderTable() {
    const table = document.querySelector('.items-table');
    if (!table) return;

    // Add data-label attributes to cells based on headers
    const headers = table.querySelectorAll('thead th');
    const headerTexts = Array.from(headers).map(header => header.textContent.trim());

    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, index) => {
            if (index < headerTexts.length) {
                cell.setAttribute('data-label', headerTexts[index]);
            }
        });
    });

    // Create a mobile-friendly summary
    const itemCount = rows.length;

    // Create collapsed view for mobile
    const collapsedView = document.createElement('div');
    collapsedView.className = 'mobile-items-summary';
    collapsedView.style.backgroundColor = '#f8f9fa';
    collapsedView.style.padding = '15px';
    collapsedView.style.borderRadius = '10px';
    collapsedView.style.marginBottom = '20px';
    collapsedView.style.textAlign = 'center';
    collapsedView.innerHTML = `
        <div class="mobile-items-header">
            <span>Всего товаров: ${itemCount}</span>
            <button class="mobile-view-items">Посмотреть список</button>
        </div>
    `;

    // Style the button
    const viewButton = collapsedView.querySelector('.mobile-view-items');
    viewButton.style.backgroundColor = '#3698D4';
    viewButton.style.color = 'white';
    viewButton.style.border = 'none';
    viewButton.style.padding = '8px 15px';
    viewButton.style.borderRadius = '50px';
    viewButton.style.fontSize = '0.9rem';
    viewButton.style.cursor = 'pointer';
    viewButton.style.marginTop = '10px';

    // Add click functionality
    viewButton.addEventListener('click', function() {
        if (table.style.display === 'none') {
            table.style.display = 'table';
            viewButton.textContent = 'Скрыть список';
        } else {
            table.style.display = 'none';
            viewButton.textContent = 'Посмотреть список';
        }
    });

    // Initially hide the table
    table.style.display = 'none';

    // Add the collapsed view before the table
    table.parentNode.insertBefore(collapsedView, table);
}

/**
 * Make sections collapsible for mobile view
 */
function makeOrderDetailsCollapsible() {
    // Only apply on mobile
    if (window.innerWidth > 768) return;

    makeCollapsible('.order-summary', 'Детали заказа');
    makeCollapsible('.shipping-info', 'Информация о доставке');
}

/**
 * Make a section collapsible on mobile
 * @param {string} selector - CSS selector for the section
 * @param {string} title - Title for the collapsible section
 */
function makeCollapsible(selector, title) {
    const section = document.querySelector(selector);
    if (!section) return;

    // Get the original title
    const originalTitle = section.querySelector('h2, h3');
    const titleText = originalTitle ? originalTitle.textContent : title;

    // Create collapsible header
    const header = document.createElement('div');
    header.className = 'collapsible-header';
    header.innerHTML = `
        <h3>${titleText}</h3>
        <span class="collapse-arrow">▼</span>
    `;

    // Style the header
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.style.padding = '15px';
    header.style.backgroundColor = '#f0f7ff';
    header.style.borderRadius = '8px';
    header.style.marginBottom = '15px';
    header.style.cursor = 'pointer';

    // Get the content to make collapsible
    const content = document.createElement('div');
    content.className = 'collapsible-content';

    // Move all children except the title to the content div
    while (section.children.length > 0) {
        if (section.firstChild === originalTitle) {
            section.removeChild(originalTitle);
        } else {
            content.appendChild(section.firstChild);
        }
    }

    // Style the content
    content.style.overflow = 'hidden';
    content.style.transition = 'max-height 0.3s ease';
    content.style.maxHeight = '1000px'; // Initially expanded

    // Add the header and content to the section
    section.appendChild(header);
    section.appendChild(content);

    // Add click event to toggle
    header.addEventListener('click', function() {
        const arrow = header.querySelector('.collapse-arrow');

        if (content.style.maxHeight === '1000px') {
            content.style.maxHeight = '0';
            arrow.textContent = '▶';
            content.style.marginTop = '0';
        } else {
            content.style.maxHeight = '1000px';
            arrow.textContent = '▼';
            content.style.marginTop = '15px';
        }
    });
}

/**
 * Add timeline visualization for steps
 */
function addStepsTimeline() {
    // Only apply on mobile
    if (window.innerWidth > 768) return;

    const nextSteps = document.querySelector('.next-steps');
    if (!nextSteps) return;

    // Get steps from ordered list
    const stepsOl = nextSteps.querySelector('ol');
    if (!stepsOl) return;

    // Create timeline container
    const timelineContainer = document.createElement('div');
    timelineContainer.className = 'steps-timeline';
    timelineContainer.style.marginTop = '20px';
    timelineContainer.style.marginBottom = '20px';

    // Get all steps
    const steps = Array.from(stepsOl.querySelectorAll('li'));

    // Create timeline HTML
    steps.forEach((step, index) => {
        const timelineStep = document.createElement('div');
        timelineStep.className = 'timeline-step';
        timelineStep.style.display = 'flex';
        timelineStep.style.marginBottom = '15px';
        timelineStep.style.position = 'relative';

        // Create step number indicator
        const stepNumber = document.createElement('div');
        stepNumber.className = 'step-number';
        stepNumber.textContent = index + 1;
        stepNumber.style.width = '28px';
        stepNumber.style.height = '28px';
        stepNumber.style.borderRadius = '50%';
        stepNumber.style.backgroundColor = '#3698D4';
        stepNumber.style.color = 'white';
        stepNumber.style.display = 'flex';
        stepNumber.style.alignItems = 'center';
        stepNumber.style.justifyContent = 'center';
        stepNumber.style.fontWeight = 'bold';
        stepNumber.style.flexShrink = '0';
        stepNumber.style.fontSize = '0.9rem';

        // Create line connecting steps
        const line = document.createElement('div');
        line.className = 'timeline-line';
        line.style.position = 'absolute';
        line.style.left = '14px'; // Half of the step number width
        line.style.top = '28px';
        line.style.width = '2px';
        line.style.backgroundColor = '#3698D4';
        line.style.height = '15px';
        line.style.opacity = '0.5';

        // If last step, don't show line
        if (index === steps.length - 1) {
            line.style.display = 'none';
        }

        // Create step content
        const stepContent = document.createElement('div');
        stepContent.className = 'step-content';
        stepContent.textContent = step.textContent;
        stepContent.style.marginLeft = '15px';
        stepContent.style.paddingTop = '5px';
        stepContent.style.fontSize = '0.95rem';
        stepContent.style.color = '#333';

        // Add to timeline step
        timelineStep.appendChild(stepNumber);
        timelineStep.appendChild(stepContent);
        if (index < steps.length - 1) {
            timelineStep.appendChild(line);
        }

        // Add to timeline container
        timelineContainer.appendChild(timelineStep);
    });

    // Replace the original ordered list with the timeline
    stepsOl.parentNode.replaceChild(timelineContainer, stepsOl);
}

/**
 * Add order sharing options for mobile
 */
function addOrderSharingOptions() {
    // Only apply on mobile
    if (window.innerWidth > 768) return;

    // Find success actions
    const successActions = document.querySelector('.success-actions');
    if (!successActions) return;

    // Get order ID
    const orderNumberEl = document.querySelector('.order-number');
    if (!orderNumberEl) return;

    // Extract order number
    const orderText = orderNumberEl.textContent;
    const orderNumber = orderText.match(/#(\d+)/);
    if (!orderNumber || !orderNumber[1]) return;

    // Create share section
    const shareSection = document.createElement('div');
    shareSection.className = 'order-share-section';
    shareSection.innerHTML = `
        <p>Поделиться заказом:</p>
        <div class="share-buttons">
            <button class="share-btn whatsapp-share">WhatsApp</button>
            <button class="share-btn telegram-share">Telegram</button>
            <button class="share-btn copy-order">Копировать №</button>
        </div>
    `;

    // Style share section
    shareSection.style.marginTop = '25px';
    shareSection.style.textAlign = 'center';
    shareSection.style.marginBottom = '20px';

    // Style share buttons container
    const shareButtons = shareSection.querySelector('.share-buttons');
    shareButtons.style.display = 'flex';
    shareButtons.style.justifyContent = 'center';
    shareButtons.style.gap = '10px';
    shareButtons.style.marginTop = '10px';
    shareButtons.style.flexWrap = 'wrap';

    // Style share buttons
    const buttons = shareSection.querySelectorAll('.share-btn');
    buttons.forEach(button => {
        button.style.border = 'none';
        button.style.padding = '8px 15px';
        button.style.borderRadius = '50px';
        button.style.fontSize = '0.9rem';
        button.style.fontWeight = '500';
        button.style.cursor = 'pointer';
        button.style.minWidth = '110px';
    });

    // Style WhatsApp button
    const whatsappBtn = shareSection.querySelector('.whatsapp-share');
    whatsappBtn.style.backgroundColor = '#25D366';
    whatsappBtn.style.color = 'white';

    // Style Telegram button
    const telegramBtn = shareSection.querySelector('.telegram-share');
    telegramBtn.style.backgroundColor = '#0088cc';
    telegramBtn.style.color = 'white';

    // Style Copy button
    const copyBtn = shareSection.querySelector('.copy-order');
    copyBtn.style.backgroundColor = '#f0f0f0';
    copyBtn.style.color = '#333';

    // Add event listeners
    whatsappBtn.addEventListener('click', function() {
        const shareText = `Я оформил(а) заказ #${orderNumber[1]} в ТД Ленинградский!`;
        const shareUrl = `whatsapp://send?text=${encodeURIComponent(shareText)}`;
        window.location.href = shareUrl;
    });

    telegramBtn.addEventListener('click', function() {
        const shareText = `Я оформил(а) заказ #${orderNumber[1]} в ТД Ленинградский!`;
        const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(window.location.href)}&text=${encodeURIComponent(shareText)}`;
        window.location.href = shareUrl;
    });

    copyBtn.addEventListener('click', function() {
        // Create a temporary input element
        const tempInput = document.createElement('input');
        tempInput.setAttribute('value', `Заказ #${orderNumber[1]}`);
        document.body.appendChild(tempInput);

        // Select and copy the text
        tempInput.select();
        document.execCommand('copy');

        // Remove the temporary element
        document.body.removeChild(tempInput);

        // Show copied feedback
        copyBtn.textContent = 'Скопировано!';
        copyBtn.style.backgroundColor = '#4CAF50';
        copyBtn.style.color = 'white';

        // Reset button after 2 seconds
        setTimeout(() => {
            copyBtn.textContent = 'Копировать №';
            copyBtn.style.backgroundColor = '#f0f0f0';
            copyBtn.style.color = '#333';
        }, 2000);
    });

    // Add to DOM
    successActions.parentNode.insertBefore(shareSection, successActions);
}

/**
 * Проверка на очень маленький экран (320px)
 * и применение соответствующих стилей
 */
function checkVerySmallScreen() {
    if (window.innerWidth <= 320) {
        // Adapt share buttons
        const shareButtons = document.querySelector('.share-buttons');
        if (shareButtons) {
            shareButtons.style.flexDirection = 'column';
            shareButtons.style.gap = '8px';

            const buttons = shareButtons.querySelectorAll('.share-btn');
            buttons.forEach(button => {
                button.style.width = '100%';
                button.style.fontSize = '0.85rem';
                button.style.padding = '7px 10px';
            });
        }

        // Make timeline more compact
        const timelineSteps = document.querySelectorAll('.timeline-step');
        if (timelineSteps.length > 0) {
            timelineSteps.forEach(step => {
                const stepNumber = step.querySelector('.step-number');
                if (stepNumber) {
                    stepNumber.style.width = '24px';
                    stepNumber.style.height = '24px';
                    stepNumber.style.fontSize = '0.8rem';
                }

                const stepContent = step.querySelector('.step-content');
                if (stepContent) {
                    stepContent.style.fontSize = '0.85rem';
                }

                const line = step.querySelector('.timeline-line');
                if (line) {
                    line.style.left = '12px'; // Adjust position of line
                    line.style.top = '24px';
                }
            });
        }

        // Adjust buttons in success-actions
        const actionButtons = document.querySelectorAll('.success-actions a');
        if (actionButtons.length > 0) {
            actionButtons.forEach(button => {
                button.style.fontSize = '0.85rem';
                button.style.padding = '8px 12px';
            });
        }
    }
}

// Add resize event listener
window.addEventListener('resize', checkVerySmallScreen);