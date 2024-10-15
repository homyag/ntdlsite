document.addEventListener('DOMContentLoaded', function() {
    var cityModal = document.getElementById('city-modal');
    var citySlug = "{{ city_slug|default:'' }}";

    if (!citySlug) {
        // Если город не выбран, показываем модальное окно
        cityModal.style.display = 'block';
    }

    // Обработчик для кнопки "Выбрать город" (если город не выбран)
    var selectCityButton = document.getElementById('select-city');
    if (selectCityButton) {
        selectCityButton.addEventListener('click', function(event) {
            event.preventDefault();
            cityModal.style.display = 'block';
        });
    }

    // Закрытие модального окна при клике вне его области
    window.onclick = function(event) {
        if (event.target == cityModal) {
            cityModal.style.display = "none";
        }
    }
});