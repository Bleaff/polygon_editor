import cv2
import json
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Polygon Editor",
        epilog="""
Controls:

Left Mouse Button (LMB):
  - Click on a point — select point (highlighted in green)
  - Drag — move the selected point
  - Release — deselect point

Right Mouse Button (RMB):
  - Click — add a new point

Middle Mouse Button (MMB / wheel click):
  - Click on a point — remove the point

Keyboard:
  - S — save points to file (normalized with precision up to 0.001)
  - ESC — exit the editor
"""
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the file with polygon points.")
    parser.add_argument("-src", "--source", required=True, help="RTSP stream URL.")
    return parser.parse_args()



def normalize_points(points, width, height):
    """Normalize point coordinates to the [0, 1] range based on frame dimensions."""
    return [[round(x / width, 3), round(y / height, 3)] for x, y in points]


def denormalize_points(points, width, height):
    """Convert normalized coordinates back to pixel coordinates."""
    return [(int(x * width), int(y * height)) for x, y in points]


def load_polygon(file_path, width, height):
    """Load polygon points from a file and convert them to pixel coordinates."""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Starting with an empty polygon.")
        return []
    try:
        with open(file_path, 'r') as f:
            normalized_points = json.load(f)
            if isinstance(normalized_points, list):
                return denormalize_points(normalized_points, width, height)
            else:
                print(f"Invalid format in {file_path}. Starting with an empty polygon.")
                return []
    except json.JSONDecodeError:
        print(f"Error parsing JSON in {file_path}. Starting with an empty polygon.")
        return []


def save_polygon(file_path, points, width, height):
    """Save current polygon points to a file in normalized format."""
    normalized_points = normalize_points(points, width, height)
    with open(file_path, 'w') as f:
        json.dump(normalized_points, f, indent=4)
    print(f"Polygon saved to {file_path}.")


def main():
    args = parse_arguments()
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print("Failed to open RTSP stream.")
        return

    # Read the first frame to get video dimensions
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab initial frame.")
        return

    height, width = frame.shape[:2]

    # Load previously saved polygon
    points = load_polygon(args.file, width, height)

    selected_point = None  # Index of the currently selected point (if any)

    def mouse_callback(event, x, y, flags, param):
        nonlocal selected_point, points

        if event == cv2.EVENT_LBUTTONDOWN:
            # Try selecting a nearby point to move
            for i, (px, py) in enumerate(points):
                if abs(x - px) < 10 and abs(y - py) < 10:
                    selected_point = i
                    break

        elif event == cv2.EVENT_MOUSEMOVE and selected_point is not None:
            # Move the selected point
            points[selected_point] = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            # Deselect the point
            selected_point = None

        elif event == cv2.EVENT_RBUTTONDOWN:
            # Add a new point
            points.append((x, y))
            print(f"Added point: ({x}, {y})")

        elif event == cv2.EVENT_MBUTTONDOWN:
            # Remove a point if clicked near it
            for i, (px, py) in enumerate(points):
                if abs(x - px) < 10 and abs(y - py) < 10:
                    points.pop(i)
                    print(f"Removed point: ({px}, {py})")
                    break

    cv2.namedWindow("Polygon Editor")
    cv2.setMouseCallback("Polygon Editor", mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Draw polygon lines and points
        for i, point in enumerate(points):
            next_point = points[(i + 1) % len(points)] if len(points) > 1 else point
            cv2.line(frame, point, next_point, (0, 255, 0), 2)

            # Green for selected point, red for others
            color = (0, 255, 0) if i == selected_point else (0, 0, 255)
            cv2.circle(frame, point, 5, color, -1)

        cv2.imshow("Polygon Editor", frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC key to exit
            break
        elif key == ord('s'):  # 's' key to save
            save_polygon(args.file, points, width, height)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
