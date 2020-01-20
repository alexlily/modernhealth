#!/usr/bin/env python
import json

class ModelObject(json.JSONEncoder):
    def __repr__(self):
        return str(self.__dict__)
    def serialize(self):
        dictionary = self.__dict__
        for key in dictionary:
            if issubclass(type(dictionary[key]), ModelObject):
                dictionary[key] = dictionary[key].__dict__
            if type(dictionary[key]) == list and issubclass(type(dictionary[key][0]), ModelObject):
                dictionary[key] = [v.__dict__ for v in dictionary[key]]
        return dictionary

class Program(ModelObject):

    def __init__(self, dbresulttuple):
        self.id, self.name, self.description = dbresulttuple    

class Section(ModelObject):

    def __init__(self, dbresulttuple, hostname):
        self.id, self.program_id, self.name, self.description, self.orderIndex, imageId = dbresulttuple
        self.imageUrl = "{}api/v1/image/{}".format(hostname, imageId.strip('\"'))

class Activity(ModelObject):

    def __init__(self, dbresulttuple):
        self.id, self.section_id, self.staticContent, self.question_text, self.answers = dbresulttuple
        if self.staticContent == None and self.question_text != None:
            self.type = "MULTIPLE_CHOICE"
        else:
            self.type = "STATIC"

