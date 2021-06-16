# Alternatives for Development Approach

## Python Virtual Environment

It is possible to leverage the functionality of Python's Virtual Environment in order to isolate the development in a self-contained directory tree that contains all the installed requirements for Pe3es IoT project.

You may follow the instructions [here](https://docs.python.org/3/tutorial/venv.html) to setup your virtual environment.

You can youse a IDE of your choice PyCharm / Visual Studio Code.

## Developing with Containers

Unfortunatelly the container functionality is not available in the PyCharm Community Edition. However, this feature is available within Visual Studio Code and the following information is valid for Visual Studio Code.

What does it mean to develop with containers is explained [here](https://code.visualstudio.com/learn/develop-cloud/containers). 

The link describes the basic and lists the pre-requisites necessary:
- `Docker Desktop` is installed on your local machine
- `Remote - Containers extension` is installed within you Visual Studio Code

The link also include a short explanatory video on the topic of developing with containers.

Visual Studio Code Documentaion page has a nice section for REMOTE development:
- [Containers Tutorial](https://code.visualstudio.com/docs/remote/containers-tutorial)
- [Create a DEV Container](https://code.visualstudio.com/docs/remote/create-dev-container)

As of now, all the setup for the remote container is available within folder `.devcontainer` of this repository.