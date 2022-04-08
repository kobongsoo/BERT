from flask import Flask, request, jsonify, render_template


def get_web_service_app(inference_fn, is_colab=True):

    app = Flask(__name__, template_folder='')
    if is_colab:
        from flask_ngrok import run_with_ngrok
        run_with_ngrok(app)
    else:
        from flask_cors import CORS
        CORS(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api', methods=['POST'])
    def api():
        query_sentence = request.json
        output_data = inference_fn(query_sentence)
        response = jsonify(output_data)
        return response

    return app
