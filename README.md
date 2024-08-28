# **Youtube and Audio Evaluator**
<hr>

## Steps to run the code

1. Clone from the dev branch:
    ```javascript
        git clone https://AmericanInference@dev.azure.com/AmericanInference/YouTube%20and%20Audio%20Evaluator/_git/YouTube%20and%20Audio%20Evaluator
    ```
2. Create a virtual environment and activate it:
    - Create:

    ```javascript
        pythom -m venv venv
    ```
    - Activate:
    
    ```javascript
        venv/Scripts/activate
    ```
3. Create a ```.env``` file in the root directory and add the following contents:

    ```javascript
        OPENAI_API_KEY = 'your_api_key'
        GROQ_API_KEY = 'your_api_key'
    ```
4. Run the following to install all necessary dependencies:
    ```javascript
        pip install requirements.txt
    ```
5. Change folder directory:
    ```javascript
        cd .\main 
    ```
6. Run the following to setup the database:
    ```javascript
        python manage.py makemigrations
    ```
    ```javascript
        python manage.py migrate
    ```
7. Run the app using:
    ```javascript
        python manage.py runserver
    ```
- ## Note
    * Always pull from the ```Dev-latest``` branch for latest code.