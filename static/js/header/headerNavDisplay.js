document.getElementById('burger').addEventListener('change', function() {
    const nav = document.querySelector('.header__nav');
    if (this.checked) {
        nav.style.display = 'flex';
    } else {
        nav.style.display = 'none';
    }
    const callback = document.querySelector('.header__callback');
    if (this.checked) {
        callback.style.display = 'flex';
        callback.style.flexDirection = 'column';
    } else {
        callback.style.display = 'none';
    }
});