import cv2 as cv
import os
import argparse

def generate_marker(marker_id=0, marker_size=600, dict_type=cv.aruco.DICT_6X6_250):
    # Create output folder
    os.makedirs("markers", exist_ok=True)

    # Load dictionary
    dictionary = cv.aruco.getPredefinedDictionary(dict_type)

    # Generate marker
    marker_image = cv.aruco.generateImageMarker(dictionary, marker_id, marker_size)

    # Save file
    filename = f"markers/aruco_marker_ID{marker_id}.png"
    cv.imwrite(filename, marker_image)

    # Show it
    cv.imshow(f"ArUco Marker ID {marker_id}", marker_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    print(f"[✓] ArUco marker ID {marker_id} saved as {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ArUco markers")
    parser.add_argument("--id", type=int, default=0, help="Marker ID (0-249)")
    parser.add_argument("--size", type=int, default=600, help="Size of marker in pixels")

    args = parser.parse_args()
    generate_marker(marker_id=args.id, marker_size=args.size)
