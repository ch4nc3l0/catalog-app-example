// User dropdown toggler
let navdropdowntoggle = 1;
function userdropdown(){
    if (navdropdowntoggle === 1){
        $('.navdropdown').removeClass('navdropdownout');
        $('.navdropdown').addClass('navdropdownin');
        $('.navdropdown').show();
        
        navdropdowntoggle = 0;
        return;
    }
    else if (navdropdowntoggle === 0){
        $('.navdropdown').removeClass('navdropdownin');
        $('.navdropdown').addClass('navdropdownout');
        // had to use timer to stop hiding navdropdown to early :(
        setTimeout(function(){
            $('.navdropdown').hide()
        },200);

        navdropdowntoggle = 1;
        return;
    }
};

// Menu dropdown toggler
function showmenu(){
    $('.smallmenu').removeClass('smallmenuout');
    $('.smallmenu').addClass('smallmenuin');
    $('.smallmenu').show();
    $('.smallmenuescape').show();
    $('.menu').hide(200);
}

function hidemenu(){
    $('.smallmenu').removeClass('smallmenuin');
    $('.smallmenu').addClass('smallmenuout');
    $('.smallmenuescape').hide();
    $('.menu').show(200);
    // had to use timer to stop hiding navdropdown to early :(
    setTimeout(function(){
        $('.smallmenu').hide()
    },200);
}
       
// Resize and show/hide elements based on screen-size/user-authority
function pageresize(user){
    // window size is xs or less:
    if ($(window).width()<599){
        // login status does not matter:
        //show
        $(".menu").show();
        $(".menubutton").show();
        //hide
        $(".loginbutt").hide();
        $(".loginbuttform").hide();
        $(".navuser").hide();
        // user is logged in:
        if (user != ''){
            // show
            $(".smallmenuimage").show();
            $(".smallmenuprofilewrapper").show();
            $(".smallmenulogoutwrapper").show();
            $(".smallmenuusername").show();
            // hide
            $(".smallmenuusernameloggedout").hide();
            $(".smallmenuimageloggedout").hide();
            $(".smallmenuloginwrapper").hide();
        }
        // user is not logged in:
        else{
            $(".smallmenuloginwrapper").show();
            $(".smallmenuimageloggedout").show();
            $(".smallmenuusernameloggedout").show();

            $(".smallmenuimage").hide();
            $(".smallmenuprofilewrapper").hide();
            $(".smallmenulogoutwrapper").hide();
            $(".smallmenuusername").hide();
        };
    }
    // window size is small or bigger:
    else if ($(window).width()>600){
        // login status does not matter:
        $(".menu").hide();
        $(".menubutton").hide();
        // user is logged in:
        if (user != ''){
            // show
            $(".navuser").show();
            $(".navidwrapper").show();
            $(".navuserid").show();
            $(".caretdown").show();
            $(".navuserimage").show();
            //hide
            $(".loginbutt").hide();
            $(".loginbuttform").hide();
        }
        // user is not logged in:
        else{
            //show
            $(".loginbutt").show();
            $(".loginbuttform").show();
            //hide
            $(".navuser").hide();
            $(".navidwrapper").hide();
            $(".navuserid").hide();
            $(".caretdown").hide();
            $(".navuserimage").hide();
        };
    }
};

// listen for enters on 'clickable' objects (for keyboard only users)
$('.navuser').on('keypress', function(e) {
    if(e.which === 13) {
        $(this).trigger('click');
    }
});

$('.smallmenuescape').on('keypress', function(e) {
    if(e.which === 13) {
        $(this).trigger('click');
    }
});

    