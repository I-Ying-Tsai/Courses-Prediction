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
    '土木_建築學': ['建築']
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
        current_index = progress.get('current_index', 0)
else:
    current_index = 0

course_names = data['科目名稱(連結課程地圖)             備註 \n             限選條件'].drop_duplicates().tolist()

# 建立 GUI
root = tk.Tk()
root.title("課程特徵選擇器")
root.geometry("700x500")

# 顯示當前課程名稱
course_label = tk.Label(root, text=f"當前課程名稱: {course_names[current_index]}", font=("Arial", 14))
course_label.pack(pady=10)

# 特徵勾選框
feature_vars = {key: tk.BooleanVar() for key in keywords.keys()}
feature_frame = tk.Frame(root)
feature_frame.pack(pady=10)

feature_label = tk.Label(feature_frame, text="選擇相關特徵:")
feature_label.grid(row=0, column=0, columnspan=2)

for i, feature in enumerate(keywords.keys()):
    tk.Checkbutton(feature_frame, text=feature, variable=feature_vars[feature]).grid(row=i + 1, column=0, sticky=tk.W)

# 更新特徵的函數
def update_features():
    global current_index
    course = course_names[current_index]
    selected_features = [key for key, var in feature_vars.items() if var.get()]

    # 將選中的特徵應用到所有同名課程
    data.loc[data['科目名稱(連結課程地圖)             備註 \n             限選條件'] == course, selected_features] = True

    # 清空勾選
    for var in feature_vars.values():
        var.set(False)

    # 前往下一個課程
    current_index += 1
    if current_index < len(course_names):
        course_label.config(text=f"當前課程名稱: {course_names[current_index]}")
    else:
        messagebox.showinfo("完成", "所有課程特徵已標註完成！")
        current_index = 0

# 保存資料和進度的函數
def save_data():
    output_file = 'enhanced_course_data.csv'
    data.to_csv(output_file, index=False)
    with open(progress_file, 'w') as f:
        json.dump({'current_index': current_index}, f)
    messagebox.showinfo("成功", f"增強後的數據集已保存到: {output_file}，進度已保存！")

# 按鈕
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

update_button = tk.Button(button_frame, text="更新並跳至下一個", command=update_features)
update_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="保存進度", command=save_data)
save_button.pack(side=tk.LEFT, padx=5)

# 啟動主循環
root.mainloop()
