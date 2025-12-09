// Переключатель темы (простой, меняет фон боди)
function toggleTheme() {
    const body = document.body;
    body.style.backgroundColor = body.style.backgroundColor === 'rgb(30, 30, 30)' ? '#0c73fe' : '#1e1e1e';
    // Для полноценной темной темы нужно больше CSS, но для MVP оставим переключение фона
}

// Функция смены городов местами
function swapCities() {
    const fromSelect = document.querySelector('select[name="from_city"]');
    const toSelect = document.querySelector('select[name="to_city"]');

    const temp = fromSelect.value;
    fromSelect.value = toSelect.value;
    toSelect.value = temp;
}