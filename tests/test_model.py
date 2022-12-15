from src.data.load_data import read_params

def test_config(config):
    assert config["model_dir"]=="models/model.joblib"