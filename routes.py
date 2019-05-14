from flask import Flask, request, jsonify
import pymongo
import uuid

app = Flask(__name__)

# Connect to the database
restaurants = None


# Database URL
db_url = 'localhost:27017'

    # Make a connection to the database.
try:
    connection = pymongo.MongoClient(db_url)
    database = connection.menus
    restaurants = database.restaurants

    print('Connection to the database successful.')

except Exception as ex:
    print('The database server might not be running. Please check!')
    print(ex)

# Check the DB connection
@app.route('/') 
def check_connection():
    return 'Hi'

# Read all the menus
@app.route('/all')
def view_all_menus():
    menus = restaurants.find()
    
    # menus = menus['menu']
    menus = [menu['name'] for menu in menus]

    # Check if menu items exist.
    if(len(menus) == 0):
        return_status = 201
        return_message = 'No items found. Start by adding a restaurant.'

        response = {
            'status' : return_status,
            'data' : return_message,
        }

        print(response)
        return jsonify(response)

    return_status = 201

    response = {
        'status' : return_status,
        'data' : menus,
    }

    return jsonify(response)

# Add a new restaurant
@app.route('/new/<string:new_type>/', methods = ['GET', 'POST'])
def add_new_item(new_type):
    if(new_type == 'restaurant'):
        restaurant_name= request.form['restaurant_name']
        try:
            insert = {
                'name': restaurant_name,
                'menu': [],
            }

            restaurants.insert_one(insert)
            print('restaurant added to the collection.')
            
            return_status = 201
            
            response = {
                'status' : return_status,
                'data' : 'Restaurant has been successfully added'
            }

            return response

        except Exception as ex:
            print(ex)
            
            return_status = 403
            response = {
                'status' : return_status,
                'error' : ex
            }
            return response

    else:

        return_status = 303

        response = {
            'status' : return_status,
            'data' : 'No data to be inserted', 
        }

        return response

# Add a new item to a particular restaurant
@app.route('/add/<restaurant_id>/')
def add_menu_item(restaurant_id):

    item_name = request.form['item_name']
    item_price = request.form['item_price']
    item_description = request.form['item_description']
    item_category = request.form['item_category']

    # Generate a temporary UUID for 'UD' operations.
     
    item_uuid = uuid.uuid4()

    find = {'_id': restaurant_id}
    
    item = {
        'item_uuid' : item_uuid,
        'item_name' : item_name,
        'item_price' : item_price,
        'item_description' : item_description,
        'item_category' : item_category,
    }

    update = {
        # Push the new item to the menu array
        # Collection restaurants
        "$push": {
            'menu' : item,
        }
    }

    try:
        restaurant_name = restaurants.find_one({find})

        restaurants.update_one(find, update)

        return_status = 201

        return_message = 'New menu item has added to ' + restaurant_name

        response = {
            'status' : return_status,
            'data' : return_message,
        }

        return jsonify(response)
    
    except Exception as ex:
        print(ex)
        return_status = 403

        return_message = 'Error occurred while adding menu item'

        response = {
            'status' : return_status,
            'data' : return_message,
        }

        return jsonify(response)

# Delete a restaurant, or a menu item
@app.route('/remove/<restaurant_id>/<string:type_of>/')
def remove_element(type_of, restaurant_id):
    if(type_of == 'restaurant'):
        try:
            # Delete the entity
            # restaurants.
            delete = {
                '_id' : restaurant_id,
            }
        
            restaurants.delete_one(delete)

            return_status = 201

            response = {
                'status' : return_status,
                'data' : 'Restaurant has been deleted.',
            }

            return jsonify(response)
        # Return a response
        
        except Exception as ex:
            print(ex)

            return_status = 403

            response = {
                'status' : return_status,
                'data' : ex,
            }
            return jsonify(response)
    else:
        # Add logic to delete a menu item from a restaurant
        item_uuid = request.form['item_uuid']

        try:
            find = {
                '_id' : restaurant_id,
            }
            
            restaurant = restaurants.find_one(find)

            item_list = restaurant['menu']

            updated_item_list = filter(lambda x: x['item_uuid'] != item_uuid, item_list)

            print(updated_item_list)

            # Try updating the menu of the restaurant.
            try:

                update = {
                    "$push" : {
                        'menu': updated_item_list,
                    },
                }

                restaurants.update_one(find, update)
            
                
                return_status = 201

                response = {
                    'status' : return_status,
                    'data' : 'Menu has been updated',
                }

                return jsonify(response)

            # Updation failed.
            except Exception as ex:
                
                return_status =404

                response = {
                    'status' : return_status,
                    'data' : ex,
                }

                return jsonify(response)

        # Finding the restaurant failed.
        except Exception as ex:

            return_status = 404

            response = {
                'status' : return_status,
                'data' : ex,
            }

            return jsonify(response)

@app.route('/update/<restaurant_id>/<string:type_of>/')
def update_entry(type_of, restaurant_id):
    if(type_of == 'restaurant'):
        new_name = request.form['new_name']
        find = {
            '_id' : restaurant_id,
        }

        try:
            # restaurant = restaurants.find_one(find)

            update = {
                'name' : new_name,
            }

            try:

                restaurants.update_one(find, update)

                return_status = 201

                response = {
                    'status' : return_status,
                    'data' : 'Restaurant information has been updated.'
                }

                return jsonify(response)
            except Exception as ex:
                
                return_status = 404

                response = {
                    'status' : return_status,
                    'data' : ex,
                }

                return jsonify(response)

        except Exception as ex:
            
            return_status = 404

            response = {
                'status' : return_status,
                'data' : ex,
            }
    
            return jsonify(response)

    else:
        # Write logic to implement the updation of the menu item
        pass


@app.route('/item/<item_uuid>')
def find_menu_item(item_uuid):
    # Write logic to find a particular menu item based on the item_uuid
    pass

@app.route('/menu/<restaurant_id>')
def show_menu_of_restaurant(restaurant_id):
    # Write logic to find the menu of a particular restaurant based on the restaurant_id
    pass

if( __name__ == "__main__"):

    # Run the application
    app.debug = True
    app.run('0.0.0.0', port = 5000)
    
