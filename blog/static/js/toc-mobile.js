document.addEventListener('DOMContentLoaded', function() {
    // Функция настройки мобильного TOC
    function setupMobileTOC() {
        const tocContainer = document.querySelector('.table-of-contents');
        if (!tocContainer) {
            return;
        }

        const tocTitle = tocContainer.querySelector('.toc-title');
        if (!tocTitle) {
            return;
        }

        const isMobile = window.innerWidth <= 576;

        // Добавляем функционал сворачивания на мобильных
        if (isMobile) {
            // Инициализируем свернутое состояние на мобильных
            tocContainer.classList.add('collapsed');

            // Удаляем существующие обработчики, чтобы избежать дубликатов
            tocTitle.removeEventListener('click', toggleTOC);

            // Добавляем обработчик клика для заголовка
            tocTitle.addEventListener('click', toggleTOC);
        } else {
            // Разворачиваем на десктопах
            tocContainer.classList.remove('collapsed');
        }
    }

    // Функция для переключения состояния TOC
    function toggleTOC() {
        const tocContainer = document.querySelector('.table-of-contents');
        if (tocContainer) {
            tocContainer.classList.toggle('collapsed');
        }
    }

    // Вызываем функцию при загрузке
    setupMobileTOC();

    // И при изменении размера окна
    window.addEventListener('resize', setupMobileTOC);
});