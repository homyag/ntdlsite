document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('feedback-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const url = form.getAttribute('data-url');

            // Отключаем кнопку отправки
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;

            // Проверка reCAPTCHA
            grecaptcha.ready(function() {
                grecaptcha.execute('6LchN2EqAAAAAFEYLgQZmZLrF_czptpdExkUsusM', {action: 'submit'}).then(function(token) {
                    // Добавляем токен reCAPTCHA в данные формы
                    const formData = new FormData(form);
                    formData.append('g-recaptcha-response', token);

                    // Получаем CSRF-токен
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                    // Отправляем данные на сервер
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
                        submitButton.disabled = false;

                        if (data.status === 'success') {
                            // Очищаем форму и показываем модальное окно
                            form.reset();
                            const modal = document.getElementById('success-feedback-form-modal');
                            modal.style.display = 'block';

                            // Закрытие модального окна по клику на кнопку "X"
                            document.querySelector('.close-btn').addEventListener('click', function() {
                                modal.style.display = 'none';
                            });

                            // Закрытие модального окна при клике вне контента
                            window.onclick = function(event) {
                                if (event.target === modal) {
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
                        submitButton.disabled = false;
                    });
                });
            });
        });
    } else {
        console.error("Форма с id='feedback-form' не найдена на странице.");
    }
});