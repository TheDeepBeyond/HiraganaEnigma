import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
from enigma_core import Enigma

class EnigmaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ひらがなエニグマ")
        self.enigma = None
        self.last_key = None

        self.input_text = tk.StringVar()
        self.mode = tk.StringVar(value="encrypt")

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="入力（ひらがな）").pack(pady=5)
        entry = ttk.Entry(self.root, textvariable=self.input_text, font=("Meiryo", 14))
        entry.pack(fill="x", padx=10)

        self.add_context_menu(entry)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=2)
        ttk.Button(button_frame, text="貼り付け", command=self.paste_to_entry).pack(side="left", padx=5)
        ttk.Button(button_frame, text="消去", command=self.clear_entry).pack(side="left", padx=5)

        ttk.Label(self.root, text="モード").pack(pady=5)
        ttk.Radiobutton(self.root, text="暗号化", variable=self.mode, value="encrypt").pack()
        ttk.Radiobutton(self.root, text="復号", variable=self.mode, value="decrypt").pack()

        ttk.Button(self.root, text="実行", command=self.run_enigma).pack(pady=10)
        ttk.Button(self.root, text="鍵を保存", command=self.save_key).pack(pady=2)
        ttk.Button(self.root, text="鍵を読み込み", command=self.load_key).pack(pady=2)

        ttk.Label(self.root, text="出力").pack(pady=5)
        self.output_box = tk.Text(self.root, height=3, font=("Meiryo", 14), wrap="word")
        self.output_box.pack(fill="x", padx=10)
        self.output_box.config(state="disabled")

        ttk.Button(self.root, text="出力をコピー", command=self.copy_output).pack(pady=2)

        self.key_text = tk.Text(self.root, height=6, font=("Meiryo", 10), state="disabled")
        self.key_text.pack(fill="x", padx=10, pady=5)

    def add_context_menu(self, widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="貼り付け", command=lambda: widget.insert(tk.END, self.root.clipboard_get()))
        widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

    def paste_to_entry(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.input_text.set(clipboard_text)
        except tk.TclError:
            messagebox.showwarning("警告", "クリップボードに有効なテキストがありません")

    def clear_entry(self):
        self.input_text.set("")

    def run_enigma(self):
        text = self.input_text.get()
        mode = self.mode.get()

        if mode == "encrypt":
            temp_enigma = Enigma()
            random_position = random.randint(0, temp_enigma.N - 1)
            self.enigma = Enigma(position=random_position)
            result = self.enigma.encrypt(text)
            self.last_key = self.enigma.export_key()
            self.show_key(self.last_key)
        else:
            if not self.last_key:
                self.show_output("鍵がありません")
                return
            self.enigma = Enigma(
                wiring=self.last_key["wiring"],
                position=self.last_key["position"]
            )
            result = self.enigma.decrypt(text)

        self.show_output(result)

    def show_output(self, text):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)
        self.output_box.config(state="disabled")

    def copy_output(self):
        self.root.clipboard_clear()
        text = self.output_box.get("1.0", tk.END).strip()
        self.root.clipboard_append(text)
        messagebox.showinfo("コピー完了", "出力をクリップボードにコピーしました")

    def show_key(self, key):
        self.key_text.config(state="normal")
        self.key_text.delete("1.0", tk.END)
        self.key_text.insert(tk.END, f"ローター配線:\n{key['wiring']}\n")
        self.key_text.insert(tk.END, f"初期位置: {key['position']}")
        self.key_text.config(state="disabled")

    def save_key(self):
        if not self.last_key:
            messagebox.showwarning("警告", "保存する鍵がありません")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("テキストファイル", "*.txt")])
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    for c in self.last_key["wiring"]:
                        f.write(c + "\n")
                    f.write(str(self.last_key["position"]) + "\n")
                messagebox.showinfo("保存完了", f"鍵を保存しました:\n{filepath}")
            except Exception as e:
                messagebox.showerror("エラー", f"鍵の保存に失敗しました:\n{e}")

    def load_key(self):
        filepath = filedialog.askopenfilename(filetypes=[("テキストファイル", "*.txt")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                wiring = lines[:-1]
                position = int(lines[-1])
                key = {"wiring": wiring, "position": position}
                self.last_key = key
                self.show_key(key)
                messagebox.showinfo("読み込み完了", f"鍵を読み込みました:\n{filepath}")
            except Exception as e:
                messagebox.showerror("エラー", f"鍵の読み込みに失敗しました:\n{e}")