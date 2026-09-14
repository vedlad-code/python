"""
A desktop file manager built with PySide6, styled after macOS Finder:
a sidebar of common locations, a breadcrumb path bar, and a main pane
that switches between an icon grid and a detailed list.
"""

import sys
import shutil
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QDir,
    QModelIndex,
    QObject,
    QSize,
    QSizeF,
    QSortFilterProxyModel,
    QRectF,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QFont,
    QKeySequence,
    QShortcut,
    QIcon,
    QAction,
    QPixmap,
    QPainter,
    QColor,
    QPainterPath,
    QImageReader,
    QImage,
    QPolygonF,
    QFontMetrics,
)
from PySide6.QtCore import QPointF
from PySide6.QtPdf import QPdfDocument
from PySide6.QtMultimedia import QMediaPlayer, QVideoSink
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QSplitter,
    QTreeView,
    QListView,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton,
    QLabel,
    QStatusBar,
    QMenu,
    QInputDialog,
    QMessageBox,
    QFileSystemModel,
    QAbstractItemView,
    QSizePolicy,
    QFrame,
    QStyle,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


# ----------------------------------------------------------------------
# Visual style
# ----------------------------------------------------------------------

COLORS = {
    "sidebar_bg": "#1b1d21",
    "content_bg": "#232529",
    "border": "#33363b",
    "text": "#d8dade",
    "text_muted": "#83878e",
    "accent": "#c9895a",
    "accent_dim": "#8a5d3c",
    "toolbar_bg": "#1e2024",
    "row_hover": "#2b2e33",
    "selected_bg": "#2c2620",
}

STYLESHEET = f"""
QMainWindow {{
    background: {COLORS['content_bg']};
}}

QWidget#toolbar {{
    background: {COLORS['toolbar_bg']};
    border-bottom: 1px solid {COLORS['border']};
}}

QWidget#sidebar {{
    background: {COLORS['sidebar_bg']};
    border-right: 1px solid {COLORS['border']};
}}

QLabel#sectionLabel {{
    color: {COLORS['text_muted']};
    font-size: 11px;
    font-weight: 600;
    padding: 10px 12px 2px 12px;
}}

QTreeView {{
    background: transparent;
    border: none;
    outline: none;
    font-size: 12.5px;
    color: {COLORS['text']};
}}

QTreeView::item {{
    height: 27px;
    border-left: 2px solid transparent;
    padding-left: 10px;
}}

QTreeView::item:hover {{
    background: {COLORS['row_hover']};
}}

QTreeView::item:selected {{
    background: {COLORS['selected_bg']};
    border-left: 2px solid {COLORS['accent']};
    color: {COLORS['text']};
}}

QTreeView::branch {{
    background: transparent;
}}

QListView {{
    background: {COLORS['content_bg']};
    border: none;
    font-size: 12px;
    color: {COLORS['text']};
}}

QListView::item {{
    border-radius: 4px;
    padding: 4px;
}}

QListView::item:hover {{
    background: {COLORS['row_hover']};
}}

QListView::item:selected {{
    background: {COLORS['selected_bg']};
    color: {COLORS['text']};
}}

QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 5px 8px;
    color: {COLORS['text']};
    font-size: 14px;
}}

QToolButton:hover {{
    background: {COLORS['row_hover']};
    border: 1px solid {COLORS['border']};
}}

QToolButton:pressed {{
    background: #34373c;
}}

QToolButton:checked {{
    background: {COLORS['selected_bg']};
    border: 1px solid {COLORS['accent_dim']};
    color: {COLORS['accent']};
}}

QToolButton:disabled {{
    color: #52565c;
}}

QToolButton#crumb {{
    font-size: 12.5px;
    font-weight: 500;
    padding: 4px 6px;
    color: {COLORS['text_muted']};
}}

QToolButton#crumb:hover {{
    color: {COLORS['text']};
    background: {COLORS['row_hover']};
}}

QToolButton#crumbCurrent {{
    font-size: 12.5px;
    font-weight: 600;
    padding: 4px 6px;
    color: {COLORS['text']};
}}

QStatusBar {{
    background: {COLORS['toolbar_bg']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_muted']};
    font-size: 11px;
}}

QFrame#divider {{
    color: {COLORS['border']};
}}

QMenu {{
    background: #1e2024;
    border: 1px solid {COLORS['border']};
    padding: 4px;
    font-size: 12px;
    color: {COLORS['text']};
}}

QMenu::item {{
    padding: 6px 20px 6px 12px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background: {COLORS['selected_bg']};
    color: {COLORS['accent']};
}}

QMenu::item:disabled {{
    color: #55585e;
}}

QMenu::separator {{
    height: 1px;
    background: {COLORS['border']};
    margin: 4px 6px;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 11px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #3c3f45;
    border-radius: 5px;
    min-height: 24px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background: #4b4e55;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""


def apply_dark_palette(app: QApplication):
    from PySide6.QtGui import QPalette, QColor

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLORS["content_bg"]))
    palette.setColor(QPalette.WindowText, QColor(COLORS["text"]))
    palette.setColor(QPalette.Base, QColor("#1a1c20"))
    palette.setColor(QPalette.AlternateBase, QColor(COLORS["sidebar_bg"]))
    palette.setColor(QPalette.Text, QColor(COLORS["text"]))
    palette.setColor(QPalette.Button, QColor(COLORS["toolbar_bg"]))
    palette.setColor(QPalette.ButtonText, QColor(COLORS["text"]))
    palette.setColor(QPalette.ToolTipBase, QColor("#1e2024"))
    palette.setColor(QPalette.ToolTipText, QColor(COLORS["text"]))
    palette.setColor(QPalette.Highlight, QColor(COLORS["selected_bg"]))
    palette.setColor(QPalette.HighlightedText, QColor(COLORS["text"]))
    palette.setColor(QPalette.PlaceholderText, QColor(COLORS["text_muted"]))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#55585e"))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor("#55585e"))
    app.setPalette(palette)


# ----------------------------------------------------------------------
# Custom icons
#
# Native folder/file icons (via QFileIconProvider) render as the same
# glossy blue folder macOS Finder uses, which is exactly what makes a
# custom file manager feel like a Finder skin. These are flat, drawn
# icons in the app's own palette instead.
# ----------------------------------------------------------------------

EXTENSION_COLORS = {
    "image": ("#5fa8d3", {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".tiff", ".heic"}),
    "code": ("#7fb069", {".py", ".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".java", ".rs", ".go", ".rb", ".sh", ".json", ".yaml", ".yml", ".html", ".css"}),
    "doc": ("#c9895a", {".txt", ".md", ".doc", ".docx", ".pdf", ".rtf", ".pages"}),
    "archive": ("#a58fc9", {".zip", ".tar", ".gz", ".rar", ".7z"}),
    "video": ("#d3705f", {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}),
    "audio": ("#e0b64c", {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"}),
}
DEFAULT_FILE_COLOR = "#8a8f97"
IMAGE_EXTENSIONS = EXTENSION_COLORS["image"][1]
VIDEO_EXTENSIONS = EXTENSION_COLORS["video"][1]
AUDIO_EXTENSIONS = EXTENSION_COLORS["audio"][1]
CODE_EXTENSIONS = EXTENSION_COLORS["code"][1]
TEXT_PREVIEW_EXTENSIONS = CODE_EXTENSIONS | {".txt", ".md", ".csv", ".log", ".ini", ".cfg"}
THUMBNAIL_DECODE_SIZE = 256
ICON_RENDER_SIZE = 64


def color_for_extension(suffix: str) -> str:
    suffix = suffix.lower()
    for color, extensions in EXTENSION_COLORS.values():
        if suffix in extensions:
            return color
    return DEFAULT_FILE_COLOR


class VideoThumbnailer(QObject):
    """Grabs a frame from a video file to use as its thumbnail.

    Decoding a video frame isn't instant, so this runs one request at a
    time in the background using Qt's own media player and reports each
    result back through a signal instead of blocking the UI.
    """

    thumbnail_ready = Signal(str, int, object)  # path, mtime, QImage or None

    def __init__(self):
        super().__init__()
        self._queue = []
        self._active = None  # (path, mtime)
        self._got_frame = False

        self._player = QMediaPlayer(self)
        self._sink = QVideoSink(self)
        self._player.setVideoSink(self._sink)
        self._sink.videoFrameChanged.connect(self._on_frame)
        self._player.mediaStatusChanged.connect(self._on_status)
        self._player.errorOccurred.connect(lambda *_: self._finish(None))

        self._timeout = QTimer(self)
        self._timeout.setSingleShot(True)
        self._timeout.timeout.connect(lambda: self._finish(None))

    def request(self, path: str, mtime: int):
        entry = (path, mtime)
        if entry == self._active or entry in self._queue:
            return
        self._queue.append(entry)
        self._process_next()

    def _process_next(self):
        if self._active is not None or not self._queue:
            return
        self._active = self._queue.pop(0)
        self._got_frame = False
        self._player.setSource(QUrl.fromLocalFile(self._active[0]))
        self._timeout.start(5000)

    def _on_status(self, status):
        if self._active is None:
            return
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            duration = self._player.duration()
            target = min(1500, duration // 4) if duration > 0 else 0
            self._player.setPosition(target)
            self._player.play()
        elif status == QMediaPlayer.MediaStatus.InvalidMedia:
            self._finish(None)

    def _on_frame(self, frame):
        if self._got_frame or self._active is None or not frame.isValid():
            return
        image = frame.toImage()
        if image.isNull():
            return
        self._got_frame = True
        self._player.pause()
        self._finish(image)

    def _finish(self, image):
        if self._active is None:
            return
        self._timeout.stop()
        path, mtime = self._active
        self._active = None
        self._player.stop()
        self.thumbnail_ready.emit(path, mtime, image)
        self._process_next()


_video_thumbnailer_instance = None


def get_video_thumbnailer():
    """Lazily creates the VideoThumbnailer.

    It owns a QMediaPlayer, which requires a QApplication to already
    exist -- creating it at module import time (before main() has
    constructed the QApplication) fails silently, so it's built on
    first use instead.
    """
    global _video_thumbnailer_instance
    if _video_thumbnailer_instance is None:
        _video_thumbnailer_instance = VideoThumbnailer()
    return _video_thumbnailer_instance


class IconFactory:
    """Renders small flat folder/file glyphs, plus real image, PDF,
    video-frame, and text-content thumbnails, and caches all of them.

    Decoding (reading pixels or text from disk) and composing (drawing
    the small icon) are cached separately, so a thumbnail is only
    decoded once per file even if it's displayed at several sizes.
    """


    _shape_cache = {}
    _decoded_cache = {}
    _icon_cache = {}

    @classmethod
    def folder_icon(cls, size=48, color=None):
        color = color or COLORS["accent"]
        key = ("folder", size, color)
        if key not in cls._shape_cache:
            cls._shape_cache[key] = QIcon(cls._render_folder(size, color))
        return cls._shape_cache[key]

    @classmethod
    def file_icon(cls, size=48, color=None):
        color = color or DEFAULT_FILE_COLOR
        key = ("file", size, color)
        if key not in cls._shape_cache:
            cls._shape_cache[key] = QIcon(cls._render_file(size, color))
        return cls._shape_cache[key]

    @classmethod
    def thumbnail_icon(cls, path: str, mtime: int, size: int, accent_hex: str, kind: str):
        """Returns a QIcon built from real file content (image, PDF
        page, video frame, or text preview), or None if it can't be
        read -- in which case the caller should fall back to a plain
        colored icon."""
        icon_key = (path, mtime, size, kind)
        if icon_key in cls._icon_cache:
            return cls._icon_cache[icon_key]

        decode_key = (path, mtime, kind)
        if decode_key not in cls._decoded_cache:
            if kind == "image":
                cls._decoded_cache[decode_key] = cls._decode_image(path)
            elif kind == "pdf":
                cls._decoded_cache[decode_key] = cls._decode_pdf(path)
            elif kind == "text":
                cls._decoded_cache[decode_key] = cls._decode_text(path)
            elif kind == "video":
                # Populated asynchronously by VideoThumbnailer -- there's
                # nothing to decode synchronously here.
                return None
            else:
                cls._decoded_cache[decode_key] = None

        content = cls._decoded_cache[decode_key]
        icon = None
        if content is not None:
            if kind == "text":
                icon = QIcon(cls._compose_text_thumb(content, accent_hex, size))
            else:
                icon = QIcon(cls._compose_thumb(content, accent_hex, size, overlay_play=(kind == "video")))
        cls._icon_cache[icon_key] = icon
        return icon

    @classmethod
    def video_decode_attempted(cls, path: str, mtime: int) -> bool:
        return (path, mtime, "video") in cls._decoded_cache

    @classmethod
    def store_video_frame(cls, path: str, mtime: int, image):
        decode_key = (path, mtime, "video")
        cls._decoded_cache[decode_key] = image
        stale_keys = [k for k in cls._icon_cache if k[0] == path and k[1] == mtime and k[3] == "video"]
        for k in stale_keys:
            del cls._icon_cache[k]

    @classmethod
    def video_placeholder_icon(cls, size=None, color=None):
        size = size or ICON_RENDER_SIZE
        color = color or EXTENSION_COLORS["video"][0]
        key = ("video_placeholder", size, color)
        if key not in cls._shape_cache:
            cls._shape_cache[key] = QIcon(cls._render_video_placeholder(size, color))
        return cls._shape_cache[key]

    @classmethod
    def audio_icon(cls, size=None, color=None):
        size = size or ICON_RENDER_SIZE
        color = color or EXTENSION_COLORS["audio"][0]
        key = ("audio", size, color)
        if key not in cls._shape_cache:
            cls._shape_cache[key] = QIcon(cls._render_audio(size, color))
        return cls._shape_cache[key]

    @staticmethod
    def _decode_text(path):
        try:
            with open(path, "rb") as handle:
                raw = handle.read(2000)
        except OSError:
            return None
        text = raw.decode("utf-8", errors="ignore")
        if not text.strip():
            return None
        lines = []
        for line in text.splitlines()[:8]:
            line = line.rstrip()
            if len(line) > 26:
                line = line[:25] + "\u2026"
            lines.append(line)
        return lines or None

    @staticmethod
    def _decode_image(path):
        reader = QImageReader(path)
        reader.setAutoTransform(True)
        src_size = reader.size()
        if not src_size.isValid() or src_size.width() <= 0 or src_size.height() <= 0:
            return None
        target = src_size
        if target.width() > THUMBNAIL_DECODE_SIZE or target.height() > THUMBNAIL_DECODE_SIZE:
            target = target.scaled(THUMBNAIL_DECODE_SIZE, THUMBNAIL_DECODE_SIZE, Qt.KeepAspectRatio)
        reader.setScaledSize(target)
        image = reader.read()
        return None if image.isNull() else image

    @staticmethod
    def _decode_pdf(path):
        doc = QPdfDocument()
        if doc.load(path) != QPdfDocument.Error.None_:
            return None
        if doc.pageCount() < 1:
            return None
        page_size = doc.pagePointSize(0)
        if page_size.width() <= 0 or page_size.height() <= 0:
            return None
        target = QSizeF(page_size).scaled(
            THUMBNAIL_DECODE_SIZE, THUMBNAIL_DECODE_SIZE, Qt.KeepAspectRatio
        ).toSize()
        if target.width() < 1 or target.height() < 1:
            return None
        image = doc.render(0, target)
        return None if image.isNull() else image

    @staticmethod
    def _compose_thumb(image, accent_hex, size, overlay_play=False):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        fold = size * 0.22
        left = size * 0.12
        right = size * 0.88
        top = size * 0.08
        bottom = size * 0.92

        page = QPainterPath()
        page.moveTo(left, top)
        page.lineTo(right - fold, top)
        page.lineTo(right, top + fold)
        page.lineTo(right, bottom)
        page.lineTo(left, bottom)
        page.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#101113"))
        painter.drawPath(page)

        inset = size * 0.05
        content_rect = QRectF(
            left + inset, top + inset, (right - left) - inset * 2, (bottom - top) - inset * 2
        )
        content_path = QPainterPath()
        content_path.addRoundedRect(content_rect, size * 0.025, size * 0.025)

        painter.save()
        painter.setClipPath(content_path)
        painter.fillRect(content_rect, QColor("#1c1e21"))

        # Flatten onto white first: transparent PNGs and PDF renders
        # both come back with an empty alpha background, which would
        # otherwise blend into the app's dark theme instead of reading
        # as a page or a photo.
        flattened = QImage(image.size(), QImage.Format_ARGB32_Premultiplied)
        flattened.fill(Qt.white)
        flatten_painter = QPainter(flattened)
        flatten_painter.drawImage(0, 0, image)
        flatten_painter.end()

        content_pixmap = QPixmap.fromImage(flattened).scaled(
            max(int(content_rect.width()), 1),
            max(int(content_rect.height()), 1),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        target_x = content_rect.center().x() - content_pixmap.width() / 2
        target_y = content_rect.center().y() - content_pixmap.height() / 2
        painter.drawPixmap(int(target_x), int(target_y), content_pixmap)

        if overlay_play:
            radius = size * 0.15
            center = content_rect.center()
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 150))
            painter.drawEllipse(center, radius, radius)
            triangle = QPolygonF([
                QPointF(center.x() - radius * 0.35, center.y() - radius * 0.5),
                QPointF(center.x() - radius * 0.35, center.y() + radius * 0.5),
                QPointF(center.x() + radius * 0.55, center.y()),
            ])
            painter.setBrush(QColor("#ffffff"))
            painter.drawPolygon(triangle)

        painter.restore()

        fold_path = QPainterPath()
        fold_path.moveTo(right - fold, top)
        fold_path.lineTo(right, top + fold)
        fold_path.lineTo(right - fold, top + fold)
        fold_path.closeSubpath()
        painter.setBrush(QColor(accent_hex))
        painter.drawPath(fold_path)

        painter.end()
        return pixmap

    @staticmethod
    def _compose_text_thumb(lines, accent_hex, size):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        fold = size * 0.22
        left = size * 0.20
        right = size * 0.80
        top = size * 0.10
        bottom = size * 0.90

        page = QPainterPath()
        page.moveTo(left, top)
        page.lineTo(right - fold, top)
        page.lineTo(right, top + fold)
        page.lineTo(right, bottom)
        page.lineTo(left, bottom)
        page.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#2c2e33"))
        painter.drawPath(page)

        fold_path = QPainterPath()
        fold_path.moveTo(right - fold, top)
        fold_path.lineTo(right, top + fold)
        fold_path.lineTo(right - fold, top + fold)
        fold_path.closeSubpath()
        painter.setBrush(QColor(accent_hex))
        painter.drawPath(fold_path)

        font = QFont("Menlo" if sys.platform == "darwin" else "Monospace")
        font.setPixelSize(max(int(size * 0.085), 5))
        painter.setFont(font)
        painter.setPen(QColor("#c7cad0"))

        metrics = QFontMetrics(font)
        line_height = metrics.height()
        text_x = left + size * 0.09
        text_y = top + fold * 0.9
        available = bottom - size * 0.06 - text_y
        max_lines = max(int(available / line_height), 1) if line_height > 0 else 0

        for i, line in enumerate(lines[:max_lines]):
            if not line:
                continue
            baseline_y = text_y + (i + 1) * line_height - metrics.descent()
            painter.drawText(QPointF(text_x, baseline_y), line)

        painter.end()
        return pixmap

    @staticmethod
    def _render_folder(size, color_hex):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        base = QColor(color_hex)
        tab = base.darker(115)
        radius = size * 0.07

        painter.setPen(Qt.NoPen)
        painter.setBrush(tab)
        tab_rect = QRectF(size * 0.10, size * 0.20, size * 0.38, size * 0.16)
        painter.drawRoundedRect(tab_rect, radius, radius)

        painter.setBrush(base)
        body_rect = QRectF(size * 0.08, size * 0.30, size * 0.84, size * 0.56)
        painter.drawRoundedRect(body_rect, radius, radius)

        painter.end()
        return pixmap

    @staticmethod
    def _render_file(size, color_hex):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        fold = size * 0.22
        left = size * 0.20
        right = size * 0.80
        top = size * 0.10
        bottom = size * 0.90

        page = QPainterPath()
        page.moveTo(left, top)
        page.lineTo(right - fold, top)
        page.lineTo(right, top + fold)
        page.lineTo(right, bottom)
        page.lineTo(left, bottom)
        page.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#2c2e33"))
        painter.drawPath(page)

        fold_path = QPainterPath()
        fold_path.moveTo(right - fold, top)
        fold_path.lineTo(right, top + fold)
        fold_path.lineTo(right - fold, top + fold)
        fold_path.closeSubpath()
        painter.setBrush(QColor(color_hex))
        painter.drawPath(fold_path)

        line_color = QColor(color_hex)
        line_color.setAlpha(140)
        painter.setBrush(line_color)
        line_h = size * 0.045
        line_left = left + size * 0.10
        line_width = (right - fold) - line_left - size * 0.06
        for i, frac in enumerate((0.55, 0.68, 0.81)):
            w = line_width if i < 2 else line_width * 0.6
            painter.drawRoundedRect(QRectF(line_left, size * frac, w, line_h), line_h / 2, line_h / 2)

        painter.end()
        return pixmap

    @staticmethod
    def _render_video_placeholder(size, color_hex):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        fold = size * 0.22
        left = size * 0.20
        right = size * 0.80
        top = size * 0.10
        bottom = size * 0.90

        page = QPainterPath()
        page.moveTo(left, top)
        page.lineTo(right - fold, top)
        page.lineTo(right, top + fold)
        page.lineTo(right, bottom)
        page.lineTo(left, bottom)
        page.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#2c2e33"))
        painter.drawPath(page)

        fold_path = QPainterPath()
        fold_path.moveTo(right - fold, top)
        fold_path.lineTo(right, top + fold)
        fold_path.lineTo(right - fold, top + fold)
        fold_path.closeSubpath()
        painter.setBrush(QColor(color_hex))
        painter.drawPath(fold_path)

        center_x = (left + right) / 2
        center_y = (top + bottom) / 2 + size * 0.03
        tri_r = size * 0.15
        triangle = QPolygonF([
            QPointF(center_x - tri_r * 0.6, center_y - tri_r),
            QPointF(center_x - tri_r * 0.6, center_y + tri_r),
            QPointF(center_x + tri_r * 0.9, center_y),
        ])
        painter.setBrush(QColor(color_hex))
        painter.drawPolygon(triangle)

        painter.end()
        return pixmap

    @staticmethod
    def _render_audio(size, color_hex):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        fold = size * 0.22
        left = size * 0.20
        right = size * 0.80
        top = size * 0.10
        bottom = size * 0.90

        page = QPainterPath()
        page.moveTo(left, top)
        page.lineTo(right - fold, top)
        page.lineTo(right, top + fold)
        page.lineTo(right, bottom)
        page.lineTo(left, bottom)
        page.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#2c2e33"))
        painter.drawPath(page)

        fold_path = QPainterPath()
        fold_path.moveTo(right - fold, top)
        fold_path.lineTo(right, top + fold)
        fold_path.lineTo(right - fold, top + fold)
        fold_path.closeSubpath()
        painter.setBrush(QColor(color_hex))
        painter.drawPath(fold_path)

        accent = QColor(color_hex)
        painter.setPen(Qt.NoPen)
        painter.setBrush(accent)

        note_r = size * 0.075
        stem_w = size * 0.032
        stem_h = size * 0.32
        base_x = left + size * 0.24
        base_y = bottom - size * 0.16

        painter.save()
        painter.translate(base_x, base_y)
        painter.rotate(-18)
        painter.drawEllipse(QPointF(0, 0), note_r, note_r * 0.78)
        painter.drawRect(QRectF(note_r - stem_w, -stem_h, stem_w, stem_h))
        flag = QPainterPath()
        flag.moveTo(note_r, -stem_h)
        flag.cubicTo(
            note_r + size * 0.16, -stem_h + size * 0.02,
            note_r + size * 0.14, -stem_h + size * 0.14,
            note_r, -stem_h + size * 0.18,
        )
        flag.closeSubpath()
        painter.drawPath(flag)
        painter.restore()

        painter.end()
        return pixmap


class IconOverrideProxyModel(QSortFilterProxyModel):
    """Swaps the file system model's native icons for real content
    thumbnails wherever one can be read -- images, PDFs, video frames,
    and a text preview for code/plain-text files -- and falls back to
    a flat colored glyph for everything else."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._video_thumbnailer = get_video_thumbnailer()
        self._video_thumbnailer.thumbnail_ready.connect(self._on_video_thumbnail_ready)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DecorationRole and index.column() == 0:
            source_index = self.mapToSource(index)
            fs_model = self.sourceModel()
            file_info = fs_model.fileInfo(source_index)

            if file_info.isDir():
                return IconFactory.folder_icon(size=ICON_RENDER_SIZE)

            suffix = f".{file_info.suffix().lower()}" if file_info.suffix() else ""
            path = file_info.absoluteFilePath()
            mtime = file_info.lastModified().toSecsSinceEpoch()
            color = color_for_extension(suffix)

            if suffix in IMAGE_EXTENSIONS:
                icon = IconFactory.thumbnail_icon(path, mtime, ICON_RENDER_SIZE, color, "image")
                if icon is not None:
                    return icon
            elif suffix == ".pdf":
                icon = IconFactory.thumbnail_icon(path, mtime, ICON_RENDER_SIZE, color, "pdf")
                if icon is not None:
                    return icon
            elif suffix in VIDEO_EXTENSIONS:
                if not IconFactory.video_decode_attempted(path, mtime):
                    self._video_thumbnailer.request(path, mtime)
                else:
                    icon = IconFactory.thumbnail_icon(path, mtime, ICON_RENDER_SIZE, color, "video")
                    if icon is not None:
                        return icon
                return IconFactory.video_placeholder_icon(size=ICON_RENDER_SIZE, color=color)
            elif suffix in AUDIO_EXTENSIONS:
                return IconFactory.audio_icon(size=ICON_RENDER_SIZE, color=color)
            elif suffix in TEXT_PREVIEW_EXTENSIONS:
                icon = IconFactory.thumbnail_icon(path, mtime, ICON_RENDER_SIZE, color, "text")
                if icon is not None:
                    return icon

            return IconFactory.file_icon(size=ICON_RENDER_SIZE, color=color)
        return super().data(index, role)

    def _on_video_thumbnail_ready(self, path, mtime, image):
        IconFactory.store_video_frame(path, mtime, image)
        fs_model = self.sourceModel()
        source_index = fs_model.index(path)
        if not source_index.isValid():
            return
        proxy_index = self.mapFromSource(source_index)
        if proxy_index.isValid():
            self.dataChanged.emit(proxy_index, proxy_index, [Qt.DecorationRole])


def system_font() -> QFont:
    if sys.platform == "darwin":
        family = ".AppleSystemUIFont"
    elif sys.platform == "win32":
        family = "Segoe UI"
    else:
        family = "Noto Sans"
    font = QFont(family, 10)
    return font


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------

class Sidebar(QWidget):
    """A grouped list of quick-access locations, similar to Finder's."""

    def __init__(self, on_location_chosen):
        super().__init__()
        self.setObjectName("sidebar")
        self.on_location_chosen = on_location_chosen

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(0)

        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setIndentation(12)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree.clicked.connect(self._handle_click)

        from PySide6.QtGui import QStandardItemModel, QStandardItem

        self.model = QStandardItemModel()
        root = self.model.invisibleRootItem()

        home = Path.home()
        favorites = [
            ("Home", home),
            ("Desktop", home / "Desktop"),
            ("Documents", home / "Documents"),
            ("Downloads", home / "Downloads"),
            ("Pictures", home / "Pictures"),
        ]
        self._add_section(root, "Favorites", favorites)

        locations = [("Computer", Path("/"))]
        self._add_section(root, "Locations", locations)

        self.tree.setModel(self.model)
        self.tree.expandAll()
        layout.addWidget(self.tree)

    def _add_section(self, root, title, entries):
        from PySide6.QtGui import QStandardItem

        header = QStandardItem(title.upper())
        header.setSelectable(False)
        header.setEnabled(False)
        font = header.font()
        font.setPointSize(9)
        font.setBold(True)
        header.setFont(font)
        header.setForeground(Qt.gray)
        root.appendRow(header)

        for label, path in entries:
            item = QStandardItem(IconFactory.folder_icon(size=18, color=COLORS["accent"]), label)
            item.setEditable(False)
            item.setData(str(path), Qt.UserRole)
            if not path.exists():
                item.setEnabled(False)
            root.appendRow(item)

    def _handle_click(self, index: QModelIndex):
        path = index.data(Qt.UserRole)
        if path:
            self.on_location_chosen(Path(path))


# ----------------------------------------------------------------------
# Breadcrumb path bar
# ----------------------------------------------------------------------

class Breadcrumb(QWidget):
    """Clickable path segments, e.g. Home > Projects > file_manager."""

    def __init__(self, on_segment_chosen):
        super().__init__()
        self.on_segment_chosen = on_segment_chosen
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.layout.addStretch(1)

    def set_path(self, path: Path):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        parts = path.parts
        accumulated = Path(parts[0])
        segments = [(self._label_for(accumulated, is_root=True), accumulated)]

        for part in parts[1:]:
            accumulated = accumulated / part
            segments.append((part, accumulated))

        for i, (label, full_path) in enumerate(segments):
            is_last = i == len(segments) - 1
            button = QToolButton()
            button.setObjectName("crumbCurrent" if is_last else "crumb")
            button.setText(label)
            button.setCursor(Qt.PointingHandCursor)
            button.setEnabled(not is_last)
            button.clicked.connect(lambda _, p=full_path: self.on_segment_chosen(p))
            self.layout.addWidget(button)

            if not is_last:
                sep = QLabel("/")
                sep.setStyleSheet(f"color: {COLORS['text_muted']}; padding: 0 2px;")
                self.layout.addWidget(sep)

        self.layout.addStretch(1)

    @staticmethod
    def _label_for(path: Path, is_root=False):
        if is_root:
            return "Computer" if str(path) == path.anchor else str(path)
        return path.name or str(path)


# ----------------------------------------------------------------------
# Main window
# ----------------------------------------------------------------------

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Files")
        self.resize(1080, 680)

        self.history = []
        self.future = []
        self.current_path = Path.home()

        self._build_model()
        self._build_ui()
        self._navigate_to(self.current_path, record_history=False)

    # -- model ------------------------------------------------------

    def _build_model(self):
        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath(QDir.rootPath())
        self.fs_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.fs_model.directoryLoaded.connect(self._on_directory_loaded)

        self.proxy_model = IconOverrideProxyModel()
        self.proxy_model.setSourceModel(self.fs_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)

    def _on_directory_loaded(self, path):
        if Path(path) == self.current_path:
            self._update_status()

    # -- ui construction ---------------------------------------------

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._build_toolbar())

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)

        self.sidebar = Sidebar(self._navigate_to)
        self.sidebar.setMinimumWidth(170)
        self.sidebar.setMaximumWidth(260)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        crumb_bar = QWidget()
        crumb_bar.setStyleSheet(f"background: {COLORS['content_bg']}; border-bottom: 1px solid {COLORS['border']};")
        crumb_layout = QHBoxLayout(crumb_bar)
        crumb_layout.setContentsMargins(10, 6, 10, 6)
        self.breadcrumb = Breadcrumb(self._navigate_to)
        crumb_layout.addWidget(self.breadcrumb)

        self.view = QListView()
        self.view.setModel(self.proxy_model)
        self.view.setViewMode(QListView.IconMode)
        self.view.setFlow(QListView.LeftToRight)
        self.view.setWrapping(True)
        self.view.setResizeMode(QListView.Adjust)
        self.view.setMovement(QListView.Static)
        self.view.setIconSize(QSize(64, 64))
        self.view.setGridSize(QSize(124, 108))
        self.view.setSpacing(10)
        self.view.setUniformItemSizes(True)
        self.view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.view.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self.view.doubleClicked.connect(self._handle_activate)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self._show_context_menu)
        self.view.selectionModel_needed = None

        content_layout.addWidget(crumb_bar)
        content_layout.addWidget(self.view)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(content)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([200, 880])

        outer.addWidget(splitter, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self._install_shortcuts()

    def _build_toolbar(self):
        bar = QWidget()
        bar.setObjectName("toolbar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        self.back_btn = QToolButton()
        self.back_btn.setText("\u2039")
        self.back_btn.setToolTip("Back")
        self.back_btn.clicked.connect(self._go_back)

        self.forward_btn = QToolButton()
        self.forward_btn.setText("\u203a")
        self.forward_btn.setToolTip("Forward")
        self.forward_btn.clicked.connect(self._go_forward)

        self.up_btn = QToolButton()
        self.up_btn.setText("\u2191")
        self.up_btn.setToolTip("Enclosing folder")
        self.up_btn.clicked.connect(self._go_up)

        self.view_toggle_btn = QToolButton()
        self.view_toggle_btn.setText("List View")
        self.view_toggle_btn.setToolTip("Switch between icon and list view")
        self.view_toggle_btn.setCheckable(True)
        self.view_toggle_btn.clicked.connect(self._toggle_view_mode)

        self.new_folder_btn = QToolButton()
        self.new_folder_btn.setText("+ Folder")
        self.new_folder_btn.setToolTip("New folder")
        self.new_folder_btn.clicked.connect(self._create_folder)

        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.up_btn)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.VLine)
        layout.addWidget(divider)

        layout.addWidget(self.view_toggle_btn)
        layout.addWidget(self.new_folder_btn)

        layout.addStretch(1)

        return bar

    def _install_shortcuts(self):
        QShortcut(QKeySequence("Backspace"), self, activated=self._go_up)
        QShortcut(QKeySequence("Ctrl+Shift+N"), self, activated=self._create_folder)
        QShortcut(QKeySequence.Delete, self, activated=self._delete_selected)

    # -- navigation ---------------------------------------------------

    def _navigate_to(self, path: Path, record_history=True):
        path = Path(path)
        if not path.is_dir():
            return

        if record_history and self.current_path != path:
            self.history.append(self.current_path)
            self.future.clear()

        self.current_path = path
        source_index = self.fs_model.index(str(path))
        proxy_index = self.proxy_model.mapFromSource(source_index)
        self.view.setRootIndex(proxy_index)
        self.breadcrumb.set_path(path)
        self._update_status()
        self.back_btn.setEnabled(bool(self.history))
        self.forward_btn.setEnabled(bool(self.future))
        self.up_btn.setEnabled(path.parent != path)

    def _go_back(self):
        if not self.history:
            return
        self.future.append(self.current_path)
        target = self.history.pop()
        self._navigate_to(target, record_history=False)
        self.back_btn.setEnabled(bool(self.history))
        self.forward_btn.setEnabled(bool(self.future))

    def _go_forward(self):
        if not self.future:
            return
        self.history.append(self.current_path)
        target = self.future.pop()
        self._navigate_to(target, record_history=False)
        self.back_btn.setEnabled(bool(self.history))
        self.forward_btn.setEnabled(bool(self.future))

    def _go_up(self):
        parent = self.current_path.parent
        if parent != self.current_path:
            self._navigate_to(parent)

    def _handle_activate(self, proxy_index: QModelIndex):
        source_index = self.proxy_model.mapToSource(proxy_index)
        path = Path(self.fs_model.filePath(source_index))
        if path.is_dir():
            self._navigate_to(path)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _toggle_view_mode(self):
        if self.view_toggle_btn.isChecked():
            self.view.setViewMode(QListView.ListMode)
            self.view.setFlow(QListView.TopToBottom)
            self.view.setWrapping(False)
            self.view.setIconSize(QSize(24, 24))
            self.view.setGridSize(QSize())
            self.view.setSpacing(2)
            self.view_toggle_btn.setText("Icon View")
        else:
            self.view.setViewMode(QListView.IconMode)
            self.view.setFlow(QListView.LeftToRight)
            self.view.setWrapping(True)
            self.view.setIconSize(QSize(64, 64))
            self.view.setGridSize(QSize(124, 108))
            self.view.setSpacing(10)
            self.view_toggle_btn.setText("List View")

    # -- file operations ------------------------------------------------

    def _selected_paths(self):
        paths = []
        for proxy_index in self.view.selectionModel().selectedIndexes():
            source_index = self.proxy_model.mapToSource(proxy_index)
            paths.append(Path(self.fs_model.filePath(source_index)))
        return paths

    def _create_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if not ok or not name.strip():
            return
        target = self.current_path / name.strip()
        try:
            target.mkdir(parents=False, exist_ok=False)
            self.status_bar.showMessage(f"Created {target.name}", 3000)
        except FileExistsError:
            QMessageBox.warning(self, "Already exists", "A file or folder with that name already exists.")
        except OSError as exc:
            QMessageBox.warning(self, "Could not create folder", str(exc))

    def _create_file(self):
        name, ok = QInputDialog.getText(self, "New File", "File name:")
        if not ok or not name.strip():
            return
        target = self.current_path / name.strip()
        try:
            target.touch(exist_ok=False)
            self.status_bar.showMessage(f"Created {target.name}", 3000)
        except FileExistsError:
            QMessageBox.warning(self, "Already exists", "A file with that name already exists.")
        except OSError as exc:
            QMessageBox.warning(self, "Could not create file", str(exc))

    def _rename_selected(self):
        paths = self._selected_paths()
        if len(paths) != 1:
            return
        old_path = paths[0]
        name, ok = QInputDialog.getText(self, "Rename", "New name:", text=old_path.name)
        if not ok or not name.strip() or name == old_path.name:
            return
        new_path = old_path.with_name(name.strip())
        try:
            old_path.rename(new_path)
            self.status_bar.showMessage(f"Renamed to {new_path.name}", 3000)
        except OSError as exc:
            QMessageBox.warning(self, "Could not rename", str(exc))

    def _delete_selected(self):
        paths = self._selected_paths()
        if not paths:
            return
        names = ", ".join(p.name for p in paths[:5])
        if len(paths) > 5:
            names += f", and {len(paths) - 5} more"
        reply = QMessageBox.question(
            self,
            "Move to Trash",
            f"Are you sure you want to delete {names}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        for path in paths:
            try:
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            except OSError as exc:
                QMessageBox.warning(self, "Could not delete", f"{path.name}: {exc}")
        self._update_status()

    def _reveal_in_terminal_or_open(self, path: Path):
        if path.is_dir():
            self._navigate_to(path)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _show_context_menu(self, position):
        menu = QMenu(self)
        selected = self._selected_paths()

        open_action = QAction("Open", self)
        open_action.triggered.connect(
            lambda: [self._reveal_in_terminal_or_open(p) for p in selected]
        )
        open_action.setEnabled(bool(selected))
        menu.addAction(open_action)

        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(self._rename_selected)
        rename_action.setEnabled(len(selected) == 1)
        menu.addAction(rename_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self._delete_selected)
        delete_action.setEnabled(bool(selected))
        menu.addAction(delete_action)

        menu.addSeparator()

        new_folder_action = QAction("New Folder", self)
        new_folder_action.triggered.connect(self._create_folder)
        menu.addAction(new_folder_action)

        new_file_action = QAction("New File", self)
        new_file_action.triggered.connect(self._create_file)
        menu.addAction(new_file_action)

        menu.exec(self.view.viewport().mapToGlobal(position))

    # -- status ---------------------------------------------------------

    def _update_status(self):
        source_root = self.fs_model.index(str(self.current_path))
        row_count = self.fs_model.rowCount(source_root)
        selected_count = len(self.view.selectionModel().selectedIndexes()) if self.view.selectionModel() else 0
        if selected_count:
            self.status_bar.showMessage(f"{row_count} items, {selected_count} selected")
        else:
            self.status_bar.showMessage(f"{row_count} items")


def main():
    app = QApplication(sys.argv)
    app.setFont(system_font())
    apply_dark_palette(app)
    app.setStyleSheet(STYLESHEET)

    window = FileManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
