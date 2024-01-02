import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog
import webbrowser

class PDFSearchTool:
    def __init__(self, master):
        self.master = master
        master.resizable(False, False)
        master.title("PDF Search Tool")

        self.path_var = tk.StringVar()
        self.keyword_var = tk.StringVar()

        tk.Label(master, text="Select PDF Directory:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        tk.Label(master, text="Enter Keyword:").grid(row=1, column=0, sticky='w', padx=5, pady=5)

        tk.Entry(master, textvariable=self.path_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(master, textvariable=self.keyword_var, width=50).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(master, text="Browse", command=self.browse_path).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(master, text="Start Search", command=self.start_search).grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(master, text="Open Selected PDF", command=self.open_selected_pdf).grid(row=3, column=0, columnspan=3, pady=10)

        self.pdf_listbox = tk.Listbox(master, width=80, height=10)
        self.pdf_listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        scrollbar_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        scrollbar_y.grid(row=4, column=3, sticky='ns')
        self.pdf_listbox.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.pdf_listbox.yview)

        scrollbar_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=5, column=0, columnspan=3, sticky='ew')
        self.pdf_listbox.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.config(command=self.pdf_listbox.xview)

    def search_keyword_in_pdf(self, directory, keyword):
        matching_pdfs = []

        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory, filename)
                keyword_info = {"filename": filename, "pages": []}

                with open(file_path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)

                    for page_num in range(len(pdf_reader.pages)):
                        page_text = pdf_reader.pages[page_num].extract_text()
                        if keyword.lower() in page_text.lower():
                            print(f"Keyword '{keyword}' found in '{filename}', Page {page_num + 1}")
                            keyword_info["pages"].append(page_num + 1)

                if keyword_info["pages"]:
                    matching_pdfs.append(keyword_info)

        return matching_pdfs

    def browse_path(self):
        folder_selected = filedialog.askdirectory()
        self.path_var.set(folder_selected)

    def open_selected_pdf(self):
        selected_index = self.pdf_listbox.curselection()
        if selected_index:
            selected_pdf_info = self.pdf_listbox.get(selected_index)
            filename = selected_pdf_info.split(":")[0].strip()
            file_path = os.path.join(self.path_var.get(), filename)
            webbrowser.open(file_path)

    def start_search(self):
        self.pdf_listbox.delete(0, tk.END)
        path = self.path_var.get()
        keyword = self.keyword_var.get()
        matching_pdfs = self.search_keyword_in_pdf(path, keyword)

        for pdf_info in matching_pdfs:
            self.pdf_listbox.insert(tk.END, f"{pdf_info['filename']}: {', '.join(map(str, pdf_info['pages']))}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSearchTool(root)
    root.mainloop()
