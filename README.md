Decorators notes
================

1. Use common function-based decorators to decorate functions.
2. Use class-based decorators with `__call__` defined to decorate functions and keep state in the decorator.
3. Use class-based decorators with `__get__` defined (non-data descriptors) to decorate class methods.


References:
-----------

* [Descriptor HowTo Guide](https://docs.python.org/2/howto/descriptor.html)
* [Python descriptors made simple](https://www.smallsurething.com/python-descriptors-made-simple/)
* [Python FAQ: Descriptors](https://eev.ee/blog/2012/05/23/python-faq-descriptors/)
* [Understanding Django's cached_property Decorator](http://ericplumb.com/blog/understanding-djangos-cached_property-decorator.html)
