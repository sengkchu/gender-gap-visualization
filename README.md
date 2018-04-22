# Gender Gap Visualization Tool

Data exploration and analysis application for San Francisco and Newport Beach public jobs. This app was created with Python and Dash, hosted at [heroku.com](https://gendergapvisualization.herokuapp.com).

![application](https://raw.githubusercontent.com/sengkchu/gendergapvisualization/master/app_preview.png)

Based on San Francisco and Newport Beach dataset found at [Transparent California](https://transparentcalifornia.com/).
For the data preprocessing and analysis of this dataset, click [here](https://codingdisciple.com/sf-gender-gap.html).

### Repo Contents:

+ data processing and analysis folder:
	+ `Investigating the Gender Wage Gap.ipynb` My data analysis notebook for this project.
	+ `newport-beach-2016.csv` Unprocessed data for Newport Beach.
	+ `database.sqlite` Unprocessed data for San Francisco.
	+ `requirements.txt` requirements for the notebook.
	
	
+ `app.py` 	The application code, contains front-end layouts, logic for graphs, inputs and output to the dataset.
+ `cleaned_nb.csv` Preprocessed data for Newport beach.
+ `cleaned_sf.csv` Preprocessed data for San Francisco.
+ `Procfile` for hosting on heroku only.
+ `requirements.txt` requirements for this application.

### Running the App Locally (Windows):

+ Clone this repository.
+ Create virtual environment `python -m virtualenv venv`.
+ Start virtual environment `.venv/Scripts/activate`. 
+ Install packages `pip install -r requirements.txt`.
+ Start the application `python app.py`.
+ Enter http://localhost:5000/ in your web browser to use the application locally.

### Running the App Locally (macOS and Linux):

+ Clone this repository.
+ Create virtual environment `python3 -m virtualenv venv`.
+ Start virtual environment `source  venv/bin/activate`. 
+ Install packages `pip install -r requirements.txt`.
+ Start the application `python3 app.py`.
+ Enter http://localhost:5000/ in your web browser to use the application locally.

