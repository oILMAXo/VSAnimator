"""
VS Animator — Vintage Story Model + Animation Editor

Architecture: bottle HTTP server + pywebview window (no js_api bridge).
File dialogs via tkinter (independent of pywebview UI thread).
All JS-to-Python communication via HTTP fetch to localhost.
"""
import base64
import json
import os
import socket
import sys
import threading

# Disable WebView2 accessibility to prevent .NET recursion crash
os.environ.setdefault('WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS',
                      '--disable-renderer-accessibility')

from bottle import Bottle, request, response, static_file
import webview


def resource_path(relative):
    """Get absolute path to resource — works in dev and PyInstaller bundle."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


# ── Bottle HTTP server ──────────────────────────────────────────

app = Bottle()


@app.route('/')
def index():
    return static_file('vs-animator.html', root=resource_path('.'))


@app.route('/presets.js')
def presets_js():
    return static_file('presets.js', root=resource_path('.'))


@app.post('/api/open')
def api_open():
    """Show native Open dialog via tkinter, return file content."""
    response.content_type = 'application/json; charset=utf-8'
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.focus_force()
        path = filedialog.askopenfilename(
            title='Открыть файл',
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        root.destroy()

        if path and os.path.isfile(path):
            raw = open(path, 'rb').read()
            text = None
            for enc in ('utf-8-sig', 'utf-8', 'cp1251', 'latin-1'):
                try:
                    text = raw.decode(enc)
                    break
                except (UnicodeDecodeError, ValueError):
                    continue
            if text is None:
                text = raw.decode('latin-1')
            return json.dumps({'path': path, 'content': text}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': str(e)})
    return json.dumps(None)


@app.post('/api/save')
def api_save():
    """Show native Save-As dialog via tkinter, write file."""
    response.content_type = 'application/json; charset=utf-8'
    try:
        data = request.json
        content = data.get('content', '')
        default_name = data.get('defaultName', 'file.json')

        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.focus_force()
        path = filedialog.asksaveasfilename(
            title='Сохранить как',
            defaultextension='.json',
            initialfile=default_name,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        root.destroy()

        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return json.dumps(path)
    except Exception as e:
        return json.dumps({'error': str(e)})
    return json.dumps(None)


@app.post('/api/write')
def api_write():
    """Write content to a known path (no dialog)."""
    response.content_type = 'application/json; charset=utf-8'
    try:
        data = request.json
        path = data.get('path', '')
        content = data.get('content', '')
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return json.dumps(path)
    except Exception as e:
        return json.dumps({'error': str(e)})
    return json.dumps(None)


@app.post('/api/read-image')
def api_read_image():
    """Read an image file and return base64 data URI."""
    response.content_type = 'application/json; charset=utf-8'
    try:
        data = request.json
        path = data.get('path', '')
        if path and os.path.isfile(path):
            with open(path, 'rb') as f:
                raw = f.read()
            b64 = base64.b64encode(raw).decode('ascii')
            ext = os.path.splitext(path)[1].lower()
            mime = 'image/png' if ext == '.png' else 'image/jpeg'
            return json.dumps({'dataUri': f'data:{mime};base64,{b64}', 'path': path})
    except Exception as e:
        return json.dumps({'error': str(e)})
    return json.dumps(None)


@app.post('/api/texture-search')
def api_texture_search():
    """Search for texture PNGs near the model file."""
    response.content_type = 'application/json; charset=utf-8'
    try:
        data = request.json
        model_path = data.get('modelPath', '')
        textures = data.get('textures', {})
        if not model_path or not textures:
            return json.dumps({})

        model_dir = os.path.dirname(os.path.abspath(model_path))
        found = {}

        # Collect search directories (walk up from model dir)
        search_dirs = []
        d = model_dir
        for _ in range(10):
            search_dirs.append(d)
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent

        for tex_name, tex_path in textures.items():
            if not tex_path or tex_path.startswith('#'):
                continue
            clean = tex_path.split(':', 1)[-1] if ':' in tex_path else tex_path
            basename = os.path.basename(clean) + '.png'

            for sd in search_dirs:
                candidates = [
                    os.path.join(sd, clean + '.png'),
                    os.path.join(sd, 'textures', clean + '.png'),
                ]
                # Also check textures subdirectory recursively for basename match
                tex_dir = os.path.join(sd, 'textures')
                if os.path.isdir(tex_dir):
                    for root, dirs, files in os.walk(tex_dir):
                        if basename in files:
                            candidates.append(os.path.join(root, basename))

                for cand in candidates:
                    if os.path.isfile(cand):
                        found[tex_name] = os.path.abspath(cand)
                        break
                if tex_name in found:
                    break

        return json.dumps(found)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.post('/api/open-image')
def api_open_image():
    """Show native Open dialog for image files, return base64."""
    response.content_type = 'application/json; charset=utf-8'
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.focus_force()
        path = filedialog.askopenfilename(
            title='Открыть текстуру',
            filetypes=[("PNG files", "*.png"), ("All images", "*.png;*.jpg;*.jpeg")]
        )
        root.destroy()
        if path and os.path.isfile(path):
            with open(path, 'rb') as f:
                raw = f.read()
            b64 = base64.b64encode(raw).decode('ascii')
            return json.dumps({'dataUri': f'data:image/png;base64,{b64}', 'path': path})
    except Exception as e:
        return json.dumps({'error': str(e)})
    return json.dumps(None)


# ── Main ────────────────────────────────────────────────────────

def main():
    port = find_free_port()

    # Start bottle server in background
    server_thread = threading.Thread(
        target=lambda: app.run(host='127.0.0.1', port=port, quiet=True),
        daemon=True
    )
    server_thread.start()

    # Create pywebview window — NO js_api, just a browser pointing to localhost
    window = webview.create_window(
        'VS Animator',
        f'http://127.0.0.1:{port}',
        width=1150,
        height=720,
        min_size=(900, 600),
        text_select=False,
    )

    webview.start(debug=('--debug' in sys.argv))


if __name__ == '__main__':
    main()
