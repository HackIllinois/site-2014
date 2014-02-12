from google.appengine.ext import ndb
from Event import Event
# import logging

class Model(ndb.Model):
    _automaticallyAddEventAsAncestor = False

    @classmethod
    def _automatically_add_event_as_ancestor(cls):
        cls._automaticallyAddEventAsAncestor = True

    def _get_required(cls):
        '''
        private method for getting a list of all required properties of a class
        '''
        properties = cls._properties
        required = []
        for p in properties:
            if properties[p]._required:
                required.append(p)
        return required

    @classmethod
    @ndb.transactional
    def f_add(cls, data, search = {}, parent=None):
        '''
        Creates a model and adds it to the database
        WILL NOT override data if already there

        @param cls: the class model to use
        @param data: the data to add in the database
        @param search: properties to search the database
        @return: whether or not the data was added to the database

        ex: add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3})
        Returns True if "doe1@illinois.edu" is not already in the database and data is successfully added
        Returns False otherwise
        OR
        add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3}, {'email':'doe1@illinois.edu'})
        Same result
        '''

        o = cls(parent=parent)
        # logging.info("Model: f_add object is none: " + str(o == None))
        for prop in data:
            setattr(o, prop, data[prop])

        ret = o.put()
        # logging.info("Model: f_add put returned " + str(ret))

        return o

    @staticmethod
    def get_default_event_parent_key():
        q = Event.query()
        if q.count() < 1:
            event = Event(name='HackIllinois')
            return event.put()
        else:
            return q.fetch()[0].key

    @classmethod
    def add(cls, data, search={}, parent=None):
        '''
        Creates a model and adds it to the database
        WILL NOT override data if already there
        WILL NOT add data if similar data is already there, determined by "search" or model's unique_properties() attribute

        @param cls: the class model to use
        @param data: the data to add in the database
        @param search: properties to search the database
        @return: whether or not the data was added to the database

        ex: add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3})
        Returns True if "doe1@illinois.edu" is not already in the database and data is successfully added
        Returns False otherwise
        OR
        add(Attendee, {'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3}, {'email':'doe1@illinois.edu'})
        Same result
        '''
        # logging.info("Model: Begining")
        # logging.info("Model: cls=" + str(cls))
        # logging.info("Model: data=" + str(data))
        # logging.info("Model: search=" + str(search))
        # logging.info("Model: parent=" + str(parent))

        if cls._automaticallyAddEventAsAncestor:
            parent = cls.get_default_event_parent_key()

        # logging.info("Model: before search")

        if(search == {}):
            try:
                properties = cls.unique_properties()
                for p in properties:
                    search[p] = data[p]
            except AttributeError:
                # logging.info("Model: AttributeError")
                #class does not have attribute unique_properties()
                return cls.f_add(data, parent=parent)
            except LookupError:
                #data does not key "p"
                # logging.info("Model: LookupError")
                return False
        # logging.info("Model: before in database")
        if not cls.in_database(search):
            # logging.info("Model: not in database")
            return cls.f_add(data, parent=parent)
        return False

    @classmethod
    def delete_search(cls, search):
        '''
        deletes a model in the database

        @param cls: the class model to use
        @param search: the parameters to search with
        @return: nothing

        ex: update_model(Attendee, {'email':'doe1@illinois.edu', 'year':3})
        '''
        #These functions need to be changed to delete all references a model ex. an Attendee in a Team
        m = cls.search_database(search).get()
        if m != None:
            cls.delete(m.key)

    @classmethod
    @ndb.transactional
    def delete(cls, key):
        '''
        deletes a model in the database

        @param cls: the class model to use
        @param key: key to delete
        @return: nothing

        ex: update_model(Attendee, key)
        '''
        #These functions need to be changed to delete all references a model ex. an Attendee in a Team
        key.delete()

    @classmethod
    def update_search(cls, data, search = {}):
        '''
        Updates a model in the database
        WILL override data if already there

        @param cls: the class model to use
        @param data: the data to change in the database
        @param search: the parameters to search with
        @return: whether or not the data was found in the database and updated

        ex: update_model(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'year':3})
        '''
        if(search == {}):
            try:
                properties = cls.unique_properties()
                for p in properties:
                    search[p] = data[p]
            except AttributeError:
                #class does not have attribute unique_properties()
                return False
            except LookupError:
                #data does not key "p"
                return False
        m = cls.search_database(search).get()
        if m != None:
            return cls.update(data, m.key)
        return False

    @classmethod
    @ndb.transactional
    def update(cls, data, key):
        '''
        Updates a model in the database
        WILL override data if already there

        @param cls: the class model to use
        @param data: the data to change in the database
        @param key: key of model
        @return: whether or not the data was updated

        ex: update_model(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, key)
        '''
        u = key.get()
        for p in data:
            setattr(u, p, data[p])
        u.put()
        return u

    @classmethod
    def add_or_update(cls, data, search = {}):
        '''
        Adds or updates a model in the database
        WILL override data if already there

        @param cls: the class model to use
        @param data: the data to change in the database
        @param search: the parameters to search with
        @return: nothing

        ex: update_model(Attendee, {'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'year':3})
        '''
        if not cls.add(data, search):
            cls.update(data, search)

    @classmethod
    def in_database(cls, search):
        '''
        Determines if the data already in the database, determined by "search"
        DOES NOT effect the database

        @param cls: the class model to use
        @param search: the data used to search the database
        @return: True if the data is in the database, False otherwise

        ex: in_database(Attendee, {'email':'doe1@illinois.edu'})
        Returns True if "doe1@illinois.edu" is already in the database
        Returns False otherwise
        '''
        s = cls.search_database(search).get()
        if s != None and (isinstance(s, list) and len(s) > 0) and s[0] != None:
            return True
        return False

    @classmethod
    def search_database(cls, search, perfect_match=True):
        '''
        Searches the database for models matching "search"
        DOES NOT effect the database

        @param cls: the class model to use
        @param search: the data used to search the database
        @perfect_match: True = every argument matches : False = one argument matches
        @return: iterator of models

        ex: search_database(Attendee, {'email':'doe1@illinois.edu'})
        '''
        if search == {}:
            return cls.gql("")
        q = "WHERE "
        if perfect_match:
            ao = " AND "
        else:
            ao = " OR "
        for param in search:
            if type(search[param]) is str:
                q += param + " = '" + search[param] + "'" + ao
            else:
                q += param + " = " + str(search[param]) + ao
            # q += param + " = '" + search[param] + "'" + ao

        q = q[:-len(ao)]
        # This is terrible terrible code. We can fix by moving off GQL :P
        if cls._automaticallyAddEventAsAncestor:
            q += " AND ANCESTOR IS :1"
            return cls.gql(q, cls.get_default_event_parent_key())
        else:
            #untested
            return ndb.transactional(lambda: cls.gql(q))



