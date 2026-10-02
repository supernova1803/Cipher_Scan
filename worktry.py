import os
import sys
import time
import wave
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter, ImageTk
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

# ==============================================================================
# THEME DEFINITIONS
# ==============================================================================
THEMES = {
    "cyber_matrix": {
        "name": "🟢 Cyber Matrix",
        "bg_app": "#0a0f14",
        "bg_panel": "#101721",
        "bg_card": "#16202c",
        "bg_input": "#0c131a",
        "border": "#1e2e3d",
        "accent": "#00ff9d",
        "accent_hover": "#05e08a",
        "accent_fg": "#0a0f14",
        "btn_sec": "#1e2b3a",
        "btn_sec_hover": "#2a3b4e",
        "fg_primary": "#e6edf3",
        "fg_secondary": "#8b949e",
        "fg_accent": "#00ff9d",
        "scanner_color": "#00ff9d",
        "badge_bg": "#063826",
        "badge_fg": "#00ff9d",
        "success": "#00ff9d",
        "error": "#ff4d4f",
        "warning": "#faad14",
        "info": "#1890ff",
    },
    "deep_space": {
        "name": "🌌 Deep Space",
        "bg_app": "#080c14",
        "bg_panel": "#0f172a",
        "bg_card": "#1e293b",
        "bg_input": "#0b1220",
        "border": "#334155",
        "accent": "#38bdf8",
        "accent_hover": "#0ea5e9",
        "accent_fg": "#080c14",
        "btn_sec": "#26354a",
        "btn_sec_hover": "#364a66",
        "fg_primary": "#f8fafc",
        "fg_secondary": "#94a3b8",
        "fg_accent": "#38bdf8",
        "scanner_color": "#38bdf8",
        "badge_bg": "#0c4a6e",
        "badge_fg": "#7dd3fc",
        "success": "#34d399",
        "error": "#f87171",
        "warning": "#fbbf24",
        "info": "#38bdf8",
    },
    "dracula_synth": {
        "name": "🔮 Dracula Synth",
        "bg_app": "#12101a",
        "bg_panel": "#1d192b",
        "bg_card": "#28233a",
        "bg_input": "#171424",
        "border": "#3f3659",
        "accent": "#c084fc",
        "accent_hover": "#a855f7",
        "accent_fg": "#12101a",
        "btn_sec": "#352e4d",
        "btn_sec_hover": "#473e66",
        "fg_primary": "#f5f3ff",
        "fg_secondary": "#c4b5fd",
        "fg_accent": "#f472b6",
        "scanner_color": "#f472b6",
        "badge_bg": "#4c1d95",
        "badge_fg": "#e9d5ff",
        "success": "#4ade80",
        "error": "#fb7185",
        "warning": "#fde047",
        "info": "#a78bfa",
    },
    "nordic_frost": {
        "name": "❄️ Nordic Frost",
        "bg_app": "#191e24",
        "bg_panel": "#22272e",
        "bg_card": "#2d333b",
        "bg_input": "#1c2127",
        "border": "#444c56",
        "accent": "#88c0d0",
        "accent_hover": "#81a1c1",
        "accent_fg": "#191e24",
        "btn_sec": "#373e47",
        "btn_sec_hover": "#444c56",
        "fg_primary": "#adbac7",
        "fg_secondary": "#768390",
        "fg_accent": "#88c0d0",
        "scanner_color": "#88c0d0",
        "badge_bg": "#1c3847",
        "badge_fg": "#88c0d0",
        "success": "#a3be8c",
        "error": "#bf616a",
        "warning": "#ebcb8b",
        "info": "#88c0d0",
    },
    "amber_sunset": {
        "name": "🔥 Amber Sunset",
        "bg_app": "#14100c",
        "bg_panel": "#1f1813",
        "bg_card": "#2b221a",
        "bg_input": "#17120e",
        "border": "#45362a",
        "accent": "#f59e0b",
        "accent_hover": "#d97706",
        "accent_fg": "#14100c",
        "btn_sec": "#3a2d22",
        "btn_sec_hover": "#4d3c2e",
        "fg_primary": "#fef3c7",
        "fg_secondary": "#d5b48c",
        "fg_accent": "#fbbf24",
        "scanner_color": "#f59e0b",
        "badge_bg": "#451a03",
        "badge_fg": "#fcd34d",
        "success": "#34d399",
        "error": "#f87171",
        "warning": "#fbbf24",
        "info": "#60a5fa",
    },
    "clean_light": {
        "name": "☀️ Modern Light",
        "bg_app": "#f1f5f9",
        "bg_panel": "#e2e8f0",
        "bg_card": "#ffffff",
        "bg_input": "#f8fafc",
        "border": "#cbd5e1",
        "accent": "#2563eb",
        "accent_hover": "#1d4ed8",
        "accent_fg": "#ffffff",
        "btn_sec": "#e2e8f0",
        "btn_sec_hover": "#cbd5e1",
        "fg_primary": "#0f172a",
        "fg_secondary": "#475569",
        "fg_accent": "#2563eb",
        "scanner_color": "#2563eb",
        "badge_bg": "#dbeafe",
        "badge_fg": "#1e40af",
        "success": "#059669",
        "error": "#dc2626",
        "warning": "#d97706",
        "info": "#2563eb",
    },
}

# ==============================================================================
# CRYPTOGRAPHIC & STEGANOGRAPHIC CORE ENGINE
# ==============================================================================

def extract_text_from_image(image_path):
    """Extract hidden LSB & MSB messages from image pixels."""
    try:
        image = Image.open(image_path).convert("RGB")
        binary_message_lsb = ""
        binary_message_msb = ""

        pixels = image.getdata()
        for pixel_index, pixel in enumerate(pixels):
            if pixel_index >= 12000:
                break
            for channel in range(3):
                binary_message_lsb += str(pixel[channel] & 1)
                binary_message_msb += str((pixel[channel] >> 7) & 1)

        def binary_to_text(binary_data, max_chars=400):
            message = ""
            for i in range(0, len(binary_data) - 7, 8):
                byte = binary_data[i:i + 8]
                char = chr(int(byte, 2))
                if char.isprintable():
                    message += char
                elif char in ('\n', '\r', '\t'):
                    message += char
                if len(message) >= max_chars:
                    break
            return message.strip()

        message_lsb = binary_to_text(binary_message_lsb) or "No readable plaintext detected in LSB."
        message_msb = binary_to_text(binary_message_msb) or "No readable plaintext detected in MSB."
        return message_lsb, message_msb
    except Exception as e:
        raise RuntimeError(f"Error during image stego analysis: {e}")

def extract_data_from_image(image_path):
    """Extract hidden metadata / chunk tags from image."""
    try:
        image = Image.open(image_path)
        metadata = image.info
        if "HiddenData" in metadata:
            return metadata["HiddenData"]
        elif metadata:
            # Fallback to general metadata info
            summary = "\n".join([f"{k}: {v}" for k, v in metadata.items() if len(str(v)) < 150])
            if summary:
                return f"Embedded Image Info:\n{summary}"
        raise ValueError("No steganographic 'HiddenData' tag found in image metadata.")
    except Exception as e:
        raise ValueError(f"Error extracting metadata from image: {e}")

def save_data_to_pdf(data, output_pdf_path):
    """Save extracted text data to a PDF report."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        safe_data = str(data).encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 8, safe_data)
        pdf.output(output_pdf_path)
        return True, f"Report successfully generated at:\n{output_pdf_path}"
    except Exception as e:
        return False, f"Error saving PDF report: {e}"

def find_watermark_without_cv2(image_path):
    """Detect potential watermark regions via edge filter & contrast enhancement."""
    try:
        img = Image.open(image_path).convert("L")
        enhanced_img = ImageEnhance.Contrast(img).enhance(2.2)
        edges = enhanced_img.filter(ImageFilter.FIND_EDGES)

        draw = ImageDraw.Draw(edges)
        width, height = edges.size
        pixel_data = edges.load()

        step = max(5, min(width, height) // 80)
        detected_count = 0
        for x in range(0, width, step):
            for y in range(0, height, step):
                if pixel_data[x, y] > 205:
                    detected_count += 1
                    draw.rectangle([(x - 4, y - 4), (x + 4, y + 4)], outline=255)

        info_msg = (
            f"Edge analysis complete.\n"
            f"Image dimensions: {width}x{height} px\n"
            f"Flagged anomaly clusters: {detected_count} regions."
        )
        return edges, info_msg
    except Exception as e:
        return None, f"Error processing watermark: {e}"

def extract_message_from_pdf(pdf_path):
    """Extract standard metadata and steganographic /Message tags from PDF."""
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        pages_count = len(reader.pages)

        result = [f"=== PDF METADATA ANALYSIS REPORT ==="]
        result.append(f"Total Pages: {pages_count}")
        result.append(f"File: {os.path.basename(pdf_path)}\n")

        if metadata:
            result.append("Standard Metadata Fields:")
            for key, value in metadata.items():
                result.append(f"  • {key}: {value}")
            if '/Message' in metadata:
                result.append(f"\n[!] HIDDEN MESSAGE DETECTED in /Message:")
                result.append(f"  >>> {metadata['/Message']} <<<")
            else:
                result.append("\n[*] No custom '/Message' stego key identified.")
        else:
            result.append("No metadata dictionary present in this PDF.")

        return "\n".join(result)
    except Exception as e:
        return f"Error extracting PDF metadata: {e}"

def remove_metadata_from_pdf(pdf_path, save_dir):
    """Sanitize and strip all metadata from PDF."""
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        writer.add_metadata({})  # Strip all metadata
        for page in reader.pages:
            writer.add_page(page)

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        cleaned_pdf_path = os.path.join(save_dir, f"{base_name}_Sanitized.pdf")
        with open(cleaned_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        return cleaned_pdf_path
    except Exception as e:
        return f"Error sanitizing PDF metadata: {e}"

def decode_text_from_audio(wav_file):
    """Decode LSB steganographic data from audio WAV frames."""
    try:
        audio = wave.open(wav_file, 'rb')
        params = audio.getparams()
        n_frames = min(params.nframes, 100000)
        frames = audio.readframes(n_frames)
        audio.close()

        # Extract least significant bits
        bits = [str(b & 1) for b in frames]
        binary_data = "".join(bits)

        message = ""
        for i in range(0, len(binary_data) - 7, 8):
            byte = binary_data[i:i + 8]
            val = int(byte, 2)
            if val == 0 and len(message) > 0:
                break
            if 32 <= val <= 126 or val in (10, 13, 9):
                message += chr(val)
            if len(message) >= 1000:
                break

        stats = (
            f"Channels: {params.nchannels} | "
            f"Sample Rate: {params.framerate} Hz | "
            f"Total Frames: {params.nframes}\n"
        )

        clean_text = message.strip()
        if not clean_text:
            return stats + "No readable plaintext identified in audio LSB stream."
        return stats + f"Decoded Content:\n{clean_text}"
    except Exception as e:
        raise RuntimeError(f"Error decoding audio: {e}")

def get_file_stats(file_path):
    """Return formatted file size and filename."""
    if not file_path or not os.path.exists(file_path):
        return "No file selected", ""
    name = os.path.basename(file_path)
    size_bytes = os.path.getsize(file_path)
    if size_bytes < 1024:
        sz = f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        sz = f"{size_bytes / 1024:.1f} KB"
    else:
        sz = f"{size_bytes / (1024 * 1024):.2f} MB"
    return name, sz

# ==============================================================================
# ANIMATED UI WIDGETS (SCANNER, TOAST, MODAL, BUTTONS)
# ==============================================================================

class AnimatedScanner(tk.Canvas):
    """High-tech cyberpunk animated radar/laser sweep indicator."""
    def __init__(self, parent, theme, height=4, **kwargs):
        super().__init__(parent, height=height, bg=theme["bg_card"], highlightthickness=0, **kwargs)
        self.theme = theme
        self.is_scanning = False
        self.pos = 0
        self.dir = 1
        self.speed = 10
        self.bar_width = 80
        self.line_id = None

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme["bg_card"])

    def start(self):
        if not self.is_scanning:
            self.is_scanning = True
            self.pos = 0
            self.dir = 1
            self._animate()

    def stop(self):
        self.is_scanning = False
        self.delete("all")

    def _animate(self):
        if not self.is_scanning:
            return
        width = self.winfo_width() or 400
        self.delete("all")

        # Draw glowing sweep
        x0 = self.pos
        x1 = self.pos + self.bar_width
        self.create_line(x0, 2, x1, 2, fill=self.theme["scanner_color"], width=3)
        self.create_oval(x1 - 3, 0, x1 + 3, 4, fill=self.theme["accent"], outline="")

        self.pos += self.speed * self.dir
        if self.pos + self.bar_width >= width:
            self.dir = -1
        elif self.pos <= 0:
            self.dir = 1

        self.after(25, self._animate)


class ToastManager:
    """Floating animated toast notification banner."""
    def __init__(self, root):
        self.root = root
        self.active_toast = None
        self.anim_step = 0

    def show(self, title, message, toast_type="info", theme=None):
        if self.active_toast:
            try:
                self.active_toast.destroy()
            except Exception:
                pass

        if theme is None:
            theme = THEMES["cyber_matrix"]

        color_map = {
            "success": theme.get("success", "#00ff9d"),
            "error": theme.get("error", "#ff4d4f"),
            "warning": theme.get("warning", "#faad14"),
            "info": theme.get("info", "#38bdf8"),
        }
        accent_c = color_map.get(toast_type, theme["accent"])

        icon_map = {
            "success": "✓",
            "error": "✕",
            "warning": "⚠",
            "info": "ℹ",
        }
        icon_str = icon_map.get(toast_type, "ℹ")

        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(bg=theme["border"])

        container = tk.Frame(toast, bg=theme["bg_card"], bd=0, padx=12, pady=10)
        container.pack(padx=1, pady=1, fill="both", expand=True)

        # Left accent stripe & icon
        icon_badge = tk.Label(
            container, text=icon_str, font=("Segoe UI", 12, "bold"),
            bg=accent_c, fg=theme["bg_app"], width=3, pady=2
        )
        icon_badge.pack(side="left", padx=(0, 10))

        content_box = tk.Frame(container, bg=theme["bg_card"])
        content_box.pack(side="left", fill="both", expand=True)

        t_lbl = tk.Label(
            content_box, text=title, font=("Segoe UI", 10, "bold"),
            bg=theme["bg_card"], fg=accent_c, anchor="w"
        )
        t_lbl.pack(fill="x")

        m_lbl = tk.Label(
            content_box, text=message, font=("Segoe UI", 9),
            bg=theme["bg_card"], fg=theme["fg_primary"], anchor="w", wraplength=280
        )
        m_lbl.pack(fill="x")

        close_btn = tk.Label(
            container, text="×", font=("Segoe UI", 14),
            bg=theme["bg_card"], fg=theme["fg_secondary"], cursor="hand2"
        )
        close_btn.pack(side="right", padx=(8, 0))
        close_btn.bind("<Button-1>", lambda e: self._dismiss_toast(toast))

        self.active_toast = toast
        toast.update_idletasks()

        # Calculate coordinates
        w = max(320, container.winfo_reqwidth() + 10)
        h = max(60, container.winfo_reqheight() + 5)
        rx = self.root.winfo_rootx() + self.root.winfo_width() - w - 24
        final_y = self.root.winfo_rooty() + 65
        start_y = final_y - 20

        toast.geometry(f"{w}x{h}+{rx}+{start_y}")
        self._slide_in(toast, rx, start_y, final_y, 0)
        self.root.after(3500, lambda: self._dismiss_toast(toast))

    def _slide_in(self, toast, x, cur_y, target_y, step):
        if not toast or not toast.winfo_exists():
            return
        if cur_y < target_y:
            next_y = min(cur_y + 4, target_y)
            toast.geometry(f"+{x}+{next_y}")
            self.root.after(16, lambda: self._slide_in(toast, x, next_y, target_y, step + 1))

    def _dismiss_toast(self, toast):
        if toast and toast.winfo_exists():
            try:
                toast.destroy()
            except Exception:
                pass
            if self.active_toast == toast:
                self.active_toast = None


class ModernModal:
    """Beautiful custom dialog with theme styling and animations."""
    @staticmethod
    def show(parent, title, message, category="info", details=None, theme=None, on_action=None, action_label=None):
        if theme is None:
            theme = THEMES["cyber_matrix"]

        modal = tk.Toplevel(parent)
        modal.title(title)
        modal.transient(parent)
        modal.grab_set()
        modal.attributes("-topmost", True)
        modal.configure(bg=theme["border"])

        # Determine category colors & symbols
        cat_configs = {
            "success": {"icon": "✓", "color": theme.get("success", "#00ff9d"), "tag": "SUCCESS"},
            "error": {"icon": "✕", "color": theme.get("error", "#ff4d4f"), "tag": "ERROR OCCURRED"},
            "warning": {"icon": "⚠", "color": theme.get("warning", "#faad14"), "tag": "WARNING"},
            "info": {"icon": "ℹ", "color": theme.get("info", "#38bdf8"), "tag": "INFORMATION"},
        }
        cfg = cat_configs.get(category, cat_configs["info"])

        frame = tk.Frame(modal, bg=theme["bg_card"], bd=0, padx=24, pady=20)
        frame.pack(padx=2, pady=2, fill="both", expand=True)

        # Header with category badge
        hdr_frame = tk.Frame(frame, bg=theme["bg_card"])
        hdr_frame.pack(fill="x", pady=(0, 15))

        badge = tk.Label(
            hdr_frame, text=f" {cfg['icon']} {cfg['tag']} ",
            font=("Segoe UI", 9, "bold"),
            bg=theme["bg_input"], fg=cfg["color"], bd=1, relief="solid"
        )
        badge.pack(side="left")

        title_lbl = tk.Label(
            hdr_frame, text=f"  {title}",
            font=("Segoe UI", 13, "bold"),
            bg=theme["bg_card"], fg=theme["fg_primary"]
        )
        title_lbl.pack(side="left")

        # Message
        msg_lbl = tk.Label(
            frame, text=message, font=("Segoe UI", 10),
            bg=theme["bg_card"], fg=theme["fg_primary"],
            justify="left", wraplength=460
        )
        msg_lbl.pack(fill="x", pady=(0, 15))

        # Optional Details text
        if details:
            details_frame = tk.Frame(frame, bg=theme["bg_input"], bd=1, relief="solid")
            details_frame.pack(fill="both", expand=True, pady=(0, 15))

            details_txt = tk.Text(
                details_frame, height=5, width=50,
                bg=theme["bg_input"], fg=theme["fg_secondary"],
                font=("Consolas", 9), relief="flat", wrap="word"
            )
            details_txt.insert("1.0", details)
            details_txt.configure(state="disabled")
            details_txt.pack(padx=8, pady=8, fill="both", expand=True)

        # Action Buttons
        btn_bar = tk.Frame(frame, bg=theme["bg_card"])
        btn_bar.pack(fill="x", pady=(5, 0))

        if on_action and action_label:
            act_btn = tk.Button(
                btn_bar, text=action_label, font=("Segoe UI", 10, "bold"),
                bg=theme["accent"], fg=theme["accent_fg"],
                activebackground=theme["accent_hover"],
                relief="flat", bd=0, padx=16, pady=6, cursor="hand2",
                command=lambda: [modal.destroy(), on_action()]
            )
            act_btn.pack(side="right", padx=(8, 0))

        close_btn = tk.Button(
            btn_bar, text="Dismiss", font=("Segoe UI", 10),
            bg=theme["btn_sec"], fg=theme["fg_primary"],
            activebackground=theme["btn_sec_hover"],
            relief="flat", bd=0, padx=16, pady=6, cursor="hand2",
            command=modal.destroy
        )
        close_btn.pack(side="right")

        # Copy button
        def copy_msg():
            parent.clipboard_clear()
            parent.clipboard_append(f"{message}\n{details or ''}")
            copy_btn.configure(text="Copied!")

        copy_btn = tk.Button(
            btn_bar, text="📋 Copy", font=("Segoe UI", 9),
            bg=theme["bg_input"], fg=theme["fg_secondary"],
            relief="flat", bd=0, padx=10, pady=5, cursor="hand2",
            command=copy_msg
        )
        copy_btn.pack(side="left")

        # Center modal on parent
        modal.update_idletasks()
        mw = max(480, frame.winfo_reqwidth() + 20)
        mh = frame.winfo_reqheight() + 20
        px = parent.winfo_rootx() + (parent.winfo_width() // 2) - (mw // 2)
        py = parent.winfo_rooty() + (parent.winfo_height() // 2) - (mh // 2)
        modal.geometry(f"{mw}x{mh}+{max(10, px)}+{max(10, py)}")


def create_styled_button(parent, text, command, theme, is_primary=False, icon="", padx=16, pady=8):
    """Create a modern hover-reactive button with micro-animations."""
    if is_primary:
        bg = theme["accent"]
        fg = theme["accent_fg"]
        hover_bg = theme["accent_hover"]
        font = ("Segoe UI", 10, "bold")
    else:
        bg = theme["btn_sec"]
        fg = theme["fg_primary"]
        hover_bg = theme["btn_sec_hover"]
        font = ("Segoe UI", 10)

    btn_text = f"{icon}  {text}".strip() if icon else text
    btn = tk.Button(
        parent, text=btn_text, command=command, font=font,
        bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
        relief="flat", bd=0, padx=padx, pady=pady, cursor="hand2"
    )

    def on_enter(e):
        btn.configure(bg=hover_bg)

    def on_leave(e):
        btn.configure(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn._base_bg = bg
    btn._hover_bg = hover_bg
    btn._is_primary = is_primary
    return btn


# ==============================================================================
# MAIN APPLICATION GUI CLASS
# ==============================================================================

class CombinedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CIPHERSCAN // Advanced Cryptographic & Steganographic Suite")
        self.root.geometry("1280x760")
        self.root.minsize(1024, 620)

        # Application state
        self.current_theme_key = "cyber_matrix"
        self.theme = THEMES[self.current_theme_key]
        self.is_fullscreen = False

        # Loaded File Paths
        self.image_path = None
        self.pdf_path = None
        self.watermark_image_path = None
        self.audio_path = None

        # Processed Watermark Image Cache
        self.watermarked_image_obj = None

        # Toast notification system
        self.toast_mgr = ToastManager(self.root)

        # Pulse animation state
        self.pulse_phase = 0

        # Build UI Architecture
        self._init_styles()
        self._create_header()
        self._create_navigation()
        self._create_content_area()
        self._create_status_bar()

        # Keyboard shortcuts
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<Control-q>", lambda e: self.exit_app())

        # Start header pulse animation
        self._pulse_status_orb()

        # Switch to first tab by default
        self.select_tab("hub")

    def _init_styles(self):
        self.root.configure(bg=self.theme["bg_app"])

    # --------------------------------------------------------------------------
    # HEADER SECTION
    # --------------------------------------------------------------------------
    def _create_header(self):
        self.header_frame = tk.Frame(self.root, bg=self.theme["bg_panel"], height=60, bd=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        # Left: App Logo & Branding
        left_box = tk.Frame(self.header_frame, bg=self.theme["bg_panel"])
        left_box.pack(side="left", padx=20, fill="y")

        self.logo_lbl = tk.Label(
            left_box, text="🛡️ CIPHERSCAN", font=("Segoe UI", 15, "bold"),
            bg=self.theme["bg_panel"], fg=self.theme["accent"]
        )
        self.logo_lbl.pack(side="left")

        self.badge_lbl = tk.Label(
            left_box, text=" v2.5 PRO ", font=("Segoe UI", 8, "bold"),
            bg=self.theme["badge_bg"], fg=self.theme["badge_fg"]
        )
        self.badge_lbl.pack(side="left", padx=(10, 0))

        # Center/Left: Animated Status Indicator
        self.pulse_canvas = tk.Canvas(left_box, width=16, height=16, bg=self.theme["bg_panel"], highlightthickness=0)
        self.pulse_canvas.pack(side="left", padx=(16, 4))
        self.pulse_dot = self.pulse_canvas.create_oval(3, 3, 13, 13, fill=self.theme["accent"], outline="")

        self.status_header_lbl = tk.Label(
            left_box, text="READY", font=("Segoe UI", 9, "bold"),
            bg=self.theme["bg_panel"], fg=self.theme["fg_secondary"]
        )
        self.status_header_lbl.pack(side="left")

        # Right: Quick Controls (Theme Selector, Fullscreen, Info, Exit)
        right_box = tk.Frame(self.header_frame, bg=self.theme["bg_panel"])
        right_box.pack(side="right", padx=15, fill="y")

        # Theme Selector Dropdown Button
        theme_names = [cfg["name"] for cfg in THEMES.values()]
        self.theme_var = tk.StringVar(value=self.theme["name"])

        self.theme_menu_btn = tk.Menubutton(
            right_box, text=f"🎨 {self.theme['name']} ▾", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            activebackground=self.theme["btn_sec_hover"],
            relief="flat", bd=0, padx=12, pady=6, cursor="hand2"
        )
        self.theme_menu = tk.Menu(self.theme_menu_btn, tearoff=False, bg=self.theme["bg_card"], fg=self.theme["fg_primary"])
        for key, t_data in THEMES.items():
            self.theme_menu.add_command(
                label=t_data["name"],
                command=lambda k=key: self.apply_theme(k)
            )
        self.theme_menu_btn["menu"] = self.theme_menu
        self.theme_menu_btn.pack(side="left", padx=5)

        self.fs_btn = tk.Button(
            right_box, text="⛶ Fullscreen", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=10, pady=6, cursor="hand2",
            command=self.toggle_fullscreen
        )
        self.fs_btn.pack(side="left", padx=5)

        self.info_btn = tk.Button(
            right_box, text="ℹ️ About", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=10, pady=6, cursor="hand2",
            command=self.show_about_modal
        )
        self.info_btn.pack(side="left", padx=5)

        # Header border line
        self.header_divider = tk.Frame(self.root, bg=self.theme["border"], height=1)
        self.header_divider.pack(fill="x", side="top")

    # --------------------------------------------------------------------------
    # NAVIGATION BAR
    # --------------------------------------------------------------------------
    def _create_navigation(self):
        self.nav_frame = tk.Frame(self.root, bg=self.theme["bg_app"], height=48)
        self.nav_frame.pack(fill="x", side="top", padx=20, pady=(10, 5))
        self.nav_frame.pack_propagate(False)

        self.nav_buttons = {}
        tabs = [
            ("hub", "⚡ Dashboard Hub"),
            ("image", "🖼️ Image Stego"),
            ("pdf", "📄 PDF Metadata"),
            ("watermark", "🔍 Watermark Scan"),
            ("audio", "🎙️ Audio Stego"),
        ]

        for tab_id, tab_label in tabs:
            btn = tk.Button(
                self.nav_frame, text=tab_label, font=("Segoe UI", 10, "bold"),
                relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
                command=lambda t=tab_id: self.select_tab(t)
            )
            btn.pack(side="left", padx=(0, 8))
            self.nav_buttons[tab_id] = btn

    # --------------------------------------------------------------------------
    # CONTENT AREA & TABS
    # --------------------------------------------------------------------------
    def _create_content_area(self):
        self.content_container = tk.Frame(self.root, bg=self.theme["bg_app"])
        self.content_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Individual tab views
        self.tab_views = {}
        self.tab_views["hub"] = self._build_hub_view(self.content_container)
        self.tab_views["image"] = self._build_image_view(self.content_container)
        self.tab_views["pdf"] = self._build_pdf_view(self.content_container)
        self.tab_views["watermark"] = self._build_watermark_view(self.content_container)
        self.tab_views["audio"] = self._build_audio_view(self.content_container)

    # --------------------------------------------------------------------------
    # TAB 1: DASHBOARD HUB VIEW
    # --------------------------------------------------------------------------
    def _build_hub_view(self, parent):
        view = tk.Frame(parent, bg=self.theme["bg_app"])

        # Hero Banner
        hero = tk.Frame(view, bg=self.theme["bg_card"], padx=24, pady=20)
        hero.pack(fill="x", pady=(5, 15))

        tk.Label(
            hero, text="CipherScan Cryptographic & Forensics Suite",
            font=("Segoe UI", 16, "bold"), bg=self.theme["bg_card"], fg=self.theme["accent"]
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="Comprehensive digital forensics platform for Steganography Detection, PDF Sanitization, Watermark Analysis, and Audio LSB Decoding.",
            font=("Segoe UI", 10), bg=self.theme["bg_card"], fg=self.theme["fg_secondary"]
        ).pack(anchor="w", pady=(4, 0))

        # Grid of tool cards
        cards_container = tk.Frame(view, bg=self.theme["bg_app"])
        cards_container.pack(fill="both", expand=True)

        tools = [
            {
                "id": "image",
                "title": "🖼️ Image Steganography",
                "desc": "Extract hidden text from Least & Most Significant Bits (LSB/MSB) and inspect embedded metadata tags.",
                "badge": "PNG / JPG",
                "btn_text": "Launch Image Analyzer"
            },
            {
                "id": "pdf",
                "title": "📄 PDF Metadata & Sanitizer",
                "desc": "Inspect hidden /Message stego payload keys, read PDF headers, and wipe all tracking metadata.",
                "badge": "PDF Forensics",
                "btn_text": "Launch PDF Inspector"
            },
            {
                "id": "watermark",
                "title": "🔍 Watermark & Edge Scanner",
                "desc": "Analyze high-contrast edge frequencies to pinpoint watermarks, digital stamps, and anomalous markings.",
                "badge": "Computer Vision",
                "btn_text": "Launch Watermark Tool"
            },
            {
                "id": "audio",
                "title": "🎙️ Audio Steganography",
                "desc": "Inspect WAV audio frames to decode LSB encoded secrets, payloads, and covert messages.",
                "badge": "WAV 16-bit",
                "btn_text": "Launch Audio Decoder"
            },
        ]

        # 2x2 Grid Layout
        for i, tool in enumerate(tools):
            r = i // 2
            c = i % 2

            card = tk.Frame(cards_container, bg=self.theme["bg_card"], bd=1, relief="solid", padx=20, pady=18)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            cards_container.grid_columnconfigure(c, weight=1)
            cards_container.grid_rowconfigure(r, weight=1)

            top_row = tk.Frame(card, bg=self.theme["bg_card"])
            top_row.pack(fill="x")

            tk.Label(
                top_row, text=tool["title"], font=("Segoe UI", 12, "bold"),
                bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
            ).pack(side="left")

            tk.Label(
                top_row, text=f" {tool['badge']} ", font=("Segoe UI", 8, "bold"),
                bg=self.theme["badge_bg"], fg=self.theme["badge_fg"]
            ).pack(side="right")

            tk.Label(
                card, text=tool["desc"], font=("Segoe UI", 9),
                bg=self.theme["bg_card"], fg=self.theme["fg_secondary"],
                wraplength=440, justify="left"
            ).pack(anchor="w", pady=(10, 16))

            btn = create_styled_button(
                card, tool["btn_text"],
                lambda tid=tool["id"]: self.select_tab(tid),
                self.theme, is_primary=False, icon="→"
            )
            btn.pack(anchor="w")

        return view

    # --------------------------------------------------------------------------
    # TAB 2: IMAGE STEGANOGRAPHY VIEW
    # --------------------------------------------------------------------------
    def _build_image_view(self, parent):
        view = tk.Frame(parent, bg=self.theme["bg_app"])

        # Split: Left Controls, Right Output Terminal
        left = tk.Frame(view, bg=self.theme["bg_card"], width=420, bd=1, relief="solid", padx=18, pady=16)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(view, bg=self.theme["bg_card"], bd=1, relief="solid", padx=16, pady=16)
        right.pack(side="right", fill="both", expand=True)

        # Left: Header
        tk.Label(
            left, text="🖼️ Image Stego Inspector", font=("Segoe UI", 13, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(anchor="w")

        tk.Label(
            left, text="Inspect LSB/MSB bits & embedded stego data", font=("Segoe UI", 9),
            bg=self.theme["bg_card"], fg=self.theme["fg_secondary"]
        ).pack(anchor="w", pady=(2, 12))

        # File Dropzone Card
        self.img_dropzone = tk.Frame(left, bg=self.theme["bg_input"], bd=1, relief="solid", padx=12, pady=14)
        self.img_dropzone.pack(fill="x", pady=(0, 12))

        self.img_file_lbl = tk.Label(
            self.img_dropzone, text="No image selected", font=("Segoe UI", 10, "bold"),
            bg=self.theme["bg_input"], fg=self.theme["fg_primary"], wraplength=340
        )
        self.img_file_lbl.pack(pady=(0, 4))

        self.img_meta_lbl = tk.Label(
            self.img_dropzone, text="Supports PNG, JPG, BMP", font=("Segoe UI", 8),
            bg=self.theme["bg_input"], fg=self.theme["fg_secondary"]
        )
        self.img_meta_lbl.pack()

        # Image Thumbnail Preview Box
        self.img_preview_box = tk.Label(
            left, text="[ Image Preview ]", font=("Segoe UI", 9),
            bg=self.theme["bg_input"], fg=self.theme["fg_secondary"],
            height=6, bd=1, relief="solid"
        )
        self.img_preview_box.pack(fill="x", pady=(0, 12))

        # Action Buttons
        b1 = create_styled_button(left, "Choose Image", self.choose_image, self.theme, is_primary=True, icon="📂")
        b1.pack(fill="x", pady=4)

        b2 = create_styled_button(left, "Analyze LSB & MSB Bits", self.run_image_analysis, self.theme, is_primary=False, icon="⚡")
        b2.pack(fill="x", pady=4)

        b3 = create_styled_button(left, "Extract Metadata / HiddenData", self.extract_image_metadata, self.theme, is_primary=False, icon="🏷️")
        b3.pack(fill="x", pady=4)

        # Right: Terminal Results Card
        top_bar = tk.Frame(right, bg=self.theme["bg_card"])
        top_bar.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_bar, text="Console Output", font=("Segoe UI", 12, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(side="left")

        # Action tools on top right
        tools_f = tk.Frame(top_bar, bg=self.theme["bg_card"])
        tools_f.pack(side="right")

        tk.Button(
            tools_f, text="📋 Copy", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.copy_console(self.image_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="💾 Export PDF", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.export_console_to_pdf(self.image_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="🧹 Clear", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.clear_console(self.image_result_text)
        ).pack(side="left", padx=3)

        # Scanner bar
        self.img_scanner = AnimatedScanner(right, self.theme)
        self.img_scanner.pack(fill="x", pady=(0, 8))

        # Styled Text Box
        txt_frame = tk.Frame(right, bg=self.theme["bg_input"], bd=1, relief="solid")
        txt_frame.pack(fill="both", expand=True)

        self.image_result_text = tk.Text(
            txt_frame, wrap="word", bg=self.theme["bg_input"], fg=self.theme["fg_primary"],
            font=("Consolas", 10), relief="flat", padx=10, pady=10, insertbackground=self.theme["accent"]
        )
        self.image_result_text.pack(fill="both", expand=True)
        self._log(self.image_result_text, "CipherScan Image Steganography Engine Initialized.\nSelect an image to begin bit-level inspection.\n")

        return view

    # --------------------------------------------------------------------------
    # TAB 3: PDF METADATA ANALYSIS VIEW
    # --------------------------------------------------------------------------
    def _build_pdf_view(self, parent):
        view = tk.Frame(parent, bg=self.theme["bg_app"])

        left = tk.Frame(view, bg=self.theme["bg_card"], width=420, bd=1, relief="solid", padx=18, pady=16)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(view, bg=self.theme["bg_card"], bd=1, relief="solid", padx=16, pady=16)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            left, text="📄 PDF Forensics & Sanitizer", font=("Segoe UI", 13, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(anchor="w")

        tk.Label(
            left, text="Audit hidden metadata tags & scrub tracking records", font=("Segoe UI", 9),
            bg=self.theme["bg_card"], fg=self.theme["fg_secondary"]
        ).pack(anchor="w", pady=(2, 12))

        self.pdf_dropzone = tk.Frame(left, bg=self.theme["bg_input"], bd=1, relief="solid", padx=12, pady=16)
        self.pdf_dropzone.pack(fill="x", pady=(0, 16))

        self.pdf_file_lbl = tk.Label(
            self.pdf_dropzone, text="No PDF selected", font=("Segoe UI", 10, "bold"),
            bg=self.theme["bg_input"], fg=self.theme["fg_primary"], wraplength=340
        )
        self.pdf_file_lbl.pack(pady=(0, 4))

        self.pdf_meta_lbl = tk.Label(
            self.pdf_dropzone, text="Supports *.pdf documents", font=("Segoe UI", 8),
            bg=self.theme["bg_input"], fg=self.theme["fg_secondary"]
        )
        self.pdf_meta_lbl.pack()

        # Action Buttons
        b1 = create_styled_button(left, "Choose PDF File", self.choose_pdf, self.theme, is_primary=True, icon="📂")
        b1.pack(fill="x", pady=4)

        b2 = create_styled_button(left, "Scan PDF Metadata & Keys", self.run_pdf_analysis, self.theme, is_primary=False, icon="🔍")
        b2.pack(fill="x", pady=4)

        b3 = create_styled_button(left, "Sanitize & Strip Metadata", self.remove_pdf_metadata, self.theme, is_primary=False, icon="🛡️")
        b3.pack(fill="x", pady=4)

        # Right: Terminal
        top_bar = tk.Frame(right, bg=self.theme["bg_card"])
        top_bar.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_bar, text="PDF Forensics Log", font=("Segoe UI", 12, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(side="left")

        tools_f = tk.Frame(top_bar, bg=self.theme["bg_card"])
        tools_f.pack(side="right")

        tk.Button(
            tools_f, text="📋 Copy", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.copy_console(self.pdf_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="💾 Export PDF", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.export_console_to_pdf(self.pdf_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="🧹 Clear", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.clear_console(self.pdf_result_text)
        ).pack(side="left", padx=3)

        self.pdf_scanner = AnimatedScanner(right, self.theme)
        self.pdf_scanner.pack(fill="x", pady=(0, 8))

        txt_frame = tk.Frame(right, bg=self.theme["bg_input"], bd=1, relief="solid")
        txt_frame.pack(fill="both", expand=True)

        self.pdf_result_text = tk.Text(
            txt_frame, wrap="word", bg=self.theme["bg_input"], fg=self.theme["fg_primary"],
            font=("Consolas", 10), relief="flat", padx=10, pady=10, insertbackground=self.theme["accent"]
        )
        self.pdf_result_text.pack(fill="both", expand=True)
        self._log(self.pdf_result_text, "PDF Sanitizer Ready.\nSelect a PDF document to inspect metadata headers and /Message tags.\n")

        return view

    # --------------------------------------------------------------------------
    # TAB 4: WATERMARK DETECTION VIEW
    # --------------------------------------------------------------------------
    def _build_watermark_view(self, parent):
        view = tk.Frame(parent, bg=self.theme["bg_app"])

        left = tk.Frame(view, bg=self.theme["bg_card"], width=420, bd=1, relief="solid", padx=18, pady=16)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(view, bg=self.theme["bg_card"], bd=1, relief="solid", padx=16, pady=16)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            left, text="🔍 Watermark & Edge Scanner", font=("Segoe UI", 13, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(anchor="w")

        tk.Label(
            left, text="High-contrast edge anomaly & watermark locator", font=("Segoe UI", 9),
            bg=self.theme["bg_card"], fg=self.theme["fg_secondary"]
        ).pack(anchor="w", pady=(2, 12))

        self.wm_dropzone = tk.Frame(left, bg=self.theme["bg_input"], bd=1, relief="solid", padx=12, pady=14)
        self.wm_dropzone.pack(fill="x", pady=(0, 12))

        self.wm_file_lbl = tk.Label(
            self.wm_dropzone, text="No image selected", font=("Segoe UI", 10, "bold"),
            bg=self.theme["bg_input"], fg=self.theme["fg_primary"], wraplength=340
        )
        self.wm_file_lbl.pack(pady=(0, 4))

        self.wm_meta_lbl = tk.Label(
            self.wm_dropzone, text="Select PNG or JPG to detect watermarks", font=("Segoe UI", 8),
            bg=self.theme["bg_input"], fg=self.theme["fg_secondary"]
        )
        self.wm_meta_lbl.pack()

        # Watermark Live Image Preview Box
        self.wm_preview_box = tk.Label(
            left, text="[ Edge Processed Preview ]", font=("Segoe UI", 9),
            bg=self.theme["bg_input"], fg=self.theme["fg_secondary"],
            height=6, bd=1, relief="solid"
        )
        self.wm_preview_box.pack(fill="x", pady=(0, 12))

        # Buttons
        b1 = create_styled_button(left, "Choose Image", self.choose_watermark_image, self.theme, is_primary=True, icon="📂")
        b1.pack(fill="x", pady=4)

        b2 = create_styled_button(left, "Detect Watermark & Edges", self.detect_watermark, self.theme, is_primary=False, icon="⚡")
        b2.pack(fill="x", pady=4)

        b3 = create_styled_button(left, "Open Processed in Viewer", self.open_processed_watermark, self.theme, is_primary=False, icon="🖼️")
        b3.pack(fill="x", pady=4)

        # Right: Terminal
        top_bar = tk.Frame(right, bg=self.theme["bg_card"])
        top_bar.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_bar, text="Watermark Scanner Log", font=("Segoe UI", 12, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(side="left")

        tools_f = tk.Frame(top_bar, bg=self.theme["bg_card"])
        tools_f.pack(side="right")

        tk.Button(
            tools_f, text="📋 Copy", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.copy_console(self.watermark_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="🧹 Clear", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.clear_console(self.watermark_result_text)
        ).pack(side="left", padx=3)

        self.wm_scanner = AnimatedScanner(right, self.theme)
        self.wm_scanner.pack(fill="x", pady=(0, 8))

        txt_frame = tk.Frame(right, bg=self.theme["bg_input"], bd=1, relief="solid")
        txt_frame.pack(fill="both", expand=True)

        self.watermark_result_text = tk.Text(
            txt_frame, wrap="word", bg=self.theme["bg_input"], fg=self.theme["fg_primary"],
            font=("Consolas", 10), relief="flat", padx=10, pady=10, insertbackground=self.theme["accent"]
        )
        self.watermark_result_text.pack(fill="both", expand=True)
        self._log(self.watermark_result_text, "Edge Frequency & Watermark Analyzer ready.\nLoad an image to filter spatial contrast and discover stamp boundaries.\n")

        return view

    # --------------------------------------------------------------------------
    # TAB 5: AUDIO STEGANOGRAPHY VIEW
    # --------------------------------------------------------------------------
    def _build_audio_view(self, parent):
        view = tk.Frame(parent, bg=self.theme["bg_app"])

        left = tk.Frame(view, bg=self.theme["bg_card"], width=420, bd=1, relief="solid", padx=18, pady=16)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(view, bg=self.theme["bg_card"], bd=1, relief="solid", padx=16, pady=16)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            left, text="🎙️ Audio Stego Decoder", font=("Segoe UI", 13, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(anchor="w")

        tk.Label(
            left, text="Decode concealed plaintext from uncompressed WAV frames", font=("Segoe UI", 9),
            bg=self.theme["bg_card"], fg=self.theme["fg_secondary"]
        ).pack(anchor="w", pady=(2, 12))

        self.audio_dropzone = tk.Frame(left, bg=self.theme["bg_input"], bd=1, relief="solid", padx=12, pady=16)
        self.audio_dropzone.pack(fill="x", pady=(0, 16))

        self.audio_file_lbl = tk.Label(
            self.audio_dropzone, text="No audio selected", font=("Segoe UI", 10, "bold"),
            bg=self.theme["bg_input"], fg=self.theme["fg_primary"], wraplength=340
        )
        self.audio_file_lbl.pack(pady=(0, 4))

        self.audio_meta_lbl = tk.Label(
            self.audio_dropzone, text="Supports uncompressed *.wav files", font=("Segoe UI", 8),
            bg=self.theme["bg_input"], fg=self.theme["fg_secondary"]
        )
        self.audio_meta_lbl.pack()

        # Action Buttons
        b1 = create_styled_button(left, "Choose Audio File", self.choose_audio, self.theme, is_primary=True, icon="📂")
        b1.pack(fill="x", pady=4)

        b2 = create_styled_button(left, "Run LSB Audio Decoding", self.run_audio_analysis, self.theme, is_primary=False, icon="⚡")
        b2.pack(fill="x", pady=4)

        # Right: Terminal
        top_bar = tk.Frame(right, bg=self.theme["bg_card"])
        top_bar.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_bar, text="Audio Decoding Log", font=("Segoe UI", 12, "bold"),
            bg=self.theme["bg_card"], fg=self.theme["fg_primary"]
        ).pack(side="left")

        tools_f = tk.Frame(top_bar, bg=self.theme["bg_card"])
        tools_f.pack(side="right")

        tk.Button(
            tools_f, text="📋 Copy", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.copy_console(self.audio_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="💾 Export PDF", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.export_console_to_pdf(self.audio_result_text)
        ).pack(side="left", padx=3)

        tk.Button(
            tools_f, text="🧹 Clear", font=("Segoe UI", 9),
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=lambda: self.clear_console(self.audio_result_text)
        ).pack(side="left", padx=3)

        self.audio_scanner = AnimatedScanner(right, self.theme)
        self.audio_scanner.pack(fill="x", pady=(0, 8))

        txt_frame = tk.Frame(right, bg=self.theme["bg_input"], bd=1, relief="solid")
        txt_frame.pack(fill="both", expand=True)

        self.audio_result_text = tk.Text(
            txt_frame, wrap="word", bg=self.theme["bg_input"], fg=self.theme["fg_primary"],
            font=("Consolas", 10), relief="flat", padx=10, pady=10, insertbackground=self.theme["accent"]
        )
        self.audio_result_text.pack(fill="both", expand=True)
        self._log(self.audio_result_text, "Acoustic Stego Engine ready.\nSelect a 16-bit PCM WAV recording to extract embedded bitstreams.\n")

        return view

    # --------------------------------------------------------------------------
    # STATUS BAR (BOTTOM)
    # --------------------------------------------------------------------------
    def _create_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg=self.theme["bg_panel"], height=32, bd=0)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)

        self.status_lbl = tk.Label(
            self.status_bar, text="● System Ready | CipherScan Core Active",
            font=("Segoe UI", 9), bg=self.theme["bg_panel"], fg=self.theme["fg_secondary"]
        )
        self.status_lbl.pack(side="left", padx=20)

        hints_lbl = tk.Label(
            self.status_bar, text="Shortcuts: [F11] Fullscreen | [Esc] Exit Fullscreen | [Ctrl+Q] Exit",
            font=("Segoe UI", 8), bg=self.theme["bg_panel"], fg=self.theme["fg_secondary"]
        )
        hints_lbl.pack(side="right", padx=20)

    # --------------------------------------------------------------------------
    # THEME ENGINE & ANIMATIONS
    # --------------------------------------------------------------------------
    def apply_theme(self, theme_key):
        """Live switch application theme across all components."""
        if theme_key not in THEMES:
            return
        self.current_theme_key = theme_key
        self.theme = THEMES[theme_key]

        # Update root
        self.root.configure(bg=self.theme["bg_app"])

        # Update Header
        self.header_frame.configure(bg=self.theme["bg_panel"])
        self.header_divider.configure(bg=self.theme["border"])
        self.logo_lbl.configure(bg=self.theme["bg_panel"], fg=self.theme["accent"])
        self.badge_lbl.configure(bg=self.theme["badge_bg"], fg=self.theme["badge_fg"])
        self.pulse_canvas.configure(bg=self.theme["bg_panel"])
        self.pulse_canvas.itemconfig(self.pulse_dot, fill=self.theme["accent"])
        self.status_header_lbl.configure(bg=self.theme["bg_panel"], fg=self.theme["fg_secondary"])

        # Theme menu button
        self.theme_menu_btn.configure(
            text=f"🎨 {self.theme['name']} ▾",
            bg=self.theme["btn_sec"], fg=self.theme["fg_primary"],
            activebackground=self.theme["btn_sec_hover"]
        )
        self.theme_menu.configure(bg=self.theme["bg_card"], fg=self.theme["fg_primary"])
        self.fs_btn.configure(bg=self.theme["btn_sec"], fg=self.theme["fg_primary"])
        self.info_btn.configure(bg=self.theme["btn_sec"], fg=self.theme["fg_primary"])

        # Navigation Bar
        self.nav_frame.configure(bg=self.theme["bg_app"])
        self.content_container.configure(bg=self.theme["bg_app"])
        self.status_bar.configure(bg=self.theme["bg_panel"])
        self.status_lbl.configure(bg=self.theme["bg_panel"], fg=self.theme["fg_secondary"])

        # Update Scanners
        for scanner in [self.img_scanner, self.pdf_scanner, self.wm_scanner, self.audio_scanner]:
            scanner.update_theme(self.theme)

        # Re-highlight active tab
        self._refresh_tab_buttons()

        # Update text consoles
        for txt in [self.image_result_text, self.pdf_result_text, self.watermark_result_text, self.audio_result_text]:
            txt.configure(
                bg=self.theme["bg_input"],
                fg=self.theme["fg_primary"],
                insertbackground=self.theme["accent"]
            )

        self.toast_mgr.show("Theme Activated", f"Switched to {self.theme['name']}", toast_type="info", theme=self.theme)

    def _pulse_status_orb(self):
        """Breathing glow animation for status indicator."""
        colors = [self.theme["accent"], self.theme["badge_bg"], self.theme["accent_hover"]]
        c = colors[self.pulse_phase % len(colors)]
        try:
            self.pulse_canvas.itemconfig(self.pulse_dot, fill=c)
        except Exception:
            pass
        self.pulse_phase += 1
        self.root.after(800, self._pulse_status_orb)

    def select_tab(self, tab_id):
        """Switch current active module tab with smooth display."""
        for tid, view in self.tab_views.items():
            view.pack_forget()

        if tab_id in self.tab_views:
            self.active_tab_id = tab_id
            self.tab_views[tab_id].pack(fill="both", expand=True)
            self._refresh_tab_buttons()

    def _refresh_tab_buttons(self):
        for tid, btn in self.nav_buttons.items():
            if tid == getattr(self, "active_tab_id", "hub"):
                btn.configure(
                    bg=self.theme["accent"], fg=self.theme["accent_fg"],
                    activebackground=self.theme["accent_hover"]
                )
            else:
                btn.configure(
                    bg=self.theme["btn_sec"], fg=self.theme["fg_secondary"],
                    activebackground=self.theme["btn_sec_hover"]
                )

    def _log(self, text_widget, content, level="INFO"):
        """Append timestamped formatted log line to terminal."""
        ts = time.strftime("[%H:%M:%S]")
        text_widget.insert("end", f"{ts} {content}\n")
        text_widget.see("end")

    def copy_console(self, text_widget):
        content = text_widget.get("1.0", "end").strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.toast_mgr.show("Copied", "Console output copied to clipboard.", toast_type="success", theme=self.theme)
        else:
            self.toast_mgr.show("Empty", "Console has no text to copy.", toast_type="warning", theme=self.theme)

    def clear_console(self, text_widget):
        text_widget.delete("1.0", "end")
        self._log(text_widget, "Console cleared.")

    def export_console_to_pdf(self, text_widget):
        content = text_widget.get("1.0", "end").strip()
        if not content:
            self.toast_mgr.show("Warning", "No console output to export!", toast_type="warning", theme=self.theme)
            return
        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")])
        if output_pdf_path:
            ok, msg = save_data_to_pdf(content, output_pdf_path)
            if ok:
                ModernModal.show(self.root, "Export Successful", msg, category="success", theme=self.theme)
                self.toast_mgr.show("Export Complete", "PDF report saved.", toast_type="success", theme=self.theme)
            else:
                ModernModal.show(self.root, "Export Failed", msg, category="error", theme=self.theme)

    # --------------------------------------------------------------------------
    # IMAGE STEGO WORKFLOW
    # --------------------------------------------------------------------------
    def choose_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp"), ("All Files", "*.*")]
        )
        if file_path:
            self.image_path = file_path
            fname, fsz = get_file_stats(file_path)
            self.img_file_lbl.configure(text=f"Selected: {fname}")
            self.img_meta_lbl.configure(text=f"Size: {fsz} | Path: {file_path[:45]}...")
            self._log(self.image_result_text, f"Image loaded: {fname} ({fsz})")
            self.toast_mgr.show("Image Loaded", fname, toast_type="info", theme=self.theme)

            # Generate Thumbnail
            try:
                img = Image.open(file_path)
                img.thumbnail((220, 100))
                self.img_tk_photo = ImageTk.PhotoImage(img)
                self.img_preview_box.configure(image=self.img_tk_photo, text="")
            except Exception as e:
                self.img_preview_box.configure(image="", text="[Preview unavailable]")

    def run_image_analysis(self):
        if not self.image_path:
            ModernModal.show(
                self.root, "No Image Selected",
                "Please choose an image file first before running stego extraction.",
                category="warning", theme=self.theme
            )
            return

        self.img_scanner.start()
        self.status_lbl.configure(text="● Analyzing image LSB/MSB stream...")

        def worker():
            try:
                time.sleep(0.3)  # Smooth UI transition
                lsb_msg, msb_msg = extract_text_from_image(self.image_path)
                self.root.after(0, lambda: self._on_image_analysis_complete(lsb_msg, msb_msg))
            except Exception as e:
                self.root.after(0, lambda: self._on_image_analysis_error(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_image_analysis_complete(self, lsb_msg, msb_msg):
        self.img_scanner.stop()
        self.status_lbl.configure(text="● Image Analysis Complete")
        self._log(self.image_result_text, f"\n--- LSB (Least Significant Bit) Plaintext ---\n{lsb_msg}\n")
        self._log(self.image_result_text, f"--- MSB (Most Significant Bit) Plaintext ---\n{msb_msg}\n")
        self.toast_mgr.show("Analysis Finished", "LSB & MSB inspection completed.", toast_type="success", theme=self.theme)

    def _on_image_analysis_error(self, err_msg):
        self.img_scanner.stop()
        self.status_lbl.configure(text="● Image Analysis Failed")
        self._log(self.image_result_text, f"[!] Error: {err_msg}")
        ModernModal.show(self.root, "Image Analysis Error", "Failed to analyze image bits.", category="error", details=err_msg, theme=self.theme)

    def extract_image_metadata(self):
        if not self.image_path:
            ModernModal.show(self.root, "Selection Required", "Please select an image file first!", category="warning", theme=self.theme)
            return

        try:
            hidden_data = extract_data_from_image(self.image_path)
            self._log(self.image_result_text, f"[+] Extracted Metadata:\n{hidden_data}\n")

            # Option to save to PDF
            def export_to_pdf():
                pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")])
                if pdf_path:
                    save_data_to_pdf(hidden_data, pdf_path)
                    self.toast_mgr.show("Saved", f"Exported to {os.path.basename(pdf_path)}", toast_type="success", theme=self.theme)

            ModernModal.show(
                self.root, "Hidden Metadata Found",
                "Successfully extracted embedded tag/metadata from image.",
                category="success", details=str(hidden_data), theme=self.theme,
                action_label="Export to PDF", on_action=export_to_pdf
            )
        except ValueError as e:
            self._log(self.image_result_text, f"[-] {e}")
            ModernModal.show(self.root, "No Hidden Metadata", str(e), category="info", theme=self.theme)

    # --------------------------------------------------------------------------
    # PDF FORENSICS WORKFLOW
    # --------------------------------------------------------------------------
    def choose_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Documents", "*.pdf"), ("All Files", "*.*")])
        if file_path:
            self.pdf_path = file_path
            fname, fsz = get_file_stats(file_path)
            self.pdf_file_lbl.configure(text=f"Selected: {fname}")
            self.pdf_meta_lbl.configure(text=f"Size: {fsz} | Path: {file_path[:45]}...")
            self._log(self.pdf_result_text, f"PDF loaded: {fname} ({fsz})")
            self.toast_mgr.show("PDF Loaded", fname, toast_type="info", theme=self.theme)

    def run_pdf_analysis(self):
        if not self.pdf_path:
            ModernModal.show(self.root, "No PDF Selected", "Please select a PDF file first!", category="warning", theme=self.theme)
            return

        self.pdf_scanner.start()
        self.status_lbl.configure(text="● Scanning PDF headers & metadata...")

        def worker():
            time.sleep(0.3)
            findings = extract_message_from_pdf(self.pdf_path)
            self.root.after(0, lambda: self._on_pdf_complete(findings))

        threading.Thread(target=worker, daemon=True).start()

    def _on_pdf_complete(self, findings):
        self.pdf_scanner.stop()
        self.status_lbl.configure(text="● PDF Analysis Complete")
        self._log(self.pdf_result_text, f"\n{findings}\n")
        self.toast_mgr.show("Scan Finished", "PDF headers inspected.", toast_type="success", theme=self.theme)

    def remove_pdf_metadata(self):
        if not self.pdf_path:
            ModernModal.show(self.root, "No PDF Selected", "Please choose a PDF document to sanitize.", category="warning", theme=self.theme)
            return

        save_dir = filedialog.askdirectory(title="Choose Directory to Save Sanitized PDF")
        if not save_dir:
            return

        self.pdf_scanner.start()
        cleaned_path = remove_metadata_from_pdf(self.pdf_path, save_dir)
        self.pdf_scanner.stop()

        if "Error" in cleaned_path:
            self._log(self.pdf_result_text, f"[!] Sanitization Failed: {cleaned_path}")
            ModernModal.show(self.root, "Sanitization Error", cleaned_path, category="error", theme=self.theme)
        else:
            self._log(self.pdf_result_text, f"[✓] Metadata scrubbed. Cleaned PDF saved at:\n{cleaned_path}\n")
            ModernModal.show(
                self.root, "PDF Sanitized",
                f"All metadata and tracking tags have been successfully stripped.\nSaved to: {cleaned_path}",
                category="success", theme=self.theme
            )
            self.toast_mgr.show("Sanitization Complete", "Cleaned PDF saved.", toast_type="success", theme=self.theme)

    # --------------------------------------------------------------------------
    # WATERMARK SCANNER WORKFLOW
    # --------------------------------------------------------------------------
    def choose_watermark_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
        )
        if file_path:
            self.watermark_image_path = file_path
            fname, fsz = get_file_stats(file_path)
            self.wm_file_lbl.configure(text=f"Selected: {fname}")
            self.wm_meta_lbl.configure(text=f"Size: {fsz} | Path: {file_path[:45]}...")
            self._log(self.watermark_result_text, f"Image loaded for watermark scan: {fname} ({fsz})")
            self.toast_mgr.show("Image Ready", fname, toast_type="info", theme=self.theme)

    def detect_watermark(self):
        if not self.watermark_image_path:
            ModernModal.show(self.root, "Selection Required", "Please select an image file first!", category="warning", theme=self.theme)
            return

        self.wm_scanner.start()
        self.status_lbl.configure(text="● Processing edge frequencies & contrast...")

        def worker():
            time.sleep(0.3)
            processed_img, msg = find_watermark_without_cv2(self.watermark_image_path)
            self.root.after(0, lambda: self._on_watermark_complete(processed_img, msg))

        threading.Thread(target=worker, daemon=True).start()

    def _on_watermark_complete(self, processed_image, message):
        self.wm_scanner.stop()
        self.status_lbl.configure(text="● Watermark Detection Complete")

        if processed_image is not None:
            self.watermarked_image_obj = processed_image
            save_path = os.path.join(os.path.dirname(self.watermark_image_path), "watermarked_detected.png")
            try:
                processed_image.save(save_path)
                self.last_watermark_saved_path = save_path
            except Exception as e:
                self.last_watermark_saved_path = None

            # Generate Thumbnail for Preview
            try:
                preview_copy = processed_image.copy()
                preview_copy.thumbnail((220, 100))
                self.wm_tk_photo = ImageTk.PhotoImage(preview_copy)
                self.wm_preview_box.configure(image=self.wm_tk_photo, text="")
            except Exception:
                pass

            self._log(self.watermark_result_text, f"[✓] {message}\nDetected output saved: {save_path}\n")
            ModernModal.show(
                self.root, "Watermark Scan Finished",
                f"{message}\nProcessed output image saved to:\n{save_path}",
                category="success", theme=self.theme,
                action_label="Open Image", on_action=self.open_processed_watermark
            )
            self.toast_mgr.show("Watermark Flagged", "Saved to watermarked_detected.png", toast_type="success", theme=self.theme)
        else:
            self._log(self.watermark_result_text, f"[!] {message}")
            ModernModal.show(self.root, "Scan Failed", message, category="error", theme=self.theme)

    def open_processed_watermark(self):
        if self.watermarked_image_obj:
            self.watermarked_image_obj.show()
        elif getattr(self, "last_watermark_saved_path", None) and os.path.exists(self.last_watermark_saved_path):
            try:
                if sys.platform.startswith('win'):
                    os.startfile(self.last_watermark_saved_path)
                else:
                    subprocess.run(["xdg-open", self.last_watermark_saved_path])
            except Exception:
                pass
        else:
            self.toast_mgr.show("Notice", "No processed watermark image available.", toast_type="warning", theme=self.theme)

    # --------------------------------------------------------------------------
    # AUDIO STEGO WORKFLOW
    # --------------------------------------------------------------------------
    def choose_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV Audio Files", "*.wav"), ("All Files", "*.*")])
        if file_path:
            self.audio_path = file_path
            fname, fsz = get_file_stats(file_path)
            self.audio_file_lbl.configure(text=f"Selected: {fname}")
            self.audio_meta_lbl.configure(text=f"Size: {fsz} | Path: {file_path[:45]}...")
            self._log(self.audio_result_text, f"WAV Audio loaded: {fname} ({fsz})")
            self.toast_mgr.show("Audio Loaded", fname, toast_type="info", theme=self.theme)

    def run_audio_analysis(self):
        if not self.audio_path:
            ModernModal.show(self.root, "Selection Required", "Please select a WAV audio file first!", category="warning", theme=self.theme)
            return

        self.audio_scanner.start()
        self.status_lbl.configure(text="● Decoding uncompressed WAV frame LSB bits...")

        def worker():
            try:
                time.sleep(0.3)
                decoded_msg = decode_text_from_audio(self.audio_path)
                self.root.after(0, lambda: self._on_audio_complete(decoded_msg))
            except Exception as e:
                self.root.after(0, lambda: self._on_audio_error(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_audio_complete(self, decoded_msg):
        self.audio_scanner.stop()
        self.status_lbl.configure(text="● Audio Decoding Complete")
        self._log(self.audio_result_text, f"\n=== DECODED AUDIO STEGO STREAM ===\n{decoded_msg}\n")

        def export_pdf():
            out_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")])
            if out_pdf:
                save_data_to_pdf(decoded_msg, out_pdf)
                self.toast_mgr.show("Saved", "Decoded audio text saved to PDF.", toast_type="success", theme=self.theme)

        ModernModal.show(
            self.root, "Audio Decoding Finished",
            "Extracted LSB message from audio frames.",
            category="success", details=decoded_msg[:400], theme=self.theme,
            action_label="Save to PDF", on_action=export_pdf
        )
        self.toast_mgr.show("Audio Decoded", "Stream decoded successfully.", toast_type="success", theme=self.theme)

    def _on_audio_error(self, err_msg):
        self.audio_scanner.stop()
        self.status_lbl.configure(text="● Audio Decoding Error")
        self._log(self.audio_result_text, f"[!] Audio Error: {err_msg}")
        ModernModal.show(self.root, "Audio Decoding Failed", err_msg, category="error", theme=self.theme)

    # --------------------------------------------------------------------------
    # WINDOW STATE & HELP
    # --------------------------------------------------------------------------
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            self.fs_btn.configure(text="✕ Exit Fullscreen")
            self.toast_mgr.show("Fullscreen Mode", "Press [F11] or [Esc] to exit.", toast_type="info", theme=self.theme)
        else:
            self.fs_btn.configure(text="⛶ Fullscreen")

    def exit_fullscreen(self):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes("-fullscreen", False)
            self.fs_btn.configure(text="⛶ Fullscreen")

    def show_about_modal(self):
        about_text = (
            "CipherScan v2.5 Forensic Suite\n\n"
            "Features:\n"
            "• Image LSB / MSB Steganography Extractor\n"
            "• PNG & EXIF HiddenData Tag Inspector\n"
            "• PDF Metadata Stripper & /Message Stego Scanner\n"
            "• High-Pass Edge & Watermark Detector\n"
            "• 16-bit PCM Audio WAV Steganography Decoder\n"
            "• Multi-Theme Engine with Dynamic Lighting\n\n"
            "Engineered for digital forensics, red-team stego analysis, and data privacy."
        )
        ModernModal.show(
            self.root, "About CipherScan",
            about_text, category="info", theme=self.theme
        )

    def exit_app(self):
        self.root.destroy()


# ==============================================================================
# MAIN APPLICATION ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedGUI(root)
    root.mainloop()

