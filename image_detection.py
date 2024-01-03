import socket

# server info
HOST = '192.168.252.1'
PORT = 8001

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST, PORT))


import cv2

from roboflow import Roboflow
rf = Roboflow(api_key="GoCmsVM2tUzTcuVTiYfX")
project = rf.workspace().project("playing-cards-ow27d")
model = project.version(4).model

# current camera
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20, (640, 480))
card = []
ans = []
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        out.write(frame)
        cv2.imshow('frame', frame)
        x = model.predict(frame, confidence=40, overlap=30).json()
        if len(x['predictions']) > 0 :
            if len(card) < 1 :
                card.append(x['predictions'][0]['class'])
            else :
                if x['predictions'][0]['class'] != card[0] :
                    card.append(x['predictions'][0]['class'])
        if len(card) == 2 :
            ans.append(card[0].lower())
            ans.append(card[1].lower())
            print(ans)
            break
        key = cv2.waitKey(1)
        # ESC
        if key == 27:
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

msg =  "p2 " + ans[0] + " " + ans[1]
s.send(msg.encode())#發送
data = s.recv(1024)#接收伺服器訊息
print(data)
s.close()
