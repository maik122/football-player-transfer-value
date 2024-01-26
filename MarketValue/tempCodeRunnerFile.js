// Get the canvas element
var canvas = document.getElementById('market-value-chart');

// Get the 2D context of the canvas
var ctx = canvas.getContext('2d');

// Define the data for the chart
var data = {
labels: ['Game 1', 'Game 2', 'Game 3'],
datasets: [{
label: 'Market Value',
data: [10, 20, 30],
backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)'
],
borderColor: [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)'
],
borderWidth: 1
}]
};

// Define the options for the chart
var options = {
scales: {
yAxes: [{
    ticks: {
    beginAtZero: true
    }
}]
}
};

// Create the chart using Chart.js
var chart = new Chart(ctx, {
type: 'bar',
data: data,
options: options
});
