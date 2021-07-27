$(document).ready(function() {
    $("#jobsTable").DataTable({
        responsive: true,
        columnDefs: [
            { responsivePriority: 1, targets: 1 },
            { responsivePriority: 2, targets: -1 },
        ]
    });
    $(window).resize(function() {
        window.location.reload();
    });
});