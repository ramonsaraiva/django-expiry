# django-expiry

Expiry rules for Django sessions.

## Installation

Install using `pip`

    pip install django-expiry

Add `expiry` to your `INSTALLED_APPS` setting

    INSTALLED_APPS = (
        ...
        'expiry',
    )

## Usage

Define a set of rules in your settings

    EXPIRY_SESSION_RULES = (
        (lambda user, request: user.is_superuser, 300)
        (lambda user, request: user.has_perms('hero'), datetime.timedelta(weeks=99999))
        ('app.expiry.special_ip', datetime.timedelta(days=10))
    )


Each rule is composed by:
* A lambda, a function or a path to a function that will validate it
* An expiry (seconds, datetime, timedelta)

Rules are processed when an user logs in and each rule receives the `user` and the `request` as context.

It is recommended to use a path or a previously defined function when your rule needs complex validations, for example:

    def special_ip(user, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip in ('100.100.100.100', '101.101.101.101', '102.102.102.102')
