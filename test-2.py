from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from werkzeug.utils import secure_filename

TOKEN = "7678402334:AAECq46dCm8piqmS0zYIK1gvgkWiuyRZt8k"
CHAT_ID = "-1003293879672"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "secret123"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        property_type = request.form.get("propertyType")
        location = request.form.get("location")
        area = request.form.get("area") or "غير محدد"
        rooms = request.form.get("rooms") or "غير محدد"
        baths = request.form.get("baths") or "غير محدد"
        price_from = request.form.get("priceFrom") or "-"
        price_to = request.form.get("priceTo") or "-"
        notes = request.form.get("notes") or ""

        # حفظ الصور المرفوعة
        uploaded_files = []
        files = request.files.getlist("images")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # إعداد رسالة Telegram
        full_message = (
            f"🏠 طلب جديد من العميل:\n\n"
            f"👤 الاسم: {name}\n📞 الهاتف: {phone}\n📍 الموقع: {location}\n"
            f"🏷️ نوع العقار: {property_type}\n📐 المساحة: {area} م²\n"
            f"🛏️ الغرف: {rooms} | 🚿 الحمامات: {baths}\n"
            f"💰 السعر: من {price_from} إلى {price_to}\n\n"
            f"📝 ملاحظات:\n{notes}"
        )

        try:
            # إرسال الرسالة النصية
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          data={"chat_id": CHAT_ID, "text": full_message})

            # إرسال الملفات
            for file_path in uploaded_files:
                with open(file_path, "rb") as f:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                                  data={"chat_id": CHAT_ID},
                                  files={"document": f})

            flash("✅ تم إرسال البيانات والملفات بنجاح.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"❌ فشل الإرسال: {e}", "danger")
            return redirect(url_for("index"))

    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
