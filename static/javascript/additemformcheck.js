function formcheck(){
newcatform = $('#newcategory').val().trim();
// item name is empty
    if( newcatform = '' ){
        document.forms['newcatform'].submit();
        return true;
    }
// item description is empty
    else if( itemdescription = '' ){
        alert('Please fill out item desctiption no empty spaces');
    }
// form is empty
    else{
        alert('Please fill out the form no empty forms and no empty spaces');
        return false;
    };
};