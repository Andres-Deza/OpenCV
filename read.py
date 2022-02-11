import cv2 as cv

# Para imagen
# img=cv.imread('imagen/prueba3.png')

# cv.imshow('Prueba', img)

# 0 es para grabar camara
capture= cv.VideoCapture('videoSalida.mp4')
salida= cv.VideoWriter('videoSalida.mp4',cv.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
while (capture.isOpened()):
   istrue, frame=capture.read()
   if istrue==True:
      cv.imshow('Video', frame)
      salida.write(frame)
      if cv.waitKey(20) & 0xFF==ord('d'):
         break
   else: break
capture.release()
# salida.release()
# cv.waitKey(0)
cv.destroyAllWindows()
