document.addEventListener('DOMContentLoaded', function () {
    // Обработчик клика для переключения выпадающего меню
    const dropdownToggles = document.querySelectorAll('.dropdown__toggle');

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            // Если это клик непосредственно на стрелке, только переключаем меню
            if (e.target.classList.contains('dropdown__arrow')) {
                e.preventDefault(); // Предотвращаем переход по ссылке
                const dropdownContent = this.nextElementSibling;

                // Закрываем все другие выпадающие меню
                document.querySelectorAll('.dropdown__content').forEach(function (content) {
                    if (content !== dropdownContent) {
                        content.style.display = 'none';
                    }
                });

                // Переключаем текущее выпадающее меню
                if (dropdownContent.style.display === 'block') {
                    dropdownContent.style.display = 'none';
                } else {
                    dropdownContent.style.display = 'block';
                }
            }
            // Если клик не на стрелке, позволяем переход по ссылке
        });

        // Дополнительный обработчик для стрелки (более надежное решение)
        const arrow = toggle.querySelector('.dropdown__arrow');
        if (arrow) {
            arrow.addEventListener('click', function(e) {
                e.preventDefault(); // Предотвращаем событие клика по ссылке
                e.stopPropagation(); // Предотвращаем всплытие события

                const dropdownContent = toggle.nextElementSibling;

                // Закрываем все другие выпадающие меню
                document.querySelectorAll('.dropdown__content').forEach(function (content) {
                    if (content !== dropdownContent) {
                        content.style.display = 'none';
                    }
                });

                // Переключаем текущее выпадающее меню
                if (dropdownContent.style.display === 'block') {
                    dropdownContent.style.display = 'none';
                } else {
                    dropdownContent.style.display = 'block';
                }
            });
        }
    });

    // Закрытие выпадающего меню при клике вне его
    window.addEventListener('click', function (e) {
        if (!e.target.matches('.dropdown__toggle') &&
            !e.target.matches('.dropdown__content') &&
            !e.target.matches('.dropdown__arrow') &&
            !e.target.closest('.dropdown__content')) {

            document.querySelectorAll('.dropdown__content').forEach(function (content) {
                content.style.display = 'none';
            });
        }
    });

    // Предотвращаем закрытие меню при клике внутри выпадающего содержимого
    document.querySelectorAll('.dropdown__content').forEach(function (content) {
        content.addEventListener('click', function (e) {
            e.stopPropagation(); // Предотвращаем всплытие события
        });
    });
});