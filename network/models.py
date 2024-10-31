from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


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
    
    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="posts")
    post_nb = models.IntegerField()  # unique post number for user, alternative to id
    message = models.TextField(max_length=280)
    ping_users = models.ManyToManyField("Profile", related_name='pinged_posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_del = models.BooleanField(default=False)
    is_arch = models.BooleanField(default=False)
    is_reported = models.ManyToManyField("Profile", related_name='reports', blank=True)
    is_edited = models.ManyToManyField("Edit", related_name='edited_posts', blank=True)
    repost_source = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name='reposts')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['creator', 'post_nb'], name='unique_post_nb_per_user')
        ]

    def save(self, *args, **kwargs):
        # Only assign post_nb if it is not already set
        if self.post_nb is None:
            # Get the last post for this user
            last_post = Post.objects.filter(creator=self.creator).order_by('post_nb').last()
            # Set post_nb as one greater than the last post_nb, or 1 if no posts exist
            self.post_nb = last_post.post_nb + 1 if last_post else 1
        super().save(*args, **kwargs)

    def is_repost(self):
        return self.repost_source is not None

    def serialize(self):
        return {
            "id": self.id,
            "post_number": self.post_nb,
            "creator": self.creator.username,
            "message": self.message,
            "pinged_users": [user.username for user in self.ping_users.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "is_reported": [user.username for user in self.is_reported.all()],
            "is_del": self.is_del,
            "is_arch": self.is_arch,
            "is_edited": [edit.id for edit in self.is_edited.all()],
            "repost_source": self.repost_source.id if self.repost_source else None,
            "is_repost": self.is_repost()
        }

    def __str__(self):
        return f'{self.creator.user.username} post:{self.post_nb}'



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
    posts = models.ManyToManyField("Post", related_name="tags")
    reference = models.IntegerField(default=0)
    name = models.CharField(max_length=64, unique=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

    # a method so that everytime a tag is created,  add one to  reference or if exists add one to current reference
    def add_reference(self):
        self.reference += 1
        self.save()
    
    def __str__(self):
        return f'{self.name} ({self.reference})'
    




class PostImages(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='images/')
    image_ref = models.IntegerField(default=0)

    def __str__(self):
        return f'pic_{self.post}_{self.image_ref}'
    



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

