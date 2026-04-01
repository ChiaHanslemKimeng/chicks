from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question
