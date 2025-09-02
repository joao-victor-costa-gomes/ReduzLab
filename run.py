import os 
from app import create_app

app = create_app()

# This block of code ensures that the folders for uploads and results exist
# before the application starts running. This prevents errors if the folders
# were not created manually.
with app.app_context():
    upload_folder = app.config['UPLOAD_FOLDER']
    results_folder = app.config['RESULTS_FOLDER']

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Created folder: {upload_folder}")

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
        print(f"Created folder: {results_folder}")

# The code inside this 'if' will only run when you execute 'python run.py'.
if __name__ == '__main__':
    # Starts the Flask development server.
    # NEVER use debug=True in a production environment.
    app.run(debug=True)