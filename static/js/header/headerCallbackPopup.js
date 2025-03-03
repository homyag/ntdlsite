document.getElementById('callback-form').addEventListener('submit', function(e) {
    e.preventDefault();

    let form = this;
    let url = this.getAttribute('data-url');  // Получаем URL из атрибута data-url

    // Отключаем кнопку отправки, чтобы предотвратить повторные нажатия
    let submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    grecaptcha.ready(function() {
        grecaptcha.execute('6LchN2EqAAAAAFEYLgQZmZLrF_czptpdExkUsusM', {action: 'submit'}).then(function(token) {
            // Добавляем токен reCAPTCHA в данные формы
            let formData = new FormData(form);
            formData.append('g-recaptcha-response', token);

            // Получаем CSRF-токен из формы
            let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                },
            })
            .then(response => response.json())
            .then(data => {
                submitButton.disabled = false;  // Включаем кнопку отправки

                if (data.status === 'success') {
                    // Закрываем попап формы
                    let formPopup = document.getElementById('callback-popup');
                    formPopup.style.display = 'none';

                    // Очищаем поля формы
                    form.reset();

                    // Показать модальное окно
                    let modal = document.getElementById('success-modal');
                    modal.style.display = 'block';

                    // Закрытие модального окна по клику на кнопку "X"
                    document.querySelector('.close-btn').addEventListener('click', function() {
                        modal.style.display = 'none';
                    });

                    // Закрытие модального окна при клике вне контента
                    window.onclick = function(event) {
                        if (event.target == modal) {
                            modal.style.display = 'none';
                        }
                    };
                } else if (data.status === 'error') {
                    if (data.errors.recaptcha) {
                        alert('Ошибка reCAPTCHA: ' + data.errors.recaptcha);
                    } else {
                        alert('Ошибка: ' + JSON.stringify(data.errors));
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                submitButton.disabled = false;  // Включаем кнопку отправки в случае ошибки
            });
        });
    });
});