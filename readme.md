# Веб-сервис, который позволяет узнавать, в какие проекты конкретный пользователь Гитхаба делал пул-реквесты и их смерджили
* python 3.9
* Коннект через [GitHubAPI](https://docs.github.com/en/rest) 


## Setup

1. Git Clone the project with: ```git clone https://github.com/Y4phets/github_tracker.git```.

2. Move to the base directory: ```cd github_tracker```

3. Create a new python enveronment with: ```python -m venv env```.

4. Activate enveronment with: ```env\Scripts\activate``` on windows, or ```source env/bin/activate``` on Mac and Linux.

5. Install required dependences with: ```pip install -U -r requirements.txt```.

6. Make migrations with: ```python manage.py makemigrations``` and then ```python manage.py migrate```.

7. Run app localy with: ```python manage.py runserver```.
