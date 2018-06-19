
from flask import Flask, jsonify, abort, request, make_response, url_for
import requests
import hashlib

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#TODO root_name
root_name = "/md5/api/v1.0"

#TODO check all response codes

#TODO returns in POST and GET f-ns

task_status = {u"none", u"running", u"done", u"failed"}


tasks = [
    {
        'id': 1,
        'url': u'http://site.com/text.txt',
        'email': u'ex@gmail.ru',
        'status': u'failed',
        'md5': None
    }
] #TODO db



@app.route('/')
@app.route('/nothing')
def nothing():
    return "just nothing"

@app.route(root_name)
def root():
    return "Hi!"


def requests_test():
    r = requests.get('https://www.google.com/images/srpr/logo11w.png')

    #r.encoding
    with open('google_logo.png', 'wb') as f:
        f.write(r.content)
    print("req_test here")


#example
# >>> curl -X POST -d "email=user@example.com&url=http://site.com/file.txt"
# http://localhost:8000/submit
#res: {"id":"0e4fac17-f367-4807-8c28-8a059a2f82ac"}

#parametrs: url and email
@app.route(root_name + '/submit', methods=['POST'])
def create_task():
    # print(request.url_root)
    # !!!print(request.args)
    print(request.form)
    print(request.form.get('email'))
    print(request.form.get('url'))
    print(request.form.get('url', 'no url'))

    if request.form.get('url') is None:  # no url in user request data
        abort(400)  # bad request

    url_for_r = request.form.get('url')
    r_file = requests.get(url_for_r)  # file downloading
    if r_file.status_code == 404: #TODO != 200 ?
        print("404 in requesting file through url")
        abort(404)

    print(r_file.status_code)


    md5hash = hashlib.md5(r_file.content).hexdigest() #content is in bytes


    new_task = {
        'id':  tasks[-1]['id'] + 1 if len(tasks) else 1,
        'url': url_for_r,
        'email': request.form.get('email', 'none'),
        'status': u'done',
        'md5': md5hash
    }

    tasks.append(new_task)
    # sent email TODO

    return jsonify({'task':new_task}), 201  # created


#>>> curl -X GET http://localhost:8000/check?id=0e4fac17-f367-
#4807-8c28-8a059a2f82ac
#{"status":"running"}
#>>> curl -X GET http://localhost:8000/check?id=0e4fac17-f367-
#4807-8c28-8a059a2f82ac
#{"md5":"f4afe93ad799484b1d512cc20e93efd1","status":"done","url":"
#http://site.com/file.txt"}
#parametr: id
@app.route(root_name + "/check", methods=['GET'])
def get_task():
    #no id?
    #task in process/ done / failed
    #done - than return url and md5
    if request.args.get('id') is None:  # no id in user url request
        abort(400)  # bad request

    print(request.args)
    print(request.args.get('id', -1))

    requested_id = int(request.args.get('id', -1)) #TODO

    for task in tasks:
        if task['id'] == requested_id:
            print("found")
            return jsonify({'task': task})
  #  print(request.args)
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
