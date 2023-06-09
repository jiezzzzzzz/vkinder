# vkinder

## Что это?

Это вк-бот для поиска людей по заданным пользователем параметрам - город, пол, возраст. У найденного человека можно посмотреть фотографии, добавить его в черный список или в избранное.

Стек: <code>sqlalchemy</code> для работы с бд, <code>vk_api</code> для работы с вк, <code>requests</code> для запросов, <code>environs</code> для перменных окружения.

---

## Как запустить? 

1. Созранить проект себе на машину:

    <code>git clone https://github.com/jiezzzzzzz/vkinder</code>
    
2. Установить зависимости: 

    <code>pip install -r requirements.txt</code>
    
3. Установить переменные окружения

4. Запустить через терминал или кнопку в пайчарме

---

## Как задать переменные окружения?

Нужно создать файл <code>.env</code> и засунуть в него все переменные, которые нужно спрятать. 

Это настройки базы данных и вк-токены. 

Пример овормления файла лежит в <code>.env.example</code> вместе со всеми комментариями.

---

## Как получить токен группы в вк?

1. ### Собственно создать сообщество 

2. ### Управление сообществом -> настройки -> работа с API -> создать ключ

3. ### Проставить все галочки в появившемся окне "Создание ключа доступа"

4. ### Скопировать ключ

---

## Как создать токен пользователя в вк?

1. ### Создать Standalone-приложение на странице "Мои приложения"

2. ### Получить client id.

Для этого снова перейти на страницу с приложениями и нажать на кнопку "Редактировать" рядом с нужным приложением. В адресной строке появится его id. 

Напрмиер, из этой ссылки: <code>https://vk.com/editapp?id=678295892</code> видно, что client_id=678295892.

3. ### Собрать ссылку для получения ключа

Пример ссылки из документации:

    <code>https://oauth.vk.com/authorize?client_id=1&display=page&scope=friends&response_type=token&v=5.92&state=123456</code>
    
<code>redirect_uri</code> указывать не надо т.к. сайт для этого прилложения не нужен
<code>response_type</code> и <code>display</code> оставить такими же, как в примере ссылки
<code>client_id</code> уже получен на шаге 2
<code>v</code> версия апи, нужно указать самую свежую, на данный момент это 5.131

Параметр <code>scope</code> отвечает за доступ к тем или иным частям приложения. Тут стоит указать <code>wall, friend, photos</code>

4. ### Вытащить токен

Перейти по собранной ссылке. В адресной строке появится параметр <code>access_token</code>. Скопировать все, что за ним, должна получиться примерно вот такая строка: 

<code>533bacf01e1165b57531ad114461ae8736d6506a3</code>

