from django.contrib.auth.models import AbstractUser
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


class Worker(AbstractUser):
	position = models.ForeignKey(
		Position,
		on_delete=models.SET_NULL,
		null=True,
		related_name="workers",
	)

	class Meta(AbstractUser.Meta):
		verbose_name = "Worker"
		verbose_name_plural = "Workers"

	def __str__(self) -> str:
		return self.username


class Task(models.Model):
	DEADLINE_ERROR_MESSAGE = "The deadline cannot be in the past."
	PRIORITY_CHOICES = [
		(4, "Urgent"),
		(3, "High"),
		(2, "Medium"),
		(1, "Low"),
	]

	name = models.CharField(max_length=100, unique=True, db_index=True)
	description = models.TextField()
	created_at = models.DateField(auto_now_add=True)
	deadline = models.DateField()
	is_completed = models.BooleanField(default=False)
	priority = models.IntegerField(choices=PRIORITY_CHOICES)
	task_type = models.ForeignKey(
		TaskType,
		on_delete=models.SET_NULL,
		null=True,
		related_name="tasks"
	)
	assignees = models.ManyToManyField(Worker, related_name="tasks")

	class Meta:
		ordering = ["-priority", "deadline"]
