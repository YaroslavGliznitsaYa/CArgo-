// --- Theme Toggle Logic ---
function toggleTheme() {
    const body = document.body;
    // Переключает класс 'dark'
    const isDark = body.classList.toggle('dark');

    // Сохранение предпочтений
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Обновление иконки
    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        // Если dark, показываем солнце (для переключения на светлую)
        icon.classList.toggle('fa-sun', isDark);
        // Если light, показываем луну (для переключения на темную)
        icon.classList.toggle('fa-moon', !isDark);
    }
}

// Инициализация темы при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Если сохранена темная тема или она предпочитается системой, устанавливаем ее
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark');
    }

    // Установка начального состояния иконки
    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        if (document.body.classList.contains('dark')) {
             icon.classList.add('fa-sun'); // Текущая тема темная -> иконка солнца
        } else {
             icon.classList.add('fa-moon'); // Текущая тема светлая -> иконка луны
        }
    }
});


// --- City Swap Logic (Для двойной стрелки) ---
function swapCities() {
    const fromSelect = document.getElementById('from_city');
    const toSelect = document.getElementById('to_city');

    if (fromSelect && toSelect) {
        const temp = fromSelect.value;
        fromSelect.value = toSelect.value;
        toSelect.value = temp;

        // Визуальное обновление
        // Запускаем событие 'change' для обновления отображения в Safari/Firefox
        const event = new Event('change');
        fromSelect.dispatchEvent(event);
        toSelect.dispatchEvent(event);
    }
}


// --- Booking Link Fix (Для кнопки "Оформить") ---
function confirmBooking(company, url) {
    // Показываем предупреждение и просим подтвердить переход
    const confirmed = confirm(
        `Вы будете перенаправлены на сайт ${company} для оформления заказа.`
        + `\n\nВнимание: На сайте ${company} вам, возможно, придётся повторно `
        + `ввести параметры доставки (город, вес). Это особенность работы агрегатора без прямого API-договора.`
        + `\n\nНажмите ОК для перехода.`
    );

    if (confirmed) {
        // Открываем ссылку в новой вкладке, чтобы не потерять наш агрегатор
        window.open(url, '_blank');
    }

    // Важно: возвращаем false, чтобы стандартное действие ссылки (href="#") не сработало
    return false;
}