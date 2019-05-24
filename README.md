# URL Shortener

A Flask Web application for shortening URL's

### Installation

1. Make sure your ```python3``` is active. Using ```conda``` or ```virtualenv``` is recommended. For ```conda``` environment:
    ```sh
    conda create -yp py3.7 python=3
    ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   
   or
   
   Simply run:
    ```sh
    ./run-script
    ```
    It will automatically setup a python 3 environment with required
    dependencies, run the test suite and launch the server application.
    As a pre-requirement, ```conda``` must be installed and must be included
    in the system ```PATH```.
    
    Note: make sure to set ```+x``` permissions on the file before running it.
   

### Usage

1. Set the variable environment **FLASK_CONFIGURATION** with the type of environment:
   * testing
   * development (default)
   * production

2. Run the application:
   ```sh
   python run.py
   ```

3. Check it running on ```http://localhost:5000```

### Tests
Run the test suite:
```sh
pytest webapp/tests/ -v
```
