document.addEventListener('DOMContentLoaded', function () {
    const pasarLabels  = JSON.parse(document.getElementById('pasar-labels-data').textContent);
    const pasarData    = JSON.parse(document.getElementById('pasar-data-data').textContent);
    const statusChart  = JSON.parse(document.getElementById('status-chart-data').textContent);

    Chart.defaults.color = '#9a9a9a';
    Chart.defaults.font.family = "'Public Sans', sans-serif";

    const chartPedagang = new Chart(document.getElementById('chartPedagang'), {
        type: 'bar',
        data: {
            labels: pasarLabels,
            datasets: [{ data: pasarData, backgroundColor: '#7f1414', borderRadius: 6, maxBarThickness: 28 }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: '#262626' }, beginAtZero: true },
                y: { grid: { display: false } }
            }
        }
    });

    const chartStatus = new Chart(document.getElementById('chartStatus'), {
        type: 'doughnut',
        data: {
            labels: ['Selesai', 'Diproses', 'Pending'],
            datasets: [{
                data: [statusChart.selesai, statusChart.diproses, statusChart.baru],
                backgroundColor: ['#22c55e', '#3b82f6', '#eab308'],
                borderColor: '#141414',
                borderWidth: 3
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, cutout: '72%', plugins: { legend: { display: false } } }
    });

    // Fix: canvas kadang stuck ukurannya setelah toggle device-toolbar / resize window drastis
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            chartPedagang.resize();
            chartStatus.resize();
        }, 150);
    });
});