// static/js/cityModal.js

document.addEventListener('DOMContentLoaded', function() {
    var cityModal = document.getElementById('city-modal');

    // Функция для открытия модального окна
    function openCityModal() {
        if (cityModal) {
            cityModal.style.display = 'block';
        }
    }

    // Добавляем обработчик клика для кнопки "Выбрать город"
    var selectCityButton = document.getElementById('select-city');
    if (selectCityButton) {
        selectCityButton.addEventListener('click', function(event) {
            event.preventDefault();
            openCityModal();
        });
    }

    // Добавляем обработчик клика для кнопки "Сменить город"
    var changeCityButton = document.getElementById('change-city');
    if (changeCityButton) {
        changeCityButton.addEventListener('click', function(event) {
            event.preventDefault();
            openCityModal();
        });
    }

    // Закрываем модальное окно при клике вне его области
    window.onclick = function(event) {
        if (event.target == cityModal) {
            cityModal.style.display = "none";
        }
    }

    // Обработка закрытия модального окна при клике на кнопку закрытия
    var closeBtn = document.querySelector('#city-modal .close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            cityModal.style.display = 'none';
        });
    }
});