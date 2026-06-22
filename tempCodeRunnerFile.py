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
            return redirect('/doctor_login')

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
            return redirect('/doctor_login')

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

    return render_template('admin_view_feedbacks.html',
                           pf=pf, pc=pc, df=df, dc=dc, dgf=dgf, dgc=dgc)




if __name__ == '__main__':
    app.run(debug=True,port=4000)
