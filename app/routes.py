from flask import request, abort, make_response, jsonify
from app import flask, tasks


@flask.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@flask.route('/submit', methods=['POST'])
def create_task():
    file_url = request.form.get('url', None)
    email = request.form.get('email', None)

    if file_url in [None, '']:
        abort(400)  # bad request
    if not file_url.startswith('http://') or len(file_url) < 8:
        abort(400)

    res = tasks.md5_counting.delay(file_url, email)

    return jsonify({'id': res.id}), 201  # created


@flask.route('/check', methods=['GET'])
def get_task():
    requested_id = request.args.get('id')
    if requested_id is None:
        abort(400)  # bad request

    task = tasks.md5_counting.AsyncResult(requested_id)

    if task.state == u'SUCCESS' and 'err' in task.result:
        if task.result['err'] == 'requests':
            abort(502)  # bad getaway
        elif task.result['err'] == 'hashlib':
            abort(500)  # internal server error
        else:  # 'lowmemory'
            response = {'status': 'failed'}

    elif task.state == u'SUCCESS':  # no err
        response = {
            'status': 'done',
            'md5': task.result['md5'],
            'url': task.result['url']}
    elif task.state == u'PENDING':
        response = {'status': "doesn't exist"}
    elif task.state in [u'RUNNING', u'RETRY']:
        response = {'status': 'running'}
    else:  # state in [u'FAILURE', u'REVOKED']
        response = {'status': 'failed'}

    return jsonify(response), 200  # ok
