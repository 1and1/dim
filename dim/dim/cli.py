import click
import dim
from flask.cli import FlaskGroup

@click.group(cls=FlaskGroup, create_app=dim.create_app)
def cli():
    print("For output check your syslog output")
