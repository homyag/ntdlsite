document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, показывался ли уже попап
    const telegramPopupShown = localStorage.getItem('telegramPopupShown');

    // Если попап еще не показывался
    if (!telegramPopupShown) {
        // Показываем попап через 3 секунды после загрузки страницы
        setTimeout(function() {
            showTelegramPopup();
        }, 15000);
    }

    // Получаем элементы попапа
    const telegramPopup = document.getElementById('telegram-popup');
    const closeBtn = document.querySelector('.telegram-close-btn');

    // Закрытие по клику на крестик
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            closeTelegramPopup();
        });
    }

    // Закрытие по клику вне попапа
    window.addEventListener('click', function(event) {
        if (event.target === telegramPopup) {
            closeTelegramPopup();
        }
    });

    // Таргетирование содержимого попапа
    targetPopupContent();
});

// Функция для определения типа страницы и настройки контента
function targetPopupContent() {
    const currentPath = window.location.pathname;
    const popupTitle = document.querySelector('.telegram-modal-header h3');
    const popupText = document.querySelector('.telegram-modal-body p');
    const popupButton = document.querySelector('.telegram-modal-body .telegram-button');
    const benefitsList = document.querySelector('.telegram-benefits');

    // Объект с вариантами контента
    const contentVariants = {
        beton: {
            title: 'Будьте в курсе цен на бетон!',
            text: 'Подписывайтесь на наш Telegram канал и узнавайте первыми о новых поставках и специальных предложениях на бетонные смеси.',
            benefits: [
                '🏗️ Акции на разные марки бетона',
                '📊 Информация о наличии на производстве',
                '💡 Советы по выбору бетона для разных типов строительства'
            ],
            buttonText: 'Следить за ценами на бетон'
        },

        // нерудные
        nerudnye: {
            title: 'Все о нерудных материалах в Telegram',
            text: 'Присоединяйтесь к нашему каналу и получайте актуальную информацию о песке, щебне и других нерудных материалах.',
            benefits: [
                '🔍 Обзоры разных фракций щебня и песка',
                '💰 Выгодные предложения на оптовые заказы',
                '🚚 Информация о сроках доставки'
            ],
            buttonText: 'Подписаться на канал'
        },

        // щебень
        sheben: {
            title: 'Следите за ценами на щебень!',
            text: 'В нашем Telegram канале первыми узнавайте о поступлении новых партий щебня разных фракций.',
            benefits: [
                '📢 Оповещения о новых снижении цен на щебень',
                '💵 Сезонные скидки на разные фракции',
                '🚛 Прямой контакт с оператором для срочной доставки'
            ],
            buttonText: 'Подписаться на обновления'
        },

        // песок
        pesok: {
            title: 'Новости и акции на песок',
            text: 'Подписывайтесь на Telegram и будьте в курсе наличия и цен на разные типы песка.',
            benefits: [
                '🏝️ Информация о наличии разных видов песка',
                '💹 Специальные оптовые цены для подписчиков',
                '⚖️ Рекомендации по выбору песка для разных работ'
            ],
            buttonText: 'Следить за ценами на песок'
        },

        // асфальт
        asfalt: {
            title: 'Все об асфальте в нашем Telegram',
            text: 'Присоединяйтесь к каналу, чтобы первыми узнавать о поставках и акциях на асфальтобетон.',
            benefits: [
                '🛣️ Информация о разных марках асфальта',
                '💲 Специальные цены на асфальт для дорожных работ',
                '📋 Рекомендации по укладке и использованию'
            ],
            buttonText: 'Подписаться на обновления'
        },

        // доставка
        delivery: {
            title: 'Оперативная информация о доставке',
            text: 'В нашем Telegram канале мы публикуем актуальные данные по доставке и логистике.',
            benefits: [
                '🚛 Текущая загруженность автопарка',
                '🗺️ Информация о зонах доставки',
                '⏱️ Возможные сроки поставки материалов'
            ],
            buttonText: 'Следить за новостями доставки'
        },

        // калькулятор
        calculator: {
            title: 'Расчет бетона стал еще проще!',
            text: 'В нашем Telegram канале регулярно публикуем полезные ссылки для строителей.',
            benefits: [
                '📱 Мобильные приложения для строителей',
                '📋 Чек-листы для проверки качества материалов'
            ],
            buttonText: 'Получить полезные инструменты'
        },

        // контакты
        contacts: {
            title: 'Всегда на связи в Telegram',
            text: 'Подписывайтесь на наш канал для быстрой связи и получения оперативных ответов на ваши вопросы.',
            benefits: [
                '👨‍💼 Прямой контакт с менеджерами',
                '⏩ Ускоренная обработка заявок для подписчиков',
                '📢 Анонсы изменений в графике работы'
            ],
            buttonText: 'Быть на связи'
        },

        // главная
        default: {
            title: 'Подписывайтесь на наш Telegram канал',
            text: 'Будьте в курсе последних новостей, акций и специальных предложений!',
            benefits: [
                '🔔 Эксклюзивные акции и скидки',
                '📦 Информация о новых поступлениях',
                '💼 Профессиональные советы по строительству'
            ],
            buttonText: 'Подписаться на канал'
        }
    };

    // Определяем тип страницы на основе URL
    let pageType = 'default';

    // Анализируем URL более детально
    const pathSegments = currentPath.split('/').filter(segment => segment.length > 0);

    // Проверяем, это страница каталога или товара
    if (pathSegments.includes('catalog')) {
        // Находим индекс 'catalog' в пути
        const catalogIndex = pathSegments.indexOf('catalog');

        // Если есть сегменты после каталога и города
        if (pathSegments.length > catalogIndex + 2) {
            // Получаем категорию из URL (после города)
            const category = pathSegments[catalogIndex + 2];

            // Определяем тип страницы по категории
            if (category === 'beton') {
                pageType = 'beton';
            } else if (category === 'nerudnye') {
                pageType = 'nerudnye';
            } else if (category === 'sheben' || category.includes('sheben')) {
                pageType = 'sheben';
            } else if (category === 'pesok' || category.includes('pesok')) {
                pageType = 'pesok';
            } else if (category === 'asfalt' || category.includes('asfalt')) {
                pageType = 'asfalt';
            }
        }
    } else {
        // Обработка других страниц как раньше
        if (currentPath.includes('/beton') || currentPath.includes('/category/beton')) {
            pageType = 'beton';
        } else if (currentPath.includes('/nerudnye') || currentPath.includes('/category/nerudnye')) {
            pageType = 'nerudnye';
        } else if (currentPath.includes('/sheben') || currentPath.includes('/category/sheben')) {
            pageType = 'sheben';
        } else if (currentPath.includes('/pesok') || currentPath.includes('/category/pesok')) {
            pageType = 'pesok';
        } else if (currentPath.includes('/asfalt') || currentPath.includes('/category/asfalt')) {
            pageType = 'asfalt';
        } else if (currentPath.includes('/delivery')) {
            pageType = 'delivery';
        } else if (currentPath.includes('/concrete_calculator') || currentPath.includes('/calc')) {
            pageType = 'calculator';
        } else if (currentPath.includes('/contacts')) {
            pageType = 'contacts';
        }
    }

    // Применяем выбранный вариант контента
    const selectedContent = contentVariants[pageType];

    if (popupTitle) {
        popupTitle.textContent = selectedContent.title;
    }

    if (popupText) {
        popupText.textContent = selectedContent.text;
    }

    if (popupButton) {
        popupButton.textContent = selectedContent.buttonText;
    }

    // Если есть список преимуществ, обновляем его
    if (benefitsList) {
        benefitsList.innerHTML = '';
        selectedContent.benefits.forEach(benefit => {
            const li = document.createElement('li');
            li.textContent = benefit;
            benefitsList.appendChild(li);
        });
    } else if (selectedContent.benefits && selectedContent.benefits.length > 0) {
        // Если списка еще нет, но есть преимущества, создаем список
        const newList = document.createElement('ul');
        newList.className = 'telegram-benefits';

        selectedContent.benefits.forEach(benefit => {
            const li = document.createElement('li');
            li.textContent = benefit;
            newList.appendChild(li);
        });

        // Вставляем список после параграфа
        if (popupText && popupText.parentNode) {
            popupText.parentNode.insertBefore(newList, popupText.nextSibling);
        }
    }

    // Добавляем настройку отслеживания для аналитики
    if (popupButton) {
        popupButton.setAttribute('data-page-type', pageType);
    }
}

// Функция для показа попапа
function showTelegramPopup() {
    const telegramPopup = document.getElementById('telegram-popup');
    if (telegramPopup) {
        // Сначала устанавливаем таргетированный контент
        targetPopupContent();

        // Затем показываем попап, добавляя класс active для flex-центрирования
        telegramPopup.classList.add('active');

        // Устанавливаем флаг, что попап был показан
        localStorage.setItem('telegramPopupShown', 'true');

        // Отправляем событие в Яндекс.Метрику, если она доступна
        if (typeof ym !== 'undefined') {
            ym(98660706, 'reachGoal', 'tg_popup_shown');
        }
    }
}

// Функция для закрытия попапа
function closeTelegramPopup() {
    const telegramPopup = document.getElementById('telegram-popup');
    if (telegramPopup) {
        // Удаляем класс active вместо установки display: none
        telegramPopup.classList.remove('active');
    }
}

// Функция для отслеживания кликов по кнопке (для аналитики)
function trackTelegramClick() {
    // Проверяем, определена ли переменная ym (Яндекс.Метрика)
    if (typeof ym !== 'undefined') {
        ym(98660706, 'reachGoal', 'tg_popup_button');
    }

    // Закрываем попап в любом случае
    closeTelegramPopup();

    return true;
}
