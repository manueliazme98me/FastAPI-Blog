import models
import main


def test_models_and_app_import():
    assert hasattr(models, "User")
    assert hasattr(models, "Post")
    assert hasattr(main, "app")
