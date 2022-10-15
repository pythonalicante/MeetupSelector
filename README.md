# MeetupSelector

This project is meant to be a landing page for the Python Alicante community and a vote-system to organize MeetUps. It allows the community members to propose Meetup topics and also to propose themselves as speakers.

## Structure Overview

Project structure is shown in the following schema:

![Project schema](./doc/schemas/MeetupSelector_overview.png)

[Schema source](./doc/schemas/MeetupSelector_overview.drawio)

## Prerequisites

- Python v3.10 or higher ([installation](https://wiki.python.org/moin/BeginnersGuide/Download)).
- Python pip package manager ([installation](https://pip.pypa.io/en/stable/installation/)).
- Python virtual environments ([doc](https://docs.python.org/3/tutorial/venv.html), [guide](https://realpython.com/python-virtual-environments-a-primer/)).
- Docker ([installation](https://docs.docker.com/engine/install/)).
- Git ([installation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).

### Optional

- Make ([doc](https://www.gnu.org/software/make/manual/make.html)).

## How to install and run the project

Fork this project in GitHub to your own account. Clone repository to your local, navigate to `MeetupSelector` directory and execute the following commands:

```
git clone https://github.com/pythonalicante/MeetupSelector.git
cd MeetupSelector
cp example.env .env  # Edit this file as you want
make setup  # To create the virtualenv and install project dependencies
make build  # To create Docker images
make run  # To run the project
make createsuperuser  # To create an administrator user in the application
```

## License

This software is released under the [GPLv3 license](LICENSE).

## Contact

- [Discord](https://discord.com/invite/aDdTHZSggd).
- [Telegram](https://t.me/python_alc).
- [Twitter](https://twitter.com/python_alc) #PythonALC.
