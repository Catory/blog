$(function () {
            $('#username').change(function () {
                var uname = $('#username').val();
                var upass = $('#password').val();
                var url = 'http://127.0.0.1:8000/blog/loginhandler/';
                $.post(url, {'username': uname, 'password': upass}, function (result) {
                    if (result.status === 'usernameFalse') {
                        alert('该用户不存在 ，请确认后重新输入或注册');
                        window.location=('/blog/login/')
                    }
                });
                $('#password').change(function () {
                    var uname = $('#username').val();
                    var upass = $(this).val();
                    var url = 'http://127.0.0.1:8000/blog/loginhandler/';
                    $.post(url, {'username': uname, 'password': upass}, function (result) {
                        if (result.status === 'pwdFalse') {
                            alert('密码错误，请重新输入');
                            window.location.href='/blog/login/'
                        }

                    })
                })
            })
        });