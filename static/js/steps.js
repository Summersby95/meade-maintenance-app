// Button event listener to add table row
$("#stepAdd").click(function() {
    tableLength = $("#stepsTable tr").length;
    stepNumber = tableLength + 1;
    $("#stepsTable").append(`
        <tr>
            <th>${stepNumber}.</th>
            <td>
                <input class="form-control"  name="step_${stepNumber}" id="step_${stepNumber}" required>
            </td>
            <td>
                <button type="button" class="btn step-up" data-step="${stepNumber}">
                    <i class="fas fa-arrow-up"></i>
                </button>
            </td>
            <td>
                <button type="button" class="btn step-down" data-step="${stepNumber}">
                    <i class="fas fa-arrow-down"></i>
                </button>
            </td>
            <td>
                <button type="button" class="btn step-delete text-danger" data-step="${stepNumber}">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `);
    $(".step-up").attr("disabled", false);
    $(".step-up:first").attr("disabled", true);

    $(".step-down").attr("disabled", false);
    $(".step-down:last").attr("disabled", true);
});

// Button event listener to delete table row
$("body").on('click', ".step-delete", function() {
    $(this).closest("tr").remove();
    $("#stepsTable tr").each(function(index, tr) {
        $(tr).children("th").html(`${index+1}.`);
        $(tr).children("td").children("input").attr('name', `step_${index+1}`);
        $(tr).children("td").children("input").attr('id', `step_${index+1}`);
        $(tr).children("td").children("button").attr('data-step', `${index+1}`);
    });
    $(".step-up").attr("disabled", false);
    $(".step-up:first").attr("disabled", true);

    $(".step-down").attr("disabled", false);
    $(".step-down:last").attr("disabled", true);
});

// Button event listener to move table row up
$("body").on('click', ".step-up", function() {
    let stepNumber = $(this).data("step");
    let topStepVal = $(`#step_${stepNumber-1}`).val();
    let botStepVal = $(`#step_${stepNumber}`).val();
    $(`#step_${stepNumber-1}`).val(botStepVal);
    $(`#step_${stepNumber}`).val(topStepVal);
});

// Button event listener to move table row down
$("body").on('click', ".step-down", function() {
    let stepNumber = $(this).data("step");
    let topStepVal = $(`#step_${stepNumber}`).val();
    let botStepVal = $(`#step_${stepNumber+1}`).val();
    $(`#step_${stepNumber}`).val(botStepVal);
    $(`#step_${stepNumber+1}`).val(topStepVal);
});
