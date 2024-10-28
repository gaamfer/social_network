from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rel_profile')
    username = models.CharField(max_length=36, unique=True)
    bio = models.TextField(max_length=280)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    following = models.ManyToManyField("self", symmetrical=False, related_name='followers', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "profile_pic": self.profile_pic.url,
            "birth_date": self.birth_date,
            "sex": self.get_sex_display(),  # Display the human-readable version of 'sex'
            "followers": self.followers.count() if self.followers.exists() else 0,
            "following": self.following.count() if self.following.exists() else 0
        }



class Post(models.Model):
    creator = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="post")#the user who creates the post
    post_nb = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="post_id")# the id of the post related to the user, aside from the id
    message = models.TextField(max_length=280) # a message with 280 characters
    tag = models.ManyToManyField("Tag", related_name='posts')# the hastags
    ping_users = models.ManyToManyField("Profile", related_name='Pinged_posts')#ping @people , users 
    timestsamp = models.DateTimeField(auto_now_add=True)# the date and time it was posted once button clicked
    is_reported = models.ManyToManyField("Profile", related_name='reports')
    is_deleted = models.ForeignKey("Profile", on_delete=models.CASCADE ,related_name='deleted_post')
    is_archived = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='archived_post')
    is_edited = models.ManyToManyField("Edit", related_name='edited_post')
    repost_source = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name='reposts')
    
    def is_repost(self):
        return self.repost_source is not None

    def serialize(self):
        return {
            "id": self.id,
            "post_number": self.post_nb.id,
            "creator": self.creator.username,
            "message": self.message,
            "tags": [tag.name for tag in self.tag.all()],
            "pinged_users": [user.username for user in self.ping_users.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "is_reported": [user.username for user in self.is_reported.all()],
            "is_deleted": self.is_deleted.username if self.is_deleted else None,
            "is_archived": self.is_archived.username if self.is_archived else None,
            "is_edited": [edit.id for edit in self.is_edited.all()],
            "repost_source": self.repost_source.id if self.repost_source else None,
            "is_repost": self.is_repost()
        }

class SavedPost(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="saved_post")#the user who saves the post
    timestamp = models.DateTimeField(auto_now_add=True)# the date and time it was saved once button clicked
    is_saved = models.BooleanField(default=False)# the post is saved
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post")# the post that is saved


class Edit(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="edit")
    edited_message = models.TextField(max_length=280)
    edited_at = models.DateTimeField(auto_now_add=True)
    editor = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="edit")


class Tag(models.Model):
    Author = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=64, unique=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

class PostImages(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='images/')
    image_ref = models.IntegerField(default=0)
    



class Comment(models.Model):
    Author = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="mycomment")
    body = models.TextField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")

class Reaction(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reaction")
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    love = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

