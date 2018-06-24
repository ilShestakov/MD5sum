# Веб-сервис для подсчета MD5-хеша

Веб-сервис для подсчета MD5-хеша от файла, расположенного в сети Интернет. Скачивание и расчет происходят в фоновом режиме.

## API сервиса:

- **POST** запрос на **/submit** с параметрами **url** и **email** (опциональный параметр). 
Cервис возвращает идентификатор задачи, по которому пользователь может узнать о состоянии ее выполнения.
Если указан email, то по окончанию выполнения задачи на него высылается результат с url файла и его MD5-хеш. 

- **GET** запрос на **/check** с параметром **id**. 
Cервис возвращает пользователю состояние задачи по указанному id. 
Состояния:  задачи не существует ('not existed'), задача в работе ('running'), задача завершена ('done'), задача завершилась неудачей ('failed'). 
Если задача завершена, так же возвращаются url файла и его посчитанный MD5-хеш. 


## Запуск

1. Клонируйте этот репозиторий.
2. Создайте virtualenv и установите все данные из requirements.txt
3. Откройте второе окно терминала и запустите локальный сервер Redis (если вы используете Linux или Mac, то выполните run-redis.sh
для установки и запуска, пользователям Windows необходимо скачать и запустить файл [отсюда](https://github.com/MicrosoftArchive/redis/releases)
4. Откройте третье окно терминала. Запустите Celery worker venv/bin/celery -A app.celery_ worker --loglevel=info
5. Запустите пакет app в исходном окне терминала: venv/bin/
  set FLASK_APP=rest-service-md5.py
  flask run


## Примеры использования:

\>>> curl -X POST -d
"email=user@example.com&url=http://site.com/file.txt" http://localhost:5000/submit

>{"id":"0e4fac17-f367-4807-8c28-8a059a2f82ac"}


\>>> curl -X GET http://localhost:5000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac

>{"status":"running"}


\>>> curl -X GET http://localhost:5000/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac

>{"md5":"f4afe93ad799484b1d512cc20e93efd1","status":"done","url":"http://site.com/file.txt"}


