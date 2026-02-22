"""
VS Animator — Vintage Story Model + Animation Editor
Python wrapper using pywebview. Supports both dev and PyInstaller bundled mode.
"""
import os
import sys
import webview


def resource_path(relative):
    """Get absolute path to resource — works in dev and PyInstaller bundle."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)


class Api:
    """Exposed to JavaScript via pywebview.api"""

    def __init__(self):
        self.window = None

    def save_file(self, content, default_name, file_types):
        """Show Save dialog, write content to chosen file. Returns path or None."""
        result = self.window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=default_name,
            file_types=(file_types, "All files (*.*)")
        )
        if result:
            path = result if isinstance(result, str) else result[0] if result else None
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return path
        return None

    def load_file(self, file_types):
        """Show Open dialog, read file. Returns {path, content} or None."""
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=(file_types, "All files (*.*)")
        )
        if result:
            path = result if isinstance(result, str) else result[0] if result else None
            if path and os.path.isfile(path):
                raw = open(path, 'rb').read()
                for enc in ('utf-8-sig', 'utf-8', 'cp1251', 'latin-1'):
                    try:
                        text = raw.decode(enc)
                        return {'path': path, 'content': text}
                    except (UnicodeDecodeError, ValueError):
                        continue
                return {'path': path, 'content': raw.decode('latin-1')}
        return None


def main():
    api = Api()

    html_path = resource_path('vs-animator.html')

    window = webview.create_window(
        'VS Animator',
        html_path,
        width=1150,
        height=720,
        min_size=(900, 600),
        js_api=api,
        text_select=False,
    )
    api.window = window

    def on_closing():
        try:
            has_dirty = window.evaluate_js(
                '(function(){return window.docs&&window.docs.some(function(d){return d.dirty;});})()'
            )
            if has_dirty:
                confirmed = window.evaluate_js(
                    'confirm("Есть несохранённые изменения.\\nЗакрыть приложение?")'
                )
                if not confirmed:
                    return True   # prevent close
        except Exception:
            pass

    window.events.closing += on_closing

    webview.start(debug=('--debug' in sys.argv))


if __name__ == '__main__':
    main()
