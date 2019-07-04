
function pwd_handler(form)
{
    var data=$(form).serializeArray();


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
	window.location.reload();
}


