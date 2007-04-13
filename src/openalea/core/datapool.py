# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""
DataPool is a global dictionnary to share data between node instance
"""


from singleton import Singleton
from observer import Observed



# Decorator to add notification to function
def notify_decorator(f):
    
    def wrapped(self, *args, **kargs):
        ret = f(self, *args, **kargs)
        self.notify_listeners(('pool_modified',))
        return ret
    wrapped.__doc__ = f.__doc__

    return wrapped


class DataPool(Observed, dict):
    """ Dictionnary of session data """

    __metaclass__ = Singleton


    def __init__(self):

        Observed.__init__(self)
        dict.__init__(self)
        
        DataPool.__setitem__ = notify_decorator(dict.__setitem__)
        DataPool.__delitem__ = notify_decorator(dict.__delitem__)
        DataPool.clear = notify_decorator(dict.clear)

        
        
    def add_data(self, key, instance):
        """ Add an instance referenced by key to the data pool """

        self[key] = instance
        self.notify_listeners(('pool_modified',))

    def remove_data(self, key):
        """ Remove the instance identified by key """

        try:
            del(self[key])
            self.notify_listeners(('pool_modified',))
        except:
            pass

