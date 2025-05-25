// static/js/cookieConsent.js - Production Version
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, дал ли пользователь согласие ранее
    const cookieConsent = localStorage.getItem('cookieConsent');
    const cookieConsentPopup = document.getElementById('cookie-consent');

    // Если согласие не дано, показываем попап через 2 секунды
    if (!cookieConsent && cookieConsentPopup) {
        setTimeout(function() {
            cookieConsentPopup.classList.add('show');
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
        });
    }

    // Обработчик закрытия попапа
    const closeBtn = document.getElementById('cookie-consent-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            hideCookieConsent();
        });
    }

    // Функция скрытия попапа
    function hideCookieConsent() {
        if (cookieConsentPopup) {
            cookieConsentPopup.classList.remove('show');
            setTimeout(function() {
                cookieConsentPopup.style.display = 'none';
            }, 500);
        }
    }
});