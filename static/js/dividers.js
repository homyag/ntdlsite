// JavaScript для интеграции простого разделителя и анимаций

document.addEventListener('DOMContentLoaded', function() {
  // Находим все секции на странице
  const sections = document.querySelectorAll('.hero-section, .services-section, .about-section, .products-section, .advantages-section, .cta-section');

  // Проверяем, есть ли секции на странице
  if (sections.length === 0) {
    return; // Прекращаем выполнение, если секции отсутствуют
  }

  // HTML для простого разделителя
  const dividerHTML = `
  <div class="simple-divider">
    <div class="divider-line"></div>
    <div class="divider-accent">
      <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30">
        <polygon points="15,0 30,15 15,30 0,15" fill="#3698D4" opacity="0.7" />
      </svg>
    </div>
  </div>`;

  // Вставляем разделитель между секциями
  for (let i = 0; i < sections.length - 1; i++) {
    const divider = document.createElement('div');
    divider.innerHTML = dividerHTML;
    sections[i].parentNode.insertBefore(divider.firstElementChild, sections[i].nextSibling);
  }

  // Добавление индикатора скролла
  const scrollIndicator = document.createElement('div');
  scrollIndicator.className = 'scroll-indicator';
  document.body.appendChild(scrollIndicator);

  // Обновление индикатора скролла при прокрутке
  window.addEventListener('scroll', function() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    scrollIndicator.style.width = scrolled + "%";

    // Анимация элементов при прокрутке
    animateOnScroll();
  });

  // Функция для анимации элементов при прокрутке
  function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    if (elements.length === 0) {
      return; // Если нет элементов с этим классом, выходим
    }

    elements.forEach(element => {
      const position = element.getBoundingClientRect();

      if (position.top < window.innerHeight * 0.85) {
        element.classList.add('visible');
      }
    });
  }

  // Добавление класса для анимации элементов
  document.querySelectorAll('.services-section, .about-section, .products-section, .advantages-section, .cta-section, .service-card, .advantage-card').forEach(element => {
    if (element) {
      element.classList.add('animate-on-scroll');
    }
  });

  // Эффект пульсации для кнопок CTA
  const ctaButtons = document.querySelectorAll('.hero__button--popup');
  if (ctaButtons.length > 0) {
    ctaButtons.forEach(button => {
      setInterval(() => {
        button.classList.add('pulse');
        setTimeout(() => {
          button.classList.remove('pulse');
        }, 1000);
      }, 5000);
    });
  }
});