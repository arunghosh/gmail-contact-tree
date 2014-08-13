__author__ = 'lenovo'
from .models import LnContact

class ImportAll:

    def __init__(self, response, user):
        self.response = response
        self.user = user

    def execute(self):
        print self.response
        for c in self.response['values']:
            ln = LnContact()
            ln.ln_id = c['id']
            if ln.ln_id != "private":
                ln.profile_url = c.get('publicProfileUrl', '')
                ln.headline = c.get('headline', '')
                ln.name = c['firstName'] + ' ' + c['lastName']
                ln.image_url = c.get('pictureUrl', '')
                ln.user = self.user
                ln.save()



