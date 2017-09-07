def unicodify(ss):
    """Returns a utf-8 encoded version of a collection of strings."""
    if type(ss) is list:
        try:
            return [ unicode(s,"utf-8") for s in ss ]
        except Exception as e:
            raise ValueError("Unicodify failed on type list", ss, e)

    elif type(ss) is dict:
        try:
            return { unicode(k,"utf-8"):unicodify(ss[k]) for k in ss }
        except Exception as e:
            raise ValueError("Unicodify failed on type dict", ss, e)

    elif isinstance(ss, basestring):
        try:
            return unicode(s, "utf-8")
        except Exception as e:
            raise ValueError("Unicodify failed on type basestring", ss, e)
