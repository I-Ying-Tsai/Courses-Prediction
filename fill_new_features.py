import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

# 讀取已清理的資料
file_path = 'cleaned_course_data.csv'
data = pd.read_csv(file_path)

# 優化後的關鍵字與細分類特徵映射
keywords = {
    '數學_微積分': ['微積分'],
    '數學_代數': ['代數'],
    '數學_幾何': ['幾何'],
    '數學_數值分析': ['數值分析'],
    '數學_分析': ['分析'],
    '統計_數據分析': ['數據分析', '分析'],
    '統計_機率': ['機率'],
    '統計_時間數列': ['時間數列'],
    '統計_貝氏統計': ['貝氏'],
    '電腦科學_深度學習': ['深度學習', '神經網絡'],
    '電腦科學_演算法': ['演算法', '算法'],
    '電腦科學_資料結構': ['資料結構'],
    '電腦科學_人工智慧': ['人工智慧', 'AI'],
    '電腦科學_程式設計': ['程式設計', '程式'],
    '電機工程_電路設計': ['電路'],
    '電機工程_電磁學': ['電磁'],
    '電機工程_模擬系統': ['模擬'],
    '測量_測量技術': ['測量'],
    '測量_地圖繪製': ['地圖'],
    '測量_GPS定位': ['定位'],
    '土木_結構設計': ['結構'],
    '土木_工程施工': ['工程'],
    '數學_應用線性代數': ['應用線性代數'],
    '數學_應用幾何': ['應用幾何'],
    '電腦科學_機器學習': ['機器學習'],
    '電腦科學_系統設計': ['系統設計'],
    '電腦科學_網路技術': ['網路技術'],
    '電機工程_信號處理': ['信號處理'],
    '法律': ['法律'],
    '測量_大地測量': ['大地測量'],
    '測量_遙感探測': ['遙感探測'],
    '測量_空間資訊': ['空間資訊'],
    '測量_攝影測量': ['攝影測量'],
    '跨領域': ['跨領域']
}

# 初始化新特徵
def initialize_features(data, keywords):
    for feature in keywords.keys():
        data[feature] = False
    return data

data = initialize_features(data, keywords)

# 保存進度的檔案
progress_file = 'progress.json'

# 加載進度
if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        progress = json.load(f)
        completed_courses = set(progress.get('completed_courses', []))
else:
    completed_courses = set()

course_names = data['科目名稱(連結課程地圖)             備註 \n             限選條件'].drop_duplicates().tolist()
remaining_courses = [course for course in course_names if course not in completed_courses]

# 建立 GUI
root = tk.Tk()
root.title("課程特徵選擇器")
root.geometry("700x500")

# 當前課程名稱
selected_course = tk.StringVar()

# 顯示下拉選單
dropdown_label = tk.Label(root, text="選擇課程名稱:", font=("Arial", 12))
dropdown_label.pack(pady=10)

dropdown_menu = ttk.Combobox(root, textvariable=selected_course, values=course_names, state="readonly", width=50)
dropdown_menu.pack(pady=10)

# 標記已完成課程的樣式
completed_style = ttk.Style()
completed_style.configure("Completed.TCombobox", background="lightgreen")
if remaining_courses:
    dropdown_menu.set(remaining_courses[0])

# 特徵勾選框
feature_vars = {key: tk.BooleanVar() for key in keywords.keys()}
feature_frame = tk.Frame(root)
feature_frame.pack(pady=10)

feature_label = tk.Label(feature_frame, text="選擇相關特徵:")
feature_label.grid(row=0, column=0, columnspan=2)

# 將特徵分為兩列顯示
columns = 2
for i, feature in enumerate(keywords.keys()):
    column = i % columns
    row = i // columns + 1
    tk.Checkbutton(feature_frame, text=feature, variable=feature_vars[feature]).grid(row=row, column=column, sticky=tk.W, padx=10)

# 更新特徵的函數
def update_features():
    course = selected_course.get()
    if not course:
        messagebox.showwarning("警告", "請選擇一門課程！")
        return

    selected_features = [key for key, var in feature_vars.items() if var.get()]

    # 將選中的特徵應用到所有同名課程
    data.loc[data['科目名稱(連結課程地圖)             備註 \n             限選條件'] == course, selected_features] = True

    # 標記課程已完成
    completed_courses.add(course)

    # 更新下拉選單樣式
    dropdown_menu.configure(style="Completed.TCombobox")

    # 清空勾選
    for var in feature_vars.values():
        var.set(False)

    messagebox.showinfo("成功", f"課程 '{course}' 已完成標記！")

# 保存資料和進度的函數
def save_data():
    output_file = 'enhanced_course_data.csv'
    data.to_csv(output_file, index=False)
    with open(progress_file, 'w') as f:
        json.dump({'completed_courses': list(completed_courses)}, f)
    messagebox.showinfo("成功", f"增強後的數據集已保存到: {output_file}，進度已保存！")

# 按鈕
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

update_button = tk.Button(button_frame, text="更新並標記完成", command=update_features)
update_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="保存進度", command=save_data)
save_button.pack(side=tk.LEFT, padx=5)

# 啟動主循環
root.mainloop()
