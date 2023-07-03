from flask import Flask,request,jsonify
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
print('connected')
# create_query = '''
#         CREATE TABLE IF NOT EXISTS vehiche (
#             bikename VARCHAR(100),
#             bike_number INT
#         )
#     '''
# cursor.execute(create_query)
    
# conn.commit()
# print("created")

# GET /students
@app.route('/vehichees', methods=['GET'])
def vehicles_details():
    query = "SELECT bikename, bike_number,bike_color,bike_model,chase_no FROM vehiche join bike_model on vehiche.id=bike_model.id"
    cursor.execute(query)
    rows = cursor.fetchall()
    bikes = []
    for row in rows:
        bikename, bike_number,bike_color,bike_model,chase_no = row
        student = {'bikename': bikename, 'bike_number': bike_number,'bike_color':bike_color,'bike_model':bike_model,'chase_no':chase_no}
        bikes.append(student)
    return jsonify(bikes)

@app.route('/vehiche_details', methods=['GET'])
def vehicle_bikemodel():
    query = "SELECT * FROM bike_model"
    cursor.execute(query)
    rows = cursor.fetchall()
    bikes = []
    for row in rows:
        id,bike_model,chase_no = row
        student = {'id':id,'bike_model':bike_model,'chase_no':chase_no}
        bikes.append(student)
    return jsonify(bikes)

# # GET /students
# @app.route('/vehichenone', methods=['GET'])
# def get_all_students():
#     query = "SELECT bikename, bike_number,bike_color FROM vehiche "
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     bikes = []
#     for row in rows:
#         bikename, bike_number,bike_color = row
#         student = {'bikename': bikename, 'bike_number': bike_number,'bike_color':bike_color}
#         bikes.append(student)
#     return jsonify(bikes)


# GET /students/<roll_number>
@app.route('/vehicheid/<int:id>', methods=['GET'])
def get_student(id):
    query = "SELECT bikename, bike_number,bike_color,bike_model,chase_no FROM vehiche inner join bike_model on vehiche.id=bike_model.id WHERE chase_no = %s"
    value = (id,)
    cursor.execute(query, value)
    row = cursor.fetchone()
    if row:
        bikename, bike_number,bike_color,bike_model,chase_no = row
        bikes =  {'bikename': bikename, 'bike_number': bike_number,'bike_color':bike_color,'bike_model':bike_model,'chase_no':chase_no}
        return jsonify(bikes)
    return jsonify({'message': 'Student not found'})

# POST /students
@app.route('/vehiche', methods=['POST'])
def add_student():
    student = request.get_json()
    bikename = student.get('bikename')
    bike_number = student.get('bike_number')
    bike_color = student.get('bike_color')
    # bike_model = student.get('bike_model')
    # chase_no = student.get('chase_no')
    query = "INSERT INTO vehiche (bikename, bike_number,bike_color) VALUES (%s, %s,%s)"
    # query1 = "INSERT INTO bike_model (bike_model,chase_no) VALUES (%s,%s)"
    values = (bikename, bike_number,bike_color)
    # values1=(bike_model,chase_no)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'message': 'Student added successfully'})


# POST /students
@app.route('/bike_model', methods=['POST'])
def add_bike_model():
    student = request.get_json()
    bike_model = student.get('bike_model')
    chase_no = student.get('chase_no')

    query = "INSERT INTO bike_model (bike_model, chase_no) VALUES (%s, %s)"
    values = (bike_model, chase_no)

    cursor.execute(query, values)
    conn.commit()
    return jsonify({'message': 'Added successfully'})


# # PUT /students/<roll_number>
# @app.route('/vehiche/<int:id>', methods=['PUT'])
# def update_student(id):
#     bike = request.get_json()
#     bikename = bike.get('bikename')
#     bike_number = bike.get('bike_number')
#     bike_color = bike.get('bike_color')
#     query = "UPDATE vehiche SET bikename = %s,bike_number=%s,bike_color=%s WHERE id = %s"
#     values = (bikename,bike_number,bike_color,id)
#     cursor.execute(query, values)
#     conn.commit()
#     return jsonify({'message': 'Student updated successfully'})

@app.route('/vehicle_update/<int:id>', methods=['PUT'])
def update_vehicle(id):
    bike = request.get_json()
    id = bike.get('id')
    bikename = bike.get('bikename')
    bike_number = bike.get('bike_number')
    bike_color = bike.get('bike_color')

    try:
        # Update the vehicle table
        vehicle_query = "UPDATE vehiche SET id=%s , bikename = %s, bike_number = %s, bike_color = %s WHERE id = %s"
        vehicle_values = (id,bikename, bike_number, bike_color, id)
        cursor.execute(vehicle_query, vehicle_values)
        conn.commit()
        return jsonify({'message': 'Vehicle updated successfully'})
    except Exception as e:
        # Handle any exceptions that may occur
        conn.rollback()
        return jsonify({'error': str(e)})

# @app.route('#a/<int:chase_no>', methods=['PUT'])
# def update_vehicle(chase_no):
#     bike = request.get_json()
#     new_id = bike.get('id')
#     bike_model = bike.get('bike_model')
#     # chase_no = bike.get('chase_no')

#     try:
#         # Update the bike_model table
#         vehicle_query = "UPDATE bike_model SET id = %s, bike_model = %s WHERE chase_no = %s"
#         vehicle_values = (new_id, bike_model, chase_no, chase_no)
#         cursor.execute(vehicle_query, vehicle_values)
#         conn.commit()
#         return jsonify({'message': 'Vehicle updated successfully'})
#     except Exception as e:
#         # Handle any exceptions that may occur
#         conn.rollback()
#         return jsonify({'error': str(e)}), 500



# DELETE /students/<roll_number>
@app.route('/vehiche_del/<int:id>', methods=['DELETE'])
def remove_vehicle(id):
    try:
        query = "DELETE FROM vehiche WHERE id = %s"
        value = (id,)
        cursor.execute(query, value)
        conn.commit()
        return jsonify({'message': 'Vehicle removed successfully'})
    except Exception as e:
        # conn.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE /students/<roll_number>
@app.route('/vehiche_bike/<int:chase_no>', methods=['DELETE'])
def remove_bike(chase_no):
    try:
        query = "DELETE FROM bike_model WHERE chase_no = %s"
        value = (chase_no,)
        cursor.execute(query, value)
        conn.commit()
        return jsonify({'message': 'Bike model removed successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)