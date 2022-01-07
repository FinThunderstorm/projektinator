from os import getenv
from invoke import task


@task
def start(ctx):
    #ctx.run('flask run --host=0.0.0.0')
    ctx.run('python3 src/index.py')


@task
def start_production(ctx):
    ctx.run(f'cd src && gunicorn app:app --bind 0.0.0.0:{getenv('PORT')}')


@task
def test(ctx):
    ctx.run('pytest src')


@task
def coverage(ctx):
    ctx.run('coverage run --branch -m pytest src')


@task(coverage)
def coverage_report(ctx):
    ctx.run('coverage xml')


@task
def lint(ctx):
    ctx.run('pylint src')
