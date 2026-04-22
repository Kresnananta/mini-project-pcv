import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread('input/parking_ori.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# remove grainy noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# otsu thresholding for separating bright(cars) and dark areas
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


kernel_open = np.ones((5, 5), np.uint8)
opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)

# memadatkan mobil
kernel_dilate = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(opened, kernel_dilate, iterations=1)


contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result_img = img_rgb.copy()
car_count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)
    
    # filter area
    if 2500 < area < 15000: 
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        
        # filter bentuk (buang garis parkir yg memanjang)
        if 0.4 < aspect_ratio < 2.5:
            car_count += 1
            cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 4)
            cv2.putText(result_img, f"{car_count}", (x, y - 7), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)


plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
plt.imshow(thresh, cmap='gray')
plt.title('1. Otsu Threshold (Banyak Noise Garis)')
plt.axis('off')
cv2.imwrite('output/steps/parking_thresh.jpg', thresh)

plt.subplot(2, 2, 2)
plt.imshow(opened, cmap='gray')
plt.title('2. Morph Opening (Garis Dihapus)')
plt.axis('off')
cv2.imwrite('output/steps/parking_opened.jpg', opened)

plt.subplot(2, 2, 3)
plt.imshow(dilated, cmap='gray')
plt.title('3. Morph Dilation (Mobil Dipadatkan)')
plt.axis('off')
cv2.imwrite('output/steps/parking_dilated.jpg', dilated)

plt.subplot(2, 2, 4)
plt.imshow(result_img)
plt.title(f'4. Hasil Akhir ({car_count} Mobil)')
plt.axis('off')
cv2.imwrite('output/parking_counted.jpg', cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR))

plt.tight_layout()
plt.show()