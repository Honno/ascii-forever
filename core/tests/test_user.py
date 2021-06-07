from pytest import mark

from .multiline import *


@mark.django_db
def test_follow_self(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")

    assert user in user.following.get_queryset().all()

    # checking if ManyRelatedMany.add prevents duplicates

    user.username = "alice"
    user.save()

    assert user.following.get_queryset().count() == 1


# fmt:off

avatar = multiline(r"""
 o
/|\
/ \
""")

avatar_padded = multiline(r"""
                        
                        
                        
                        
                        
                        
                        
           o            
          /|\           
          / \           
                        
                        
                        
                        
                        
                        
""")


# fmt:on


@mark.django_db
def test_user_avatar_fill(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")

    user.avatar = avatar
    user.save()

    multiline_assert(user.avatar, avatar_padded)
