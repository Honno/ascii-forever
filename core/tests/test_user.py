from pytest import mark


@mark.django_db
def test_follow_self(django_user_model):
    user = django_user_model.objects.create(username="bob", password="pass")

    assert user in user.following.get_queryset().all()

    # checking if ManyRelatedMany.add prevents duplicates

    user.username = "alice"
    user.save()

    assert user.following.get_queryset().count() == 1
