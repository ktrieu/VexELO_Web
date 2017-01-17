$(document).ready(function () {
    $(rankings_table).DataTable({
        ajax: 'api/elo_data',
        columns: [
            { data: 'name' },
            { data: 'elo' }
        ]
    })

    $('.autocomplete').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        async: true,
        limit: 4,
        source: function (query, processSync, processAsync) {
            return $.ajax({
                url: 'api/team_autocomplete',
                type: 'GET',
                data: { query: query },
                dataType: 'json',
                valueKey: '',
                success: function (data) {
                    return processAsync(data.results)
                }
            })
        }
    })

    document.getElementById("predictButton").onclick = function () {
        makePredictRequest($('#inputRedTeam1').val(), $('#inputRedTeam2').val(), $('#inputBlueTeam1').val(), $('#inputBlueTeam2').val())
    }
});

setWinProb = function (prob, id) {
    document.getElementById(id).innerHTML = prob.toString()
}

makePredictRequest = function (redTeam1, redTeam2, blueTeam1, blueTeam2) {
    $.ajax({
        url: "api/predict_match",
        type: "get", //send it through get method
        data: {
            redTeam1: redTeam1,
            redTeam2: redTeam2,
            blueTeam1: blueTeam1,
            blueTeam2: blueTeam2
        },
        success: function (response) {
            setWinProb(response.response.redProb, "redWinProb")
            setWinProb(response.response.blueProb, "blueWinProb")
        },
        error: function (xhr) {
            //Do Something to handle error
        }
    });
}

