$("#send_all").click(function () {
    var data={
        text : $("#in_message").val(),
        action :'new_mes'

    };


    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/com", // адрес, на который будет отправлен запрос
        data: data, // новый контекст исполнения функции
        success: function () { // если запрос успешен вызываем функцию
            alert("Сообщение отправлено"); // добавлем текстовое содержимое в элемент с классом .myClass
        },
        error: function (data) {
            alert(data.responseText);
        }
    });
});

$("#new_shop").click(function () {
    var data={
        content : $("#new_shop").val(),
        slat : $("#slat").val(),
        slon : $("#slon").val(),
        sname : $("#sname").val(),
        action :'new_shop'
    };


    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/com", // адрес, на который будет отправлен запрос
        data: data, // новый контекст исполнения функции
        success: function (data) { // если запрос успешен вызываем функцию
            alert("Магазин добавлен"); // добавлем текстовое содержимое в элемент с классом .myClass
        },
        error: function (data) {
            alert(data.responseText);
        }
    });
    return true;
});

$("#new_ask").click(function () {
    var data=$('#quiz').serializeArray();

    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/com", // адрес, на который будет отправлен запрос
        data: data, // новый контекст исполнения функции
        success: function (data) { // если запрос успешен вызываем функцию
            alert(data.responseText);
        },
        error: function (data) {
            alert(data.responseText);
        }
    });
    return true;
});
