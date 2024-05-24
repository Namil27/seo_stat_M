document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const welcome = document.getElementById('welcome');
    const mainContent = document.getElementById('main-content');
    const chartCanvas = document.getElementById('myChart');
    let myChart;
    let currentData = [];
    let currentSite = '';

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
                                    <img src="https://www.liveinternet.ru/favicon/${item.link}.ico" width="16" height="16" border="0">
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
                        visitors: data.content[date] !== null ? data.content[date] : null // Используем null для пропуска пустых точек
                    }));
                    currentSite = site;

                    // Инициализация datepicker с доступными датами
                    const availableDates = Object.keys(data.content).map(date => {
                        const [year, month, day] = date.split('-');
                        return new Date(year, month - 1, day);
                    });

                    availableDates.sort((a, b) => a - b); // Сортируем даты

                    // Устанавливаем первую и последнюю даты
                    const firstDate = availableDates[0];
                    const lastDate = availableDates[availableDates.length - 1];

                    startDateInput.value = `${firstDate.getFullYear()}-${String(firstDate.getMonth() + 1).padStart(2, '0')}-${String(firstDate.getDate()).padStart(2, '0')}`;
                    endDateInput.value = `${lastDate.getFullYear()}-${String(lastDate.getMonth() + 1).padStart(2, '0')}-${String(lastDate.getDate()).padStart(2, '0')}`;

                    $('.input-daterange').datepicker('destroy'); // Удаляем предыдущий datepicker
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

                    updateChartAndTable(currentData, site);
                }
            })
            .catch(error => {
                mainContent.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            });
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
        siteTitle.innerHTML = `<img src="https://www.liveinternet.ru/favicon/${site}.ico" width="24" height="24" border="0"> ${site}`;

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
        updateTable(data.reverse());
    }

    function updateTable(data) {
        const tableBody = document.querySelector('#myTable tbody');
        tableBody.innerHTML = '';

        data.forEach((row, index) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${row.date}</td>
                <td>${row.visitors !== null ? row.visitors : '-'}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    function filterDataByDate(startDate, endDate) {
        const filteredData = currentData.filter(item => {
            const date = new Date(item.date);
            return date >= new Date(startDate) && date <= new Date(endDate);
        });
        updateChartAndTable(filteredData.reverse(), currentSite);
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
});

