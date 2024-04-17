from flask import Flask, request, jsonify,send_file
import os
import json
app = Flask(__name__)


@app.route('/upload-files-day', methods=['POST'])
def upload_file():
    print('================Upload logs===========================')
    try: 
        if  request.method != 'POST':
            resp = jsonify({'message' : 'Method is not allowed'})
            resp.status_code = 400
            return resp
    
        file_logs = request.files.getlist('file')                  # nhận file
        date_folder = request.form['date']                         # nhận ngày lấy ra báo cáo: yyyy-mm-dd
        date_folder = ".".join(date_folder.split("-")[::-1])       # convert yyyy-mm-dd -> dd.mm.yyyy  
        for f in file_logs:
            print(f.filename)
            filepath = os.path.join('./docx',date_folder, f.filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)  # tạo foldder  './docx/dd.mm.yyyy/filename'
            f.save(filepath)
            print('Save file files: ' + str(f.filename))
    except Exception as e:
        print('Upload files get error!')
        print(e)
        return jsonify({'success': False, 'message': str(e)})
    return jsonify({'success': True, 'message': 'files upload successfull!'})


@app.route('/download-file-day', methods=['POST'])
def download_file():
    print('================Send file logs===========================')
    try:
        date_folder = request.form['date']                             # nhận ngày lấy ra báo cáo: yyyy-mm-dd
        date_folder = ".".join(date_folder.split("-")[::-1])           # convert yyyy-mm-dd -> dd.mm.yyyy    
        if not date_folder:
            return jsonify({'message': 'Date parameter is missing'}), 400
        
        directory_path = os.path.join('./BCC', date_folder,"BCC.docx")
        if not os.path.exists(directory_path):
            return jsonify({'message': 'No file found for the given date'}), 404
         
        return send_file(directory_path, as_attachment=True)
        
    except Exception as e:
        print('Download file get error!')
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/statistical-day',methods=['POST'])
def statistical():
    print('================Statistical logs===========================')
    try:
        region = request.form['region']               #  khu vực(Vùng Trời hoặc Vùng Biển)            
        start_date = request.form['start_date']       # ngày bắt đầu
        end_date = request.form['end_date']           # ngày kết thúc

        if not all([region, start_date, end_date]):
            return jsonify({'message': 'Missing one or more parameters'}), 400
    
        # Lấy ra file json tương ứng
        if region == "Vùng Trời":                                     
            file_path = "./Statistical/VungTroi.json"
        elif region == "Vùng Biển":
            file_path = "./Statistical/VungBien.json"
        else:
            return jsonify({'message': 'Choose the another region'}), 400
        if not os.path.exists(file_path):
            return jsonify({'message': 'No file generated for the given parameters'}), 404
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print('Statistical file generation error!')
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
