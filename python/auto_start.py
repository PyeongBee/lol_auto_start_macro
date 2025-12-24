import pyautogui
import time
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox

# 안전모드 설정: 마우스를 화면 왼쪽 상단 구석으로 가져가면 스크립트가 강제 종료됩니다.
pyautogui.FAILSAFE = True

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LOL 자동 게임 수락")
        self.root.geometry("300x200")
        
        # 상태 변수
        self.is_running = False
        self.target_image = "start_button.png"
        self.thread = None

        # UI 구성
        self.create_widgets()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        self.lbl_info = tk.Label(self.root, text="LOL 자동 게임 수락", font=("Arial", 14, "bold"))
        self.lbl_info.pack(pady=(10, 10))

        self.lbl_status = tk.Label(self.root, text="상태: 중지됨", fg="red")
        self.lbl_status.pack(pady=5)

        self.btn_start = tk.Button(self.root, text="시작", command=self.start_monitoring, width=10, bg="lightgreen")
        self.btn_start.pack(pady=5)

        self.btn_stop = tk.Button(self.root, text="중지", command=self.stop_monitoring, width=10, bg="lightpink")
        self.btn_stop.pack(pady=5)

    def start_monitoring(self):
        if self.is_running:
            return
        
        image_path = self.resource_path(self.target_image)
        if not os.path.exists(image_path):
            messagebox.showerror("오류", f"이미지 파일을 찾을 수 없습니다:\n{image_path}")
            return

        self.is_running = True
        self.lbl_status.config(text="상태: 실행 중...", fg="green")
        self.btn_start.config(state="disabled")
        
        # 별도 스레드에서 감시 루프 실행
        self.thread = threading.Thread(target=self.click_loop, args=(image_path,), daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        if not self.is_running:
            return
            
        self.is_running = False
        self.lbl_status.config(text="상태: 중지됨", fg="red")
        self.btn_start.config(state="normal")

    def click_loop(self, image_path):
        print(f"감지 시작: {image_path}")
        
        while self.is_running:
            try:
                # 0.8초마다 검사 (너무 빠르면 CPU 점유율 증가)
                location = pyautogui.locateOnScreen(image_path, confidence=0.8, grayscale=True)

                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    print(f"클릭 완료: {center}")
                    
                    # 클릭 후 잠시 대기 (중복 클릭 방지)
                    time.sleep(2)
                else:
                    time.sleep(5)

            except pyautogui.ImageNotFoundException:
                time.sleep(0.5)
                continue
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    
    # 창 닫을 때 프로세스 완전 종료
    def on_closing():
        app.is_running = False
        root.destroy()
        sys.exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
