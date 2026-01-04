from flask import Flask, render_template, request
import os
import uuid
import cv2

from image_processing.dilation import apply_dilation
from image_processing.erosion import apply_erosion
from image_processing.opening import apply_opening
from image_processing.closing import apply_closing

from utils.kernel import create_kernel
from utils.image_loader import load_image

# ======================
# Konfigurasi Aplikasi
# ======================
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# ======================
# Utilitas
# ======================
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Mapping operasi morfologi
OPERATIONS = {
    "dilation": apply_dilation,
    "erosion": apply_erosion,
    "opening": apply_opening,
    "closing": apply_closing
}

# ======================
# Routes
# ======================
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # ======================
        # 1. Validasi input
        # ======================
        if 'image' not in request.files:
            return "File tidak ditemukan", 400

        image_file = request.files['image']

        if image_file.filename == '':
            return "Nama file kosong", 400

        if not allowed_file(image_file.filename):
            return "Format file tidak didukung", 400

        operation = request.form.get('operation')
        kernel_size = int(request.form.get('kernel'))
        image_mode = request.form.get('mode')

        if operation not in OPERATIONS:
            return "Operasi tidak valid", 400

        # ======================
        # 2. Simpan gambar asli
        # ======================
        filename = f"{uuid.uuid4()}_{image_file.filename}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        # ======================
        # 3. Load image
        # ======================
        image = load_image(image_path, image_mode)

        if image is None:
            return "Gagal membaca gambar", 400

        # ======================
        # 4. Buat kernel
        # ======================
        kernel = create_kernel(kernel_size)

        # ======================
        # 5. Proses morfologi
        # ======================
        result = OPERATIONS[operation](image, kernel)

        # ======================
        # 6. Simpan hasil
        # ======================
        result_filename = f"result_{filename}"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        cv2.imwrite(result_path, result)

        # ======================
        # 7. Kirim ke frontend
        # ======================
        return render_template(
            'index.html',
            original_image=image_path,
            result_image=result_path,
            operation=operation,
            kernel_size=kernel_size
        )

    except Exception as e:
        # Error handler sederhana (cukup untuk konteks akademis)
        return f"Terjadi kesalahan: {str(e)}", 500

# ======================
# Main
# ======================
if __name__ == '__main__':
    app.run(debug=True)
