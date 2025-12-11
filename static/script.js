// Переключение темы (только иконка)
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        icon.classList.toggle('fa-sun', isDark);
        icon.classList.toggle('fa-moon', !isDark);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark');
    }

    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        if (document.body.classList.contains('dark')) {
            icon.classList.add('fa-sun');
        } else {
            icon.classList.add('fa-moon');
        }
    }
});

// Обмен городов местами
function swapCities() {
    const fromSelect = document.getElementById('from_city');
    const toSelect = document.getElementById('to_city');
    if (fromSelect && toSelect) {
        const temp = fromSelect.value;
        fromSelect.value = toSelect.value;
        toSelect.value = temp;

        const event = new Event('change');
        fromSelect.dispatchEvent(event);
        toSelect.dispatchEvent(event);
    }
}

// Диалог перед переходом на сайт ТК
function confirmBooking(company, url) {
    const confirmed = confirm(
        `Вы будете перенаправлены на сайт ${company} для оформления заказа.\n\n` +
        `Возможно, там потребуется повторно ввести параметры доставки (город, вес и т.д.).\n\n` +
        `Нажмите ОК для перехода.`
    );
    if (confirmed) {
        window.open(url, '_blank');
    }
    return false;
}
