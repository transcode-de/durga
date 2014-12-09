*****
Usage
*****

To use Durga in a project define a ``class`` that extends
:py:class:`durga.resource.Resource`. This example uses the Flickr API
`flickr.photos.search <https://www.flickr.com/services/api/flickr.photos.search.htm>`_:

.. literalinclude:: ../tests/test_flickr.py
   :linenos:
   :lines: 7, 11-34

.. note::

    For convenience :py:class:`durga.resource.Resource` and the `schema
    library <https://github.com/keleshev/schema>`_ are available at the
    top module level.

Now you can search for the first 10 cat images::

    FlickrResource().collection.filter(text='Cat', per_page=10)

This will return a :py:class:`durga.collection.Collection` with a
:py:class:`durga.element.Element` for each result.
