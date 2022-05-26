from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class RangeIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.pop("validators", [])
        
        # turn min_value and max_value params into validators
        min_value = kwargs.pop("min_value", None)
        max_value = kwargs.pop("max_value", None)
        if min_value is None or not isinstance(min_value, int):
            raise TypeError("Expected 'int' value for min_value")
        if max_value is None or not isinstance(max_value, int):
            raise TypeError("Expected 'int' value for max_value")
        
        if min_value > max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        
        validators.append(MinValueValidator(min_value))
        validators.append(MaxValueValidator(max_value))

        kwargs["validators"] = validators

        super().__init__(*args, **kwargs)


class SomeModel(models.Model):
    some_value = RangeIntegerField(min_value=42, max_value=451)
