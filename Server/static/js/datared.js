$("#new_ask").on('click',(function () {
    alert('100');
    var data={
        id : $(this).data('name'),
        st : $(this).val,
        action :'new_data_info'

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
}));



