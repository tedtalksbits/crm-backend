from django.contrib.auth import get_user_model

# accounts/utils.py

def get_crm_bot_user(company):
    User = get_user_model()
    bot_username = f"{company.name} Bot".replace(" ", "_").lower()
    bot_user, created = User.objects.get_or_create(
        username=bot_username,
        defaults={
            "first_name": company.name,
            "last_name": "Bot",
            "email": f"{bot_username}@crm.com",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "company": company,
            "role": "bot"
        }
    )
    if created:
        bot_user.set_unusable_password()
        bot_user.save()
    return bot_user
