class Note(ndb.Model):
    emailTo = ndb.StringProperty(required=True)
    emailFrom = ndb.StringProperty(required=True)
    dateTime = ndb.DateTimeProperty(required=True)
    subject = ndb.StringProperty()
    text = ndb.TextProperty(required=True)

    @classmethod
    def new(cls, data):
        required = _get_required(cls)
        for r in required:
            if r not in data:
                raise BadValueError('Property %s is required' % r)

        # TODO: use required as params instead of hardcoding
        team = cls(emailTo='PlaceHolder', emailFrom='PlaceHolder', dateTime=dt.datetime.now(), text='PlaceHolder')
        for k in data:
            setattr(team, k, data[k])
        return team

    @classmethod
    def new2(cls, mEmailTo, mEmailFrom, mDateTime, mSubject, mText):
        return cls(emailTo=mEmailTo, emailFrom=mEmailFrom, dateTime=mDateTime, subject=mSubject, text=mText)

