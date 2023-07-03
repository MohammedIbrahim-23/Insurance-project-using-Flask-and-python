from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='day1',
    user='postgres',
    password='#86089070j'
)
cursor = conn.cursor()

# GET /vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    query = "SELECT * FROM vehiche"
    cursor.execute(query)
    vehicles = cursor.fetchall()
    vehicles_data = []
    for vehicle in vehicles:
        vehicle_data = {
            'id': vehicle[0],
            'bikename': vehicle[1],
            'bike_number': vehicle[2],
            'bike_color': vehicle[3]
        }
        vehicles_data.append(vehicle_data)
    return jsonify(vehicles_data)

@app.route('/vehicles_chases', methods=['GET'])
def get_vehicles():
    query = "SELECT * FROM bike_model"
    cursor.execute(query)
    vehicles = cursor.fetchall()
    vehicles_data = []
    for vehicle in vehicles:
        vehicle_data = {
            'id': vehicle[0],
            'bike_model': vehicle[1],
            'chase_no': vehicle[2]
        }
        vehicles_data.append(vehicle_data)
    return jsonify(vehicles_data)


# GET /vehicles/<id>
@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    query = "SELECT * FROM vehiche WHERE id = %s"
    cursor.execute(query, (id,))
    vehicle = cursor.fetchone()
    if vehicle:
        vehicle_data = {
            'id': vehicle[0],
            'bikename': vehicle[1],
            'bike_number': vehicle[2],
            'bike_color': vehicle[3]
        }
        return jsonify(vehicle_data)
    else:
        return jsonify({'message': 'Vehicle not found'})

# POST /vehicles
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    vehicle = request.get_json()
    bikename = vehicle.get('bikename')
    bike_number = vehicle.get('bike_number')
    bike_color = vehicle.get('bike_color')

    query = "INSERT INTO vehicle (bikename, bike_number, bike_color) VALUES (%s, %s, %s) RETURNING id"
    values = (bikename, bike_number, bike_color)
    cursor.execute(query, values)
    new_vehicle_id = cursor.fetchone()[0]
    conn.commit()
    return jsonify({'id': new_vehicle_id, 'message': 'Vehicle added successfully'})

# PUT /vehicles/<id>
@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    vehicle = request.get_json()
    bikename = vehicle.get('bikename')
    bike_number = vehicle.get('bike_number')
    bike_color = vehicle.get('bike_color')

    query = "UPDATE vehicle SET bikename = %s, bike_number = %s, bike_color = %s WHERE id = %s"
    values = (bikename, bike_number, bike_color, id)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'message': 'Vehicle updated successfully'})

# DELETE /vehicles/<id>
@app.route('/vehicles/<int:id>', methods=['DELETE'])
def remove_vehicle(id):
    query = "DELETE FROM vehicle WHERE id = %s"
    value = (id,)
    cursor.execute(query, value)
    conn.commit()
    return jsonify({'message': 'Vehicle removed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
