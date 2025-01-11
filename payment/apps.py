from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """
    Configuration class for the Payment app.

    This class sets the default auto field type for models in the Payment app
    and specifies the app's name for Django to recognize it.

    Attributes:
        default_auto_field (str): Specifies the type of primary key to use by default
                                  for models that do not explicitly define one.
        name (str): The name of the app, used by Django to locate and reference it.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "payment"
