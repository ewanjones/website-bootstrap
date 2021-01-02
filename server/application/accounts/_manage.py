def update_user(*, user, full_name, nickname, email, phone, password):
    """
    Provide new values for the user.

    This function won't overwrite values with Falsey values. This would protect against users
    accidentally deleting the text in a field.
    """

    if full_name:
        user.full_name = full_name
    if nickname:
        user.nickname = nickname
    if email:
        user.email = email
    if phone:
        user.phone = phone

    user.save()

    if password:
        user.set_password(password)

    return user
