"#CZ4034-Assignment"

1. Install virtualenv package:

pip install virtualenv

2. Create virtual environment

virtualenv venv

3. Activate the created virtual environment

Using Git Bash (reccommended):
. venv/Scripts/activate

4. Using Command Prompt:
venv\Scripts\activate.bat

5. Install senticnet from this link : https://github.com/yurimalheiros/senticnetapi

6. In setup.py in senticnetapi change license=open('LICENSE').read(), to license=open('LICENSE',encoding="utf-8").read(),

7. run python setup.py install

8. Install requirements:

pip install -r requirements.txt

9. Run search_starter.py
