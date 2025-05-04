document.addEventListener('DOMContentLoaded', function() {
    // Ищем блок с контентом статьи
    const contentElement = document.querySelector('.post-content');

    if (!contentElement) {
        return;
    }

    // Ищем все заголовки внутри контента
    const headings = contentElement.querySelectorAll('h1, h2, h3, h4, h5, h6');

    // Если заголовков нет, не создаем оглавление
    if (headings.length == 0) {
        return;
    }

    // Создаем контейнер для оглавления
    const tocContainer = document.createElement('div');
    tocContainer.className = 'table-of-contents';
    tocContainer.innerHTML = '<h4 class="toc-title">Содержание</h4>';

    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';

    // Отслеживаем уровни заголовков для правильной вложенности
    let previousLevel = 0;
    let currentList = tocList;
    let listStack = [tocList];

    // Обрабатываем каждый заголовок
    headings.forEach((heading, index) => {
        // Добавляем ID к заголовку, если его нет
        if (!heading.id) {
            heading.id = 'heading-' + index;
        }

        const headingLevel = parseInt(heading.tagName.substring(1));
        const headingText = heading.textContent;

        // Создаем элемент оглавления
        const listItem = document.createElement('li');
        listItem.className = 'toc-item toc-level-' + headingLevel;

        const link = document.createElement('a');
        link.href = '#' + heading.id;
        link.textContent = headingText;
        link.className = 'toc-link';

        listItem.appendChild(link);

        // Обрабатываем вложенность в зависимости от уровня заголовков
        if (headingLevel > previousLevel) {
            // Создаем новый вложенный список
            const nestedList = document.createElement('ul');
            nestedList.className = 'toc-sublist';

            // Если это первый заголовок - просто добавляем его в основной список
            if (previousLevel === 0) {
                currentList.appendChild(listItem);
            } else {
                // Иначе добавляем вложенный список к последнему элементу текущего списка
                if (listStack[listStack.length - 1].lastChild) {
                    listStack[listStack.length - 1].lastChild.appendChild(nestedList);
                    listStack.push(nestedList);
                    currentList = nestedList;
                } else {
                    // Если последнего элемента нет, добавляем в текущий список
                    currentList.appendChild(listItem);
                }
            }
        } else if (headingLevel < previousLevel) {
            // Поднимаемся на уровень вверх
            const levelsUp = previousLevel - headingLevel;
            for (let i = 0; i < levelsUp; i++) {
                if (listStack.length > 1) {
                    listStack.pop();
                }
            }
            currentList = listStack[listStack.length - 1];
            currentList.appendChild(listItem);
        } else {
            // Тот же уровень - просто добавляем в текущий список
            currentList.appendChild(listItem);
        }

        previousLevel = headingLevel;
    });

    tocContainer.appendChild(tocList);

    // Добавляем оглавление перед контентом
    contentElement.parentNode.insertBefore(tocContainer, contentElement);

    // Добавляем подсветку активного раздела при прокрутке
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;

        // Находим, какой заголовок сейчас видим
        headings.forEach((heading) => {
            const headingTop = heading.getBoundingClientRect().top + window.scrollY;
            const headingBottom = headingTop + heading.offsetHeight;

            if (scrollPosition >= headingTop - 100 && scrollPosition < headingBottom) {
                // Убираем активный класс со всех ссылок
                document.querySelectorAll('.toc-link').forEach(link => {
                    link.classList.remove('active');
                });

                // Добавляем активный класс текущему заголовку
                const correspondingLink = document.querySelector(`.toc-link[href="#${heading.id}"]`);
                if (correspondingLink) {
                    correspondingLink.classList.add('active');
                }
            }
        });
    });

    // Добавляем функциональность сворачивания для мобильных устройств
    const tocTitle = tocContainer.querySelector('.toc-title');
    if (tocTitle) {
        tocTitle.addEventListener('click', function() {
            if (window.innerWidth <= 576) {
                tocContainer.classList.toggle('collapsed');
            }
        });

        // По умолчанию сворачиваем на мобильных
        if (window.innerWidth <= 576) {
            tocContainer.classList.add('collapsed');
        }
    }
});