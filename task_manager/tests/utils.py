import datetime

from django.contrib.auth import get_user_model

from task_manager.models import Position, Task, TaskType, Worker


def get_actual_deadline(days: int = 1) -> datetime.date:
	"""Return a future date as the deadline."""
	return datetime.date.today() + datetime.timedelta(days=days)


def get_past_deadline(days: int = 1) -> datetime.date:
	"""Return a past date as the deadline."""
	return datetime.date.today() - datetime.timedelta(days=days)


def get_str_over_length_limit(length_limit: int = 100) -> str:
	"""Return a string over the given length limit."""
	return "x" * (length_limit + 1)


def create_position(name: str = "Developer") -> Position:
	"""Create and return a Position instance."""
	return Position.objects.create(name=name)


def create_task_type(name: str = "Bug") -> TaskType:
	"""Create and return a TaskType instance."""
	return TaskType.objects.create(name=name)


def create_worker(username: str = "test-user", **kwargs) -> Worker:
	"""Create and return a User instance."""
	return get_user_model().objects.create_user(
		username=username, password="test-password", **kwargs
	)


def create_task(
	name: str = "test-name",
	description: str = "test-description",
	deadline: datetime.date = get_actual_deadline(),
	is_completed: bool = False,
	priority: int = 1,
	task_type: TaskType = None,
) -> Task:
	"""Create and return a Task instance."""
	if task_type is None:
		task_type = create_task_type(name=name)

	return Task.objects.create(
		name=name,
		description=description,
		deadline=deadline,
		is_completed=is_completed,
		priority=priority,
		task_type=task_type,
	)
