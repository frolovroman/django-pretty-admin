from django.db import models


class MyModel(models.Model):
    STATUSES = [(str(ind), "Status {}".format(ind)) for ind in range(14)]

    title = models.CharField(max_length=255)
    status = models.CharField(choices=STATUSES, max_length=5, default=STATUSES[0][0])
    datetime = models.DateTimeField(null=True)
    external_url = models.URLField()

    def __str__(self):
        return self.title


class RelatedModel(models.Model):
    parent = models.ForeignKey(MyModel, related_name='related')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
