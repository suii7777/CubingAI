import cv2

def list_cameras():
    available_cameras = []
    for i in range(10):  # Check first 10 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera {i} is available")
                available_cameras.append(i)
            cap.release()
        else:
            print(f"Camera {i} is not available")
    return available_cameras

if __name__ == "__main__":
    print("Checking available cameras...")
    cameras = list_cameras()
    if cameras:
        print(f"\nFound {len(cameras)} available camera(s) at indices: {cameras}")
    else:
        print("\nNo cameras found!")
