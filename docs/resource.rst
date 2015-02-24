************************
How to define a resource
************************


base_url `(required)`
=====================

Each REST API has a fixed main URL behind that contains all other resources.
You can find this value for your application of durga in the used API
documentation.

Examples
^^^^^^^^
::

    base_url = 'https://api.flickr.com/services'

::

    base_url = 'http://musicbrainz.org/ws/2'


path `(required)`
=================

Defines path of API resource you would like to use. You can find it in your
API method description.


path_params
===========

With setting `path_params` you lists your all your placeholder in `path`.

Example
^^^^^^^
::

    path = 'movies/{movie_name}/{movie_year}/actors'
    path_params = ('movie_name', 'movie_year')


id_attribute
============

Attribute `url` is taken per default to has a complete unique resource url.
If you would like to change this, you can define a `id_attribute` by your own.
And set your defined attribute manually.

Default
^^^^^^^
::

    url = 'https://api.example.com/movies/23'

Changed id_attribute
^^^^^^^^^^^^^^^^^^^^
::

    id_attribute = 'id'
    id = '23'


object_path
===========

Indicates the sub path behind the `base_url`.

objects_path
============

It is used if a single resource is returned where the data is somewhere deeper
inside the response. Often your response contains meta information next to
your necesssary objects. So you have show the resource the path to that data.

Example
^^^^^^^

If your JSON response looks like kind of this

.. literalinclude:: ../tests/fixtures/movies.json
   :lines: 1-16, 41-43


Then your attribute `objects_path` is defined in this way

.. literalinclude:: ../tests/conftest.py
   :dedent: 4
   :lines: 16

query
=====

Describes all your query specific params like `format, method` or `params` and
so on.

Example
^^^^^^^

.. literalinclude:: ../tests/test_flickr.py
   :dedent: 4
   :lines: 30-35


schema
======

Is a data type representation of your API response which is necessary if you
would like to validate your incoming data. Look at `schema documentation
<https://github.com/keleshev/schema>`_ and examples in :doc:`usage` to define
your own schema.
