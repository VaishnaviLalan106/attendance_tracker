from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Data storage file
DATA_FILE = 'attendance_data.json'

def load_data():
    """Load attendance data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'students': [], 'attendance': []}
    return {'students': [], 'attendance': []}

def save_data(data):
    """Save attendance data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    """Landing page"""
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    """Dashboard page"""
    data = load_data()
    return render_template("dashboard.html", students=data['students'])

@app.route("/api/students", methods=['GET', 'POST'])
def manage_students():
    """Get all students or add a new student"""
    data = load_data()
    
    if request.method == 'POST':
        student_data = request.json
        new_student = {
            'id': len(data['students']) + 1,
            'name': student_data.get('name'),
            'roll_number': student_data.get('roll_number'),
            'class': student_data.get('class'),
            'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['students'].append(new_student)
        save_data(data)
        return jsonify({'success': True, 'student': new_student}), 201
    
    return jsonify(data['students']), 200

@app.route("/api/attendance", methods=['GET', 'POST'])
def manage_attendance():
    """Record or get attendance"""
    data = load_data()
    
    if request.method == 'POST':
        attendance_data = request.json
        new_record = {
            'id': len(data['attendance']) + 1,
            'student_id': attendance_data.get('student_id'),
            'date': attendance_data.get('date'),
            'status': attendance_data.get('status'),  # 'present' or 'absent'
            'recorded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['attendance'].append(new_record)
        save_data(data)
        return jsonify({'success': True, 'record': new_record}), 201
    
    return jsonify(data['attendance']), 200

@app.route("/api/statistics", methods=['GET'])
def get_statistics():
    """Get attendance statistics"""
    data = load_data()
    total_students = len(data['students'])
    total_records = len(data['attendance'])
    
    present_count = sum(1 for rec in data['attendance'] if rec['status'] == 'present')
    absent_count = sum(1 for rec in data['attendance'] if rec['status'] == 'absent')
    
    return jsonify({
        'total_students': total_students,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
