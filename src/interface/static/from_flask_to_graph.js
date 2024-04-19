/* globals Chart:false */

(() => {
    'use strict'

    // Graphs
    const ctx = document.getElementById('myChart')
    const dataFromPython = JSON.parse('{{ chart_data | safe}}'); // Получаем данные из Flask

    const labels = Object.keys(dataFromPython); // Получаем ключи словаря как метки
    const values = Object.values(dataFromPython); // Получаем значения словаря как данные графика

    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#007bff',
                borderWidth: 4,
                pointBackgroundColor: '#007bff'
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    boxPadding: 3
                }
            }
        }
    })
})()