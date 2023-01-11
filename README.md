# JDrive API Backend
JDrive API Backend is a REST API backend server that provides general cloud drive services based on DJango and DRF.
> **Warning** The project is still under development!!

# Front-End
You can also access the flutter based front-end of [JDrive](https://github.com/JenkinsGage/JDrive)

# Features
1. User Auth/Register
2. File Download/Upload/Manage
3. Folder Create/Manage
4. Files are efficiently stored in disk by hash and will be cleaned automatically if file instances no longer refer to them
5. Share folders and files with others

# Available APIs
- GET files/ - To get all the files the user owned
- POST files/ - To upload and create a new file to the server
- GET folders/ - To get all the folders the user owned
- POST folders/ - To create a new folder
- POST user/register/ - To register a new user
- GET hash/ - To get the files with the same hash
- GET files/<str:pk>/ - To get the file detail info of a given id
- PUT files/<str:pk>/ - To modify the file with given id
- DELETE files/<str:pk>/ - To delete the file with given id
- GET folders/<str:pk>/ - To get the folder detail info of a given id
- PUT folders/<str:pk>/ - To modify the folder with given id
- DELETE folders/<str:pk>/ - To delete the folder with given id
- GET user/info/ - To get the basic info of user
- GET root/ - To get the root folder info of user
- GET download/<str:id>/ - To download the file with a given id


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
