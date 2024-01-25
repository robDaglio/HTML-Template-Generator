# Project Template Generator
**Author: Rob Daglio**

### Description
PTG is a web development boilerplate template generator for developers not wanting to burden themselves with creating these pages manually or via copy paste. The application automatically generates the directory structure for the project based on provided arguments.

### Dependencies
* Tested on Ubuntu 22.04 and Mac OS Sonoma
* Python 3.10 or later
* virtualenv
* pip

Before attempting installation, please assure that **virtualenv** and **pip** are both installed on your system.

### Installation
Once **virtualenv** and **pip** are installed, create and activate a new virtual environment.
```
$ python -m venv test_venv; source test_venv/bin/activate
$ python -m pip install --upgrade pip; python -m pip install -r requirements.txt
```

Run **install.sh** which will prompt you for an administrator password as well as the target install directory.
```
$ ./install.sh
```

### Running the application
Run **ptg --help** for usage options.
```
usage: ptg [-h] [-p PATH] [-t TYPE] [-l LOG_LEVEL] [-d]

Configuration options for project template generator

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path of the new project. (default: template)
  -t TYPE, --type TYPE  The type of project (native | django | flask) (default: native)
  -l LOG_LEVEL, --log-level LOG_LEVEL
  -d, --download-resources
                        Download additional resources, i.e., bootstrap. (default: False)

```