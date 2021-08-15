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

var jwc = document.getElementById('jobsWeekChart').getContext('2d');
var jobsWeekChart = new Chart(jwc, {
    type: 'doughnut',
    data: {
        labels: [
            'Completed',
            'Outstanding'
        ],
        datasets: [{
            label: 'Jobs Week',
            data: [
                chart_data.jobs.week.completed_week, 
                chart_data.jobs.week.started_week
            ],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'This Week'
            }
        }
    }
});

var htc = document.getElementById('hoursTodayChart').getContext('2d');
var hoursTodayChart = new Chart(htc, {
    type: 'doughnut',
    data: {
        labels: [
            'Projects',
            'General'
        ],
        datasets: [{
            label: 'Hours Today',
            data: [
                chart_data.hours.today.project_hours, 
                chart_data.hours.today.total_hours - chart_data.hours.today.project_hours
            ],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Hours Today'
            }
        }
    }
});
