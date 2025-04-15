// static/js/cityModal.js

document.addEventListener('DOMContentLoaded', function() {
    var cityModal = document.getElementById('city-modal');

    function openCityModal() {
        if (cityModal) {
            cityModal.style.display = 'block';
        }
    }

    function closeCityModal() {
        if (cityModal) {
            cityModal.style.display = 'none';
        }
    }

    // Обработчик для кнопки "Выбрать город"
    var selectCityButton = document.getElementById('select-city');
    if (selectCityButton) {
        selectCityButton.addEventListener('click', function(event) {
            event.preventDefault();
            openCityModal();
        });
    }

    // Обработчик для кнопки "Сменить город"
    var changeCityButton = document.getElementById('change-city');
    if (changeCityButton) {
        changeCityButton.addEventListener('click', function(event) {
            event.preventDefault();
            openCityModal();
        });
    }

    // Получаем список city_slugs из JSON
    var citiesSlugsElement = document.getElementById('cities-data');
    var citiesSlugs = [];
    if (citiesSlugsElement) {
        citiesSlugs = JSON.parse(citiesSlugsElement.textContent);
    }

    // Обработка отправки формы выбора города
    var cityForm = document.getElementById('city-form');
    if (cityForm) {
        cityForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var selectedCitySlug = cityForm.elements['city_slug'].value;

            // Получаем текущий путь
            var path = window.location.pathname;

            // Проверяем, начинается ли путь с '/catalog/'
            if (path.startsWith('/catalog/')) {
                // Разбиваем путь на части
                var pathParts = path.split('/').filter(function(part) {
                    return part.length > 0;
                });

                // 'catalog' должен быть первым компонентом
                if (pathParts[0] === 'catalog') {
                    if (pathParts.length > 1 && citiesSlugs.includes(pathParts[1])) {
                        // Заменяем существующий city_slug на новый
                        pathParts[1] = selectedCitySlug;
                    } else {
                        // Вставляем новый city_slug после 'catalog'
                        pathParts.splice(1, 0, selectedCitySlug);
                    }

                    // Формируем новый путь
                    var newPath = '/' + pathParts.join('/') + '/';

                    // Перенаправляем пользователя на новый URL
                    window.location.href = newPath + window.location.search + window.location.hash;
                } else {
                    // Если 'catalog' не найден в пути, перенаправляем на каталог с выбранным городом
                    var newPath = '/catalog/' + selectedCitySlug + '/';
                    window.location.href = newPath + window.location.search + window.location.hash;
                }
            } else {
                // Для не-каталог страниц, отправляем форму на 'set_city' без изменения URL

                // Создаем скрытую форму для отправки POST запроса
                var form = document.createElement('form');
                form.method = 'POST';
                form.action = window.setCityUrl;  // Используем глобальную переменную, установленную в шаблоне

                // Добавляем CSRF токен
                var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                var csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                // Добавляем выбранный city_slug
                var cityInput = document.createElement('input');
                cityInput.type = 'hidden';
                cityInput.name = 'city_slug';
                cityInput.value = selectedCitySlug;
                form.appendChild(cityInput);

                // Добавляем форму в документ и отправляем
                document.body.appendChild(form);
                form.submit();
            }
        });
    }

    // Закрываем модальное окно при клике на крестик
    var closeBtn = document.querySelector('#city-modal .close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            closeCityModal();
        });
    }

    // Закрываем модальное окно при клике вне его области
    window.onclick = function(event) {
        if (event.target == cityModal) {
            closeCityModal();
        }
    }
});