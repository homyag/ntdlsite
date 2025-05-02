/**
 * Mobile-friendly enhancements for order success page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile order success features
    initMobileOrderSuccess();

    // Add confetti animation for celebration
    showSuccessConfetti();

    // Add delivery tracking preview
    addDeliveryTrackingPreview();

    // Add order sharing options
    addOrderShareOptions();
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

    // Add click event
    backButton.addEventListener('click', function() {
        window.location.href = '/';
    });

    // Insert at the top of container
    successContent.insertBefore(backButton, successContent.firstChild);

    // Make order details collapsible
    makeCollapsible('.order-summary', 'Детали заказа');

    // Make shipping info collapsible
    makeCollapsible('.shipping-info', 'Информация о доставке');

    // Enhance next steps section
    enhanceNextSteps();
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
 * Enhance the next steps section
 */
function enhanceNextSteps() {
    const nextSteps = document.querySelector('.next-steps');
    if (!nextSteps) return;

    // Create a timeline visualization
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

        // Create step number indicator
        const stepNumber = document.createElement('div');
        stepNumber.className = 'step-number';
        stepNumber.textContent = index + 1;
        stepNumber.style.width = '30px';
        stepNumber.style.height = '30px';
        stepNumber.style.borderRadius = '50%';
        stepNumber.style.backgroundColor = '#3698D4';
        stepNumber.style.color = 'white';
        stepNumber.style.display = 'flex';
        stepNumber.style.alignItems = 'center';
        stepNumber.style.justifyContent = 'center';
        stepNumber.style.fontWeight = 'bold';
        stepNumber.style.flexShrink = '0';

        // Create line connecting steps
        const line = document.createElement('div');
        line.className = 'timeline-line';
        line.style.width = '2px';
        line.style.backgroundColor = '#3698D4';
        line.style.margin = '0 auto';
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

        // Add to timeline step
        timelineStep.appendChild(stepNumber);
        timelineStep.appendChild(stepContent);

        // Add to timeline container
        timelineContainer.appendChild(timelineStep);

        // Add connecting line if not last step
        if (index < steps.length - 1) {
            const lineContainer = document.createElement('div');
            lineContainer.style.display = 'flex';
            lineContainer.style.paddingLeft = '15px';
            lineContainer.appendChild(line);
            timelineContainer.appendChild(lineContainer);
        }
    });

    // Replace the original ordered list with the timeline
    stepsOl.parentNode.replaceChild(timelineContainer, stepsOl);
}

/**
 * Show success confetti animation
 */
function showSuccessConfetti() {
    // Check if we're on mobile
    if (window.innerWidth > 768) return;

    // Find success icon
    const successIcon = document.querySelector('.success-icon');
    if (!successIcon) return;

    // Create canvas for confetti
    const canvas = document.createElement('canvas');
    canvas.id = 'success-confetti';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '100';

    // Add to DOM
    document.body.appendChild(canvas);

    // Simple confetti effect using canvas
    const ctx = canvas.getContext('2d');
    const particles = [];
    const colors = ['#3698D4', '#113E71', '#4CAF50', '#FFC107', '#FF5722'];

    // Create particles
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            size: Math.random() * 5 + 5,
            color: colors[Math.floor(Math.random() * colors.length)],
            speed: Math.random() * 3 + 2,
            angle: Math.random() * 2 - 1,
            rotation: Math.random() * 360,
            rotationSpeed: Math.random() * 10 - 5
        });
    }

    // Animation function
    function animate() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw and update particles
        for (let i = 0; i < particles.length; i++) {
            const particle = particles[i];

            // Draw particle
            ctx.save();
            ctx.translate(particle.x, particle.y);
            ctx.rotate(particle.rotation * Math.PI / 180);
            ctx.fillStyle = particle.color;
            ctx.fillRect(-particle.size / 2, -particle.size / 2, particle.size, particle.size);
            ctx.restore();

            // Update particle
            particle.y += particle.speed;
            particle.x += particle.angle;
            particle.rotation += particle.rotationSpeed;

            // Reset particle when it goes off screen
            if (particle.y > canvas.height) {
                particles[i].y = -particle.size;
                particles[i].x = Math.random() * canvas.width;
            }
        }

        // Continue animation
        requestAnimationFrame(animate);
    }

    // Start animation
    animate();

    // Remove after 5 seconds
    setTimeout(() => {
        canvas.remove();
    }, 5000);
}

/**
 * Add delivery tracking preview
 */
function addDeliveryTrackingPreview() {
    // Check if we're on mobile
    if (window.innerWidth > 768) return;

    // Find shipping info section
    const shippingInfo = document.querySelector('.shipping-info');
    if (!shippingInfo) return;

    // Create tracking preview
    const trackingPreview = document.createElement('div');
    trackingPreview.className = 'delivery-tracking-preview';
    trackingPreview.innerHTML = `
        <h4>Статус доставки</h4>
        <div class="tracking-status">
            <div class="status-circle active"></div>
            <div class="status-line"></div>
            <div class="status-circle"></div>
            <div class="status-line"></div>
            <div class="status-circle"></div>
            <div class="status-line"></div>
            <div class="status-circle"></div>
        </div>
        <div class="tracking-labels">
            <div class="status-label active">Заказ принят</div>
            <div class="status-label">Обработка</div>
            <div class="status-label">Отправлен</div>
            <div class="status-label">Доставлен</div>
        </div>
        <p class="tracking-note">Следите за статусом заказа в личном кабинете</p>
    `;

    // Style the tracking preview
    trackingPreview.style.backgroundColor = '#f8f9fa';
    trackingPreview.style.padding = '15px';
    trackingPreview.style.borderRadius = '8px';
    trackingPreview.style.marginTop = '20px';

    // Style tracking status
    const trackingStatus = trackingPreview.querySelector('.tracking-status');
    trackingStatus.style.display = 'flex';
    trackingStatus.style.alignItems = 'center';
    trackingStatus.style.marginBottom = '10px';

    // Style status circles
    const statusCircles = trackingPreview.querySelectorAll('.status-circle');
    statusCircles.forEach(circle => {
        circle.style.width = '20px';
        circle.style.height = '20px';
        circle.style.borderRadius = '50%';
        circle.style.backgroundColor = '#ddd';
        circle.style.flexShrink = '0';
    });

    // Style active circle
    const activeCircle = trackingPreview.querySelector('.status-circle.active');
    if (activeCircle) {
        activeCircle.style.backgroundColor = '#4CAF50';
    }

    // Style status lines
    const statusLines = trackingPreview.querySelectorAll('.status-line');
    statusLines.forEach(line => {
        line.style.flex = '1';
        line.style.height = '2px';
        line.style.backgroundColor = '#ddd';
    });

    // Style tracking labels
    const trackingLabels = trackingPreview.querySelector('.tracking-labels');
    trackingLabels.style.display = 'flex';
    trackingLabels.style.justifyContent = 'space-between';
    trackingLabels.style.fontSize = '0.8rem';
    trackingLabels.style.color = '#666';

    // Style active label
    const activeLabel = trackingPreview.querySelector('.status-label.active');
    if (activeLabel) {
        activeLabel.style.color = '#4CAF50';
        activeLabel.style.fontWeight = 'bold';
    }

    // Style tracking note
    const trackingNote = trackingPreview.querySelector('.tracking-note');
    trackingNote.style.fontSize = '0.85rem';
    trackingNote.style.color = '#666';
    trackingNote.style.marginTop = '15px';
    trackingNote.style.textAlign = 'center';
    trackingNote.style.fontStyle = 'italic';

    // Add to shipping info section
    shippingInfo.appendChild(trackingPreview);
}

/**
 * Add order sharing options for mobile
 */
function addOrderShareOptions() {
    // Check if we're on mobile
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
            <button class="share-btn whatsapp-share">
                <span>WhatsApp</span>
            </button>
            <button class="share-btn telegram-share">
                <span>Telegram</span>
            </button>
            <button class="share-btn copy-order">
                <span>Копировать №</span>
            </button>
        </div>
    `;

    // Style share section
    shareSection.style.marginTop = '25px';
    shareSection.style.textAlign = 'center';

    // Style share buttons container
    const shareButtons = shareSection.querySelector('.share-buttons');
    shareButtons.style.display = 'flex';
    shareButtons.style.justifyContent = 'center';
    shareButtons.style.gap = '10px';
    shareButtons.style.marginTop = '10px';

    // Style share buttons
    const buttons = shareSection.querySelectorAll('.share-btn');
    buttons.forEach(button => {
        button.style.border = 'none';
        button.style.padding = '8px 15px';
        button.style.borderRadius = '50px';
        button.style.fontSize = '0.9rem';
        button.style.fontWeight = '500';
        button.style.cursor = 'pointer';
        button.style.display = 'flex';
        button.style.alignItems = 'center';
        button.style.justifyContent = 'center';
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
            copyBtn.innerHTML = '<span>Копировать №</span>';
            copyBtn.style.backgroundColor = '#f0f0f0';
            copyBtn.style.color = '#333';
        }, 2000);
    });

    // Add to DOM
    successActions.parentNode.insertBefore(shareSection, successActions.nextSibling);
}