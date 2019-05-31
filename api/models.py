from django.db import models


class Employee(models.Model):
    """Employee model represents employees at Luizalabs."""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Override save method to convert Employee's name to title before saving."""
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} at {}".format(self.name, self.department)

    class Meta:
        ordering = ('name',)
