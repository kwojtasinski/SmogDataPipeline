from smog_data_pipeline.module import add


def test_add_returns_correct_sum():
    assert add(1, 2, 3) == 6
