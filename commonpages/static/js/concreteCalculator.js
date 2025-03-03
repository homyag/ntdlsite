document.addEventListener('DOMContentLoaded', function () {
    const structureTypeSelect = document.getElementById('structure-type');
    const descriptionContent = document.getElementById('description-content');

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
    });
});