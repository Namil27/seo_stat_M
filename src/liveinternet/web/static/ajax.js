document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.sidebar-button');
    const applyButton = document.getElementById('apply-dates');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const welcome = document.getElementById('welcome');
    const mainContent = document.getElementById('main-content');
    const chartCanvas = document.getElementById('myChart');
    const tableContainer = document.querySelector('.table-responsive');
    let myChart;
    let currentData = [];
    let currentSite = '';

    // Проверяем, есть ли сохраненный сайт в localStorage
    const savedSite = localStorage.getItem('selectedSite');
    if (savedSite) {
        loadSite(savedSite);
    } else {
        // Если сохраненного сайта нет, показать блок приветствия
        welcome.classList.remove('hidden');
    }

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const site = this.getAttribute('data-section');
            localStorage.setItem('selectedSite', site); // Сохраняем сайт в localStorage
            loadSite(site);
        });
    });

    applyButton.addEventListener('click', function () {
        console.log('Apply button clicked');
        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);

        if (!isNaN(startDate) && !isNaN(endDate)) {
            console.log('Valid dates selected');
            const filteredData = filterDataByDate(currentData, startDate, endDate);
            updateChartAndTable(filteredData, currentSite);
        } else {
            console.log('Invalid date range');
        }
    });

    function filterDataByDate(data, startDate, endDate) {
        return data.filter(item => {
            const itemDate = new Date(item.date);
            return itemDate >= startDate && itemDate <= endDate;
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
                    setInitialDates(currentData);
                    updateChartAndTable(currentData, site);
                }
            })
            .catch(error => {
                mainContent.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            });
    }

    function setInitialDates(data) {
        const availableDates = data.map(item => new Date(item.date));
        availableDates.sort((a, b) => a - b);

        const firstDate = availableDates[0];
        const lastDate = availableDates[availableDates.length - 1];

        startDateInput.value = `${firstDate.getFullYear()}.${String(firstDate.getMonth() + 1).padStart(2, '0')}.${String(firstDate.getDate()).padStart(2, '0')}`;
        endDateInput.value = `${lastDate.getFullYear()}.${String(lastDate.getMonth() + 1).padStart(2, '0')}.${String(lastDate.getDate()).padStart(2, '0')}`;

        $('.input-daterange').datepicker({
            format: "yyyy.mm.dd",
            todayBtn: "linked",
            language: "ru",
            todayHighlight: true,
            beforeShowDay: function(date) {
                const formattedDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                const isAvailable = availableDates.some(availableDate =>
                    availableDate.getTime() === formattedDate.getTime());
                return isAvailable ? { enabled: true } : { enabled: false, classes: 'disabled-date' };
            }
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
        const labels = trimmedData.map(item => item.date);
        const values = trimmedData.map(item => item.visitors !== null ? item.visitors : NaN); // Используем NaN для пропуска пустых точек

        const siteTitle = document.getElementById('site-name');
        siteTitle.innerHTML = `${site} <img src="https://www.liveinternet.ru/favicon/${site}.ico" width="24" height="24" border="0">`;

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
                    lineTension: 0,
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
                        beginAtZero: true
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
});
