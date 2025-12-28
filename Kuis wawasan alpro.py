import customtkinter as ctk
from tkinter import messagebox
import pygame  # untuk musik


# ======================
# DATA SOAL
# ======================

QUIZZES = {
    "Kuis Matematika": [
        {
            "question": "1. Berapa hasil 12 + 7?",
            "options": ["17", "18", "19", "20"],
            "answer": "19",
        },
        {
            "question": "2. Hasil dari 9 × 6 adalah?",
            "options": ["42", "48", "52", "54"],
            "answer": "54",
        },
        {
            "question": "3. Berapa akar kuadrat dari 81?",
            "options": ["7", "8", "9", "10"],
            "answer": "9",
        },
        {
            "question": "4. 3/4 dalam bentuk persen adalah?",
            "options": ["50%", "60%", "70%", "75%"],
            "answer": "75%",
        },
        {
            "question": "5. 100 − 37 = ...",
            "options": ["53", "63", "73", "83"],
            "answer": "63",
        },
    ],
    "Kuis Pengetahuan Umum": [
        {
            "question": "1. Ibu kota Indonesia adalah?",
            "options": ["Bandung", "Jakarta", "Surabaya", "Medan"],
            "answer": "Jakarta",
        },
        {
            "question": "2. Benua terbesar di dunia adalah?",
            "options": ["Afrika", "Asia", "Eropa", "Amerika"],
            "answer": "Asia",
        },
        {
            "question": "3. Alat untuk melihat benda langit adalah?",
            "options": ["Mikroskop", "Teleskop", "Periskop", "Stetoskop"],
            "answer": "Teleskop",
        },
        {
            "question": "4. Hewan tercepat di darat adalah?",
            "options": ["Cheetah", "Kuda", "Singa", "Kelinci"],
            "answer": "Cheetah",
        },
        {
            "question": "5. Laut terluas di dunia adalah?",
            "options": ["Samudra Hindia", "Samudra Pasifik", "Samudra Atlantik", "Laut Cina Selatan"],
            "answer": "Samudra Pasifik",
        },
    ],
    "Kuis Teka-teki": [
        {
            "question": "1. Aku punya jarum tapi tidak bisa menjahit. Aku siapa?",
            "options": ["Pohon", "Jam", "Paku", "Kaktus"],
            "answer": "Jam",
        },
        {
            "question": "2. Semakin dikasih makan, aku semakin kecil. Aku apa?",
            "options": ["Lilin", "Batu", "Kayu", "Lilin (salah ejaan)"],
            "answer": "Lilin",
        },
        {
            "question": "3. Ia punya gigi tapi tidak bisa menggigit. Itu apa?",
            "options": ["Sisiran", "Sisir", "Gergaji", "Zebra"],
            "answer": "Sisir",
        },
        {
            "question": "4. Apa yang bisa naik tapi tidak pernah turun?",
            "options": ["Umur", "Bola", "Hujan", "Pesawat"],
            "answer": "Umur",
        },
        {
            "question": "5. Bulat, ada di meja belajar, diputar untuk melihat dunia. Itu apa?",
            "options": ["Kompas", "Jam dinding", "Globe", "Piring"],
            "answer": "Globe",
        },
    ],
}

KAHOOT_COLORS = ["#E21B3C", "#1368CE", "#26890C", "#FFA602"]  # merah, biru, hijau, kuning


class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Kuis Wawasan (KW)")
        self.geometry("600x450")
        self.resizable(False, False)

        self.current_quiz_name = None
        self.current_quiz_questions = []
        self.current_index = 0
        self.score = 0
        self.selected_option = ctk.StringVar()
        self.time_left = 0
        self.timer_id = None  # simpan id after() [web:123]

        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.init_music()
        self.show_home()

    # ======================
    # MUSIK
    # ======================

    def init_music(self):
        pygame.mixer.init()
        self.play_lobby_music()

    def play_lobby_music(self):
        try:
            pygame.mixer.music.load("lobby.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Gagal load lobby.mp3:", e)

    def play_quiz_music(self):
        try:
            pygame.mixer.music.load("quiz.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Gagal load quiz.mp3:", e)

    def play_once(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        except Exception as e:
            print("Gagal putar:", filename, e)

    # ======================
    # HOME
    # ======================

    def show_home(self):
        self.cancel_timer()  # pastikan timer mati saat balik menu
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.play_lobby_music()
        self.main_frame.configure(fg_color="#46178F")

        title = ctk.CTkLabel(
            self.main_frame,
            text="KUIS WAWASAN BERHADIA",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="white",
        )
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Pilih salah satu kuis di bawah:",
            font=ctk.CTkFont(size=14),
            text_color="white",
        )
        subtitle.pack(pady=(0, 20))

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        quiz_buttons = [
            (" Kuis Matematika", "Kuis Matematika"),
            (" Pengetahuan Umum", "Kuis Pengetahuan Umum"),
            (" Teka-teki", "Kuis Teka-teki"),
        ]

        for text, key in quiz_buttons:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                corner_radius=18,
                height=40,
                width=260,
                fg_color="#1368CE",
                hover_color="#0E4EA1",
                text_color="white",
                command=lambda name=key: self.start_quiz(name),
            )
            btn.pack(pady=8)

        exit_btn = ctk.CTkButton(
            self.main_frame,
            text="Keluar",
            fg_color="#FF3B30",
            hover_color="#FF6259",
            corner_radius=18,
            command=self.destroy,
        )
        exit_btn.pack(pady=(25, 10))

    # ======================
    # MULAI KUIS
    # ======================

    def start_quiz(self, quiz_name):
        self.current_quiz_name = quiz_name
        self.current_quiz_questions = QUIZZES[quiz_name]
        self.current_index = 0
        self.score = 0

        self.play_quiz_music()
        self.show_question()

    # ======================
    # TAMPILKAN SOAL
    # ======================

    def show_question(self):
        self.cancel_timer()  # hentikan timer lama sebelum buat baru
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        q = self.current_quiz_questions[self.current_index]
        self.main_frame.configure(fg_color="#46178F")

        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(15, 5), padx=15)

        title = ctk.CTkLabel(
            header_frame,
            text=self.current_quiz_name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
        )
        title.pack(side="left", anchor="w")

        self.timer_label = ctk.CTkLabel(
            header_frame,
            text="Time: 20",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
        )
        self.timer_label.pack(side="right", anchor="e")

        progress = ctk.CTkLabel(
            self.main_frame,
            text=f"Soal {self.current_index + 1} dari {len(self.current_quiz_questions)}",
            font=ctk.CTkFont(size=13),
            text_color="white",
        )
        progress.pack(pady=(0, 5))

        question_label = ctk.CTkLabel(
            self.main_frame,
            text=q["question"],
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=520,
            justify="center",
            text_color="white",
        )
        question_label.pack(pady=(15, 10), padx=20)

        self.selected_option.set("")

        options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=60, pady=(5, 20))

        for i, opt in enumerate(q["options"]):
            color = KAHOOT_COLORS[i % len(KAHOOT_COLORS)]
            btn = ctk.CTkButton(
                options_frame,
                text=opt,
                fg_color=color,
                hover_color="#FFFFFF",
                text_color="white",
                corner_radius=8,
                height=50,
                command=lambda value=opt: self.select_and_next(value),
            )
            btn.pack(fill="x", pady=6)

        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=10, padx=20)

        back_btn = ctk.CTkButton(
            bottom_frame,
            text="Berhenti",
            fg_color="#EEEEEE",
            text_color="black",
            hover_color="#DDDDDD",
            corner_radius=18,
            command=self.show_home,
        )
        back_btn.pack(side="left", padx=(0, 10))

        next_btn = ctk.CTkButton(
            bottom_frame,
            text="Lewati Soal",
            corner_radius=18,
            fg_color="#1368CE",
            hover_color="#0E4EA1",
            command=self.skip_question,
        )
        next_btn.pack(side="right")

        self.start_timer()

    # ======================
    # TIMER
    # ======================

    def start_timer(self):
        self.time_left = 20
        self.update_timer()

    def cancel_timer(self):
        if self.timer_id is not None:
            try:
                self.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

    def update_timer(self):
        if not hasattr(self, "timer_label"):
            return

        if self.time_left <= 0:
            self.selected_option.set("")
            self.next_question()
            return

        if self.time_left <= 5:
            self.timer_label.configure(
                text=f"Time: {self.time_left}",
                text_color="#FF3B30",
            )
        else:
            self.timer_label.configure(
                text=f"Time: {self.time_left}",
                text_color="white",
            )

        self.time_left -= 1
        self.timer_id = self.after(1000, self.update_timer)

    # ======================
    # JAWABAN
    # ======================

    def select_and_next(self, value):
        self.selected_option.set(value)
        self.next_question()

    def next_question(self):
        self.cancel_timer()  # stop timer sebelum pindah soal

        if self.selected_option.get() == "":
            pass

        correct = self.current_quiz_questions[self.current_index]["answer"]
        if self.selected_option.get() == correct:
            self.score += 1

        self.current_index += 1

        if self.current_index < len(self.current_quiz_questions):
            self.show_question()
        else:
            self.show_result()

    def skip_question(self):
        self.selected_option.set("")
        self.next_question()

    # ======================
    # HASIL
    # ======================

    def show_result(self):
        self.cancel_timer()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        total = len(self.current_quiz_questions)
        result_text = f"Kuis: {self.current_quiz_name}\n\nSkor kamu: {self.score} dari {total}\n"

        if self.score == total:
            result_text += "\nara ara kok kamu gacor x king"
            self.play_once("win.mp3")
        elif self.score >= total // 2:
            result_text += "\nyah setengah doang bener"
            self.play_once("lose.mp3")
        else:
            result_text += "\nkayaknya mirza lebih pinter deh dari kamu"
            self.play_once("lose.mp3")

        self.main_frame.configure(fg_color="#46178F")

        result_label = ctk.CTkLabel(
            self.main_frame,
            text=result_text,
            font=ctk.CTkFont(size=18),
            justify="center",
            text_color="white",
        )
        result_label.pack(pady=40)

        btn_again = ctk.CTkButton(
            self.main_frame,
            text="Kembali ke Menu",
            corner_radius=18,
            fg_color="#1368CE",
            hover_color="#0E4EA1",
            text_color="white",
            command=self.show_home,
        )
        btn_again.pack(pady=10)

        btn_exit = ctk.CTkButton(
            self.main_frame,
            text="Keluar",
            fg_color="#FF3B30",
            hover_color="#FF6259",
            corner_radius=18,
            command=self.destroy,
        )
        btn_exit.pack(pady=5)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
