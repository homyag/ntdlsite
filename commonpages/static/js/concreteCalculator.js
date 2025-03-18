document.addEventListener('DOMContentLoaded', function () {
    const structureTypeSelect = document.getElementById('structure-type');
    const descriptionContent = document.getElementById('description-content');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // Проверяем, есть ли доступные продукты
    const hasProducts = window.availableConcreteProducts && window.availableConcreteProducts.length > 0;

    // Отладочная информация
    console.log(`Доступно ${hasProducts ? window.availableConcreteProducts.length : 0} продуктов с бетоном`);
    if (hasProducts && window.availableConcreteProducts.length > 0) {
        console.log("Доступные продукты:", window.availableConcreteProducts);
    }

    // Объект с описаниями для каждого типа конструкции
    const descriptions = {
        'slab': `
            <p><strong>Фундаментная плита</strong> — это монолитная плита, служащая основой для зданий и сооружений. Она применяется для распределения нагрузки от конструкции на грунт, особенно в случаях слабых или неоднородных грунтов. Калькулятор поможет вам рассчитать необходимый объем бетона для вашей плиты с учетом длины, ширины и толщины.</p>
        `,
        'column': `
            <p><strong>Колонна</strong> — вертикальный несущий элемент конструкции, передающий нагрузку от здания на фундамент. Колонны используются в различных типах зданий для обеспечения прочности и устойчивости. Наш калькулятор поможет вам определить объем бетона, необходимый для изготовления колонны, учитывая высоту и периметр.</p>
        `,
        'foundation': `
            <p><strong>Ленточный фундамент</strong> — тип фундамента, представляющий собой непрерывную ленточную основу под несущие стены здания. Он обеспечивает равномерное распределение нагрузки и подходит для большинства типов грунтов. Используя наш калькулятор, вы сможете точно рассчитать объем бетона для вашего ленточного фундамента, учитывая периметр, ширину и глубину.</p>
        `,
        // Добавьте другие описания конструкций здесь
    };

    // Словарь с рекомендуемыми марками бетона для разных типов конструкций
    const recommendedConcreteTypes = {
        'slab': ['М200', 'М250', 'М300'],
        'column': ['М300', 'М350', 'М400'],
        'foundation': ['М200', 'М250', 'М300'],
        // Добавьте другие рекомендации для других типов конструкций
    };

    // Функция для отображения соответствующих полей формы
    function toggleStructureInputs(selectedType) {
        // Скрываем все группы ввода
        document.querySelectorAll('.structure-input').forEach(function (group) {
            group.style.display = 'none';
        });

        if (selectedType && descriptions[selectedType]) {
            // Отображаем нужную группу ввода
            const inputs = document.getElementById(`${selectedType}-inputs`);
            if (inputs) {
                inputs.style.display = 'block';
            }

            // Обновляем описание
            descriptionContent.innerHTML = descriptions[selectedType];
        } else {
            // Если ничего не выбрано, показываем стандартное описание
            descriptionContent.innerHTML = '<p>Пожалуйста, выберите тип конструкции, чтобы увидеть описание.</p>';
        }

        // Скрываем рекомендации при смене типа конструкции
        if (recommendationsContainer) {
            recommendationsContainer.style.display = 'none';
        }
    }

    // Инициализация при загрузке страницы
    toggleStructureInputs(structureTypeSelect.value);

    // Обработчик изменения выбора конструкции
    structureTypeSelect.addEventListener('change', function () {
        toggleStructureInputs(this.value);
    });

    // Обработчик отправки формы
    const concreteForm = document.getElementById('concrete-form');
    const calculationResult = document.getElementById('calculation-result');

    concreteForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const selectedType = structureTypeSelect.value;

        // Получение значений полей в зависимости от типа конструкции
        let volume = 0;
        if (selectedType === 'slab') {
            const length = parseFloat(document.getElementById('slab-length').value);
            const width = parseFloat(document.getElementById('slab-width').value);
            const thickness = parseFloat(document.getElementById('slab-thickness').value);
            volume = length * width * thickness;
        } else if (selectedType === 'column') {
            const height = parseFloat(document.getElementById('column-height').value);
            const perimeter = parseFloat(document.getElementById('column-diameter').value);
            // Предположим, что толщина колонны постоянна, например, 0.3 м
            const thickness = 0.3;
            volume = perimeter * thickness * height;
        } else if (selectedType === 'foundation') {
            const perimeter = parseFloat(document.getElementById('foundation-length').value);
            const width = parseFloat(document.getElementById('foundation-width').value);
            const depth = parseFloat(document.getElementById('foundation-depth').value);
            volume = perimeter * width * depth;
        }
        // Добавьте расчеты для других типов конструкций

        if (isNaN(volume) || volume <= 0) {
            calculationResult.style.display = 'block';
            calculationResult.style.borderColor = '#dc3545';
            calculationResult.style.backgroundColor = '#f8d7da';
            calculationResult.style.color = '#721c24';
            calculationResult.textContent = 'Пожалуйста, заполните все поля корректно.';

            // Скрываем блок рекомендаций при ошибке
            if (recommendationsContainer) {
                recommendationsContainer.style.display = 'none';
            }
            return;
        }

        // Округляем до двух знаков после запятой
        volume = Math.round(volume * 100) / 100;

        // Отображаем результат
        calculationResult.style.display = 'block';
        calculationResult.style.borderColor = '#28a745';
        calculationResult.style.backgroundColor = '#d4edda';
        calculationResult.style.color = '#155724';
        calculationResult.textContent = `Необходимый объем бетона: ${volume} куб. м.`;

        // Показываем рекомендации
        if (recommendationsContainer) {
            recommendationsContainer.style.display = 'block';

            // Получаем контейнер для списка рекомендаций
            const recommendationsList = document.getElementById('recommendations-list');

            // Очищаем предыдущие рекомендации
            if (recommendationsList) {
                recommendationsList.innerHTML = '';

                // Если нет доступных продуктов, предлагаем выбрать город
                if (!hasProducts) {
                    recommendationsList.innerHTML = '<li>Для просмотра рекомендаций необходимо <a href="#" id="open-city-modal">выбрать город</a></li>';

                    // Добавляем обработчик для открытия модального окна выбора города
                    const openCityBtn = document.getElementById('open-city-modal');
                    if (openCityBtn) {
                        openCityBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            if (typeof openCityModal === 'function') {
                                openCityModal();
                            }
                        });
                    }
                    return;
                }

                // Получаем рекомендуемые типы для выбранной конструкции
                const recommendedTypes = recommendedConcreteTypes[selectedType] || [];

                // Отображаем доступные продукты, выделяя рекомендуемые
                let foundProducts = false;

                // Сначала отображаем рекомендуемые типы бетона
                if (recommendedTypes.length > 0) {
                    for (const product of window.availableConcreteProducts) {
                        // Проверяем, соответствует ли продукт одному из рекомендуемых типов
                        const isRecommended = recommendedTypes.some(type =>
                            product.name.includes(type)
                        );

                        if (isRecommended) {
                            foundProducts = true;
                            const listItem = document.createElement('li');
                            listItem.className = 'recommended-product';

                            // Рассчитываем общую стоимость (цена за единицу * объем)
                            const totalPrice = (product.price * volume).toFixed(2);

                            const link = document.createElement('a');
                            link.href = product.url;
                            link.textContent = product.name;

                            // Добавляем информацию о цене
                            const priceInfo = document.createElement('span');
                            priceInfo.className = 'price-info';
                            priceInfo.innerHTML = `<br>Цена: ${product.price} руб/м³<br>Стоимость для объема ${volume} м³: <strong>${totalPrice} руб</strong>`;

                            // Добавляем отметку "Рекомендуется"
                            const recommendedBadge = document.createElement('span');
                            recommendedBadge.className = 'recommended-badge';
                            recommendedBadge.textContent = 'Рекомендуется';

                            listItem.appendChild(recommendedBadge);
                            listItem.appendChild(link);
                            listItem.appendChild(priceInfo);
                            recommendationsList.appendChild(listItem);
                        }
                    }
                }

                // Затем отображаем остальные доступные типы бетона
                for (const product of window.availableConcreteProducts) {
                    // Проверяем, соответствует ли продукт одному из рекомендуемых типов
                    const isRecommended = recommendedTypes.some(type =>
                        product.name.includes(type)
                    );

                    // Отображаем только те, которые не были отображены как рекомендуемые
                    if (!isRecommended) {
                        foundProducts = true;
                        const listItem = document.createElement('li');

                        // Рассчитываем общую стоимость (цена за единицу * объем)
                        const totalPrice = (product.price * volume).toFixed(2);

                        const link = document.createElement('a');
                        link.href = product.url;
                        link.textContent = product.name;

                        // Добавляем информацию о цене
                        const priceInfo = document.createElement('span');
                        priceInfo.className = 'price-info';
                        priceInfo.innerHTML = `<br>Цена: ${product.price} руб/м³<br>Стоимость для объема ${volume} м³: <strong>${totalPrice} руб</strong>`;

                        listItem.appendChild(link);
                        listItem.appendChild(priceInfo);
                        recommendationsList.appendChild(listItem);
                    }
                }

                // Если не найдено ни одного продукта
                if (!foundProducts) {
                    recommendationsList.innerHTML = '<li>В выбранном городе нет подходящих типов бетона для данной конструкции. <a href="#" id="open-city-modal">Выбрать другой город</a></li>';

                    // Добавляем обработчик для открытия модального окна выбора города
                    const openCityBtn = document.getElementById('open-city-modal');
                    if (openCityBtn) {
                        openCityBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            if (typeof openCityModal === 'function') {
                                openCityModal();
                            }
                        });
                    }
                }
            }
        }
    });
});