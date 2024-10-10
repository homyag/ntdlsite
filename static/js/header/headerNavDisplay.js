document.getElementById('burger').addEventListener('change', function() {
    const nav = document.querySelector('.header__nav');
    const callback = document.querySelector('.header__callback');

    if (this.checked) {
        nav.style.display = 'flex';
        callback.style.display = 'flex';
        callback.style.flexDirection = 'column';
    } else {
        nav.style.display = 'none';
        callback.style.display = 'none';
    }
});