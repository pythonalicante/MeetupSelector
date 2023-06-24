# Which code style are used in this project?

For code style we use `PEP 8`[^pep-8], but with `black`[^tools-black].

For Naming conventions we attach to [PEP8 Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions).

For functions/methods/classes/modules/etc. documentation (docstrings) we use [Numpy Documentation Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html).

We type the code, so we're following `PEP 484`[^pep-484] recommendations.


## Tools to ensure you're code is compliant with our code style.

In this project we use `black`[^tools-black] to format the code.

> `Black` is a `PEP 8`[^pep-8] compliant opinionated formatter

To sort imports, we use `isort`[^tools-isort], which is a tool that manages the order of imports in a file.

To check if you typed the code, we use `mypy`[^tools-mypy], which is a checker for `PEP 484`[^pep-484].

For checking that you don't let some imports, variables, etc. unused, some bad programming practices, and a lot of things more, we use `flake8`[^tools-flake8].

And for checking that the `docstrings` are well formatted, we use `flake8-pydocstyle`[^tools-pydocstyle].


## How to run the tools to check if everything is correct

You must run the next command: `make lint`.

It automatically runs all the tools, if it returns any errors, please fix it before making the commit.

If you want to apply `black` and `isort` to whole project (if you don't have this tools configured in your editor), you can run the command: `make apply_black_isort`.


[^tools-black]: [black](https://github.com/psf/black)
[^tools-mypy]: [mypy](http://mypy-lang.org/)
[^tools-isort]: [isort](https://github.com/PyCQA/isort)
[^tools-flake8]: [flake8](https://flake8.pycqa.org/en/latest/)
[^tools-pydocstyle]: [pydocstyle](https://github.com/KRunchPL/flake8-pydocstyle)
[^numpy-docstyle]: [Numpy Doc style](https://numpydoc.readthedocs.io/en/latest/format.html)
[^pep-8]: [PEP 8 Specification](https://peps.python.org/pep-0008/)
[^pep-484]: [PEP 484 Specification](https://peps.python.org/pep-0484/)
