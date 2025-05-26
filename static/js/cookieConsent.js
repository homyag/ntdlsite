document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, дал ли пользователь согласие ранее
    const cookieConsent = localStorage.getItem('cookieConsent');
    const cookieConsentPopup = document.getElementById('cookie-consent');

    // Если согласие не дано, показываем попап через 2 секунды
    if (!cookieConsent && cookieConsentPopup) {
        setTimeout(function() {
            cookieConsentPopup.classList.add('show');
            // Блокируем скролл страницы
            document.body.style.overflow = 'hidden';
        }, 2000);
    }

    // Обработчик принятия cookies
    const acceptBtn = document.getElementById('cookie-consent-accept');
    if (acceptBtn) {
        acceptBtn.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'accepted');
            hideCookieConsent();

            // Отправляем событие в Яндекс.Метрику, если она доступна
            if (typeof ym !== 'undefined') {
                ym(98660706, 'reachGoal', 'cookie_accepted');
            }
        });
    }

    // Обработчик отклонения cookies
    const declineBtn = document.getElementById('cookie-consent-decline');
    if (declineBtn) {
        declineBtn.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'declined');
            hideCookieConsent();

            // Отправляем событие в Яндекс.Метрику, если она доступна
            if (typeof ym !== 'undefined') {
                ym(98660706, 'reachGoal', 'cookie_declined');
            }

            // Отключаем аналитику если пользователь отказался
            disableAnalytics();
        });
    }

    // УБИРАЕМ обработчик закрытия попапа по крестику
    // Теперь попап можно закрыть только через кнопки "Принять" или "Отклонить"

    // Блокируем закрытие по клику вне попапа
    if (cookieConsentPopup) {
        cookieConsentPopup.addEventListener('click', function(e) {
            // Если клик был по самому попапу (не по содержимому), ничего не делаем
            e.stopPropagation();
        });
    }

    // Блокируем закрытие по Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && cookieConsentPopup && cookieConsentPopup.classList.contains('show')) {
            // Не закрываем попап по Escape
            e.preventDefault();
            return false;
        }
    });

    // Функция скрытия попапа
    function hideCookieConsent() {
        if (cookieConsentPopup) {
            cookieConsentPopup.classList.remove('show');
            setTimeout(function() {
                cookieConsentPopup.style.display = 'none';
                // Восстанавливаем скролл страницы
                document.body.style.overflow = '';
            }, 500);
        }
    }

    // Функция отключения аналитики
    function disableAnalytics() {
        // Устанавливаем флаг отключения аналитики
        localStorage.setItem('analyticsDisabled', 'true');

        // Здесь можно добавить код отключения других аналитических систем
        console.log('Analytics disabled by user choice');
    }

    // Проверяем статус аналитики при загрузке страницы
    function checkAnalyticsStatus() {
        const analyticsDisabled = localStorage.getItem('analyticsDisabled');
        const cookieConsent = localStorage.getItem('cookieConsent');

        if (cookieConsent === 'declined' || analyticsDisabled === 'true') {
            // Аналитика отключена
            console.log('Analytics is disabled');
        } else if (cookieConsent === 'accepted') {
            // Аналитика разрешена
            console.log('Analytics is enabled');
        }
    }

    // Проверяем статус при загрузке
    checkAnalyticsStatus();
});