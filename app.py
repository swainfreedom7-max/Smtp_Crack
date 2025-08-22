from flask import Flask, render_template, request, session, redirect, url_for, send_file
from smtp_checker import process_email_list
from config import Config
import io
import csv
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
            
        if file and file.filename.endswith('.txt'):
            emails = file.read().decode('utf-8').splitlines()
            results = process_email_list(emails[:app.config['MAX_ENTRIES']])
            session['results'] = results
            return redirect(url_for('results'))
    
    return render_template('index.html')

@app.route('/results')
def results():
    if 'results' not in session:
        return redirect(url_for('index'))
    
    valid_count = sum(1 for r in session['results'] if r['valid'])
    return render_template(
        'results.html',
        results=session['results'],
        valid_count=valid_count,
        invalid_count=len(session['results']) - valid_count
    )

@app.route('/download')
def download():
    if 'results' not in session:
        return redirect(url_for('index'))
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email', 'Password', 'SMTP Host', 'Port', 'Encryption'])
    
    for result in session['results']:
        if result['valid']:
            writer.writerow([
                result['email'],
                result['password'],
                result['host'],
                result['port'],
                result['encryption']
            ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='smtp_configs.csv'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)