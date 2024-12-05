from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
import os
import yaml
from main import main

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)


def load_yaml(file_path):
    try:
        # Try opening the YAML file in read mode
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  # Load YAML data safely
            if data is None:  # Check if the file is empty
                raise ValueError("YAML file is empty")  # Raise an error if empty
            return data  # Return the loaded data if valid
    except FileNotFoundError:
        # Handle case when file is not found
        print(f"File not found at {file_path}. Creating a default file.")
    except yaml.YAMLError as e:
        # Handle parsing errors (invalid YAML format)
        raise ValueError(f"Error parsing YAML file: {e}")
    except ValueError as ve:
        # Handle the case when YAML is empty
        print(f"Error: {ve}. Creating a default file.")


def save_yaml(data, file_path):
    try:
        # Try opening the YAML file in write mode
        with open(file_path, 'w') as file:
            # Dump the data to the file in YAML format, with readable style
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
    except Exception as e:
        # If an error occurs raise a ValueError with the error message
        raise ValueError(f"Error saving YAML file: {e}")


@app.route('/upload_file', methods=['POST'])
def upload_file():
    """
    Upload a file for a specific animal
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to upload
    responses:
      200:
        description: File saved successfully
      400:
        description: Invalid input
      409:
        description: File already exists
    """
    if 'file' not in request.files:
        return 'No file part', 400  # Check if the file is present in the request

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400  # Check if the file has a valid filename

    app.config['UPLOAD_FOLDER'] = "data"  # Set the upload folder path

    # Create the folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file_name = file.filename  # Get the filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)  # Define the file path

    if os.path.exists(file_path):
        return 'File already exists', 409  # Check if the file already exists

    file.save(file_path)
    return f'File saved at {file_path}', 200


@app.route('/list_files', methods=['GET'])
def list_txt_files():
    """
    List all files for a specific animal
    ---
    responses:
      200:
        description: List of files
        schema:
          type: array
          items:
            type: string
      400:
        description: Invalid input
    """
    File_Path = "data"  # Define the directory path

    # Check if the directory exists
    if not os.path.exists(File_Path):
        return jsonify(
            {"error": "Invalid animal type or path does not exist"}), 400  # Return error if path doesn't exist

    # List all files in the directory
    file_names = [file for file in os.listdir(File_Path)]
    return jsonify(file_names)


@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    """
    Delete a file for a specific animal
    ---
    parameters:
      - name: body
        in: body
        required: true
        description: JSON object containing the file name
        schema:
          type: object
          properties:
            file_name:
              type: string
              example: chicken_boundingbox.txt
    responses:
      200:
        description: File deleted successfully
      400:
        description: Invalid input
      404:
        description: File not found
    """
    data = request.json  # Get JSON data from the request
    file_name = data['file_name']

    # Check if 'file_name' is provided
    if not file_name:
        return jsonify({"error": "'file_name' is required."}), 400  # Return error if no file name is provided

    File_Path = "data"  # Define the directory path

    # Check if the directory exists
    if not os.path.isdir(File_Path):
        return jsonify({"error": "path does not exist"}), 404

    file_path = os.path.join(File_Path, file_name)  # Create the full file path

    # Check if the file exists, and delete it if found
    if os.path.isfile(file_path):
        os.remove(file_path)  # Remove the file
        return jsonify({"message": f"File '{file_name}' deleted successfully."}), 200
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/update_config', methods=['PUT'])
def update_config():
    """
    Update configuration settings in a YAML file
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            selectedFile:
              type: string
              example: chicken_boundingbox.txt
            radius:
              type: integer
              example: 100
            subject:
              type: integer
              example: 9
            animal:
              type: string
              example: pig

    responses:
      200:
        description: YAML configuration updated successfully
    """
    file_path = 'configuration.yml'

    # Load existing YAML data
    data = load_yaml(file_path)
    if data is None:
        return {"error": "Failed to load YAML file"}, 500

    # Get JSON input
    input_data = request.get_json()
    if input_data is None:
        return {"error": "No data provided in the request"}, 400

    # Validate and update the YAML data
    try:
        data['radius'] = int(input_data.get('radius', data.get('radius', 0)))
        data['subject'] = int(input_data.get('subject', data.get('subject', '')))
        data['data_file'] = input_data.get('selectedFile', data.get('data_file', ''))
        data['animal'] = input_data.get('animal', data.get('animal', ''))
    except (ValueError, TypeError) as e:
        return {"error": f"Invalid input data: {e}"}, 400

    # Save updated YAML data
    try:
        save_yaml(data, file_path)
    except ValueError as e:
        return {"error": str(e)}, 500
    return jsonify({"message": "YAML file updated successfully!", "updated_data": data}), 200

@app.route('/data', methods=['GET'])
def return_data():
    """
    Fetch processed data from the `main` function
    ---
    responses:
      200:
        description: Successfully retrieved the data
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
              description: return a list of dictionaries contain plot's data
      500:
        description: Internal server error
    """
    try:
        data = main()
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/config_data', methods=['GET'])
def get_data():
    """
    Get configuration data from a YAML file
    ---
    responses:
      200:
        description: A JSON object containing configuration data
        schema:
          type: object
          properties:
            subject:
              type: integer
              example: 9
            radius:
              type: integer
              example: 100
            animal:
              type: string
              example: pig
            selectedFile:
              type: string
              example: chicken_boundingbox.txt
    """
    file_path = 'configuration.yml'  # Path to your YAML file
    data = load_yaml(file_path)  # Load the YAML file
    if data is None:
        raise ValueError("YAML file is empty or could not be loaded")

    required_keys = ["subject", "radius", "animal", "data_file"]
    # Check if all required keys are present in the YAML data
    if not all(key in data for key in required_keys):
        raise KeyError(f"YAML file is missing required keys: {required_keys}")

    # Create a dictionary with values from the YAML, with default values if keys are missing
    data_return = {
        "subject": data.get("subject", "subject"),
        "radius": data.get("radius", 0),
        "animal": data.get("animal", "animal"),
        "selectedFile": data.get("data_file", "file")
    }
    return jsonify(data_return)


if __name__ == '__main__':
    app.run(debug=True)
