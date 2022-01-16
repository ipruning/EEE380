import tempfile

import nox

src = "fd_detector", "fd_client", "fd_server"


# from nox_poetry import session
# session.install("black")
def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session
def formatting(session):
    install_with_constraints(session, "black", "isort")
    session.run("black", ".")
    session.run("isort", ".")


@nox.session
def formatting_check(session):
    install_with_constraints(session, "black", "isort")
    session.run("black", ".", "--check")
    session.run("isort", ".", "--check")


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def testing(session):
    install_with_constraints(session, "pytest", "pytest-cov", "coverage[toml]", "loguru")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "report")


@nox.session
def linting(session):
    install_with_constraints(session, "flake8")
    session.run("flake8", ".", "--exit-zero")


@nox.session
def linting_pylint(session):
    install_with_constraints(session, "pylint")
    session.run("pylint", "--fail-under=9", *src)


@nox.session
def typing(session):
    install_with_constraints(session, "mypy")
    session.run("mypy", *src)


@nox.session
def building(session):
    pass


@nox.session
def building_fd_driver(session):
    session.run("pio", "run", "-e", "uno")
