
        if (user != ''){
            document.getElementById('loginButt').style.display = 'none';
            document.getElementById('logoutButt').style.display = '';
            document.getElementById('newCat').style.display = '';
            if(categories != ''){
                document.getElementById('editCat').style.display = '';
                document.getElementById('delCat').style.display = '';
            }
        }
        else{
            document.getElementById('logoutButt').style.display = 'none';
            document.getElementById('loginButt').style.display = '';
            document.getElementById('newCat').style.display = 'none';
            if(categories != ''){
                document.getElementById('editCat').style.display = 'none';
                document.getElementById('delCat').style.display = 'none';
            }
        }