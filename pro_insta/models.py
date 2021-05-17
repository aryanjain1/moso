from django.db import models


# Create your models here.
class insta(models.Model):
    follower = models.IntegerField()
    followee = models.IntegerField()
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=540, null=True)
    Bio = models.CharField(max_length=500)
    city = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=100, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "follower": self.follower,
            "followee": self.followee,
            "name": self.name,
            "category": self.category,
            "Bio": self.Bio,
            "city": self.city,
            "contact": self.contact
        }
