# 🧠 Smart AOI Demo (Concept)

This project demonstrates a **Smart Automatic Optical Inspection (AOI)** workflow for PCB inspection.

---

## 🚀 Key Idea

Traditional AOI:

* Detects everything → many false fails

Smart AOI:

* Filters intelligently → highlights real defects

---

## 🔍 Features

* 📸 Load Golden vs Test images
* 🟡 Wave AOI → raw detection (many defects)
* 🔴 Smart AOI → filtered detection (real defects)
* 🔎 Zoom view for inspection
* ⏭ Navigate defects (Next / Prev)

---
## 🔷 Broader Application

This concept is not limited to AOI.

The same approach can be applied in any process where a reference sample (golden sample) is used for comparison.

By separating detection from intelligent filtering, it becomes possible to reduce noise and focus only on meaningful differences across various inspection or validation steps.


## 🎯 Demo Focus

This repository focuses on:

* AOI workflow visualization
* Wave vs Smart comparison
* UI interaction and inspection flow

> ⚠️ The detection engine is intentionally abstracted.

---

## 🧪 Example

| Mode      | Result                                 |
| --------- | -------------------------------------- |
| Wave AOI  | Many detections (false fails included) |
| Smart AOI | Reduced, meaningful defects            |

---

## 📸 Screenshots

(Add your images in `/screenshots`)
                          
---

## 🛠 Installation

```bash
pip install -r requirements.txt
python main.py
```

---

## 🧠 Future Work

* IC pin bridging detection
* Connector short detection
* Missing component detection (Staging AOI)
* AI-assisted defect classification

---

## 🔒 Note

The full detection engine is not included in this public version.

This project is intended to demonstrate the **concept and workflow** of Smart AOI.

---

## 👤 Author

Nallan Anbanandam                    
