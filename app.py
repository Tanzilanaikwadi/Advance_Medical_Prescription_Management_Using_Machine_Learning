from flask import Flask, render_template, request, redirect, url_for,flash,session,jsonify,send_file,session
import mysql.connector
import os
import re
import MySQLdb
from datetime import datetime
import joblib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF
import io
from werkzeug.utils import secure_filename
import string
import random
import uuid  # Add this at the top of your app
from textblob import TextBlob
app = Flask(__name__)

# Define separate upload folders
DOCTOR_UPLOAD_FOLDER = 'static/doctor_documents'
PATIENT_UPLOAD_FOLDER = 'static/patient_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg'}

UPLOAD_FOLDER = 'static/uploads/'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')



app.config['PATIENT_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'patient_images')
upload_folder = app.config['PATIENT_UPLOAD_FOLDER']
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = '1236'   

app.config['DOCTOR_UPLOAD_FOLDER'] = DOCTOR_UPLOAD_FOLDER
app.config['PATIENT_UPLOAD_FOLDER'] = PATIENT_UPLOAD_FOLDER

EMERGENCY_IMAGE_DIR = 'static/emergency_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg'}


# Create the folder if it doesn't exist
os.makedirs(EMERGENCY_IMAGE_DIR, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create the folder if it doesn't exist
os.makedirs(EMERGENCY_IMAGE_DIR, exist_ok=True)

# Default admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


departments = [
    {"name": "Surgery", "description": "Deals with physical structure to diagnose or prevent treatment."},
    {"name": "Cardiology", "description": "Concerned with heart health and treatment of the heart and circulatory system."}
]

# Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="medical",
        autocommit=True,
       # This ensures the result is a dictionary
    )
    conn.ping(reconnect=True, attempts=3, delay=2)
    return conn


# Symptom-to-Medicine and Diet Mapping
# Sample mapping with disease info
disease_medicine_mapping = {
    "Diabetes": {
        "medicine": "Metformin",
        "diet": "Low Sugar Diet",
        "diet_plan": "Whole grains, leafy greens, avoid sugar",
        "dosage": "500mg twice a day",
        "doses": 2
    },
    "Hypertension": {
        "medicine": "Amlodipine",
        "diet": "Low Sodium Diet",
        "diet_plan": "Fruits, vegetables, less salt",
        "dosage": "5mg once a day",
        "doses": 1
    },
    "Asthma": {
        "medicine": "Salbutamol Inhaler",
        "diet": "Anti-inflammatory Diet",
        "diet_plan": "Omega-3 rich foods, avoid allergens",
        "dosage": "2 puffs every 4 hours",
        "doses": 6
    },
    "Arthritis": {
        "medicine": "Ibuprofen",
        "diet": "Joint Health Diet",
        "diet_plan": "Omega-3, turmeric, green tea",
        "dosage": "400mg every 8 hours",
        "doses": 3
    },
    "Anemia": {
        "medicine": "Iron Supplement",
        "diet": "Iron-Rich Diet",
        "diet_plan": "Spinach, red meat, legumes",
        "dosage": "Once daily after food",
        "doses": 1
    },
    "Thyroid Disorder": {
        "medicine": "Levothyroxine",
        "diet": "Thyroid Support Diet",
        "diet_plan": "Iodine-rich foods, avoid soy & gluten",
        "dosage": "25mcg once daily",
        "doses": 1
    },
    "Migraine": {
        "medicine": "Sumatriptan",
        "diet": "Trigger-Free Diet",
        "diet_plan": "Avoid chocolate, caffeine, alcohol",
        "dosage": "50mg as needed",
        "doses": 1
    },
    "Depression": {
        "medicine": "Sertraline",
        "diet": "Mood-Boosting Diet",
        "diet_plan": "Fish, nuts, berries, avoid alcohol",
        "dosage": "50mg daily",
        "doses": 1
    },
    "High Cholesterol": {
        "medicine": "Atorvastatin",
        "diet": "Heart-Healthy Diet",
        "diet_plan": "Oats, olive oil, nuts, avoid trans fats",
        "dosage": "10mg daily",
        "doses": 1
    },
    "Obesity": {
        "medicine": "Orlistat",
        "diet": "Low-Calorie Diet",
        "diet_plan": "Lean protein, fiber-rich foods, cut sugar",
        "dosage": "120mg before meals",
        "doses": 3
    },
    "Acid Reflux": {
        "medicine": "Omeprazole",
        "diet": "GERD-Friendly Diet",
        "diet_plan": "Avoid spicy, acidic, and fried foods",
        "dosage": "20mg daily before breakfast",
        "doses": 1
    },
    "Constipation": {
        "medicine": "Lactulose",
        "diet": "High-Fiber Diet",
        "diet_plan": "Whole grains, fruits, lots of water",
        "dosage": "15ml twice a day",
        "doses": 2
    },
    "UTI": {
        "medicine": "Nitrofurantoin",
        "diet": "Hydration-Focused Diet",
        "diet_plan": "Water, cranberry juice, avoid caffeine",
        "dosage": "100mg twice daily",
        "doses": 2
    },
    "Allergies": {
        "medicine": "Cetirizine",
        "diet": "Allergen-Free Diet",
        "diet_plan": "Avoid dairy, gluten, processed foods",
        "dosage": "10mg once daily",
        "doses": 1
    },
    "Cold and Flu": {
        "medicine": "Paracetamol",
        "diet": "Immunity Boosting Diet",
        "diet_plan": "Citrus fruits, ginger, honey, fluids",
        "dosage": "500mg every 6 hours",
        "doses": 4
    },
    "Fever": {
        "medicine": "Paracetamol",
        "diet": "Hydration and Light Foods",
        "diet_plan": "Warm fluids, light soups, avoid heavy meals",
        "dosage": "500mg every 6 hours",
        "doses": 4
    },
    "Cough": {
        "medicine": "Dextromethorphan Syrup",
        "diet": "Throat-Soothing Diet",
        "diet_plan": "Warm teas, honey, avoid cold drinks",
        "dosage": "10ml three times a day",
        "doses": 3
    },
    "Weakness": {
        "medicine": "Multivitamin Tablet",
        "diet": "Energy-Rich Diet",
        "diet_plan": "Bananas, dry fruits, protein sources",
        "dosage": "1 tablet daily after breakfast",
        "doses": 1
    },
    "Diarrhea": {
        "medicine": "ORS & Loperamide",
        "diet": "BRAT Diet",
        "diet_plan": "Bananas, rice, applesauce, toast; hydrate well",
        "dosage": "Loperamide 2mg after each loose stool",
        "doses": 2
    }
}




@app.route('/disease_plan')
def disease_plan():
    diseases = list(disease_medicine_mapping.keys())
    return render_template('disease_plan.html', diseases=diseases)

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    selected_diseases = data.get('diseases', [])
    symptoms_text = data.get('symptoms', '')

    if not selected_diseases and symptoms_text:
        # NLP Feature: Predict disease from free text symptoms
        words = TextBlob(symptoms_text.lower()).words
        predicted = []
        for disease, info in disease_medicine_mapping.items():
            if any(w in disease.lower() or w in info['diet_plan'].lower() or w in info['medicine'].lower() for w in words):
                predicted.append(disease)
        if predicted:
            selected_diseases = predicted

    if not selected_diseases:
        return jsonify({"error": "No diseases selected or found from symptoms"}), 400

    for disease in selected_diseases:
        if disease in disease_medicine_mapping:
            entry = disease_medicine_mapping[disease]
            final_medicine = entry["medicine"]
            final_diet = entry["diet"]
            diet_plan = entry["diet_plan"]
            dosage = entry["dosage"]
            doses = entry["doses"]
            break
    else:
        return jsonify({"error": "No valid recommendation found"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM patient WHERE id = %s", (session['user_id'],))
    patient = cursor.fetchone()
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient_name, phone_no = patient

    issue_date = datetime.now().strftime("%Y-%m-%d")
    issue_time = datetime.now().strftime("%H:%M:%S")

    # Save to patient_history table
    cursor.execute("""
        INSERT INTO patient_history (patient_id, patient_name, phone, selected_diseases, medicine, dosage, doses, diet, diet_plan, issue_date, issue_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        session['user_id'],
        patient_name,
        phone_no,
        ', '.join(selected_diseases),
        final_medicine,
        dosage,
        doses,
        final_diet,
        diet_plan,
        issue_date,
        issue_time
    ))
    conn.commit()
    conn.close()

    session['prescription_data'] = {
        "medicine": final_medicine,
        "diet": final_diet,
        "diet_plan": diet_plan,
        "dosage": dosage,
        "doses": doses,
        "patient_name": patient_name,
        "phone_no": phone_no,
        "selected_diseases": selected_diseases
    }

    return jsonify({
        "medicine": final_medicine,
        "diet": final_diet,
        "diet_plan": diet_plan,
        "dosage": dosage,
        "doses": doses,
        "patient_name": patient_name,
        "phone_no": phone_no
    })

@app.route('/patient_history')
def patient_history():
    if 'user_id' not in session:
        return redirect(url_for('patient_registration'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT selected_diseases, medicine, dosage, doses, diet, diet_plan, issue_date, issue_time
        FROM patient_history
        WHERE patient_id = %s
        ORDER BY issue_date DESC, issue_time DESC
    """, (session['user_id'],))
    history_records = cursor.fetchall()
    conn.close()

    return render_template('patient_history.html', history=history_records)
   
@app.route('/download_prescription')
def download_prescription():
    if 'user_id' not in session:
        return "User not logged in", 401

    data = session.get('prescription_data')
    if not data:
        return "No prescription found", 404

    prescription_id = str(random.randint(10000, 99999))
    issue_date = datetime.now().strftime("%d-%m-%Y")
    issue_time = datetime.now().strftime("%I:%M %p")

    pdf = FPDF(format='A5')
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)  # disable auto page break to keep 1 page

    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # ===== Header =====
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "SHREE HEALTH CLINIC", ln=True, align='C')

    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, "City Center, Maharashtra - 416416", ln=True, align='C')
    pdf.cell(0, 6, "Phone: +91-9876543210 | Email: care@shreeclinic.com", ln=True, align='C')
    pdf.ln(3)
    y = pdf.get_y()
    pdf.set_draw_color(100, 100, 100)
    pdf.line(10, y, 140, y)
    pdf.ln(5)

    # ===== Patient Info =====
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"Patient Name: {data['patient_name']}", ln=True)
    pdf.cell(0, 6, f"Phone Number: {data['phone_no']}", ln=True)
    pdf.cell(0, 6, f"Prescription ID: {prescription_id}", ln=True)
    pdf.cell(0, 6, f"Issued On: {issue_date} at {issue_time}", ln=True)
    pdf.ln(5)

    # ===== Medicine Section =====
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(204, 229, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, " Prescribed Medicine", ln=True, fill=True)

    pdf.set_font("Arial", '', 10)
    med_text = f"{data['medicine']} - {data['dosage']} ({data['doses']} doses per day)"
    pdf.multi_cell(0, 8, med_text, border=1)
    pdf.ln(4)

    # ===== Diet Section =====
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(204, 255, 229)
    pdf.cell(0, 8, " Diet Plan", ln=True, fill=True)

    pdf.set_font("Arial", '', 10)
    diet_text = f"{data['diet']} - {data['diet_plan']}"
    pdf.multi_cell(0, 8, diet_text, border=1)
    pdf.ln(10)

    # ===== Footer =====
    pdf.set_y(120)  # push footer near bottom
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Doctor's Signature: __________________", ln=True, align='C')
    pdf.cell(0, 6, "This is a digitally generated prescription", ln=True, align='C')

    # ===== Save and Send =====
    filename = f"prescription_{prescription_id}.pdf"
    pdf_path = os.path.join("static", filename)
    pdf.output(pdf_path)

    return send_file(pdf_path, as_attachment=True)


@app.route('/patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for('patient_registration'))

    patient_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, phone, address, gender, birth_date, blood_group, image FROM patient WHERE id = %s", (patient_id,))
    user = cursor.fetchone()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('patient_registration'))

    # Check for rescheduled appointment notifications
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = %s AND shedule = 'Rescheduled'", (patient_id,))
    notification_count = cursor.fetchone()[0]
    has_notification = notification_count > 0

    patient = {
        "id": user[0], "name": user[1], "email": user[2], "phone": user[3], "address": user[4], 
        "gender": user[5], "birth_date": user[6], "blood_group": user[7], "image": user[8]
    }

    return render_template('patient_dashboard.html', patient=patient, has_notification=has_notification)


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/index")
def index():
    return render_template("index.html", departments=departments)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template("contact.html", departments=departments)

@app.route('/patient')
def patient():
    return render_template('patient_dashboard.html')

@app.route('/patient_info')
def patient_info():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch patient details
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()

    # Fetch appointment details for each patient
    cursor.execute("""
        SELECT a.*, p.name AS patient_name FROM appointments a
        JOIN patient p ON a.patient_id = p.id
    """)
    appointments = cursor.fetchall()

    return render_template('patient_info.html', patients=patients, appointments=appointments)

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First delete all appointments for the patient
        cursor.execute("DELETE FROM appointments WHERE patient_id = %s", (id,))

        # Now delete the patient
        cursor.execute("DELETE FROM patient WHERE id = %s", (id,))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('patient_info'))



@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('patient_info'))





@app.route('/doctor')
def doctor():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, department, license_no, mobile, photo FROM doctor WHERE status='approved'")
    doctors = cursor.fetchall()
    conn.commit()
    return render_template('doctor.html', doctors=doctors)

@app.route('/doctorlogin')
def doctorlogin():
    return render_template('doctor_login.html')

# Route for doctor's dashboard
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')

        if not name or not password:
            flash("Username and password are required!", "error")
            return redirect(url_for('doctorlogin'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM doctor WHERE name=%s AND password=%s AND status='approved'", (name, password))
        doctor = cursor.fetchone()

        if doctor:
            session['doctor_id'] = doctor['id']
            session['doctor_name'] = doctor['name']

            cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s", (doctor['id'],))
            appointments = cursor.fetchall()
            conn.close()

            urgent_keywords = ['chest pain', 'bleeding', 'severe', 'heart', 'unconscious', 'breathing', 'stroke', 'emergency', 'faint']
            for appt in appointments:
                symptoms = appt.get('symptoms', '') or ''
                words = TextBlob(symptoms.lower()).words
                appt['is_urgent'] = any(word in words for word in urgent_keywords) or any(k in symptoms.lower() for k in urgent_keywords)

            return render_template('doctor.html', doctor=doctor, appointments=appointments)
        else:
            flash("Invalid name or password!", "error")
            return redirect(url_for('doctorlogin'))
    
    # If request method is GET, check if already logged in
    if 'doctor_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor WHERE id=%s", (session['doctor_id'],))
        doctor = cursor.fetchone()
        
        if doctor:
            cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s", (doctor['id'],))
            appointments = cursor.fetchall()
            conn.close()
            
            urgent_keywords = ['chest pain', 'bleeding', 'severe', 'heart', 'unconscious', 'breathing', 'stroke', 'emergency', 'faint']
            for appt in appointments:
                symptoms = appt.get('symptoms', '') or ''
                words = TextBlob(symptoms.lower()).words
                appt['is_urgent'] = any(word in words for word in urgent_keywords) or any(k in symptoms.lower() for k in urgent_keywords)

            return render_template('doctor.html', doctor=doctor, appointments=appointments)
        else:
            session.clear()
            return redirect(url_for('doctorlogin'))
            
    return redirect(url_for('doctorlogin'))

@app.route('/doctor_profile/<int:id>')
def doctor_profile(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctor WHERE id = %s", (id,))
    doctor = cursor.fetchone()
    conn.close()
    
    if doctor:
        return render_template('doctor_profile.html', doctor=doctor)
    else:
        flash("Doctor not found.", "error")
        return redirect(url_for('doctor_dashboard'))

@app.route('/dlogout')
def dlogout():
    flash("You have been logged out successfully!", "success")
    return redirect(url_for('home'))


# Route for updating appointment status

# Patient checks their latest appointment status
@app.route('/check_status')
def check_status():
    if 'user_id' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('patient_registration'))

    patient_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch patient details
    cursor.execute("SELECT id, name, email, phone FROM patient WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()

    # Fetch the latest appointment (including video_link)
    cursor.execute("""
        SELECT a.name, a.id, a.preferred_date, a.status, a.video_link, d.id AS doctor_id 
        FROM appointments a 
        JOIN doctor d ON a.doctor_id = d.id
        WHERE a.patient_id = %s 
        ORDER BY a.preferred_date DESC LIMIT 1
    """, (patient_id,))
    appointment = cursor.fetchone()

    cursor.close()
    conn.close()

    # Show flash message if rescheduled
    if appointment and appointment['status'] == 'Rescheduled':
        flash(f"Your appointment has been rescheduled to {appointment['preferred_date']} at {appointment['preferred_time']}", "info")

    return render_template('patient_status.html', appointment=appointment, patient=patient)

@app.route('/doctor_reschedule/<int:appointment_id>', methods=['GET', 'POST'])
def doctor_reschedule(appointment_id):
    if request.method == 'POST':
        new_date = request.form['new_date']
        new_time = request.form['new_time']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE appointments 
            SET preferred_date=%s, preferred_time=%s, shedule='Rescheduled' 
            WHERE id=%s
        """, (new_date, new_time, appointment_id))

        conn.commit()
        cursor.close()

        flash("Appointment rescheduled successfully!")
        return redirect(url_for('doctor_dashboard'))

    # For GET
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments WHERE id=%s", (appointment_id,))
    appointment = cursor.fetchone()
    cursor.close()
    return render_template('reschedule.html', appointment=appointment)


@app.route('/notification')
def notification():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to view notifications.", "warning")
        return redirect(url_for('patient_registration'))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM appointments 
        WHERE patient_id = %s AND shedule = 'Rescheduled'
    """, (user_id,))
    rescheduled_appointments = cursor.fetchall()
    cursor.close()
    conn.close()

    message = "Your appointment has been rescheduled. Please check details." if rescheduled_appointments else None
    return render_template('notifications.html', message=message, appointments=rescheduled_appointments)


@app.context_processor
def inject_notification_flag():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(*) AS count FROM appointments 
            WHERE patient_id = %s AND shedule = 'Rescheduled'
        """, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {'has_notification': result['count'] > 0}
    return {'has_notification': False}



@app.route('/admin_doctors')
def admin_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT `id`, `name`, `email`, `department`, `license_no`, `mobile`, `photo`, `status`, `active`, `password`, `education`, `passing_year`, `experience`, `document` FROM `doctor`")
    doctors = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM doctor WHERE active=1")
    active_count = cursor.fetchone()[0]
    return render_template('admin_doctors.html', doctors=doctors, active_count=active_count)

@app.route('/approve_doctor/<int:id>')
def approve_doctor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE doctor SET status='approved' WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for('admin_doctors'))

@app.route('/reject_doctor/<int:id>')
def reject_doctor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctor WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for('admin_doctors'))

@app.route('/toggle_doctor_status/<int:id>')
def toggle_doctor_status(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT active, status FROM doctor WHERE id=%s", (id,))
    result = cursor.fetchone()
    
    if result and result[1] == 'approved':  # Ensure only approved doctors can be activated/deactivated
        new_status = 1 if result[0] == 0 else 0
        cursor.execute("UPDATE doctor SET active=%s WHERE id=%s", (new_status, id))
        conn.commit()
        flash("Doctor status updated successfully!", "info")
    else:
        flash("Only approved doctors can be activated or deactivated!", "error")

    return redirect(url_for('admin_doctors'))


@app.route('/emergency_services')
def emergency_services():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch emergency services
    cursor.execute("SELECT * FROM emergency_services")
    services = cursor.fetchall()

    # Fetch hospital emergency resources
    cursor.execute("SELECT * FROM hospital_resources")
    resources = cursor.fetchone()

    # Handle case where no resources are found
    if resources is None:
        resources = (0, "Unknown", "Not Available")  # Default values

    return render_template('emergency_services.html', services=services, beds=resources[1], helpline=resources[2])

@app.route('/update_resources', methods=['POST'])
def update_resources():
    beds = request.form['beds']
    helpline = request.form['helpline']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE hospital_resources SET available_beds=%s, ambulance_helpline=%s", (beds, helpline))
    conn.commit()
    return redirect(url_for('emergency_services'))


import os
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename

# Define image folder path and allowed extensions
EMERGENCY_IMAGE_DIR = 'static/emergency_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg'}

# Create folder if it doesn't exist
os.makedirs(EMERGENCY_IMAGE_DIR, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_emergency_service', methods=['POST'])
def add_emergency_service():
    service_name = request.form['service_name']
    contact_number = request.form['contact_number']
    address = request.form['address']
    
    file = request.files['image']  # The name in HTML form input must be 'image'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(EMERGENCY_IMAGE_DIR, filename)
        file.save(file_path)

        # Save relative path to DB using forward slash for URL compatibility
        image_url = f"/{EMERGENCY_IMAGE_DIR}/{filename}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emergency_services (name, contact_number, image_url, address) VALUES (%s, %s, %s, %s)",
            (service_name, contact_number, image_url, address)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('emergency_services'))
    else:
        return "Invalid image file or no image uploaded.", 400





@app.route('/remove_emergency_service', methods=['POST'])
def remove_emergency_service():
    service_id = request.form['service_id']  # Assuming the form sends a service_id to delete

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM emergency_services WHERE id = %s", (service_id,))
    
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('emergency_services'))

@app.route('/patient_emergency_services')
def patient_emergency_services():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch emergency services
    cursor.execute("SELECT * FROM emergency_services")
    services = cursor.fetchall()

    # Fetch hospital emergency resources
    cursor.execute("SELECT * FROM hospital_resources")
    resources = cursor.fetchone()

    # Handle case where no resources are found
    if resources is None:
        resources = (0, "Unknown", "Not Available")  # Default values

    return render_template('patient_emergency_services.html', services=services, beds=resources[1], helpline=resources[2])


def validate_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[@$!%*?&]", password)):
        return False
    return True

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    education = request.form['education']
    certificate = request.files.get('certificate')

    passing_year = request.form['passing_year']
    experience = request.form['experience']
    license_no = request.form['license_no']
    mobile = request.form['mobile']
    password = request.form['password']
    photo = request.files['photo']
    document = request.files['document']

    if not validate_password(password):
        flash("Password must be at least 8 characters long and include an uppercase letter, lowercase letter, number, and special character.", "error")
        return redirect(url_for('doctor'))

    # Save files
    photo_filename = secure_filename(photo.filename)
    photo_path = os.path.join(app.config['DOCTOR_UPLOAD_FOLDER'], photo_filename)
    photo.save(photo_path)

    cert_filename = None
    if certificate and certificate.filename:
       cert_filename = secure_filename(certificate.filename)
       cert_path = os.path.join(app.config['DOCTOR_UPLOAD_FOLDER'], cert_filename)
       certificate.save(cert_path)


    doc_filename = secure_filename(document.filename)
    doc_path = os.path.join(app.config['DOCTOR_UPLOAD_FOLDER'], doc_filename)
    document.save(doc_path)

    # Insert into DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO doctor (name, email, department, education, certificate, passing_year, experience, license_no, mobile, password, photo, document, status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, email, department, education, cert_filename, passing_year, experience, license_no, mobile, password, photo_filename, doc_filename, 'pending'))

    conn.commit()

    flash("Doctor registered successfully and awaiting approval.", "success")
    return redirect(url_for('doctorlogin'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin_doctors'))
        else:
            return render_template("admin.html", error="Invalid credentials!")
    return render_template("admin.html")

@app.route('/patient_registration')
def patient_registration():
    return render_template('patient_registration.html')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    address = request.form['address']
    gender = request.form['gender']
    birth_date = request.form['birth_date']
    blood_group = request.form['blood_group']
    image = request.files['image']
    
    if not validate_password(password):
        flash("Password must be at least 8 characters long, include an uppercase letter, lowercase letter, number, and special character.", "error")
        return redirect(url_for('patient_registration'))

    filename = image.filename
    image.save(os.path.join(app.config['PATIENT_UPLOAD_FOLDER'], filename))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient WHERE email = %s", (email,))
    if cursor.fetchone():
        flash("Email already registered!", "danger")
        return redirect(url_for('patient_registration'))

    cursor.execute("""
        INSERT INTO patient (name, email, password, phone, address, gender, birth_date, blood_group, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, email, password, phone, address, gender, birth_date, blood_group, filename))
    conn.commit()

    flash("Registration successful! Please log in.", "success")
    return redirect(url_for('patient_registration'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionary

    cursor.execute("SELECT id, name, email, phone, address, gender, birth_date, blood_group, image FROM patient WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user["id"]              # Store patient ID
        session['user_name'] = user["name"]          # ✅ Store patient name
        session['user_role'] = 'patient'             # Optional: track user role
        flash("Login successful!", "success")
        return render_template('patient_dashboard.html', patient=user)
    else:
        flash("Invalid credentials!", "danger")
        return redirect(url_for('patient_registration'))
    
@app.route('/plogout')
def plogout():
    flash("You have been logged out successfully!", "success")
    return redirect(url_for('home'))




@app.route('/profile/<int:patient_id>')
def profile(patient_id):
    conn = get_db_connection()  # Ensure connection is initialized first
    cursor = conn.cursor()  # Now conn is defined, so no error

    # Fetch patient details from the database
    query = "SELECT name, email, phone, address, blood_group, image FROM patient WHERE id = %s"
    cursor.execute(query, (patient_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()  # Close connection to avoid memory leaks

    if not result:
        return "Patient not found", 404

    patient = {
        "name": result[0],
        "email": result[1],
        "phone": result[2],
        "address": result[3],
        "blood_group": result[4],
        "image": result[5]  # Image path stored in database
    }

    return render_template('profile.html', patient=patient, patient_id=patient_id)

@app.route('/update_profile/<int:patient_id>', methods=['POST'])
def update_profile(patient_id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    blood_group = request.form['blood_group']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Handle profile picture upload
    file = request.files.get('profile_pic')
    if file and file.filename:
        if allowed_file(file.filename):
            # Create consistent filename for patient
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"patient_{patient_id}.{ext}"
            filepath = os.path.join(app.config['PATIENT_UPLOAD_FOLDER'], filename)

            # Save/overwrite image
            file.save(filepath)

            image_path = f"patient_images/{filename}"
            cursor.execute("UPDATE patient SET image = %s WHERE id = %s", (image_path, patient_id))
        else:
            flash("Invalid image format. Use JPG, JPEG or PNG.", "danger")
            return redirect(url_for('profile', patient_id=patient_id))

    # Update other profile details
    cursor.execute("""
        UPDATE patient
        SET name=%s, email=%s, phone=%s, address=%s, blood_group=%s
        WHERE id=%s
    """, (name, email, phone, address, blood_group, patient_id))

    conn.commit()
    conn.close()

    flash("Profile updated successfully!", "success")
    return redirect(url_for('profile', patient_id=patient_id))

@app.route('/take_appointment/<int:patient_id>')
def take_appointment(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch patient details
    cursor.execute("SELECT * FROM patient WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()

    # Fetch all doctors
    cursor.execute("SELECT id, name, department FROM doctor")
    doctors = cursor.fetchall()

    conn.close()
    return render_template('appointment.html', patient=patient, doctors=doctors)


@app.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    patient_id = request.form.get('patient_id')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    # Safely get gender and blood group, fallback to DB if missing
    gender = request.form.get('gender')
    blood_group = request.form.get('blood_group')
    
    if not gender or not blood_group:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT gender, blood_group FROM patient WHERE id = %s", (patient_id,))
        p_data = cursor.fetchone()
        if p_data:
            gender = gender or p_data['gender']
            blood_group = blood_group or p_data['blood_group']
        conn.close()

    doctor_id = request.form.get('doctor')
    preferred_date = request.form.get('prefer_date')
    preferred_time = request.form.get('prefer_time')
    consultation_mode = request.form.get('consultation_mode')
    symptoms = request.form.get('symptoms', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO appointments (patient_id, name, email, phone, gender, blood_group, doctor_id, preferred_date, preferred_time, consultation_mode, status, symptoms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s)",
        (patient_id, name, email, phone, gender, blood_group, doctor_id, preferred_date, preferred_time, consultation_mode, symptoms)
    )
    conn.commit()
    conn.close()

    flash("Appointment Requested Successfully", "success")
    
    # ✅ Fix: Redirect to a success page or return a response
    return redirect(url_for('appointment_success'))  # Redirect to a success page


# ✅ Define a success page
@app.route('/appointment_success')
def appointment_success():
    flash("Appointment successfully submitted!", "success")
    return render_template('appointment_success.html')


@app.route('/appointment_unsuccess')
def appointment_unsuccess():
    return render_template('appointment_unsuccess.html')

# Route: Druggist Login Page
@app.route('/druggist', methods=['GET', 'POST'])
def druggist_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM druggist WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['druggist_logged_in'] = True
            session['druggist_name'] = user['username']  # ✅ Store name in session
            return redirect(url_for('druggist_dashboard'))
        else:
            flash("Invalid Username or Password", "danger")

    return render_template('druggist_login.html')


# Route: Druggist Dashboard
@app.route('/druggist_dashboard')
def druggist_dashboard():
    if not session.get('druggist_logged_in'):
        return redirect(url_for('druggist_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prescriptions")
    prescriptions = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('druggist_dashboard.html', prescriptions=prescriptions)


@app.route('/delete_prescription/<int:id>')
def delete_prescription(id):
    if not session.get('druggist_logged_in'):
        return redirect(url_for('druggist_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prescriptions WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('druggist_dashboard'))




@app.route('/update_prescription/<int:id>/<status>')
def update_prescription(id, status):
    if not session.get('druggist_logged_in'):
        return redirect(url_for('druggist_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE prescriptions SET status=%s WHERE id=%s", (status, id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('druggist_dashboard'))

@app.route('/view_pdf/<filename>')
def view_pdf(filename):
    return render_template('view_pdf.html', filename=filename)

# Route: Add Medicine
@app.route('/add_medicine', methods=['GET', 'POST'])
def add_medicine():
    if not session.get('druggist_logged_in'):
        return redirect(url_for('druggist_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    search_query = ''
    medicines = []
    did_you_mean = None

    if request.method == 'POST':
        search_query = request.form['search'].strip()
        cursor.execute("SELECT * FROM medicines WHERE name LIKE %s", ('%' + search_query + '%',))
        medicines = cursor.fetchall()
        
        # NLP Fuzzy Matching if no exact matches found
        if not medicines and search_query:
            cursor.execute("SELECT name FROM medicines")
            all_meds = [row[0] for row in cursor.fetchall()]
            import difflib
            matches = difflib.get_close_matches(search_query, all_meds, n=1, cutoff=0.5)
            if matches:
                did_you_mean = matches[0]
                cursor.execute("SELECT * FROM medicines WHERE name LIKE %s", ('%' + did_you_mean + '%',))
                medicines = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('add_medicine.html', medicines=medicines, search_query=search_query, did_you_mean=did_you_mean)

@app.route('/suggest_medicine')
def suggest_medicine():
    query = request.args.get('query', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM medicines WHERE name LIKE %s LIMIT 10", (query + '%',))
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(results)

@app.route('/add_new_medicine', methods=['GET', 'POST'])
def add_new_medicine():
    if not session.get('druggist_logged_in'):
        return redirect(url_for('druggist_login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.files['image']

        if name and price and image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO medicines (name, image, price) VALUES (%s, %s, %s)",
                           (name, filename, price))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('add_medicine'))

    return render_template('add_new_medicine.html')

# Route: View Medicines
@app.route('/view_medicine')
def view_medicine():
    if not session.get('druggist_logged_in'):
        return redirect(url_for('druggist_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_medicine.html', medicines=medicines)

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('druggist_logged_in', None)
    return redirect(url_for('home'))

UPLOADED_FOLDER = 'static/prescriptions'  # 👈 Changed folder name
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOADED_FOLDER'] = UPLOADED_FOLDER

# Create the folder if it doesn't exist
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_prescription', methods=['GET', 'POST'])
def upload_prescription():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        file = request.files['prescription']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOADED_FOLDER'], filename)
            file.save(path)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prescriptions (patient_name, filename) VALUES (%s, %s)", 
                           (patient_name, filename))
            flash("Prescription uploaded successfully!", "success")
            conn.commit()
            cursor.close()
            conn.close()
            

    return render_template('upload_prescription.html')

@app.route('/prescription_status', methods=['GET', 'POST'])
def prescription_status():
    status = None
    if request.method == 'POST':
        name = request.form['patient_name']
        pdf_name = request.form['pdf_name']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT status FROM prescriptions WHERE patient_name=%s AND filename=%s LIMIT 1",
            (name, pdf_name)
        )
        result = cursor.fetchone()
        status = result['status'] if result else "No record found"
        cursor.close()
        conn.close()
    return render_template('prescription_status.html', status=status)

import requests
from flask import flash, redirect, request, url_for
import html

@app.route('/update_status/<int:appointment_id>/<string:status>')
def update_status(appointment_id, status):
    print("function call")
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            flash("Database connection error.", "error")
            return redirect(request.referrer or url_for('doctor_dashboard'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT consultation_mode FROM appointments WHERE id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            flash("Appointment not found.", "error")
            return redirect(request.referrer or url_for('doctor_dashboard'))

        consultation_mode = appointment['consultation_mode'].strip().lower()
        normalized_status = status.strip().capitalize()

        if consultation_mode == 'video' and normalized_status == 'Accepted':
            try:
                api_url = "http://work.ecssofttech.com/testwhereby.php"
                headers = {
                    'User-Agent': 'Mozilla/5.0'
                }
                response = requests.get(api_url, headers=headers, timeout=5)
                raw_response = response.text.strip()
                print("API raw response:", raw_response)

                video_link = html.unescape(raw_response).replace('"', '')
                print("Cleaned video link:", video_link)

                if video_link and video_link.startswith("https://"):
                    cursor.execute(
                        "UPDATE appointments SET status = %s, video_link = %s WHERE id = %s",
                        (normalized_status, video_link, appointment_id)
                    )
                    conn.commit()
                    flash("Video link generated and appointment accepted.", "success")
                else:
                    flash("Invalid video link format received. Please try again.", "error")
                    return redirect(request.referrer or url_for('doctor_dashboard'))

            except requests.exceptions.RequestException as e:
                flash(f"Error while calling video link API: {e}", "error")
                return redirect(request.referrer or url_for('doctor_dashboard'))
        else:
            cursor.execute(
                "UPDATE appointments SET status = %s WHERE id = %s",
                (normalized_status, appointment_id)
            )
            conn.commit()
            flash(f"Appointment status updated to {normalized_status}.", "success")

    except Exception as e:
        flash(f"Unexpected error occurred: {e}", "error")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(request.referrer or url_for('doctor_dashboard'))







@app.route('/patient_feedback', methods=['GET', 'POST'])
def patient_feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        name = session.get('user_name')

        if not name:
            flash("Session expired or not logged in!", "danger")
            return redirect('/login')

        conn = get_db_connection()
        cursor = conn.cursor()

        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO patient_feedback (name, feedback, submitted_at) VALUES (%s, %s, %s)", (name, feedback, submitted_at))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('thank_you'))  # ✅ Redirect here
    return render_template('patient_feedback.html')


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')



@app.route('/patient_complaint', methods=['GET', 'POST'])
def patient_complaint():
    if request.method == 'POST':
        complaint = request.form['complaint']
        name = session.get('user_name')  # ✅ Get name from session

        if not name:
            flash("Session expired or not logged in!", "danger")
            return redirect('/login')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patient_complaint (complaint) VALUES (%s)", (complaint,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('thank_you'))  # ✅ Redirect here
    return render_template('patient_complaint.html')


@app.route('/doctor_feedback', methods=['GET', 'POST'])
def doctor_feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        name = session.get('doctor_name')  # ✅ Get name from session

        if not name:
            flash("Session expired or not logged in!", "danger")
            return redirect(url_for('doctorlogin'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctor_feedback (name, feedback) VALUES (%s, %s)", (name, feedback))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/thank_you')  # or redirect('/doctor_feedback') if you prefer
    return render_template('doctor_feedback.html')


@app.route('/doctor_complaint', methods=['GET', 'POST'])
def doctor_complaint():
    if request.method == 'POST':
        complaint = request.form['complaint']
        name = session.get('doctor_name')  # ✅ Get name from session

        if not name:
            flash("Session expired or not logged in!", "danger")
            return redirect(url_for('doctorlogin'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctor_complaint (name, complaint) VALUES (%s, %s)", (name, complaint))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/thank_you')  # or redirect('/doctor_complaint')
    return render_template('doctor_complaint.html')


from datetime import datetime

@app.route('/druggist_feedback', methods=['GET', 'POST'])
def druggist_feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        name = session.get('druggist_name')  # ✅ Get name from session
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not name:
            flash("Session expired or not logged in!", "danger")
            return redirect('/druggist')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO druggist_feedback (name, feedback, submitted_at) VALUES (%s, %s, %s)", (name, feedback, submitted_at))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/thank_you')  # Or '/druggist_feedback'
    return render_template('druggist_feedback.html')



@app.route('/druggist_complaint', methods=['GET', 'POST'])
def druggist_complaint():
    if request.method == 'POST':
        complaint = request.form['complaint']
        name = session.get('druggist_name')  # ✅ Get name from session
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not name:
            flash("Session expired or not logged in!", "danger")
            return redirect('/druggist')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO druggist_complaint (name, complaint, submitted_at) VALUES (%s, %s, %s)", (name, complaint, submitted_at))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/thank_you')  # Or '/druggist_complaint'
    return render_template('druggist_complaint.html')


# ===== Admin Routes to View Feedback and Complaints =====
@app.route('/admin_view_feedbacks')
def admin_view_feedbacks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, feedback, submitted_at FROM patient_feedback")
    pf = cursor.fetchall()

    cursor.execute("SELECT name, complaint, submitted_at FROM patient_complaint")
    pc = cursor.fetchall()

    cursor.execute("SELECT name, feedback, submitted_at FROM doctor_feedback")
    df = cursor.fetchall()

    cursor.execute("SELECT name, complaint, submitted_at FROM doctor_complaint")
    dc = cursor.fetchall()

    cursor.execute("SELECT name, feedback, submitted_at FROM druggist_feedback")
    dgf = cursor.fetchall()

    cursor.execute("SELECT name, complaint, submitted_at FROM druggist_complaint")
    dgc = cursor.fetchall()

    conn.close()

    def analyze_sentiment(feedback_list, text_key):
        for item in feedback_list:
            text = item.get(text_key, '')
            if text:
                polarity = TextBlob(text).sentiment.polarity
                if polarity > 0.1:
                    item['sentiment'] = 'Positive'
                elif polarity < -0.1:
                    item['sentiment'] = 'Negative'
                else:
                    item['sentiment'] = 'Neutral'
            else:
                item['sentiment'] = 'Neutral'

    analyze_sentiment(pf, 'feedback')
    analyze_sentiment(df, 'feedback')
    analyze_sentiment(dgf, 'feedback')

    return render_template('admin_view_feedbacks.html',
                           pf=pf, pc=pc, df=df, dc=dc, dgf=dgf, dgc=dgc)




if __name__ == '__main__':
    app.run(debug=True,port=4000)
