$(function () {
    $('#username').change(function () {
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#pwd').val();
        var cpassword=$('#cpwd').val();
        var url = 'http://127.0.0.1:8000/blog/registhandler/';
        $.post(url,{'username':username,'email':email,'password':password,'cpassword':cpassword},function (status) {
            if(status.result == 'username_not_standard'){
                $('#username').css('border-color','red');
                $('.note').first().text('用户名格式错误,长度要在20以内哈');
                $('.note').first().css('color','red');
                $('#username').val('');
            }
            else if(status.result == 'username_already_existed') {

                $('#username').css('border-color','red');
                $('.note').first().text('用户名已存在，请重新设置');
                $('.note').first().css('color','red');
                $('#username').val('');
            }
            else{
                $('.note').first().text('ok');
                $('.note').first().css('color','green');
            }

        })
    });
    $('#pwd').change(function () {
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#pwd').val();
        var cpassword=$('#cpwd').val();
        var url = 'http://127.0.0.1:8000/blog/registhandler/';
        $.post(url,{'username':username,'email':email,'password':password,'cpassword':cpassword},function (status) {
            if(status.result == 'password_not_standard') {

                $('#pwd').css('border-color', 'red');
                $('.note').last().text('密码不规范，至少8位，不能纯数字，仔细填写哈');
                $('.note').last().css('color', 'red');
                $('#pwd').val('');
            }

            else {

                $('.note').last().text('ok');
                $('.note').last().css('color', 'green');
            }
        });

    });
    $('#cpwd').change(function () {
        var username = $('#username').val();
        var email = $('#email').val();
        var password = $('#pwd').val();
        var cpassword=$('#cpwd').val();
        var url = 'http://127.0.0.1:8000/blog/registhandler/';
        $.post(url,{'username':username,'email':email,'password':password,'cpassword':cpassword},function (status) {

            if(status.result == 'password_not_same') {
                $('#pwd').val = '';
                $('#pwd').css('border-color', 'red');
                $('.note').last().text('两次密码不一致，重新填写');
                $('.note').last().css('color', 'red');
                $('#pwd').val('');
            }
            else {

                $('.note').last().text('ok');
                $('.note').last().css('color', 'green');
            }
        });

    })
});