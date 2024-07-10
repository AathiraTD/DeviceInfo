from flask import Flask, request, jsonify
from flask_cors import CORS
from user_agents import parse

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    with open('index.html', 'r') as file:
        return file.read()

@app.route('/api/device-info', methods=['POST'])
def device_info():
    user_agent_string = request.headers.get('User-Agent')
    user_agent = parse(user_agent_string)
    feature_detection = request.json.get('features', {})

    android_version = 'Unknown'
    if user_agent.os.family == 'Android':
        version_parts = user_agent.os.version_string.split('.')
        if len(version_parts) >= 2:
            android_version = f"{version_parts[0]}.{version_parts[1]}"
        else:
            android_version = user_agent.os.version_string

        # Check feature detection results to refine Android version estimate
        feature_based_version = feature_detection.get('estimatedVersion', 'Unknown')
        if feature_based_version != 'Unknown' and float(feature_based_version.split('+')[0]) > float(android_version):
            android_version = feature_based_version

    return jsonify({
        'osName': user_agent.os.family,
        'osVersion': android_version if user_agent.os.family == 'Android' else user_agent.os.version_string,
        'deviceType': 'Mobile' if user_agent.is_mobile else ('Tablet' if user_agent.is_tablet else 'Desktop'),
        'browserName': user_agent.browser.family,
        'browserVersion': user_agent.browser.version_string,
        'deviceBrand': user_agent.device.brand,
        'deviceModel': user_agent.device.model,
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
