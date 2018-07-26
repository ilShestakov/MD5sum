from flask import request, abort, make_response, jsonify
from app import flask, tasks


@flask.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@flask.route('/submit', methods=['POST'])
def create_task():
    file_url = request.form.get('url', None)

    if file_url in [None, '']:
        abort(400)  # bad request

    res = tasks.md5_counting.delay(file_url)

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
            'status':  task.state,
            'md5': task.result['md5'],
        }
    else:
        response = {'status': task.state}

    return jsonify(response), 200  # ok
