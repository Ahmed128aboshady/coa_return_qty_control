# COA Return Quantity Control (`coa_return_qty_control`)

## 📌 الوصف العام (Overview)
Block returning more than the delivered quantity and show returned / remaining quantities on the return wizard and picking

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_return_qty_control`
- **التصنيف (Category):** `Inventory`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`
- **الملف:** `models\stock_return_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.return.picking.line`, `stock.return.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\stock_picking_views.xml`, `views\stock_return_picking_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Return Quantity Control` أو `coa_return_qty_control` والضغط على **تثبيت (Install)**.
