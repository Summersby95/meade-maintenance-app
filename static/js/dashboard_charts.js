/* jshint esversion: 7 */

chart_data = JSON.parse(document.getElementById("chart_data").textContent);
console.log(chart_data);

var jtc = document.getElementById('jobsTodayChart').getContext('2d');
var jobsTodayChart = new Chart(jtc, {
    type: 'doughnut',
    data: {
        labels: [
            'Completed',
            'Outstanding'
        ],
        datasets: [{
            label: 'Jobs Today',
            data: [
                chart_data.jobs.today.completed_today, 
                chart_data.jobs.today.started_today
            ],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4,
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Today'
            }
        }
    }
});
