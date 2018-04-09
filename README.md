# Gender Gap Visualization Tool

---

Data exploration and analysis application created with Python and Dash, hosted at [heroku.com](https://gendergapvisualization.herokuapp.com).

IMAGE

Based on San Francisco and Newport Beach dataset found at [Transparent California](https://transparentcalifornia.com/) for analysis of the public jobs in California. 

### Repo Contents:

---

+ `app.py` 	The application code, contains front-end layouts, logic for graphs, inputs and output to the dataset.
+ `cleaned_nb.csv` Preprocessed data for Newport beach.
+ `cleaned_sf.csv` Preprocessed data for San Francisco.
+ `Procfile` for hosting on heroku only.

### Running the App Locally:

---

+ Clone this repository.
+ Create virtual environment `python -m virtualenv venv` (Optional).
+ Start virtual environment `source venv/Scripts/activate` (Optional). 
+ Install packages `pip install -r requirements.txt`.
+ Start the application `python app.py`.
+ Enter http://localhost:5000/ in your web browser to use the application locally.

