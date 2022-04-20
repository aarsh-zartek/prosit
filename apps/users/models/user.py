from apps.firebase.models import AbstractFirebaseUser


# Create your models here.

class User(AbstractFirebaseUser):
    """Default user for prosit which inherits from FirebaseUser"""
    pass

    def delete(self):
        self.is_active = False
        self.save()

