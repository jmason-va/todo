import os
import urllib

import jinja2
import webapp2
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Entry(ndb.Model):
    content = ndb.StringProperty()

    @classmethod
    def build_key(cls, content):
        return ndb.Key(cls, content)    # builds a key from the content

    @classmethod
    def create_entry(cls, content):
        key = cls.build_key(content)
        entry = key.get()               # if there is an entry in the database get it
        if entry is not None:           # make sure that there isnt existing data
            raise ValueError("A MyModel with that unique_id already exists.")
        new_entry = cls(key=key, content=content)       # create a new entry with the key and properties
        new_entry.put()                                 # put the entry in the database
        return new_entry                                # return the new entry in case they want to set it to something


class MainPage(webapp2.RequestHandler):
    def get(self):
        entry_list = Entry.query().fetch(10)
        template_values = {
            'entry_list': entry_list
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class AddEntry(webapp2.RequestHandler):
    def post(self):
        content = self.request.get('todo_entry')
        Entry.create_entry(content)
        self.redirect('/?')


class DeleteEntry(webapp2.RequestHandler):
    def post(self):
        entry_content = self.request.get('entry_to_delete')
        entry_to_delete = Entry.build_key(entry_content)
        entry_to_delete.delete()
        self.redirect('/?')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_entry', AddEntry),
    ('/delete_entry', DeleteEntry)
], debug=True)
