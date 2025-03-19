document.addEventListener('DOMContentLoaded', function () {
    const structureTypeSelect = document.getElementById('structure-type');
    const descriptionContent = document.getElementById('description-content');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // Проверяем, есть ли доступные продукты
    const hasProducts = window.availableConcreteProducts && window.availableConcreteProducts.length > 0;

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
        'slab': ['М150', 'М200', 'М250', 'М300', 'М350', 'М400'],
        'column': ['М200', 'М250', 'М300', 'М350', 'М400'],
        'foundation': [], // Для ленточного фундамента все типы бетона
        // Добавьте другие рекомендации для других типов конструкций
    };

    // Функция для проверки подходит ли бетон для типа конструкции
    function isConcreteGradeValid(productName, structureType) {
        // Для ленточного фундамента подходят все типы бетона
        if (structureType === 'foundation') {
            return true;
        }

        // Извлекаем марку бетона из названия продукта
        const gradeMatch = productName.match(/М(\d+)/);
        if (!gradeMatch) {
            return false; // Не удалось определить марку
        }

        const gradeNumber = parseInt(gradeMatch[1], 10);

        // Проверка по типу конструкции
        if (structureType === 'slab' && gradeNumber >= 150) {
            return true;
        } else if (structureType === 'column' && gradeNumber >= 200) {
            return true;
        }

        return false;
    }

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

                // Если нет доступных продуктов вообще (ни одного)
                if (!hasProducts) {
                    // Изменяем заголовок контейнера рекомендаций
                    const recommendationsTitle = recommendationsContainer.querySelector('h3');
                    if (recommendationsTitle) {
                        recommendationsTitle.textContent = 'Нет подходящих типов бетона';
                    }

                    // Изменяем параграф под заголовком
                    const recommendationsIntro = recommendationsContainer.querySelector('p');
                    if (recommendationsIntro) {
                        recommendationsIntro.textContent = 'К сожалению в Вашем регионе нет выбранного типа бетона.';
                    }

                    // Добавляем сообщение с телефоном
                    recommendationsList.innerHTML = '<li>Оставьте заявку менеджеру по телефону <strong>+7 (949) 624-2644</strong></li>';
                    return;
                }

                // Получаем рекомендуемые типы для выбранной конструкции
                const recommendedTypes = recommendedConcreteTypes[selectedType] || [];

                // Фильтруем доступные продукты по требованиям к марке бетона
                const filteredProducts = window.availableConcreteProducts.filter(product =>
                    isConcreteGradeValid(product.name, selectedType)
                );

                // Отображаем доступные продукты, выделяя рекомендуемые
                let foundProducts = false;

                // Сначала отображаем рекомендуемые типы бетона
                if (recommendedTypes.length > 0) {
                    for (const product of filteredProducts) {
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

                // Затем отображаем остальные доступные типы бетона, подходящие по марке
                for (const product of filteredProducts) {
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

                // Если не найдено ни одного подходящего продукта
                if (!foundProducts) {
                    // Изменяем заголовок контейнера рекомендаций
                    const recommendationsTitle = recommendationsContainer.querySelector('h3');
                    if (recommendationsTitle) {
                        recommendationsTitle.textContent = 'Нет подходящих типов бетона';
                    }

                    // Изменяем параграф под заголовком
                    const recommendationsIntro = recommendationsContainer.querySelector('p');
                    if (recommendationsIntro) {
                        recommendationsIntro.textContent = 'К сожалению в' +
                            ' Вашем регионе нет подходящих под конструкцию' +
                            ' типов бетона.';
                    }

                    // Добавляем сообщение с телефоном
                    recommendationsList.innerHTML = '<li>Оставьте заявку менеджеру по телефону <strong><a href="tel:+79496242644">+7 (949) 624-2644</a></strong></li>';
                }
            }
        }
    });
});