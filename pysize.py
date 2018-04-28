import sys
from inspect import isgetsetdescriptor, ismemberdescriptor
from collections import Iterable, Mapping


DICT = '__dict__'
SLOTS = '__slots__'


def get_size(obj):
    """
    Iteratively computes the size of Python objects in bytes.

    :param obj:
    :return:
    """

    size, queue, seen = 0, [obj], set()

    while queue:
        obj = queue.pop()
        cls = obj.__class__
        obj_id = id(obj)

        if obj_id not in seen:
            size += sys.getsizeof(obj)
            seen.add(obj_id)

            if DICT in cls.__dict__:
                for cls_0 in cls.__mro__:
                    if DICT in cls_0.__dict__:
                        d = cls_0.__dict__['__dict__']

                        if (isgetsetdescriptor(d)
                                or ismemberdescriptor(d)):
                            queue.append(obj.__dict__)
                            queue.extend(obj.__dict__.keys())
                            queue.extend(obj.__dict__.values())

                        break

            elif SLOTS in cls.__dict__:
                if issubclass(cls, tuple):
                    if isinstance(obj, Iterable):
                        queue.extend(obj)

                else:
                    for cls_0 in cls.__mro__:
                        if hasattr(cls_0, '__slots__'):
                            queue.append(cls_0.__slots__)

                            if isinstance(cls_0.__slots__, str):
                                queue.append(getattr(obj, cls_0.__slots__))

                            else:
                                for attr in cls_0.__slots__:
                                    d = getattr(cls_0, attr)

                                    if (isgetsetdescriptor(d)
                                            or ismemberdescriptor(d)):
                                        queue.append(getattr(obj, attr))

            else:
                if isinstance(obj, Mapping):
                    queue.extend(obj.values())
                    queue.extend(obj.keys())

                elif (isinstance(obj, Iterable)
                        and not isinstance(obj, (bytes, bytearray, str))):
                    queue.extend(obj)

    return size
