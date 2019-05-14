import pymongo

class Worker:
    def __init__(self):

        # Database URL
        db_url = 'localhost:27017'

        # Make a connection to the database.
        try:
            connection = pymongo.MongoClient(db_url)
            database = connection.menus
            self.restaurants = database.restaurants

            print('Connection to the database successful.')

        except Exception as ex:
            print('The database server might not be running. Please check!')
            print(ex)

    def find_all_restaurant(self):
        restaurant_list = self.restaurants.find()

        names = [menu['name'] for menu in restaurant_list]

        # Check if menu items exist.
        if(len(names) == 0):
            return_status = 201
            return_message = 'No items found. Start by adding a restaurant.'

            response = {
                'status' : return_status,
                'data' : return_message,
            }

            print(response)
            return (response)

        return_status = 201

        response = {
            'status' : return_status,
            'data' : names,
        }

        return (response)

    def add_new_restaurant(self, restaurant_name):
        try:
            insert = {
                'name': restaurant_name,
                'menu': [],
            }

            self.restaurants.insert_one(insert)
            print('restaurant added to the collection.')
            
            return_status = 201
            
            response = {
                'status' : return_status,
                'data' : 'Restaurant has been successfully added'
            }

            return (response)

        except Exception as ex:
            print(ex)
            
            return_status = 403
            response = {
                'status' : return_status,
                'error' : ex
            }
            return (response)