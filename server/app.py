from flask import Flask, jsonify, send_from_directory
import os
import json

app = Flask(__name__, static_folder='../client/build')


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/report/latest', methods=['GET'])
def get_latest_report():
    report_path = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'report.json')
    if os.path.exists(report_path):
        with open(report_path, 'r') as report_file:
            report_data = json.load(report_file)
        return jsonify(report_data), 200
    else:
        return jsonify({"error": "Report not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
