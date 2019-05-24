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
Run the test 