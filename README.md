# FileShare
FileShare is a REST API server that prodiveds general cloud drive services based on DJango and DJango Rest Framework.
> **Warning** The project is still under development!!

# Front-End
You can also access the flutter based front-end [JDrive](https://github.com/JenkinsGage/JDrive)

# Features
1. User Auth
2. File Download/Upload/Manage
3. Folder Create/Manage
4. Files are efficiently stored in disk by hash and will be cleaned automatically if file instances no longer refer to them

# Getting Started
1. Clone the project ```git clone https://github.com/JenkinsGage/FileShare.git```
2. Ensure miniconda is installed https://docs.conda.io/en/main/miniconda.html
3. Open miniconda prompt from the project folder
4. Install all the Dependencies via ```conda env create --name <env_name> --file environment.yml```
5. Activate the environment by ```conda activate <env_name>```
6. Migrate database by
```
python manage.py makemigrations
python manage.py migrate
```
7. Create super user
```
python manage.py createsuperuser
```
8. Run the server
```
python manage.py runserver
```
