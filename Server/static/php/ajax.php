<?php


//header('Content-Type: text/html; charset=utf-8');
// Настройка локали
//setlocale(LC_ALL, 'ru_RU.65001', 'rus_RUS.65001', 'Russian_Russia. 65001', 'russian');

//Устанавливаем доступы к базе данных:
$host = 'localhost'; //имя хоста, на локальном компьютере это localhost
$user = 'neafiol_bd'; //имя пользователя, по умолчанию это root
$password = 'pvolnov'; //пароль, по умолчанию пустой
$db_name = 'neafiol_bd'; //имя базы данных

//Соединяемся с базой данных используя наши доступы:
//$link = mysqli_connect($host, $user, $password, $db_name);
$arr = [22, 29, 95, 68, 112];

printf("<th scope=\"row\" >%s</th>","1");
$idx = 1;
foreach($arr as $value) {
    echo("<td>$value</td>");
}
die();
//if(isset($_GET['action'])){
//    if($_GET['action']=="put"){
//        $sql = "INSERT INTO `caam_db`(`WatherTemp`, `AirTemp`, `AirHum`, `qst_description`)
//             VALUES (" . 28 . ",'" . $text . "'," . $ask_nom .",'".$comment."')"
//
//
//        $result = mysqli_query($link, $sql) or die(mysqli_error($link));
//
//        echo ($result) ;
//    }
//    if($_GET['action']=='get'){
//        $sql = "SELECT * FROM `caam_db`";
//        $arr = [22, 31, 95, 68, 59];
//
//        printf("<th scope=\"row\" >%s</th>","1");
//        $idx = 1;
//        foreach($arr as $value) {
//            echo("<td>$value</td>");
//        }
//    }
//}


?>