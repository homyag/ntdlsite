 // Ваш JavaScript код
    const popup = document.getElementById('callback-popup');
    const popupTrigger = document.querySelector('.header_callback--popup');
    const closeBtn = document.querySelector('.popup .close-btn');

    popupTrigger.addEventListener('click', function() {
    popup.style.display = 'block';
});

    closeBtn.addEventListener('click', function() {
    popup.style.display = 'none';
});

    window.addEventListener('click', function(event) {
    if (event.target === popup) {
    popup.style.display = 'none';
}
});