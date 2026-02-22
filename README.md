# VS Animator

> ⚠️ **Версия 0.1 — приложение в ранней стадии разработки, возможны баги и недоработки.**

3D-редактор моделей и анимаций для игры Vintage Story.

Позволяет импортировать VS shape JSON, просматривать и редактировать модели (элементы, иерархия, позиции, вращения), создавать анимации с ключевыми кадрами и экспортировать результат обратно в формат Vintage Story.

## Возможности

- Импорт/экспорт VS shape JSON (модели + анимации)
- 3D-превью модели с вращением камеры
- Система вкладок — несколько документов одновременно
- Дерево элементов с раскрытием/сворачиванием
- Редактор свойств элемента (from/to, rotationOrigin, rest rotation)
- CRUD элементов: добавить, дочерний, дублировать, удалить
- Режимы «Модель» и «Анимация»
- Таймлайн с ключевыми кадрами (добавить, удалить, копировать, вставить)
- Несколько анимаций в одном документе
- 148 пресетов анимаций из игры (walk, run, idle, attack и др.)
- Плавное воспроизведение с зацикливанием
- Перетаскивание элементов в 3D
- Выделение по клику на грань
- Подтверждение при закрытии с несохранёнными изменениями

## Автор

Идея и концепция: **ilmax** ([oILMAXo](https://github.com/oILMAXo))

Разработка: **Claude** (Anthropic), модель Claude Opus 4

## Технологии

- Python 3.11 + pywebview (десктопное окно)
- HTML/CSS/JS (интерфейс, единый файл ~82 КБ)
- PyInstaller (сборка в .exe)

## Запуск

Запустить `VSAnimator.exe`. Установка не требуется.

Для запуска из исходников:
```
pip install pywebview
python src/vs_animator_app.py
```

---

# VS Animator (English)

> ⚠️ **Version 0.1 — early development stage, bugs and rough edges expected.**

3D model and animation editor for the game Vintage Story.

Import VS shape JSON files, view and edit models (elements, hierarchy, positions, rotations), create keyframe animations, and export back to Vintage Story format.

## Features

- Import/export VS shape JSON (models + animations)
- 3D model preview with camera rotation
- Tab system — multiple documents at once
- Element tree with expand/collapse
- Element property editor (from/to, rotationOrigin, rest rotation)
- Element CRUD: add, add child, duplicate, delete
- "Model" and "Animation" editor modes
- Timeline with keyframes (add, remove, copy, paste)
- Multiple animations per document
- 148 built-in animation presets from the game (walk, run, idle, attack, etc.)
- Smooth playback with looping
- Drag-to-move elements in 3D
- Face-click selection
- Unsaved changes confirmation on close

## Author

Idea and concept: **ilmax** ([oILMAXo](https://github.com/oILMAXo))

Development: **Claude** (Anthropic), Claude Opus 4 model

## Tech stack

- Python 3.11 + pywebview (desktop window)
- HTML/CSS/JS (UI, single file ~82 KB)
- PyInstaller (exe build)

## Running

Run `VSAnimator.exe`. No installation required.

To run from source:
```
pip install pywebview
python src/vs_animator_app.py
```
