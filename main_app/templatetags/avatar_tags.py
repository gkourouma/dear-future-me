from django import template
from django.templatetags.static import static
from cloudinary import CloudinaryImage


register = template.Library()

@register.simple_tag
def avatar_preview(user, size=150):
    pic = getattr(user.profile, 'profile_picture', None)
    if pic:
        # Extract the public_id string
        public_id = getattr(pic, 'public_id', None) or str(pic)
        url = CloudinaryImage(public_id).build_url(
            width=300,
            height=300,
            crop='fit',
            fetch_format='auto',
            quality='auto:best'
        )
    else:
        url = static('media/default-avatar.png')
    return url