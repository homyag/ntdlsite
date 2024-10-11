document.getElementById('callback-form').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);
    let url = this.getAttribute('data-url');  // Получаем URL из атрибута data-url

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Закрываем попап формы
            let formPopup = document.getElementById('callback-popup');
            formPopup.style.display = 'none';

            // Очищаем поля формы
            document.getElementById('callback-form').reset();

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
            alert('Ошибка: ' + JSON.stringify(data.errors));
        }
    })
    .catch(error => console.error('Ошибка:', error));
});