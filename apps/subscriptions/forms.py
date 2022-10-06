from django.forms import ModelForm

from lib.choices import SUBSCRIPTION_STATUS_CHOICES


class UserSubscriptionForm(ModelForm):
    TRANSITIONS = {
        "active": ["expired", "cancelled"],
        "expired": ["expired"],
        "cancelled": ["cancelled"],
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        status = self.fields["subscription_status"]
        transition = self.TRANSITIONS.get(self.instance.subscription_status)
        if transition is not None:
            status.choices = [
                (key, value) for key, value in status.choices
                if key == self.instance.subscription_status or key in transition
            ]

