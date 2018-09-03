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

Add `expiry.middleware.ExpirySessionMiddleware` to your middleware setting

    MIDDLEWARE = (
        ...
        'expiry.middleware.ExpirySessionMiddleware',
    )

Or to middleware classes if your Django is >= 1.10

    MIDDLEWARE_CLASSES = (
        ...
        'expiry.middleware.ExpirySessionMiddleware',
    )

The middleware will process rules and default ages for fresh sessions.

## Usage

### Ages

Default ages can be set for anonymous and authenticated users. When not set, the session age behaviour will default to Django.

`EXPIRY_ANON_SESSION_AGE`  
Default: not set.

The default age of an anonymous session, in seconds.

`EXPIRY_ANON_KEEP_ALIVE`  
Default: `False`

Keeps the authenticated session alive, refreshing its expiry for every request, according to its default value and rules.

`EXPIRY_AUTH_SESSION_AGE`  
Default: not set.

The default age of an authenticated session, in seconds.

`EXPIRY_AUTH_KEEP_ALIVE`  
Default: `False`

Keeps the anonymous session alive, refreshing its expiry for every request, according to its default value and rules.

### Rules

A set of rules should be defined in your settings file.
You can have rules for anonymous users and authenticated users, handled separately.

#### Expiry rules for authenticated users only

Processed whenever an user logs in. Its callable should always accept an `user` and a `request` object.

    EXPIRY_AUTH_SESSION_RULES = (
        (lambda request, user: user.is_staff, 300),
        (lambda request, user: user.is_superuser, datetime.timedelta(weeks=2)),
        (lambda request, user: user.has_perms('hero'), 99999999),
    )

#### Expiry rules for anonymous users only

Processed whenever a session is 

    EXPIRY_ANON_SESSION_RULES = (
        (lambda request: request.META.get('REMOTE_ADDR') == '192.168.0.1', 999)
    )

#### Rule composition

A rule is a tuple composed by:
* A callable or the path to a callable that will validate it
* An expiry (seconds, datetime, timedelta)

In the examples, all rules are lambdas, but you can also send the path to a function that will validate it.
For example:

    EXPIRY_AUTH_SESSION_RULES = (
        ('app.module.complex_rule', datetime.timedelta(days=64)),
    )

Then define the rule in that specific module:

    def complex_rule(user, request):
        ...
