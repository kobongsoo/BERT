from flask import Flask, request, jsonify, render_template
from model import classification_model_eval, sbert_model_eval, summarizer_model_eval

#def get_web_service_app(inference_fn):
def get_web_service_app():
    
    app = Flask(__name__, template_folder='')
  
    #=============================================
    # 네이버 무비 classification 예제임
    @app.route('/sc')
    def index():
        return render_template('classification.html')

    @app.route('/api', methods=['POST'])
    def api():
        query_sentence = request.json
        output_data = classification_model_eval(query_sentence)
        response = jsonify(output_data)
        return response
    #=============================================

    #=============================================
    # sentence-bert 문장 유사도 예제임
    @app.route('/sb')
    def sb():
        return render_template('sb.html')

    @app.route('/api_sb', methods=['POST'])
    def api_sb():
        inputs = request.json
        #print(f'inputs:{inputs}')
        output_data = sbert_model_eval(inputs["querys"], inputs["labels"])
        #print(f'outputs:{output_data}')
        response = jsonify(output_data)
        return response
    #=============================================
    
    #=============================================
    # sentence-bert 추출 요약 예제임
    @app.route('/summ')
    def summ():
        return render_template('summarizer.html')

    @app.route('/api_summ', methods=['POST'])
    def api_summ():
        inputs = request.json
        #print(f'inputs:{inputs}')
        output_data = summarizer_model_eval(inputs)
        #print(f'outputs:{output_data}')
        response = jsonify(output_data)
        return response
    #=============================================
    
    return app
