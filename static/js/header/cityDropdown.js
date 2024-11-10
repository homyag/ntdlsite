document.addEventListener('DOMContentLoaded', function () {
    // Обработчик клика для переключения выпадающего меню
    const dropdownToggles = document.querySelectorAll('.dropdown__toggle');

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
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
        });
    });

    // Закрытие выпадающего меню при клике вне его
    window.addEventListener('click', function (e) {
        if (!e.target.matches('.dropdown__toggle')) {
            document.querySelectorAll('.dropdown__content').forEach(function (content) {
                content.style.display = 'none';
            });
        }
    });
});