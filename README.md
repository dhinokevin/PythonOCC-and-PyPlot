
# 🛠️ PythonOCC and PyPlot - IIT Internship Screening Tasks

This repository showcases solutions to two compulsory tasks for the IIT internship screening, demonstrating proficiency in **CAD development** and **data visualization** using Python.

---

## 🎯 Area of Interest

- **PythonOCC** – 3D CAD modeling in Python  
- **PyPlot (Matplotlib)** – Scientific plotting and diagramming  
- **CAD Development** – Engineering modeling using scripting

---

## 📁 Repository Structure

```
├── task1/                         # Task 1: Shear Force & Bending Moment Diagram
│   ├── main.py                    # Script to generate SFD and BMD
│   ├── beam_data.xlsx             # Input Excel file with load and support data
│   └── Task1_results.png          # Output image of SFD and BMD

├── task2/                         # Task 2: 3D CAD Model of Laced Compound Column
│   ├── main.py                    # PythonOCC script for CAD modeling
│   └── output.png                 # Rendered image of the CAD column

└── IIT_Internship_Tasks_Report.pdf   # Complete LaTeX-based PDF report
```

---

## ✅ Task 1 – Plotting SFD and BMD Using PyPlot

### 📌 Objective:
To create a Python program that reads beam and loading data from an Excel sheet and plots:
- Shear Force Diagram (SFD)
- Bending Moment Diagram (BMD)

### 📂 Input:
- `beam_data.xlsx`: Contains span length, support positions, point loads, and UDLs.

### 📤 Output:
- `Task1_results.png`: Shows both SFD and BMD plots generated using Matplotlib.

### ▶️ How to Run:
```bash
cd task1
pip install matplotlib pandas openpyxl
python main.py
```

---

## ✅ Task 2 – 3D CAD Drawing of Laced Compound Column

### 📌 Objective:
To model a laced compound column with ISA sections and diagonal lacing using `PythonOCC`.

### 🔩 Key Features:
- ISA sections modeled as vertical elements
- Diagonal bars modeled using swept edges
- Full solid modeling with accurate dimensions
- Rendered using built-in PythonOCC viewer

### 📤 Output:
- `output.png`: Rendered view of the completed CAD model.

### ▶️ How to Run:
```bash
cd task2
pip install -r requirements.txt
python main.py
```

> 💡 PythonOCC rendering window opens automatically after script execution.

---

## 📝 Report

📄 A comprehensive PDF report is included for submission:  
**[`IIT_Internship_Tasks_Report.pdf`](./IIT_Internship_Tasks_Report.pdf)**  
This report explains:
- Task objectives
- Code structure and logic
- How to run each task
- Output images with explanation

---

## 👨‍💻 Author

**Dhino Kevin B**  
📧 dhinokevin@gmail.com  
🎓 Final Year Engineering Student | Full-Stack Developer | AI & CAD Enthusiast  

---

## 📚 Tools & Libraries Used

- [Matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [PythonOCC](https://github.com/tpaviot/pythonocc-core)
- [OpenCASCADE](https://www.opencascade.com/)

---

## 🛠 License

This repository is intended for academic evaluation and learning purposes.  
All rights reserved © Dhino Kevin B

---
