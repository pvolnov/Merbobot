from catboost import CatBoostClassifier
import matplotlib
import scipy.misc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import catboost
import cv2
import numpy as np
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):

    mask = np.zeros_like(img)   
    
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
  
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=(255, 0, 0), thickness=7):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros(img.shape, dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)
def add_data(file_name, to_show = False):
    img = cv2.imread(file_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    size = 700
    #im = image.load_img('10.jpg', target_size = (size, size))
    #img = 255 - img
    #show(img)
    #img[img<100]=0

    img = cv2.resize(img, (size, size))
    im = np.array(img)
    #img = 1 - img
    gray = grayscale(img)
    blur = gaussian_blur(gray, 7)
    edge = canny(blur, 50, 300)
    
    img = np.array(im)
    l = 0;
    r = 300

    #print(lines is None)
    while l + 1 != r:
        m = (l + r)//2
        #print(m)
        lines = cv2.HoughLines(edge, 1, np.pi/180, m)
        size = 0;
        if(not(lines is None)): size = len(lines)
        if size > 10:
            l = m
        else:
            r = m
    if len(lines) < 2: 
        return -1
    #print(l)
    #print(lines.shape)
    def gety(p):
        a = np.cos(p[1])
        b = np.sin(p[1])
        y0 = b*p[0]
        y1 = int(y0)
        return y1

    def gety2(p):
        a = np.cos(p[1])
        b = np.sin(p[1])
        x0 = a*p[0]
        y0 = b*p[0]
        y2 = int(y0 - img.shape[0]*(a))
        return y2

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    mean_angle = lines[:,:,1].mean()
    eps = np.pi / 10;
    new_lines = []
    for i in lines:
        if abs(i[:,1] - mean_angle) < eps:
            new_lines.append(i)
    lines = np.array(new_lines)
    if len(lines) < 2: 
        return -1

    new_lines = []
    hight = []
    for i in lines:
        hight.append(gety(i[0]))
    dist = []
    hight.sort()
    for i in range(len(hight) - 1):
        dist.append(hight[i + 1] - hight[i])
    mean_hi = np.array(dist).mean() / 1.2
    #mean_hi = 50
    y_cord = []
    #print(mean_hi)
    for i in lines:
        y = gety(i[0])
        if len(y_cord) == 0 or abs(find_nearest(np.array(y_cord), y) - y) > mean_hi:
            new_lines.append(i)
        y_cord.append(y)
    lines = np.array(new_lines)
    if len(lines) < 2: 
        return -1
    hight = []
    for i in lines:
        hight.append(gety(i[0]))
    dist = []
    hight.sort()
    for i in range(len(hight) - 1):
        dist.append(hight[i + 1] - hight[i])
    min_dist = np.array(dist).min()
    lines = np.array(sorted(lines, key=lambda x: gety(x[0])))
    if len(lines) < 2: 
        return -1
    
    add_lines = []
    for i in range(lines.shape[0] - 1):
        dist = gety(lines[i + 1][0]) - gety(lines[i][0])
        mean_angle = (lines[i + 1][0][1] + lines[i][0][1])/2;

        num = int(round(dist / min_dist)) - 1;
        curr_d = dist / (num + 1)
        for j in range(num):
            line = np.array(lines[i])
            line[0][0] += (j + 1) * curr_d;
            line[0][1] = mean_angle;
            add_lines.append(line)

    for i in lines:
        add_lines.append(i)
    lines = np.array(add_lines)
    #print(lines.shape)
    lines = np.array(sorted(lines, key=lambda x: gety(x[0])))

    #!!!!!!!!!!!!!!!
    step = min_dist // 3
    color_vector = []
    product_data = []
    all_data = []
    amount_shelfs = 0;
    for i in range(lines.shape[0] - 1):
        #break
        y1 = gety(lines[i][0])
        y2 = gety2(lines[i][0])
        Y1 = gety(lines[i + 1][0])
        Y2 = gety2(lines[i + 1][0])
        #print('y1 = ', y1, " Y1 = ", Y1)
        center1 = (y1 + Y1) // 2;
        center2 = (y2 + Y2) // 2;
        #print('center1 = ', center1)
        ##!!!!!!!!!!!!!!
        d = int(((Y1 - y1 + Y2 - y2) / 4 / 1.3))
        #print('d = ', d)
        j = 0;
        shelf = []
        while j < img.shape[0] - step:
            x1 = j;
            x2 = j + step;
            y = j*(center2 - center1) // img.shape[0] + center1;
            y_1 = y - d;
            y_2 = y + d
            #numpy.mean(image_array, axis=0)`
            #print(x1, x2, y_1, y_2)
            curr = []
            vec = im[y_1:y_2, x1:x2]
            h = (y_2 - y_1)//3
            color = np.median(vec, axis=(0, 1))
            color2 = np.mean(vec, axis=(0, 1))

            for k in range(3):
                curr.append(color[k])
                curr.append(color2[k])
                max1 = np.max(vec[:,:,k])

            for u in range(3):
                vec1 = vec[u*h: (u + 1)*h, : ]
                color = np.median(vec1, axis=(0, 1))
                color2 = np.mean(vec1, axis=(0, 1))

                for k in range(3):
                    curr.append(color[k])
                    curr.append(color2[k])
                    max1 = np.max(vec1[:,:,k])


            #print(color.shape)
            #img[y_1:y_2, x1:x2] = color
            if len(curr) > 0:
                all_data.append(np.array(curr))
                shelf.append(np.array(curr))
            #cv2.rectangle(img,(x1,x2),(y_1, y_2),(0,255,0),1)
            #print(color)
            j += step
            cv2.rectangle(img,(x1,y_1),(x2,y_2),(0,255,0),1)
            #break;
        #print("")
        product_data.append(np.array(shelf))
        #break;
    
    
    product_data = np.array(product_data)

    for j in lines:
        for rho,theta in j:
            #print(theta)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            #print(y1)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

    #cv2.imwrite('houghlines3.jpg',img)
    #if(to_show): show(img)
    return all_data
    #color_vector = color_vector.astype(int)
    #print(product_data.shape)
    #color_vector[0][0] = 255
    #color_vector[-1,:, 0] = 255
    #print(color_vector[:5][:5])
    #show(color_vector)
    #print(color_vector.shape)
    #print(img.shape)
def get_arrage_status(name):
    model = CatBoostClassifier()
    model.load_model("catboost_detect")
    a = add_data(name)
    if a == -1:
        return 0
    if len(a) <2:
        return 0
    img_data = np.array(a)
    img_data /= 255
    out_pred = model.predict_proba(img_data)
    s = ""
    uv = []
    out = ''
    for i in out_pred:
        #print(i)
        s += str(i.argmax())
        uv.append(i.max())
    #print(len(s))
    l = 0
    s += '9'
    r = 0
    c = '9'
    arr = []
    for i in s:
        if(i == '0'):
            c = '9'
        if i!=c:
            arr.append(l)
            c = i;
            l = 1
        else:
            l += 1
    arr.sort()
    arr.reverse()
    metric = np.array(arr[:5]).sum()
    return metric
    #print(metric)
#     for i in range(num):
#         for j in range(k):
#             out += s[r]
#             r+=1
#         out +='\n'
    
# print(out)
#print(123)
#print(get_arrage_status("1.jpg"))