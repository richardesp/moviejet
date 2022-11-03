This repository is a web application about the final work of the subject advanced databases.

# Installation guide

You must execute the following script to install the dependencies of the project:

```bash
sh install_repo.sh
```

This command will install the dependencies of the project and **will create the database with all the records** (including the 
creation of a pip3 venv).

# Run the project

To run the project you must execute the following command:

```bash
sh run_app.sh
```

# Restore and initialize the database

To restore and initialize the database you must execute the following command (remember that the installation process will automatically initialize the database, this can be done to leave the database in an initial state):

```bash
flask init-db
```