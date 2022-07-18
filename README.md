# snippet-server
A server that displays random photos and small selections of videos from a given media directory

# Running locally
- Create a python3 virtual environment `python3 -m venv name-of-venv`
- Activate your virtual environment `source path-to-venv/bin/activate`
- Install required packages with `pip install -r requirements.txt`
- Create a flask 'secret key':
    ```python
    import secrets
    print(secrets.token_urlsafe(16))
    ```
- Create a file named *.env* at the root of your repo, and put in the following export commands
  (replacing placeholder values with your own values):
    ```bash
    export FLASK_APP=albumcollections
    export FLASK_ENV=development
    ```
    - **note**: The sqlite database will be created at the path you specify upon the first run of the site.
- Place video and image files inside of the 'media' directoroy. Files can be nested into directories.