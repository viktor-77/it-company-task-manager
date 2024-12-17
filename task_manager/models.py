from django.db import models


class TaskType(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return self.name


class Position(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return self.name
