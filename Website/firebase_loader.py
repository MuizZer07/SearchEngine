import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class firebase_loader():

    # def firework(self, data):
    #     new_entry = self.ref.push(data)
    
    #     print("Pushed to database...")
        
    def initiate(self):
        self.cred = credentials.Certificate('serviceKey.json')
        self.default_app = firebase_admin.initialize_app(self.cred, {
            'databaseURL' : 'https://search-9a5cb.firebaseio.com/'
        })

        # Get a database reference to our posts
        self.ref = db.reference()

    # Read the data at the posts reference (this is a blocking operation)
    # print(ref.get())
    # var  = ref.get()
    # var = ref.child('asin').get()
    # print(var)
    # for item in var:
    #     print(item['asin'],' ---- \n')



    # from firebase_admin import db

    # root = db.reference()
    # # Add a new user under /users.
    # new_user = root.child('users').push({
    #     'name' : 'Mary Anning', 
    #     'since' : 1700
    # })

    # # Update a child attribute of the new user.
    # new_user.update({'since' : 1799})

    # # Obtain a new reference to the user, and retrieve child data.
    # # Result will be made available as a Python dict.
    # mary = db.reference('users/{0}'.format(new_user.key)).get()
    # print 'Name:', mary['name']
    # print 'Since:', mary['since']