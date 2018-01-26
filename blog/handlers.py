from django.db.models.signals import post_save
from .models import Comment
from notifications.signals import notify


def comment_handler(sender, instance, created, **kwargs):
    if created:
        # 若评论为根评论
        if instance.reply_to is None:
            # 在且仅在根评论不是作者本人的情况下，通知文章作者
            if instance.author != instance.post.author:
                recipient = instance.post.author
                notify.send(
                    instance.author, recipient=recipient,
                    verb='发表了评论', action_object=instance,
                    target=instance.post, description=instance.content
                )
        else:
            # 确认不是自己回复自己,如果自己回复自己不通知
            if instance.author != instance.reply_to.author:
            # 若回复对象就是文章作者本人，则只通知作者
                if instance.reply_to.author == instance.post.author:
                    # 仅通知作者
                    recipient = instance.post.author
                    notify.send(
                        instance.author, recipient=recipient,
                        verb='回复了你', action_object=instance,
                        target=instance.post, description=instance.content
                    )
                else:
                    # 分别通知作者和被回复人
                    # 通知作者A 回复了 B
                    notify.send(
                        instance.author, recipient=instance.post.author,
                        verb='回复了', action_object=instance,
                        target=instance.post, description=instance.content
                    )
                    # 通知被回复人
                    notify.send(
                        instance.author, recipient=instance.reply_to.author,
                        verb='回复了你', action_object=instance,
                        target=instance.post, description=instance.content
                    )

post_save.connect(comment_handler, sender=Comment)
