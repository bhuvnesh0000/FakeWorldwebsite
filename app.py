from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import os
import requests

app = Flask(__name__)

#EXTERNAL_API_URL = "http://localhost:5001/generate"  # The URL for the local server API
EXTERNAL_API_URL = "https://fakeworld-1-qhlr.onrender.com"  # The URL for the external API

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    file = request.files['file']
    
    # Send the uploaded file to the external API for synthetic data generation
    try:
        # Prepare the file to be sent in the request
        files = {'file': (file.filename, file, file.content_type)}

        # Send the file to the external API
        response = requests.post(EXTERNAL_API_URL, files=files)
        
        if response.status_code == 200:
            # If the response is successful, the synthetic data is returned as a CSV file
            synthetic_data_csv = response.content

            # Save the synthetic data to a file
            filename = 'synthetic_data.csv'
            output_path = os.path.join('generated_files', filename)

            os.makedirs('generated_files', exist_ok=True)

            with open(output_path, 'wb') as f:
                f.write(synthetic_data_csv)

            return jsonify({'url': f'/download/{filename}'}), 200
        else:
            return jsonify({'message': 'Error from external API', 'error': response.text}), 500

    except Exception as e:
        return jsonify({'message': 'An error occurred while generating data', 'error': str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        return send_file(os.path.join('generated_files', filename), mimetype='text/csv', as_attachment=True)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        feedback = data['feedback']

        file_path = 'feedback.xlsx'

        if os.path.exists(file_path):
            df = pd.read_excel(file_path) 
        else:
            df = pd.DataFrame(columns=['Name', 'Email', 'Feedback'])  

        new_data = pd.DataFrame([[name, email, feedback]], columns=['Name', 'Email', 'Feedback'])
        df = pd.concat([df, new_data], ignore_index=True)

        df.to_excel(file_path, index=False, engine='openpyxl')

        return jsonify({'message': 'Feedback saved successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
