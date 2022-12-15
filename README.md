churn_model
==============================

mlops end to end lifecycle

# Step 1: Create project-specific conda env

create env

```bash
conda create -n churn_env python=3.7 -y
```

activate env

```bash
conda activate churn_env
```
# Step 2: Use Cookiecutter DS template
create DS project scaffolding run below command
```bash
pip install cookiecutter

# git url for template
cookiecutter https://github.com/drivendata/cookiecutter-data-science

cd churn_model
```
# Step 3: Add first commit to github
Setup the git repo and initialize same locally, if running project locally instead of using CodeSpaces.

Run the below command after setting up remote git repository

```bash
git init
git add .
git commit -m "first commit with cookiecutter"
git branch -M main
git remote add origin <your github remote repo name>
git push -u origin main
```
In case running locally then if error comes for email and user.name please setup the same. 


# Step 4: Download data

Download the training data from kaggle [link](https://www.kaggle.com/c/customer-churn-prediction-2020/data?select=train.csv) and put it in the *external folder* inside the data folder.

Or use the below **bash command** to directly download in the external folder 

```bash
curl -L "https://drive.google.com/uc?export=download&id=1AgAnGFxj0TVfoD9tC4kAv0XPzFUB3mnd" --output data/external/churn_data.csv
```




 There are 4 folders inside the data main folder. We will be only using external, raw, and processed folders in this project.

**external**: External files (ex. train.csv or churn_data.csv from Kaggle or gdrive)

**raw**: Raw data for this project

**Processed**: Processed files using the raw files

# Step 5: DVC install 
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

## Setup 5.1: Add current project to PYTHONPATH
Below command will add path temporarily to the environment variables
```bash
export PYTHONPATH=/workspaces/churn_model:$PYTHONPATH
```

For permanently adding run the below command
```bash
vim ~/.bash_profile
export PYTHONPATH=/workspaces/churn_model:$PYTHONPATH
:w
:q
source ~/.bash_profile
```


# Step 6: Create the source code inside the src folder

All project related scripts will be written inside the src folder.
There are 4 folders within `src` folder namely: 
- data (data related scripts e.g. load_data.py,split_data.py etc.)
- features (features engineering related scripts e.g. data_processing.py, feature_engineer.py etc. )
- models (model related scripts e.g. train.py, prod_model_selection.py etc.) 
- visualizations(e.g. reports.py)

## Step 6.1 Create params.yaml config file
We will start with `params.yaml`. This file will hold all the project related configurations.

```bash
touch params.yaml
```
*tip:* on windows cmd prompt you can try this -> `copy nul "params.yaml"` which works same as *touch* in bash.

Update the `params.yaml` with all project related config.

## Step 6.2 Create `load.py` file

Within the `src/data` folder create load_data.py file.

```bash
touch src/data/load_data.py
```

Write code to read configuration and load data from external sources to raw folder.
Add methods :
    - read_params
    - load_data
    - load_raw_data

After updating `load_data.py` file,commit and push code changes.

```bash
git add . && git commit -m "update params.yaml and load_data.py"

git push origin main
```

## Step 6.3: Add `dvc.yaml` file

Create `dvc.yaml` file in the root directory of the project.

This will be the important file for setting up the ML-pipeline in stages. 

```bash
touch dvc.yaml
```
Add or modify stage-1 `load_data` config lines in the `dvc.yaml` file.

After updating `dvc.yaml` Run the below command to see the DAG in terminal window
```bash
dvc dag
``` 

Run the `dvc repro` command on the shell window to execute the load_data.py and new file `dvc.lock` will be created in the root.

Finally do the git commit & push stage-1

```bash
git add . && git commit -m "added stage-1"

git push origin main
```
## Step 6.4 Add `split_data.py` and `stage-2` in dvc.yaml

```bash
touch src/data/split_data.py
```
Add code for splitting data and save it to disc.

Add stage-2(split-data) of split_data.py in dvc.yaml file and run `dvc repro` command

git add,commit and push stage-2 changes to main branch

```bash
git add . && git commit -m "stage-2 completed"
git push origin main
```

## Step 6.5 Add train_model and select best-model from mlflow experiment tracker

First ensure that **mlflow** is already installed in environment.

We will be adding the **train_model.py** code and **production_selection.py** code to train model 
and select the best model.

*train_model.py* is already created as a part of scaffolding.we need to create the 
*production_model_selection.py* in the `src/models` folder

```bash
touch src/models/production_model_selection.py
```
Write code for both python files.

Once added next we need to update the `dvc.yaml` file for both train_model and select production model.

Post this we need to start the mlflow server and run the `dvc repro` in the terminal

MLflow needs two resources to work nicely
- Storage disk or Blob storage or s3 storage location (for storing artifacts like model file,plot files etc.)
- sql db(e.g. sqlite, postgresql, mysql etc) for storing the metrics 

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0 -p 1234
```

Above command will open new popup browser for mlflow-server. 

We are storing metrics in local sqlite db and local artifacts folder.

Run the complete pipeline and check the dvc.lock and models folder.

```bash
dvc repro
```
modify the `max_depth` parameter to `7` in the `params.yaml` and re-run the `dvc repro`

Models will be versioned and moved from staging to production stage based on best accuracy metrics.

`dvc.lock` file should be updated and models folder should have a new `model.joblib` file within it.

Once completed above steps push changes to git

```bash
git add . && git commit -m "stage-3 completed and model file generated"

git push origin main
```

# 7. Prediction Service via API
# 8.
# 9.
# .... 
We will be using **pytest** for our unit testing module, create the tests folder within the main folder and add `__init__.py`.

```bash
mkdir tests
touch tests/__init__.py

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
