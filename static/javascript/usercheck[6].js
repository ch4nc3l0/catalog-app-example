function loggedin(user) {
    // user is logged in:
    if (user != '') {
        $('.categorybuttons').show();
        $('.newcat').show();

    }
    // user is not logged in:
    else {
        $('.categorybuttons').hide();
        $('.newcat').hide();
    };
}

function formcheck() {
    newcatform = $('#newcategory').val().trim();
    // form is not empty
    if (newcatform != '') {
        document.forms['newcatform'].submit();
        return true;
    }
    // form is empty
    else {
        alert('Please fill out the form no empty forms and no empty spaces');
        return false;
    };
};