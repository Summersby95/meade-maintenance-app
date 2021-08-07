$(document).ready(function() {
    $("#dataTable").DataTable({
        responsive: {
            details: false
        },
        columnDefs: [
            { responsivePriority: 1, targets: 1 },
            { responsivePriority: 2, targets: -1 },
        ]
    });
    $(window).resize(function() {
        window.location.reload();
    });
});