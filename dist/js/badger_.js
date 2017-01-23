var loggedInUserId = 'pmatheson@csc.com';
var userId;
var apiKey;
var badge;

/////NAVIGATION

//OnClick for side navigation
//<a> must have data-include populated
$('body').on('click', '.nav li a',
    function (e) {
        target=e.currentTarget
        if (typeof target.dataset.include != 'undefined'){
            console.log(target);
            console.log("./includes/" + target.dataset.include + ".html");
            $('#page-wrapper').load("./includes/" + target.dataset.include + ".html");
        }
    }
);

$('body').on('click', '#renderEmailButton',
    function (e) {
        $('#page-wrapper').load("./includes/render-email-badges.html");
    }
);

$('body').on('click', '#loginButton',function (e) {
    loggedInUserId = $('#loggedInUserId').val();
    e.preventDefault();
    window.location.href = "index.html"
});


$('body').on('click','.clickable_badge',
    function(e){
        var badgeId = e.currentTarget.alt;
        result = $.ajax({
          url: "https://x0cqlc5za2.execute-api.ap-southeast-2.amazonaws.com/dev/badges/" + badgeId,
          success: function(data){
            badge = data;
            $('#page-wrapper').load("./includes/render-badge.html");
          }
        });
    }
);

$('body').on('click', '.recipient',function (e) {
    userId = e.currentTarget.text;
    $('#page-wrapper').load("./includes/render-user.html");
});








$('body').on('click', '.addBadgeButton',function (e) {
    badgeId=e.currentTarget.dataset.badgeid
    addBadge(loggedInUserId, badgeId, 'Obtained')
});

$('body').on('click', '.interestBadgeButton',function (e) {
    badgeId=e.currentTarget.dataset.badgeid
    addBadge(loggedInUserId, badgeId, 'Interested')
});

$('body').on('click', '.inProgressBadgeButton',function (e) {
    badgeId=e.currentTarget.dataset.badgeid
    addBadge(loggedInUserId, badgeId, 'In Progress')
});









//Page Construction

$(document).ready(function () {
    renderPage();
})

function renderPage(){
    renderHead();
    renderPageWrapper();
    renderNavigation();
    loadJavaScripts()
}

function renderHead(){
    $('head').load("./includes/head.html");
}

function renderPageWrapper(){
    $('#page-wrapper').load("./includes/index.html");
}

function renderNavigation(){
    $('.navbar').load("./includes/navigation.html");
}

function loadJavaScripts(){
    $.getScript("../vendor/bootstrap/js/bootstrap.min.js")
    //$.getScript("../vendor/metisMenu/metisMenu.min.js")
    $.getScript("../vendor/raphael/raphael.min.js")
    $.getScript("../vendor/morrisjs/morris.min.js")
    $.getScript("../dist/js/moment.min.js")
    $.getScript("../data/morris-data.js")
    $.getScript("../dist/js/sb-admin-2.js")
}

function imgError(image, size) {
    console.log(image.alt)
    result = $.ajax({
                url: "https://x0cqlc5za2.execute-api.ap-southeast-2.amazonaws.com/dev/badges/" + image.alt,
                success: function(data){
                    image.onerror = "";
                    if (data.category == 'Spoken Languages'){
                        image.src = '../images/badges/' + size + '/placeholder_spoken_language.png';
                    }
                    else if (data.category == 'Skills - Technology'){
                        image.src = '../images/badges/' + size + '/placeholder_programing_language.png';
                    }
                    else{
                        image.src = '../images/badges/' + size + '/placeholder_badge.png';
                    }
                }
            })

    return true;
}

function addBadge(userId, badgeId, status){
    var json_data = JSON.stringify({
        "recipient": userId,
        "badgeId": badgeId,
        "status": status,
        "privacy": 'public'
    });

    //FIXME: use request var
    var request = $.ajax({
        url: "https://x0cqlc5za2.execute-api.ap-southeast-2.amazonaws.com/dev/userAssertions",
        type: "POST",
        contentType: 'application/json',
        dataType: "json",
        data: json_data,
        processData: false,
        success: function (data) {
            alert("Added: " + json_data);
        },
        error: function (data) {
            alert("Failed: " + error);
        }
    });
}





//Format file name and remove urlencoding
    function parseDateAsLocal(value, row, index) {
        //console.log(moment.utc(value))
        //console.log(value)
        result = moment.utc(value).local().format('YYYY/MM/DD');
        if (result == 'Invalid date'){
            result = value
            return result;
        }
        else {
            return result;
        }
    }