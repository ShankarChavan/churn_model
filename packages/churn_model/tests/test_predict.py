import math

from churn_model.predict import make_prediction
from churn_model.config.utils import load_dataset


def test_make_single_prediction():
    # Given
    test_data = load_dataset()
    single_test_input = test_data[0:1]

    # When
    subject = make_prediction(input_data=single_test_input)

    # Then
    assert subject is not None
    assert isinstance(subject.get('predictions')[0], str)
    assert subject.get('predictions')[0] == 'no'


def test_make_multiple_predictions():
    # Given
    test_data = load_dataset()
    original_data_length = len(test_data)
    multiple_test_input = test_data

    # When
    subject = make_prediction(input_data=multiple_test_input)

    # Then
    assert subject is not None
    assert len(subject.get('predictions')) == original_data_length
