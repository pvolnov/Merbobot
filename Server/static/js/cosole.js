$(document).ready(function(){
    $("#reload").click(function(e) { //устанавливаем событие отправки для формы с id=form
        $.ajax({
            url: "./php/ajax.php",// адрес обработчика
            type: "post",
            dataType: "json",
            data: 'action=take',//данные для обработчика
            success: function (data) {
                $('#dbtable').html(data["responseText"]);
            },
            error: function (data) {


                $('#dbtable').html(data["responseText"]);
                console.log(data);
            }
        });
    })
});