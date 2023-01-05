import math

from app.predict import make_prediction
from utils import load_sample_data


def test_make_single_prediction():
    # Given
    test_data = load_sample_data()
    single_test_input = test_data[0:1]

    # When
    subject = make_prediction(single_test_input)

    # Then
    assert subject is not None
    assert isinstance(subject.get('predictions')[0], str)
    assert subject.get('predictions')[0] == 'no'


def test_make_multiple_predictions():
    # Given
    test_data = load_sample_data()
    original_data_length = len(test_data)
    multiple_test_input = test_data

    # When
    subject = make_prediction(multiple_test_input)

    # Then
    assert subject is not None
    assert len(subject.get('predictions')) == original_data_length
