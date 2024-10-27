ymaps.ready(init);

function init() {
    // Стоимость за км за м³ бетона (руб)
    const RATE_PER_KM_PER_M3 = 600; // Замените на вашу актуальную стоимость

    // Базовая точка доставки (замените на ваши координаты)
    const BASE_POINT = [60.906882, 30.067233];

    // Инициализация карты
    const myMap = new ymaps.Map('map', {
        center: BASE_POINT,
        zoom: 9,
        controls: []
    });

    // Создаем панель маршрутизации
    const routePanelControl = new ymaps.control.RoutePanel({
        options: {
            showHeader: true,
            title: 'Расчёт доставки'
        }
    });

    // Добавляем элементы управления на карту
    myMap.controls.add(routePanelControl).add(new ymaps.control.ZoomControl({
        options: {
            size: 'small',
            float: 'none',
            position: {
                bottom: 145,
                right: 10
            }
        }
    }));

    // Ограничиваем типы маршрутов только автомобилем
    routePanelControl.routePanel.options.set({
        types: { auto: true }
    });

    // Задаем неизменяемую точку "откуда"
    routePanelControl.routePanel.state.set({
        fromEnabled: false,
        from: 'Мариуполь, улица Сортировочная 1' // Замените на ваш адрес отправки
    });

    // Получаем ссылку на маршрут
    routePanelControl.routePanel.getRouteAsync().then(function (route) {
        // Задаем максимально допустимое число маршрутов
        route.model.setParams({ results: 1 }, true);

        // Обработка события успешного построения маршрута
        route.model.events.add('requestsuccess', function () {
            const activeRoute = route.getActiveRoute();
            if (activeRoute) {
                const length = activeRoute.properties.get("distance");
                const distanceKm = length.value / 1000; // Расстояние в километрах (с дробной частью)

                // Получение объема бетона из формы
                const volumeInput = document.getElementById('volume');
                const volume = parseFloat(volumeInput.value);

                if (isNaN(volume) || volume <= 0) {
                    alert("Пожалуйста, введите корректный объем бетона.");
                    return;
                }

                // Вычисление общей стоимости доставки
                const totalCost = distanceKm * volume * RATE_PER_KM_PER_M3;

                // Создание макета содержимого балуна маршрута
                const balloonContentLayout = ymaps.templateLayoutFactory.createClass(
                    `<span>Расстояние: ${length.text}.</span><br/>` +
                    `<span>Объем заказа: ${volume} м³.</span><br/>` +
                    `<span>Стоимость за 1 км за 1 м³: ${RATE_PER_KM_PER_M3} руб.</span><br/>` +
                    `<span style="font-weight: bold; font-style: italic">Общая стоимость доставки: ${totalCost.toFixed(2)} руб.</span>`
                );

                // Установка макета для содержимого балуна
                activeRoute.options.set('routeBalloonContentLayout', balloonContentLayout);

                // Открытие балуна маршрута
                activeRoute.balloon.open();

                // Отображение стоимости доставки на странице
                document.getElementById('delivery-cost').innerHTML =
                    `Предварительная стоимость доставки составляет: <strong>${totalCost.toFixed(2)} руб.</strong>`;
            }
        });
    });

    // Обработка отправки формы для пересчета стоимости при изменении объема
    const form = document.getElementById('delivery-form');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        // Перестроение маршрута для обновления стоимости
        const routeControl = myMap.controls.get('routePanelControl');
        if (routeControl) {
            // Получаем текущее место назначения из маршрутизации
            const toState = routeControl.routePanel.state.get('to');
            if (toState) {
                routeControl.routePanel.state.set('to', toState);
            } else {
                alert("Пожалуйста, введите адрес доставки на карте.");
            }
        }
    });
}