const rowsPerPage = 10;  // Количество строк на страницу
let currentPage = 1;
const rows = document.querySelectorAll('.table .data-row');  // Удостоверьтесь, что класс 'data-row' используется в строках таблицы
const totalRows = rows.length;
const totalPages = Math.ceil(totalRows / rowsPerPage);
const tableBody = document.querySelector('.table tbody'); // Получаем тело таблицы

function updateTableDisplay() {
    // Скрытие всех строк
    rows.forEach(row => {
        row.style.display = 'none';
    });

    // Показываем нужные строки текущей страницы
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    let visibleRows = 0; // Счётчик видимых строк

    rows.forEach((row, index) => {
        if (index >= start && index < end) {
            row.style.display = '';
            visibleRows++;
        }
    });

    // Добавление пустых строк, если видимых меньше, чем rowsPerPage
    while (visibleRows < rowsPerPage) {
        const emptyRow = document.createElement('tr');
        emptyRow.classList.add('empty-row');
        for (let i = 0; i < 3; i++) { // Добавляем три ячейки, соответствующие количеству столбцов
            const td = document.createElement('td');
            emptyRow.appendChild(td);
        }
        tableBody.appendChild(emptyRow);
        visibleRows++;
    }

    // Удаление лишних пустых строк (если они были добавлены при предыдущем вызове)
    const extraRows = document.querySelectorAll('.empty-row');
    extraRows.forEach((row, index) => {
        if (index >= rowsPerPage - visibleRows) {
            tableBody.removeChild(row);
        }
    });
}

function changePage(direction) {
    currentPage += direction;
    // Проверка границ страниц
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    updateTableDisplay();
}

// Инициализация таблицы при первой загрузке
document.addEventListener('DOMContentLoaded', () => {
    updateTableDisplay();  // Вызов функции для инициализации отображения таблицы
});