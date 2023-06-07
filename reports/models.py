from django.db import models

from authentication.models import User
from posts.models import Post


class Report(models.Model):
    issue = models.CharField(max_length=120)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.issue

    class Meta:
        abstract = True


class IssueReport(Report):
    pass


class InappropriateReport(Report):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)


class Attachment(models.Model):
    file = models.URLField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.file


class IssueAttachment(Attachment):
    report = models.ForeignKey(IssueReport, on_delete=models.CASCADE)


class InappropriateAttachment(Attachment):
    report = models.ForeignKey(InappropriateReport, on_delete=models.CASCADE)
