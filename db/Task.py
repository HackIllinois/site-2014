class Task(ndb.Model):
    jobFunction = ndb.StringProperty(required=True)
    gsObjectName = ndb.StringProperty()
    complete = ndb.BooleanProperty(default=False)
    data = nbd.JsonProperty()
    creationTime = ndb.DateTimeProperty()
    errorMessages = ndb.TextProperty()

    @classmethod
    def new(cls, data):
        attendee = cls()
        for k in data:
            setattr(task, k, data[k])
        return task