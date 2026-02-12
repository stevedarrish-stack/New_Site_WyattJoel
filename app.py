from flask import Flask, jsonify, redirect, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/insights.json')
def insights():
    return send_from_directory('.', 'insights.json')


@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    # Supports both HTML form posts and JSON API calls.
    payload = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})

    # Replace with persistence/email integration when ready.
    app.logger.info('New inquiry received: %s', payload)

    if request.form:
        return redirect('/?submitted=1#contact')

    return jsonify(
        {
            'status': 'success',
            'message': 'Inquiry received',
            'data': payload,
        }
    ), 200


@app.route('/api/contact', methods=['POST'])
def api_contact():
    return submit_inquiry()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
