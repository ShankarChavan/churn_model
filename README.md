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

We will be adding the **train_model.py** code and **production_model_selection.py** code to train model 
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

We will create a new folder `prediction_service`

```bash

mkdir prediction_service
mkdir prediction_service/model_service_dir
touch prediction_service/model_service_dir/.gitignore
echo '/model.joblib'>>prediction_service/model_service_dir/.gitignore
touch prediction_service/model_service_dir/.gitkeep

mkdir app
mkdir app/model_app_dir
touch app/model_app_dir/.gitignore
echo '/model.joblib'>>app/model_app_dir/.gitignore
touch app/model_app_dir/.gitkeep

```
Ensure that `params.yaml` file is updated with model-directory path of api and webapp.


```yaml
model_service_dir: prediction_service/model_service_dir/model.joblib
model_webapp_dir: app/model_app_dir/model.joblib
```
Also update the code in `src/models/production_model_selection.py` file to dump dynamically selected model from mlflow model registry into the above directory.This will automate the dumping process to different services and ensure model version consistency.

We will use `FastAPI` for building api service and `pydantic` for validating the input data feilds.
We will also need `uvicorn` package to initialize the api server. more details about the packages are below
- [FastAPI](https://fastapi.tiangolo.com/)
- [pydantic](https://docs.pydantic.dev/)
- [uvicorn](https://www.uvicorn.org/)

update the `requirements.txt` with fastapi, pydantic and uvicorn and run the pip install.

```bash
- pydantic
- fastapi
- uvicorn
pip install -r requirements.txt
```

Create `datamodel.py` to hold input datatype and validation range via api.
```bash
touch prediction_service/datamodel.py
```

But how do we get the valid range for our input data sources, head over to `EDA.ipynb` file in notebooks folder to understand how we can achieve that. 

create `service_params.yaml` within the prediction_service folder

```bash
touch prediction_service/service_params.yaml
```
update the path for model and variables list in the yaml file.

Add the `utils.py` to read and load the model file. 

```touch
touch prediction_service/utils.py
```

Add the `predict.py` responsible to generate the prediction for live input data coming via post request.  

```touch
touch prediction_service/predict.py
```
Once code is added to the above file run the below bash command to bring the api service up and running for test

```bash
uvicorn predict:app --reload
```
Below landing page will pop-up after running the above command

![FastAPI api page](/assets/fastapi_loading_page.png "FastAPI docs")

Click on the post dropdown and test the prediction-service using demo data.

# 7.1 Critical step to update the model file

We observed that `model.joblib` file created in the **step 6** will create a problem because it will have dependency on mlflow class, so instead perform following 

- use latest code from `production_model_selection.py`.
- update `params.yaml` file for model.pkl instead of model.joblib
- run `dvc repro` from root of the folder.

This will download the `model.pkl` file from artifacts model folder of mlflow to the local models folder.

# 8. Creating packages folder 
Before moving ahead we will do the folder structure change.

Because we want to keep all the packaging in one folder.It will also make it easy to create test folder for all the packages.

So let's create a folder called `packages`, make sure you're at the root of the project

```bash
mkdir packages

mkdir packages/churn_model
mkdir packages/churn_model/churn_model
mkdir packages/churn_model/tests

mkdir packages/ml_api
mkdir packages/ml_api/churn_api
mkdir packages/ml_api/tests

mkdir packages/ml_webapp
mkdir packages/ml_webapp/app
mkdir packages/ml_webapp/tests
```
Now we need to copy the prediction_service files and folder as it is in the packages folder and do the following:
- copy all the files and folder in `packages/ml_api/churn_api/` from prediction_service
- remove the service_params.yaml
- add the `config.py` file
- copy the `model.pkl` to `packages/ml_api/churn_api/model_service_dir/`  
```bash
cp -r prediction_service/* packages/ml_api/churn_api/
rm -v packages/ml_api/churn_api/service_params.yaml
touch packages/ml_api/churn_api/config.py
cp models/model.pkl packages/ml_api/churn_api/model_service_dir/
```
In the `config.py` add the code for configuration of model_dir and model file.

**Reason**: we added `config.py` instead of using `service_params.yaml` is that pytest module is unable to recognize or read the yaml files in subdirectories. 
update the `utils.py` 

run the fastapi service quickly

```bash
uvicorn predict:app --reload
```
After running the above command, Open this -> [localhost url](http://127.0.0.1:8000 )

# 8.1 Create unit-tests for API endpoint

create tests folder within `packages/ml_api/` and add `test_predict.py` & `__init__.py` files

Also ensure to add the `pyproject.toml` file in the `ml_api` folder for the pytest to recognize the churn_api package

```bash
mkdir packages/ml_api/tests
touch packages/ml_api/tests/test_predict.py
touch packages/ml_api/tests/__init__.py
touch packages/ml_api/pyproject.toml
```
Add the code to test the post and get method of the api.

Unit-test usually follows `AAA` approach

- AAA: stands for assemble,action and assert.

We need to assemble required input for our function,execute the action using the input and assert the result of excution with expected output. 

Also update the `pyproject.toml` file for configuring pytest.

```bash
python -m pytest packages/ml_api/
```

Delete the `prediction_service` folder from project root path.

# 8.2 Create the docker file for the api

We will create the docker file in the ml_api folder.

```bash
touch packages/ml_api/Dockerfile
touch packages/ml_api/.dockerignore
```
Add the docker file related commands in the **Dockerfile**. 

More info on [docker basics is here](https://docs.docker.com/get-started/overview/) 

Some of the basic commands are 
- docker build (This is used to build docker image locally)
- docker run (This is used to run the docker container locally)
- docker pull 
- docker push

Run the following command after updating the Dockerfile and moving into `packages/ml_api/`
```bash
docker build -t churn_api_image .
```
[Docker build commands documentation](https://docs.docker.com/engine/reference/commandline/build/) 

Above command will build the docker image for our api and below will run the created image container locally

```bash
docker run -d --name churnapicontainer -p 8000:8000 churn_api_image
```

[Docker run commands documentation](https://docs.docker.com/engine/reference/commandline/run/) 

To list all the docker container 

```bash
docker ps
```

After testing docker image we can stop and remove the docker container from the running process.

```bash
docker stop churnapicontainer
docker rm churnapicontainer
```

Once docker file is created we can push it to **Azure container registry** using `docker push` command and create new VM hosting our api created from docker file.

# 8.3 Create pip installable python package for churn-model

We have already created churn_model folder within packages folder.

## a. setup files and folder for package
We will start adding the files and folders for churn_model pip package.

```bash
# files within churn_model->churn_model
touch packages/churn_model/churn_model/__init__.py
touch packages/churn_model/churn_model/predict.py
touch packages/churn_model/churn_model/VERSION
# files within churn_model
touch packages/churn_model/pyproject.toml
touch packages/churn_model/setup.py
touch packages/churn_model/requirements.txt

# files within churn_model->churn_model->config
mkdir packages/churn_model/churn_model/config
touch packages/churn_model/churn_model/config/config.py
touch packages/churn_model/churn_model/config/utils.py

# files within churn_model->churn_model->datasets
mkdir packages/churn_model/churn_model/datasets
touch packages/churn_model/churn_model/datasets/__init__.py

# files within churn_model->churn_model->model_dir
mkdir packages/churn_model/churn_model/model_dir
touch packages/churn_model/churn_model/model_dir/.gitkeep
touch packages/churn_model/churn_model/model_dir/.gitignore
echo '/model.pkl'>>packages/churn_model/churn_model/model_dir/.gitignore

# files within churn_model->churn_model->processing
mkdir packages/churn_model/churn_model/processing
touch packages/churn_model/churn_model/processing/__init__.py
touch packages/churn_model/churn_model/processing/validation.py

```

## b. download the data and pkl files required
- copy the model.pkl file into the model_dir
- download the sample test data without target variable in the datasets folder with name *churn_test.csv*

```bash
# copy model.pkl
cp models/model.pkl packages/churn_model/churn_model/model_dir
# download the file locally
curl -L "https://drive.google.com/uc?export=download&id=1vNT232rZweCeLzjvOLSiDLj1YKjdAWHu" --output packages/churn_model/churn_model/datasets/churn_test.csv
```
## c. install required packages 
We will need to validate input schema at Dataframe level we can leverage something called as [`pandera`](https://pandera.readthedocs.io/en/stable/schema_models.html)
This library has inbuilt integration with `pydantic` & `fastapi`.
It also supports following Dataframe types:
- Pandas
- Dask
- Modin
- pyspark.pandas
Let's add the pandera to requirements.txt at the root path
```bash
- pandera
pip install -r requirements.txt
```
## d. add the required code 

Add the code for all the `.py` files.
Most of the code remains same except for validation of the input dataframe we have added the seperate class in `validation.py`  

## e. update the version file

Add the version as **0.1**

# 8.4 Add the unit-tests for package churn-model

Add the test_predict.py within `packages/churn_model/` folder.

Write important unit test for your predict file following AAA aproach.

Also update the `pyproject.toml` file for configuring pytest.

Run the following command

```bash
python -m pytest /packages/churn_model
```

# 8.5 Create the install package with setup.py

We need to update the setup.py and requirements.txt within `packages/churn_model` folder.

we will use `setuptools` package setup function to pip installable **.whl**  file.

Some of the important metdata of setup functione we need to enter are following:

- name of package
- description of the package
- python_requires tells which version of python required
- package_data tells which files we need to include apart from .py files.This is critical because we can include our .pkl file in this metdata.
- license tells under which license we are creating this package(e.g. MIT, apache,BSD etc). 
 
Update the `requirements.txt` file with all the required packages for our churn_model
- pickle
- pandas
- scikit-learn
- pandera

Run the command
```bash
python setup.py sdist bdist_wheel 
```

We can clearly see new folders created

![Wheel file created](/assets/pip_package_folder.png "build and dist folder")

Within the dist folder we can see our file `churn_model-0.1-py3-none-any.whl` 

We can use this file to host it on pypi or Gemfury or Azure devops artifacts  


# 8.6 Creating webapp 

We can quickly create web app using two open-source tools

- streamlit
- gradio

pip install both streamlit and gradio in the environment.

We have already created `ml_webapp` folder within packages folder in previous step.

## a. setup files and folders 

Create following folders and files:
```bash

mkdir packages/ml_webapp/app
mkdir packages/ml_webapp/app/datasets
touch packages/ml_webapp/app/datasets/__init__.py
mkdir packages/ml_webapp/app/model_app_dir

touch packages/ml_webapp/app/app.py
touch packages/ml_webapp/app/app_gradio.py

touch packages/ml_webapp/app/config.py
touch packages/ml_webapp/app/predict.py
touch packages/ml_webapp/app/utils.py
touch packages/ml_webapp/app/validation.py
touch packages/ml_webapp/app/__init__.py

mkdir packages/ml_webapp/tests
touch packages/ml_webapp/tests/__init__.py
touch packages/ml_webapp/tests/test_predict.py
touch packages/ml_webapp/pyproject.toml

touch packages/ml_webapp/requirements_app.txt

``` 

Same as in previous step of pip-package creation we will follow the steps

## b. download the pickle and test data file
- copy the model.pkl file into the model_app_dir
- download the sample test data without target variable in the datasets folder with name *churn_test.csv*

```bash
# copy model.pkl
cp models/model.pkl packages/ml_webapp/app/model_app_dir
# download the file locally
curl -L "https://drive.google.com/uc?export=download&id=1vNT232rZweCeLzjvOLSiDLj1YKjdAWHu" --output packages/ml_webapp/app/datasets/churn_test.csv
```

## c. add the code and unit-test

Add the code in `app.py` and `app_gradio.py` files.Rest of the files have almost similar code as in package section.

Move into the app folder within `packages/ml_webapp/app`

Run below bash command to bring up the app.
```bash
streamlit run app/app.py
```

URL link will appear with ip and port in terminal, click on it and page will appear on the browser.

![streamlit page](/assets/streamlit_page.png "streamlit app")

Run below bash command to bring up the gradio app.
```bash
python app_gradio.py
```
URL link will appear with ip and port in terminal, click on it and login page will appear on the browser.

We can see the login page and enter the user-name and password as `admin`,`admin`

![Gradio page](/assets/gradio_login.png "Login app")

After clicking on the login button we can see following landing page

![Gradio landing page](/assets/gradio_landing.png "Landing app")

Gradio provides an option to share app with outer world if we set the argument `share=True` in the launch function. 

We can test prototype-app for our model and create docker file if required for the app to hosted on VM

## d. create the unit-test for the app

Unit-test for the app is same as we had in package section.




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
