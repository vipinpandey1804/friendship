============
friendship
============

friendship is a Django app to facilitate web-based friendship management.
For each user, they can send, accept, or decline friendship requests.


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "friendship" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "friendship",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("friendship/", include("friendship.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.

5. Visit the ``/friendship/`` URL to participate in the poll.