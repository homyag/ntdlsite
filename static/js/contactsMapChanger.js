document.addEventListener('DOMContentLoaded', function() {
    const defaultMapUrl = "https://yandex.ru/map-widget/v1/?um=constructor%3A1f6ab6d20d724b84b9429d0528d2aa6e8c20abec0fd4be523dbcd16d4ce88297&amp;source=constructor";
    const mapFrame = document.getElementById('map-frame');

    if (!mapFrame) {
        console.error("Map frame not found!");
        return;
    }

    let currentMapUrl = defaultMapUrl;

    // Функция для изменения карты
    function changeMap(url) {
        console.log("Changing map to:", url); // Логирование изменения карты
        mapFrame.src = url;
    }

    // Обработчики событий для каждой карточки
    document.querySelectorAll('.location-card').forEach(card => {
        const mapUrl = card.getAttribute('data-map-url');
        console.log("Card URL:", mapUrl); // Логирование URL каждой карточки

        card.addEventListener('mouseover', function() {
            if (currentMapUrl !== mapUrl) {
                currentMapUrl = mapUrl;
                changeMap(mapUrl);
            }
        });

        card.addEventListener('touchstart', function() {
            if (currentMapUrl !== mapUrl) {
                currentMapUrl = mapUrl;
                changeMap(mapUrl);
            }
        });
    });
});
