#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) 2023 Markus Ottela

This file is part of Calorinator.
Calorinator is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. Calorinator is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License
along with Calorinator. If not, see <https://www.gnu.org/licenses/>.
"""

from invoke import task


@task
def start(ctx):
    ctx.run("python3 calorinator.py", pty=True)


@task
def test(ctx):
    ctx.run("python3 -m pytest tests", pty=True)


# TODO: Figure out how to properly omit ui.
@task
def coverage_report(ctx):
    ctx.run("python3 -m pytest tests "
            "--cov=src/common "
            "--cov=src/database "
            "--cov=src/diet "
            "--cov=src/entities "
            "--cov-report=html", pty=True)


@task
def mypy(ctx):
    ctx.run("python3 -m mypy src", pty=True)


@task
def lint(ctx):
    ctx.run("poetry run python3 -m pylint src --rcfile=.pylintrc", pty=True)


@task
def pep8(ctx):
    ctx.run("poetry run autopep8 --in-place --recursive src", pty=True)
