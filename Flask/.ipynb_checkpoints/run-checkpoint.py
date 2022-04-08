from webservice import get_web_service_app
from model import classification_model_eval, sbert_model_eval

app = get_web_service_app(classification_model_eval)
app.run(host='0.0.0.0', port=5000)