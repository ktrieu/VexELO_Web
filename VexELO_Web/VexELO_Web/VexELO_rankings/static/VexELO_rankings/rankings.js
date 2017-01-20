$(document).ready(function () {
    $(rankings_table).DataTable({
        ajax: 'api/elo_data',
        columns: [
            { data: 'name' },
            { data: 'elo' }
        ]
    })

    var teams = new Bloodhound({
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: 'api/get_teams',
            transform: function (response) {
                return response.teams
            }
        }
    })

    $('.autocomplete').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        source: teams
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

