    const popup = document.getElementById('callback-popup');
    const popupTrigger = document.querySelectorAll('.header_callback--popup,' +
        ' .hero__button--popup');
    const closeBtn = document.querySelector('.popup .close-btn');

    popupTrigger.forEach(trigger => {
    trigger.addEventListener('click', function() {
        popup.style.display = 'block';
    })
});

    closeBtn.addEventListener('click', function() {
    popup.style.display = 'none';
});

    window.addEventListener('click', function(event) {
    if (event.target === popup) {
    popup.style.display = 'none';
}
});