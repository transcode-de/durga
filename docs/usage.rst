*****
Usage
*****

Flickr example
==============

To use Durga in a project define a ``class`` that extends
:py:class:`durga.Resource <durga.resource.Resource>`. This example uses the
Flickr API `flickr.photos.search
<https://www.flickr.com/services/api/flickr.photos.search.htm>`_ with Python 3:

.. literalinclude:: ../tests/test_flickr.py
   :linenos:
   :lines: 7, 11-35

.. note::

    For convenience :py:class:`durga.Resource <durga.resource.Resource>`. and
    the `schema library <https://github.com/keleshev/schema>`_ are available at
    the top module level.

Now you can search for the first 10 cat images::

    cats = FlickrResource().collection.filter(text='Cat', per_page=10)

This will return a :py:class:`durga.Collection <durga.collection.Collection>`
with a :py:class:`durga.Element <durga.element.Element>` for each result.

MusicBrainz example
===================

`Musicbrainz <http://musicbrainz.org/>`_ is an open music encyclopedia that
collects music metadata and makes it available to the public. With `Artist
<http://wiki.musicbrainz.org/Development/JSON_Web_Service#Artist>`_ you get
detailed entry for a single artist.

.. literalinclude:: ../tests/test_musicbrainz.py
   :linenos:
   :lines: 4-5, 9-11, 16-69

.. note::

    In the example above you can see a more complex usage of validation.

    For example to validate UUIDs:

    .. literalinclude:: ../tests/test_musicbrainz.py
       :language: python
       :dedent: 12
       :lines: 29

    For example to validate date:

    .. literalinclude:: ../tests/test_musicbrainz.py
       :language: python
       :dedent: 12
       :lines: 38

Now let's use the MusicBrainzResource::

    MusicBrainzResource().collection.get(id='05cbaf37-6dc2-4f71-a0ce-d633447d90c3').name

That returns name of artist with given id::

    '東方神起'

