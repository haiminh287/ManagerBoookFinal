import cv2
from pyzbar.pyzbar import decode
def scan_barcode():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        return "Không thể mở webcam."
    print("Đưa mã vạch hoặc mã QR vào trước camera...")
    while True:
        ret, frame = cap.read()
        if not ret:
            return "Không thể nhận hình ảnh từ webcam."
        barcodes = decode(frame)
        if barcodes:
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                print(f"Đã quét: {barcode_data} (Loại: {barcode_type})")
                return barcode_data
        cv2.imshow("Quét mã vạch", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return "Đã quét mã vạch thành công."