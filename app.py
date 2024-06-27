import os
import time

from flask import Flask, request, jsonify
from gevent import pywsgi

app = Flask(__name__)
token = os.environ.get('TOKEN')

dev_path = './'
prod_path = '/www/fileRepo/'


@app.route('/file-upload', methods=['POST'])
def file_upload():
    file = request.files['file']
    if token != request.form.get('token'):
        res_data = {
            'code': 10001,
            'msg': '身份认证失败'
        }
        return jsonify(res_data)
    filename = file.filename
    # 更新文件名
    filename_prefix, filename_suffix = split_filename(filename)
    timestamp = int(time.time_ns()/1e6)
    if filename_suffix == '':
        update_filename = f'{filename_prefix}{timestamp}'
    else:
        update_filename = f'{filename_prefix}{timestamp}.{filename_suffix}'
    # 区分开发环境和生产环境
    if os.environ.get('FLASK_ENV') == 'development':
        file.save(f'{dev_path}{update_filename}')
    else:
        file.save(f'{prod_path}{update_filename}')
    res_data = {
        'code': 10000,
        'msg': '文件上传成功',
        'file': update_filename

    }
    return jsonify(res_data)


def split_filename(filename):
    if '.' in filename:
        # 分割文件名，取最后一个元素作为后缀名
        filename_prefix = filename.rsplit('.', 1)[0]
        filename_suffix = filename.rsplit('.', 1)[1]

        return filename_prefix, filename_suffix
    else:
        return filename, ''


if __name__ == '__main__':
    port = 5888
    server = pywsgi.WSGIServer(('127.0.0.1', port), app)
    print(f'Running on http://127.0.0.1:{port}')
    print(f'TOKEN:{token}')
    print(f"FLASK_ENV:{os.environ.get('FLASK_ENV')}")
    server.serve_forever()
