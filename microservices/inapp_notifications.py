from core.models import Notification


def create_notification(user, content, image, title):

    notification = Notification.objects.create(
        user=user,
        title=title,
        content=content,
        image=image
    )

    return notification
