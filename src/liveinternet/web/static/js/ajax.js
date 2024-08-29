document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const welcome = document.getElementById('welcome');
    const mainContent = document.getElementById('main-content');
    const chartCanvas = document.getElementById('myChart');
    const sidebarMenu = document.getElementById('sidebarMenu');
    let myChart;
    let currentData = [];
    let currentSite = '';

    // Инициализация оффканвас меню
    const offcanvas = new bootstrap.Offcanvas(sidebarMenu);

    function renderTable(data) {
        searchResults.innerHTML = '';
        const table = document.createElement('table');
        table.classList.add('table-extra', 'noBorder', 'table', 'table-sm');
        const tableBody = document.createElement('tbody');

        data.forEach(item => {
            const tr = document.createElement('tr');

            const rankTd = document.createElement('td');
            rankTd.classList.add('text-end');
            rankTd.innerHTML = `<div class="table-text-grey">${item.rank}</div>`;
            tr.appendChild(rankTd);

            const linkTd = document.createElement('td');
            const button = document.createElement('button');
            button.classList.add('sidebar-button', 'link-offset-2', 'link-offset-3-hover', 'link-underline', 'link-underline-opacity-0', 'link-underline-opacity-75-hover');
            button.setAttribute('data-section', item.link);
            button.innerHTML = `<div class="truncate-140">
                                    <img src="/static/icons/${item.link}.ico" width="16" height="16" border="0">
                                    ${item.link}
                                </div>`;
            linkTd.appendChild(button);
            tr.appendChild(linkTd);

            const visitorsTd = document.createElement('td');
            visitorsTd.classList.add('text-end');
            visitorsTd.innerHTML = `<div class="table-text-grey truncate-80">${item.visitors}</div>`;
            tr.appendChild(visitorsTd);

            tableBody.appendChild(tr);
        });
        table.appendChild(tableBody);
        table.appendChild(tableBody);
        searchResults.appendChild(table);

        // После обновления результатов поиска заново инициализируем обработчики событий
        initializeButtonHandlers();
    }

    function performSearch(query) {
        fetch(`/search?q=${query}`)
            .then(response => response.json())
            .then(data => {
                renderTable(data);
            });
    }

    function initializeButtonHandlers() {
        const buttons = document.querySelectorAll('.sidebar-button');
        buttons.forEach(button => {
            button.addEventListener('click', function () {
                const site = this.getAttribute('data-section');
                localStorage.setItem('selectedSite', site); // Сохраняем сайт в localStorage
                loadSite(site);

                // Закрываем сайдбар на мобильных устройствах
                offcanvas.hide();
            });
        });
    }

    function loadSite(site) {
        fetch(`/content/${site}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    mainContent.innerHTML = `<p style="color: red;">${data.error}</p>`;
                } else {
                    currentData = Object.keys(data.content).map(date => ({
                        date: date,
                        visitors: data.content[date] !== null ? data.content[date] : null
                    }));
                    currentSite = site;

                    // Определяем доступные даты
                    const availableDates = Object.keys(data.content).map(date => {
                        const [year, month, day] = date.split('-');
                        return new Date(year, month - 1, day);
                    });
                    availableDates.sort((a, b) => a - b);

                    // Определяем диапазон последних 30 дней
                    const today = new Date();
                    const thirtyDaysAgo = new Date(today);
                    thirtyDaysAgo.setDate(today.getDate() - 32);

                    // Фильтруем доступные даты для последних 30 дней
                    const availableDatesLast30Days = availableDates.filter(date => date >= thirtyDaysAgo && date <= today);

                    // Если доступные даты последних 30 дней есть, устанавливаем их в datepicker
                    if (availableDatesLast30Days.length > 0) {
                        const firstDate = availableDatesLast30Days[0];
                        const lastDate = availableDatesLast30Days[availableDatesLast30Days.length - 1];

                        startDateInput.value = `${firstDate.getFullYear()}-${String(firstDate.getMonth() + 1).padStart(2, '0')}-${String(firstDate.getDate()).padStart(2, '0')}`;
                        endDateInput.value = `${lastDate.getFullYear()}-${String(lastDate.getMonth() + 1).padStart(2, '0')}-${String(lastDate.getDate()).padStart(2, '0')}`;
                    } else {
                        // Если нет данных за последние 30 дней, можно установить даты по умолчанию или обработать исключение
                        console.log('Нет данных за последние 30 дней');
                    }

                    $('.input-daterange').datepicker('destroy');
                    $('.input-daterange').datepicker({
                        format: "yyyy-mm-dd",
                        language: "ru",
                        autoclose: true,
                        todayHighlight: true,
                        beforeShowDay: function (date) {
                            const formattedDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                            const isAvailable = availableDates.some(availableDate =>
                                availableDate.getTime() === formattedDate.getTime());
                            return isAvailable ? {enabled: true} : {enabled: false, classes: 'disabled-date'};
                        }
                    }).on('changeDate', function () {
                        const startDate = startDateInput.value;
                        const endDate = endDateInput.value;
                        if (startDate && endDate) {
                            filterDataByDate(startDate, endDate);
                        }
                    });

                    // Фильтруем данные за последние 30 дней и обновляем график и таблицу
                    filterDataByDate(startDateInput.value, endDateInput.value);
                }
            })
            .catch(error => {
                mainContent.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            });
    }


    function filterDataByDate(startDate, endDate) {
        const filteredData = currentData.filter(item => {
            const date = new Date(item.date);
            return date >= new Date(startDate) && date <= new Date(endDate);
        });
        updateChartAndTable(filteredData, currentSite);
    }


    function updateChartAndTable(data, site) {
        // Обрезаем конечные пустые данные для графика
        let trimmedData = data.slice();
        for (let i = trimmedData.length - 1; i >= 0; i--) {
            if (trimmedData[i].visitors !== null) {
                break;
            }
            trimmedData.pop();
        }

        const ctx = chartCanvas.getContext('2d');
        const labels = trimmedData.map(item => item.date.slice(5));
        const values = trimmedData.map(item => item.visitors !== null ? item.visitors : NaN); // Используем NaN для пропуска пустых точек

        const siteTitle = document.getElementById('site-name');
        siteTitle.innerHTML = `<img src="/static/icons/${site}.ico" width="24" height="24" border="0"> ${site}`;

        welcome.classList.add('hidden');
        mainContent.classList.remove('hidden');

        if (myChart) {
            myChart.destroy();
        }
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Посещений',
                    data: values,
                    lineTension: 0.33,
                    backgroundColor: 'transparent',
                    borderColor: '#007bff',
                    borderWidth: 4,
                    pointBackgroundColor: '#007bff',
                    spanGaps: true // Пропускаем пустые точки
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        grace: '20%',
                        ticks: {
                            callback: function (value) {
                                if (value >= 1000000) {
                                    return (value / 1000000).toFixed(1) + 'm'; // Миллионы
                                } else if (value >= 1000) {
                                    return (value / 1000) + 'k'; // Тысячи
                                }
                                return value;
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        boxPadding: 3
                    }
                }
            }
        });

        // Обновляем таблицу с исходными данными
        updateTable(data);
    }

    function updateTable(data) {
        const tableBody = document.querySelector('#myTable tbody');
        tableBody.innerHTML = '';

        // Массив для хранения строк
        const rows = [];
        let previousDayVisitors = null;

        // Перебираем данные
        data.forEach((row, index) => {
            const tr = document.createElement('tr');

            let formattedVisitors = row.visitors !== null ? row.visitors.toLocaleString('ru') : '-';
            const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                timeZone: 'UTC'
            };

            // Вычисляем разницу с предыдущим днем
            let visitorsMargin = previousDayVisitors !== null ? (row.visitors - previousDayVisitors) : null;
            let formattedMargin = '';

            if (visitorsMargin !== null) {
                if (visitorsMargin < 0) {
                    formattedMargin = `<span style="color: red">${visitorsMargin.toLocaleString("ru")}</span>`;
                } else if (visitorsMargin > 0) {
                    formattedMargin = `<span style="color: green">+${visitorsMargin.toLocaleString("ru")}</span>`;
                }
            }

            let currentDate = new Date(row.date);
            let localizedDate = currentDate.toLocaleDateString("ru-RU", options).replace(/ г\.$/, '');
            let dayOfWeek = days[currentDate.getDay()];

            tr.innerHTML = `
            <td>${data.length - index}</td>
            <td>${row.date}</td>
            <td>${dayOfWeek}</td>
            <td>${formattedVisitors}</td>
            <td>${formattedMargin}</td>
            `
            ;

            // Сохраняем строку в массив
            rows.push({tr, visitors: row.visitors});
x
            // Обновляем значение предыдущих посещений для следующей итерации
            previousDayVisitors = row.visitors;
        });

        // Добавляем строки в таблицу в обратном порядке
        for (let i = rows.length - 1; i >= 0; i--) {
            tableBody.appendChild(rows[i].tr);
        }
    }

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;
        performSearch(query);
    });

    performSearch(''); // Выполните поиск с пустым запросом при загрузке страницы

    const savedSite = localStorage.getItem('selectedSite');
    if (savedSite) {
        loadSite(savedSite);
    } else {
        welcome.classList.remove('hidden');
    }
    initializeButtonHandlers(); // Инициализируем обработчики событий для кнопок

    // Функция экспорта в CSV
    function exportToCsv() {
        var csv = [];
        const fileName = currentSite.replace(/\./g, '') + '_' + startDateInput.value + '_'
            + endDateInput.value + '.csv'
        const url = `/csv/kp.ru?s=${startDateInput.value}&e=${endDateInput.value}`;

        // Опции запроса
        const options = {
            method: 'GET', // тип запроса (GET, POST, etc.)
            headers: {
                'Content-Type': 'application/json' // заголовки запроса, если нужно
            }
        };

        // Выполнение запроса
        fetch(url, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // преобразование ответа в JSON
            })
            .then(data => {
                var csv = [];
                var headers = ['"Индекс"', '"Дата"', '"Трафик"']; // Adjust header as needed
                csv.push(headers.join(";"));

                // Предположим, что data - это объект с полем 'content', в котором данные строки
                let tableData = data['content'].split(" "); // Разделяем строку на элементы

                // Пройдемся по каждому элементу в массиве tableData
                for (var i = 0; i < tableData.length; i++) {
                    let row = tableData[i]// Корректируем разделитель в зависимости от данных
                    csv.push(row); // Добавляем строку в CSV с разделителем ';'
                }

                var csvContent = "data:text/csv;charset=utf-8," + csv.join("\n"); // Преобразуем в CSV формат

                var link = document.createElement("a");
                link.setAttribute("href", encodeURI(csvContent));
                link.setAttribute("download", fileName);
                link.style.display = "none";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });

    }

    // Event listener for export button
    const exportButton = document.getElementById('export-button');
    exportButton.addEventListener('click', function () {
        exportToCsv();
    });

    // Обрабатываем событие keydown
    searchInput.addEventListener('keydown', function (event) {
        // Проверяем, если нажата клавиша Enter (код клавиши 13)
        if (event.key === 'Enter') {
            event.preventDefault(); // Отключаем действие Enter
        }
    });

});