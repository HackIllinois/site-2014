class Sponsor(ndb.Model):
    companyName = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    levelOfSponsorship = ndb.IntegerProperty()
    notes = ndb.StructuredProperty(Note, repeated=True)

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(companyName='PlaceHolder', email='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mCompanyName, mContactName, mEmail):
        return cls(companyName=mCompanyName, contactName=mContactName, email=mEmail)

    def addNote(self, note):
        if type(note) == Note:
            self.notes.append(note)
            self.put()
        return type(note) == Note
