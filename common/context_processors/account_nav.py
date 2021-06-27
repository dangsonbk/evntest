from quiz.models import Profile


def account_nav(request):
    user_info = Profile.objects.filter(user__id=request.user.id)
    if user_info.exists():
        user_info = user_info.first()

    return {
        'user_info': user_info,
    }
