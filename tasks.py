from invoke import task


@task
def start(ctx):
    ctx.run('flask run --host=0.0.0.0')


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
