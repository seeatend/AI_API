# AI_API

This is a Flask API for AI Engine.

### Dependencies

* [Python](https://www.python.org/) - Programming Language
* [Flask](https://flask.palletsprojects.com/) - The framework used
* [Pip](https://pypi.org/project/pip/) - Dependency Management
* [RESTful](https://restfulapi.net/) - REST docs
* [Representational State Transfer](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) - Article by Roy Fielding

### Virtual environments
You need ```python``` >=3.11 and ```pip``` >=23

First, you need to create a venv and activate it

For Windows:
```
python3 -m venv venv
cd venv/Scripts
source activate
```

### Install dependencies

#### dependencies for SadTalker:
```
sudo apt update && sudo apt upgrade
sudo apt install ffmpeg

pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
```

#### dependencies for Flask:
```
pip install Flask
pip install -r requirements.txt
```
### Download Models for SadTalker
```
bash app/sadtalker/scripts/download_models.sh
```
### Create following folders to generate video
```
mkdir images
mkdir audios
mkdir videos
```

### Running

For Linux and Mac:
```
export FLASK_APP=app.py
export FLASK_ENV=development
python3 -m flask run
```

For Windows:
```
set FLASK_APP=app.py
set FLASK_ENV=development
python3 -m flask run
```

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production.

If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong.

If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:

```
flask run --host=0.0.0.0 --port=4000 --debug
```

## Contributing

This API was developed based on:

[Flask documentation](https://flask.palletsprojects.com/)

[REST APIs with Flask and Python](https://www.udemy.com/rest-api-flask-and-python/) 

[The Ultimate Flask Course](https://www.udemy.com/the-ultimate-flask-course) 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details