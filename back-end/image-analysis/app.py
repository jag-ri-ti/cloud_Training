
from flask import Flask, request, jsonify
from flask_cors import CORS
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}})

# Load environment variables
load_dotenv()
AI_ENDPOINT = os.getenv('AI_SERVICE_ENDPOINT')
AI_KEY = os.getenv('AI_SERVICE_KEY')

# Initialize Azure AI Vision client
cv_client = ImageAnalysisClient(endpoint=AI_ENDPOINT, credential=AzureKeyCredential(AI_KEY))

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        image_data = image_file.read()

        # Analyze image
        result = cv_client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
            ]
        )

        # Prepare and return response
        response_data = {}
        if result.caption:
            response_data['caption'] = {
                'text': result.caption.text,
                'confidence': result.caption.confidence
            }
        if result.tags:
            response_data['tags'] = [{'name': tag.name, 'confidence': tag.confidence} for tag in result.tags.list]
        if result.objects:
            response_data['objects'] = [
                {
                    'tags': [{'name': obj_tag.name, 'confidence': obj_tag.confidence} for obj_tag in obj.tags],
                    'bounding_box': {
                        'x': obj.bounding_box.x,
                        'y': obj.bounding_box.y,
                        'width': obj.bounding_box.width,
                        'height': obj.bounding_box.height
                    }
                }
                for obj in result.objects.list
            ]

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5273)