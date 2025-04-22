// Карточки услуг
const serviceCards = document.querySelectorAll('.service-card');
serviceCards.forEach(card => {
  // Обработчик наведения
  card.addEventListener('mouseenter', function() {
    // Плавно увеличиваем номер услуги
    const serviceNumber = card.querySelector('.service-number');
    if (serviceNumber) {
      serviceNumber.style.transform = 'scale(1.2)';
      serviceNumber.style.color = 'rgba(54, 152, 212, 0.4)';
    }
  });

  // Обработчик ухода мыши
  card.addEventListener('mouseleave', function() {
    // Возвращаем номер в исходное состояние
    const serviceNumber = card.querySelector('.service-number');
    if (serviceNumber) {
      serviceNumber.style.transform = '';
      serviceNumber.style.color = '';
    }
  });
});