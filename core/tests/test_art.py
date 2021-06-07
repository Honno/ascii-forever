import re

from pytest import fixture
from pytest import mark

from core.models import *

from .multiline import *

# ------------------------------------------------------------------------------
# Art


# fmt:off


py_logo = multiline(r"""
                   _.gj8888888lkoz.,_
                d888888888888888888888b,
               j88P""V8888888888888888888
               888    8888888888888888888
               888baed8888888888888888888
               88888888888888888888888888
                            8888888888888
    ,ad8888888888888888888888888888888888  888888be,
   d8888888888888888888888888888888888888  888888888b,
  d88888888888888888888888888888888888888  8888888888b,
 j888888888888888888888888888888888888888  88888888888p,
j888888888888888888888888888888888888888'  8888888888888
8888888888888888888888888888888888888^"   ,8888888888888
88888888888888^'                        .d88888888888888
8888888888888"   .a8888888888888888888888888888888888888
8888888888888  ,888888888888888888888888888888888888888^
^888888888888  888888888888888888888888888888888888888^
 V88888888888  88888888888888888888888888888888888888Y
  V8888888888  8888888888888888888888888888888888888Y
   `"^8888888  8888888888888888888888888888888888^"'
               8888888888888
               88888888888888888888888888
               8888888888888888888P""V888
               8888888888888888888    888
               8888888888888888888baed88V
                `^888888888888888888888^
                  `'"^^V888888888V^^'
""")

py_logo_render = multiline(r"""
                   _.gj8888888lkoz.,_                                           
                d888888888888888888888b,                                        
               j88P""V8888888888888888888                                       
               888    8888888888888888888                                       
               888baed8888888888888888888                                       
               88888888888888888888888888                                       
                            8888888888888                                       
    ,ad8888888888888888888888888888888888  888888be,                            
   d8888888888888888888888888888888888888  888888888b,                          
  d88888888888888888888888888888888888888  8888888888b,                         
 j888888888888888888888888888888888888888  88888888888p,                        
j888888888888888888888888888888888888888'  8888888888888                        
8888888888888888888888888888888888888^"   ,8888888888888                        
88888888888888^'                        .d88888888888888                        
8888888888888"   .a8888888888888888888888888888888888888                        
8888888888888  ,888888888888888888888888888888888888888^                        
^888888888888  888888888888888888888888888888888888888^                         
 V88888888888  88888888888888888888888888888888888888Y                          
  V8888888888  8888888888888888888888888888888888888Y                           
""")

mrlc_test = multiline(r"""
 _____  _                                ___   ___     _____      _       ___     _____                   _ 
|  __ \(_)                              / _ \ / _ \   / ____|    | |     |__ \   / ____|                 | |
| |  | |_ ___     _____   _____ _ __   | (_) | | | | | |     ___ | |___     ) | | (___  _   _ _ __ ___   | |
| |  | | / __|   / _ \ \ / / _ \ '__|   > _ <| | | | | |    / _ \| / __|   / /   \___ \| | | | '__/ _ \  | |
| |__| | \__ \  | (_) \ V /  __/ |     | (_) | |_| | | |___| (_) | \__ \  |_|    ____) | |_| | | |  __/  |_|
|_____/|_|___/   \___/ \_/ \___|_|      \___/ \___/   \_____\___/|_|___/  (_)   |_____/ \__,_|_|  \___|  (_)
""")


mrlc_test_native = multiline(r"""
 _____  _                                ___   ___     _____      _       ___   
|  __ \(_)                              / _ \ / _ \   / ____|    | |     |__ \  
| |  | |_ ___     _____   _____ _ __   | (_) | | | | | |     ___ | |___     ) | 
| |  | | / __|   / _ \ \ / / _ \ '__|   > _ <| | | | | |    / _ \| / __|   / /  
| |__| | \__ \  | (_) \ V /  __/ |     | (_) | |_| | | |___| (_) | \__ \  |_|   
|_____/|_|___/   \___/ \_/ \___|_|      \___/ \___/   \_____\___/|_|___/  (_)   
""")


# fmt:on

# ------------------------------------------------------------------------------
# Tests


@mark.django_db
def test_render_thumb(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")
    art = Art(artist=user, title="python logo", text=py_logo)

    multiline_assert(art.renderable_thumb, py_logo_render)


@mark.django_db
def test_native_thumb(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")
    art = Art(artist=user, title="mrlc's test", text=mrlc_test)

    multiline_assert(art.natively_thumb, mrlc_test_native)


@mark.django_db
def test_self_like(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")

    art = Art(artist=user, title="mrlc's test", text=mrlc_test, nsfw=False)
    art.save()

    assert user in art.likes.get_queryset().all()


@mark.django_db
def test_art_delete(django_user_model):
    artist = django_user_model.objects.create(username="bob", password="pass")
    art = Art(artist=artist, title="python logo", text=py_logo, nsfw=False)
    art.save()

    author = django_user_model.objects.create(username="alice", password="pass")
    comment = Comment(author=author, art=art, text="foo")
    comment.save()

    art.delete()

    assert Art.objects.count() == 0
    assert Art._objects.count() == 1
    assert Comment.objects.count() == 1
