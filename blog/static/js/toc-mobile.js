document.addEventListener('DOMContentLoaded', function() {
    const tocContainer = document.querySelector('.table-of-contents');
    const tocTitle = document.querySelector('.toc-title');

    if (!tocContainer || !tocTitle) {
        return;
    }

    // Проверяем, не установлены ли уже какие-то обработчики
    const clonedTitle = tocTitle.cloneNode(true);
    tocTitle.parentNode.replaceChild(clonedTitle, tocTitle);

    // Добавляем явный обработчик
    clonedTitle.addEventListener('click', function(e) {
        if (window.innerWidth <= 576) {
            tocContainer.classList.toggle('collapsed');
        }
    });
});