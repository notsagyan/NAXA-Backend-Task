from celery import shared_task

@shared_task
def wish_birthday() -> None:
    print('Happy birthday')