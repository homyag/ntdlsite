document.addEventListener('DOMContentLoaded', function () {
    const structureTypeSelect = document.getElementById('structure-type');
    const structureInputs = document.querySelectorAll('.structure-input');
    const concreteForm = document.getElementById('concrete-form');
    const calculationResult = document.getElementById('calculation-result');

    // Функция для отображения соответствующих полей ввода
    structureTypeSelect.addEventListener('change', function () {
        const selectedType = this.value;
        structureInputs.forEach(function (inputGroup) {
            if (inputGroup.id === `${selectedType}-inputs`) {
                inputGroup.style.display = 'block';
            } else {
                inputGroup.style.display = 'none';
            }
        });
        // Скрыть результат при смене типа конструкции
        calculationResult.style.display = 'none';
    });

    // Обработка отправки формы
    concreteForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const selectedType = structureTypeSelect.value;
        let volume = 0;

        switch (selectedType) {
            case 'slab':
                const slabLength = parseFloat(document.getElementById('slab-length').value);
                const slabWidth = parseFloat(document.getElementById('slab-width').value);
                const slabThickness = parseFloat(document.getElementById('slab-thickness').value);
                if (isValidInputs([slabLength, slabWidth, slabThickness])) {
                    volume = slabLength * slabWidth * slabThickness;
                }
                break;
            case 'column':
                const columnHeight = parseFloat(document.getElementById('column-height').value);
                const columnDiameter = parseFloat(document.getElementById('column-diameter').value);
                if (isValidInputs([columnHeight, columnDiameter])) {
                    const radius = columnDiameter / 2;
                    volume = Math.PI * Math.pow(radius, 2) * columnHeight;
                }
                break;
            case 'foundation':
                const foundationLength = parseFloat(document.getElementById('foundation-length').value);
                const foundationWidth = parseFloat(document.getElementById('foundation-width').value);
                const foundationDepth = parseFloat(document.getElementById('foundation-depth').value);
                if (isValidInputs([foundationLength, foundationWidth, foundationDepth])) {
                    volume = foundationLength * foundationWidth * foundationDepth;
                }
                break;
            // Добавьте другие типы конструкций здесь
            default:
                alert('Пожалуйста, выберите тип конструкции.');
                return;
        }

        if (volume > 0) {
            calculationResult.innerHTML = `Необходимый объем бетона: <strong>${volume.toFixed(2)} м³</strong>`;
            calculationResult.style.display = 'block';
        } else {
            calculationResult.innerHTML = '';
            calculationResult.style.display = 'none';
        }
    });

    // Функция для проверки корректности ввода
    function isValidInputs(inputs) {
        for (let input of inputs) {
            if (isNaN(input) || input <= 0) {
                alert('Пожалуйста, введите корректные положительные значения для всех полей.');
                return false;
            }
        }
        return true;
    }
});