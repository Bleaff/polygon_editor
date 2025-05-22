# 🖼️ Polygon Editor – Interactive RTSP Polygon Annotator

An interactive tool for editing polygonal regions on an RTSP video stream. Add, move, and delete points with your mouse, and save them in a normalized JSON format with precision up to 3 decimal places.

---

## 🚀 Features

- Connect to an RTSP stream
- Draw and edit polygons interactively
- Add / move / delete points with mouse
- Save polygons in normalized JSON (x, y in range [0, 1])
- Highlight selected point (green)

---

## 📦 Installation

Install required dependencies:

```python3

pip install opencv-python

```
---

## ▶️ Usage

Run the script with RTSP source and output polygon file:
```
python polygon_editor.py -src <rtsp_url> -f <polygon.json>
```

Example:
python polygon_editor.py -src rtsp://192.168.1.10:554/stream1 -f zone.json



---

## 🖱️ Controls

| Action                        | Input                        |
|------------------------------|------------------------------|
| Select & move point          | Left-click + drag            |
| Add a new point              | Right-click                  |
| Delete a point               | Middle-click (wheel click)   |
| Save polygon to file         | Press `S`                    |
| Exit editor                  | Press `ESC`                  |

💡 Selected point is highlighted **green**, all others are **red**.

---

## 📝 Output Format

Saved JSON contains **normalized coordinates** with **3 decimal places**:

```json
[
    [0.253, 0.372],
    [0.412, 0.684],
    [0.612, 0.399]
]
```

🛠 Use Cases

    Define zones for object tracking or detection

    Annotate video for computer vision models

    Create ROIs in real time with visual feedback

🧠 Author

Built with ❤️ by a computer vision infrastructure engineer.
