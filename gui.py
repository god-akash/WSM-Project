import tkinter as tk
from tkinter import filedialog, messagebox
import os

from document_loader import load_documents
from tokenizer import tokenize
from normalizer import normalize
from inverted_index import build_index
from boolean_search import boolean_search


class SearchGUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Information Retrieval System")
        self.root.geometry("1000x720")
        self.root.minsize(850, 600)

        # -----------------------------------------
        # Colors
        # -----------------------------------------

        self.bg_color = "#0f172a"
        self.panel_color = "#1e293b"
        self.input_color = "#334155"
        self.text_color = "#f8fafc"
        self.secondary_text = "#94a3b8"
        self.accent_color = "#38bdf8"
        self.button_color = "#0284c7"
        self.highlight_color = "#fde047"

        self.root.configure(
            bg=self.bg_color
        )

        # -----------------------------------------
        # Data
        # -----------------------------------------

        self.documents = {}
        self.index = {}

        # -----------------------------------------
        # Load documents folder automatically
        # -----------------------------------------

        documents_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "documents"
        )

        if os.path.exists(documents_folder):

            try:
                self.documents = load_documents(
                    documents_folder
                )
            except Exception:
                self.documents = {}

        # -----------------------------------------
        # Build index
        # -----------------------------------------

        self.rebuild_index()

        # -----------------------------------------
        # Create GUI
        # -----------------------------------------

        self.create_gui()

    # =====================================================
    # GUI
    # =====================================================

    def create_gui(self):

        # -----------------------------------------
        # Header
        # -----------------------------------------

        header = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        title = tk.Label(
            header,
            text="INFORMATION RETRIEVAL",
            font=("Segoe UI", 24, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Search your documents quickly and accurately",
            font=("Segoe UI", 11),
            fg=self.secondary_text,
            bg=self.bg_color
        )

        subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        student_details = tk.Label(
            header,
            text="ASHOK BISWAL , B524018",
            font=("Segoe UI", 11),
            fg=self.secondary_text,
            bg=self.bg_color
        )

        student_details.pack(
            anchor="w",
            pady=(3, 0)
        )

        # -----------------------------------------
        # Search Panel
        # -----------------------------------------

        search_panel = tk.Frame(
            self.root,
            bg=self.panel_color
        )

        search_panel.pack(
            fill="x",
            padx=30,
            pady=15
        )

        search_label = tk.Label(
            search_panel,
            text="SEARCH",
            font=("Segoe UI", 9, "bold"),
            fg=self.accent_color,
            bg=self.panel_color
        )

        search_label.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        # -----------------------------------------
        # Search Row
        # -----------------------------------------

        search_row = tk.Frame(
            search_panel,
            bg=self.panel_color
        )

        search_row.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        self.search_entry = tk.Entry(
            search_row,
            font=("Segoe UI", 13),
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat"
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self.search_entry.insert(
            0,
            "Enter search query..."
        )

        self.search_entry.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.perform_search()
        )

        # Search button

        search_button = tk.Button(
            search_row,
            text="SEARCH",
            command=self.perform_search,
            font=("Segoe UI", 11, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8
        )

        search_button.pack(
            side="right"
        )

        # -----------------------------------------
        # Controls
        # -----------------------------------------

        controls = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=5
        )

        add_button = tk.Button(
            controls,
            text="Add Documents",
            command=self.add_documents,
            font=("Segoe UI", 10, "bold"),
            bg=self.panel_color,
            fg=self.text_color,
            activebackground=self.input_color,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        add_button.pack(
            side="left"
        )

        self.document_label = tk.Label(
            controls,
            text=f"  Documents: {len(self.documents)}",
            font=("Segoe UI", 10),
            fg=self.secondary_text,
            bg=self.bg_color
        )

        self.document_label.pack(
            side="left",
            padx=15
        )

        # -----------------------------------------
        # Results Header
        # -----------------------------------------

        results_header = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        results_header.pack(
            fill="x",
            padx=30,
            pady=(15, 5)
        )

        results_title = tk.Label(
            results_header,
            text="SEARCH RESULTS",
            font=("Segoe UI", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )

        results_title.pack(
            side="left"
        )

        self.result_count = tk.Label(
            results_header,
            text="",
            font=("Segoe UI", 10),
            fg=self.accent_color,
            bg=self.bg_color
        )

        self.result_count.pack(
            side="left",
            padx=10
        )

        # -----------------------------------------
        # Results Container
        # -----------------------------------------

        result_frame = tk.Frame(
            self.root,
            bg=self.panel_color
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 15)
        )

        scrollbar = tk.Scrollbar(
            result_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_area = tk.Text(
            result_frame,
            font=("Consolas", 11),
            bg=self.panel_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            selectbackground=self.accent_color,
            selectforeground="white",
            relief="flat",
            wrap="word",
            yscrollcommand=scrollbar.set,
            padx=20,
            pady=15
        )

        self.result_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.result_area.yview
        )

        # -----------------------------------------
        # Text Styles
        # -----------------------------------------

        self.result_area.tag_config(
            "highlight",
            background=self.highlight_color,
            foreground="#000000"
        )

        self.result_area.tag_config(
            "document",
            foreground=self.accent_color,
            font=("Segoe UI", 13, "bold")
        )

        self.result_area.tag_config(
            "info",
            foreground=self.secondary_text
        )

        self.result_area.tag_config(
            "separator",
            foreground="#475569"
        )

        self.result_area.tag_config(
            "position",
            foreground="#a78bfa"
        )

        # Read-only

        self.result_area.config(
            state="disabled"
        )

        # -----------------------------------------
        # Status Bar
        # -----------------------------------------

        status_bar = tk.Frame(
            self.root,
            bg="#020617",
            height=30
        )

        status_bar.pack(
            fill="x"
        )

        self.status_label = tk.Label(
            status_bar,
            text=f"Ready • {len(self.documents)} document(s) loaded",
            font=("Segoe UI", 9),
            fg="#22c55e",
            bg="#020617"
        )

        self.status_label.pack(
            side="left",
            padx=30,
            pady=5
        )

    # =====================================================
    # Placeholder
    # =====================================================

    def clear_placeholder(self, event):

        if self.search_entry.get() == "Enter search query...":

            self.search_entry.delete(
                0,
                tk.END
            )

    # =====================================================
    # Add Documents
    # =====================================================

    def add_documents(self):

        file_paths = filedialog.askopenfilenames(
            title="Select Documents",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if not file_paths:
            return

        added = 0

        for file_path in file_paths:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    content = file.read()

                filename = os.path.basename(
                    file_path
                )

                self.documents[filename] = content

                added += 1

            except Exception as error:

                messagebox.showerror(
                    "File Error",
                    f"Could not read:\n{file_path}\n\n{error}"
                )

        self.rebuild_index()

        self.document_label.config(
            text=f"  Documents: {len(self.documents)}"
        )

        self.status_label.config(
            text=f"● {added} document(s) added successfully",
            fg="#22c55e"
        )

    # =====================================================
    # Build Index
    # =====================================================

    def rebuild_index(self):

        self.index = build_index(
            self.documents,
            tokenize,
            normalize
        )

    # =====================================================
    # Search
    # =====================================================

    def perform_search(self):

        query = self.search_entry.get().strip()

        if query == "Enter search query...":
            query = ""

        if not query:

            messagebox.showwarning(
                "Search",
                "Please enter a search query."
            )

            return

        if not self.documents:

            messagebox.showwarning(
                "Documents",
                "No documents are available."
            )

            return

        # -----------------------------------------
        # Boolean / Wildcard / Normal Search
        # -----------------------------------------

        results = boolean_search(
            query,
            self.index,
            tokenize,
            normalize
        )

        words = query.split()

        if "AND" in words or "OR" in words:
            search_type = "Boolean Search"
        elif "*" in query or "?" in query:
            search_type = "Wildcard Search"
        else:
            search_type = "Normal Search"

        self.display_results(
            query,
            results,
            search_type
        )

    # =====================================================
    # Display Results
    # =====================================================

    def display_results(
        self,
        query,
        results,
        search_type
    ):

        self.result_area.config(
            state="normal"
        )

        self.result_area.delete(
            "1.0",
            tk.END
        )

        # -----------------------------------------
        # No Results
        # -----------------------------------------

        if not results:

            self.result_area.insert(
                tk.END,
                f'\n  No results found for "{query}".'
            )

            self.result_area.config(
                state="disabled"
            )

            self.result_count.config(
                text="• 0 results"
            )

            self.status_label.config(
                text="● No results found",
                fg="#ef4444"
            )

            return

        # -----------------------------------------
        # Result Count
        # -----------------------------------------

        self.result_count.config(
            text=f"• {len(results)} documents"
        )

        self.status_label.config(
            text=f"● {search_type} completed",
            fg="#22c55e"
        )

        # -----------------------------------------
        # Header
        # -----------------------------------------

        self.result_area.insert(
            tk.END,
            f'Query: "{query}"\n',
            "document"
        )

        self.result_area.insert(
            tk.END,
            f"Search Type: {search_type}\n\n",
            "info"
        )

        # -----------------------------------------
        # Documents
        # -----------------------------------------

        for document_name, positions in results.items():

            document_text = self.documents[
                document_name
            ]

            # Document name

            self.result_area.insert(
                tk.END,
                f"{document_name}\n",
                "document"
            )

            # Match count

            self.result_area.insert(
                tk.END,
                f"    Matches found: {len(positions)}\n\n",
                "info"
            )

            # -----------------------------------------
            # Position Information
            # -----------------------------------------

            for number, position in enumerate(
                positions,
                start=1
            ):

                self.result_area.insert(
                    tk.END,
                    f"    Match {number}  →  ",
                    "info"
                )

                self.result_area.insert(
                    tk.END,
                    f"Word Index: {position['word_index']}   "
                    f"Characters: {position['start']}-"
                    f"{position['end']}\n",
                    "position"
                )

            # -----------------------------------------
            # Full Document
            # -----------------------------------------

            self.result_area.insert(
                tk.END,
                "\n    FULL DOCUMENT\n",
                "document"
            )

            self.result_area.insert(
                tk.END,
                "    " + "-" * 70 + "\n",
                "separator"
            )

            # -----------------------------------------
            # INSERT DOCUMENT WITH HIGHLIGHTS
            # -----------------------------------------

            self.insert_highlighted_document(
                document_text,
                positions
            )

            # -----------------------------------------
            # Space
            # -----------------------------------------

            self.result_area.insert(
                tk.END,
                "\n\n"
            )

            self.result_area.insert(
                tk.END,
                "=" * 80 + "\n\n",
                "separator"
            )

        # -----------------------------------------
        # Read Only
        # -----------------------------------------

        self.result_area.config(
            state="disabled"
        )

        self.result_area.see(
            "1.0"
        )

    # =====================================================
    # Insert Document With Exact Highlights
    # =====================================================

    def insert_highlighted_document(
        self,
        document_text,
        positions
    ):

        # Sort matches by character position

        positions = sorted(
            positions,
            key=lambda position: position["start"]
        )

        current_position = 0

        for position in positions:

            start = position["start"]
            end = position["end"]

            # Safety check

            if start < current_position:
                continue

            # -----------------------------------------
            # Insert normal text before match
            # -----------------------------------------

            normal_text = document_text[
                current_position:start
            ]

            if normal_text:

                self.result_area.insert(
                    tk.END,
                    normal_text
                )

            # -----------------------------------------
            # Insert matching word with highlight
            # -----------------------------------------

            matched_text = document_text[
                start:end
            ]

            self.result_area.insert(
                tk.END,
                matched_text,
                "highlight"
            )

            # Move forward

            current_position = end

        # -----------------------------------------
        # Insert remaining text
        # -----------------------------------------

        remaining_text = document_text[
            current_position:
        ]

        if remaining_text:

            self.result_area.insert(
                tk.END,
                remaining_text
            )

    # =====================================================
    # Run
    # =====================================================

    def run(self):

        self.root.mainloop()