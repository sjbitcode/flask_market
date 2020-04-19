from flask import Blueprint

main_blueprint = Blueprint('brownie', __name__)


@main_blueprint.route('/')
def hello_world():
    return 'Hello World! Howdy World! Greeting Bods Promods Quotes'


@main_blueprint.route('/name')
def name():
    return 'my name is sangeeta'
