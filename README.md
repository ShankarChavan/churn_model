churn_model
==============================

mlops end to end lifecycle

# Step 1:

create env

```bash
conda create -n  python=3.7 -y
```

activate env

```bash
conda activate churn_env
```
# Step 2:
create DS project scaffolding run below command
```bash
pip install cookiecutter

# git url for template
cookiecutter https://github.com/drivendata/cookiecutter-data-science

cd churn_model
```
# Step 3:
Setup the git repo and initialize same locally, if running project locally instead of using CodeSpaces.

Run the below command after setting up remote git repository

```bash
git init
git add .
git commit -m "first commit with cookiecutter"
git branch -M main
git remote add origin https://github.com/ShankarChavan/churn_model.git
git push -u origin main
```
In case running locally then if error comes for email and user.name please setup the same. 


# Step 4:


Download the training data from kaggle [link](https://www.kaggle.com/c/customer-churn-prediction-2020/data?select=train.csv) Or from [gdrive link](https://drive.google.com/file/d/1AgAnGFxj0TVfoD9tC4kAv0XPzFUB3mnd/view?usp=share_link) and put it in the *external folder* inside the data folder.

 There are 4 folders inside the data main folder. We will be only using external, raw, and processed folders in this project.

**external**: External files (ex. train.csv or churn_data.csv from Kaggle or gdrive)

**raw**: Raw data for this project

**Processed**: Processed files using the raw files

# Step 5:
Install dvc package if not installed already.This will be used for tracking data and versioning it.

For more details about dvc refer to [this link](https://dvc.org/doc)

Ensure that `/data/` folder in .gitignore file is commented before running `dvc init and dvc add` commands. 

```bash
pip install dvc
dvc init 
dvc add data/external/churn_data.csv

git add data/external/.gitignore data/external/churn_data.csv.dvc

```
Lastly commit the recent changes to git till step 5.

```bash
git add . && git commit -m "update Readme.md and added dvc"
git push origin main
```



Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
