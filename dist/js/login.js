$('body').on('click', '#loginButton',function (e) {
    e.preventDefault();
    loggedInUserId = $('#loggedInUserId').val();
    console.log('UserID: ' + loggedInUserId)
    window.location.href = "index.html"
});