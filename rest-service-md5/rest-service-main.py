
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__)  # создание объекта приложения (экземпляр класса Фласк) экземпляр класса - наше WSGI приложение
# wsgi - стандарт взаимодействия между Python-программой, выполняющейся на стороне сервера, и самим веб-сервером


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


root_name = "/md5/api/v1.0"



tasks = [
    {
        'url': "",
        'id': 1,
        'md5': u'none1',
    }
] #TODO db




@app.route('/')
@app.route('/nothing')
def nothing():
    return "just nothing"

@app.route(root_name)
def root():
    return "Hi!"


#parametrs: url and email
@app.route(root_name + '/submit', methods=['POST'])
def create_task():
    # check errors
    # load file by url
    # create task
    # sent email
    # return id
    return "pass"

# request.json - содержит данные запроса


#parametr: id
#synch status code
@app.route(root_name + "/check/<int:task_id>", methods=['GET'])
def get_task(task_id):
    #no id?
    #task in process/ done / failed
    #done - than return url and md5
    return "pass"




if __name__ == '__main__':
    app.run(debug=True)
