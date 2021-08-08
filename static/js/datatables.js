$(document).ready(function() {
    $("#dataTable").DataTable({
        responsive: {
            details: true
        },
        columnDefs: [
            { responsivePriority: 1, targets: 1 },
            { responsivePriority: 2, targets: -1 },
        ]
    });
});