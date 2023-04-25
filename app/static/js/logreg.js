$(document).ready(function(){
        $("#btmSumbit").click(function(){
            $.ajax(
                {
                    url: '/token',
                    method: 'post',
                    data: {'username':$('#val1').val(), 'password':$('#val2').val()},
                    success: function(dt){
                        window.location.replace('/chats')
                        console.log(dt)
                    },
                    error: function (err){
                        console.log(err)
                    }

                }

            )

        });
        $("#rbtmSumbit").click(function(){
            $.ajax(
                {
                    url: '/reg',
                    method: 'post',
                    data: {'username':$('#rval1').val(), 'email': $('#rval2').val(), 'password':$('#rval3').val()},
                    success: function(dt){
                        console.log(dt)
                    },
                    error: function (err){
                        console.log(err)
                    }

                }

            )

        });
        $("#btnLogout").click(function(){
            $.ajax({
                url: '/logout',
                method: 'post',
                data: {},
                success: function(dt){
                        window.location.replace('/chats')
                        console.log(dt)

                },
                error: function (err){
                        console.log(err)
                }

            })
        });
        $('.change').click(function (){
            if ($('.log').css('display') == 'none'){
                $('.log').css('display', 'block')
                $('.reg').css('display', 'none')
            } else {
                $('.log').css('display', 'none')
                $('.reg').css('display', 'block')
            }
            }
        )
    });