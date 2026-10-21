import models
import main


def test_models_and_app_import():
    assert hasattr(models, "User")
    assert hasattr(models, "Post")
    assert hasattr(main, "app")


def test_named_page_routes_exist():
    assert main.app.url_path_for("home") == "/"
    assert main.app.url_path_for("login_page") == "/login"
    assert main.app.url_path_for("register_page") == "/register"
    assert main.app.url_path_for("account_page") == "/account"
    assert main.app.url_path_for("forgot_password_page") == "/forgot-password"
    assert main.app.url_path_for("reset_password_page") == "/reset-password"
