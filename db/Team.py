class Team(ndb.Model):
    name = ndb.StringProperty(required=True)
    teamMembers = ndb.StructuredProperty(Attendee, repeated=True)

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(name='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def unique_properties(cls):
        return ['name']

    @classmethod
    def new2(cls, mName):
        return cls(name=mName)

    def addMember(self, person):
        if type(person) == Attendee:
            self.teamMembers.append(person)
            person.team = self.key
            self.put()
            person.put()
        return type(person) == Attendee
