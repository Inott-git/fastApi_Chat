    function new_ws(){
    let client_id = document.querySelector("meta[name='client_id']").getAttribute('content')
    let chat_id = document.querySelector("meta[name='chat_id']").getAttribute('content')
    var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}/${chat_id}`)
    ws.onmessage = function(event) {
        var data = JSON.parse(event.data)
        var messageList = document.getElementById('message_list')
        var msg = document.createElement('div')
        if (parseInt(client_id) == data.uid) {
            msg.className = 'you_msg'
        }
        else {
            msg.className = 'notyou_msg'
        }
        var content = document.createTextNode(data['msg'])
        msg.appendChild(content)
        messageList.appendChild(msg)
    };
    return ws
    }
    function get_hist(msgs) {
        var messageList = document.getElementById('message_list')
        var client_id = $('meta[name="client_id"]')[0].content
        msgs.map(function (msg_) {
            var msg = document.createElement('div')
            if (parseInt(client_id) == msg_['user_id']) {
                msg.className = 'you_msg'
            } else {
                msg.className = 'notyou_msg'
            }
            var content = document.createTextNode(msg_['text'])
            msg.appendChild(content)
            messageList.appendChild(msg)
        });
    };
    $(document).ready(function(){
        $("body").on("click", ".chat_min", function(e) {
            chat_click_id = e.currentTarget.children[0].content
            name_user = e.currentTarget.children[2].innerText
            $('#main_name')[0].innerText = name_user
            $('#message_list')[0].innerHTML = ''
            $('meta[name="chat_id"]')[0].content = chat_click_id
            var msgs
            $.ajax(
                {
                    url: `/chats/${chat_click_id}/hist`,
                    method: 'post',
                    data: chat_click_id,
                    success: function(dt){
                        msgs = dt
                        get_hist(msgs)
                        var div = document.getElementById('message_list');
                        div.scrollTop = 1e9
                    },
                    error: function (err){
                        console.log(err)
                    }

                });

            ws = new_ws()



        });
         $('.menu_btn').click(function (){

            if ($('.opacity').css('display') == 'none'){
                $('.opacity').css('display', 'block')
                $('.div_menu').css('display', 'block')
            } else {
                $('.opacity').css('display', 'none')
                $('.div_menu').css('display', 'none')
            }

        })
        $('.logout_btn').click(function (){
            $.ajax(
                {
                    url: '/logout',
                    method: '/post',
                    success: function (dt){
                        window.location.replace('/')
                    },
                    error: function (err){
                        window.location.replace('/')
                    }
                }
            )
        })
    });


    function sendMessage(event, client_id) {
        var input = document.getElementById("sendbtn")
        var data = {'user_id': client_id, 'msg': input.value}
        let chat_id = document.querySelector("meta[name='chat_id']").getAttribute('content')
        ws.send(data.msg)
        console.log(client_id, chat_id, data.msg)
        $.ajax(
            {
                url: `/chats/add`,
                method: 'post',
                data: {'chat_id': chat_id, 'user_id': client_id, 'text': data.msg},
                success: function(dt){
                        var div = document.getElementById('message_list');
                        div.scrollTop = 1e9
                    },
                error: function (err){
                        console.log(err)
                    }
            }
        )
        input.value = ''
        event.preventDefault()
    };