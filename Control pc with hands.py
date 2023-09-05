import cv2
from mediapipe import solutions
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui as pg
import time 

#%%

# Kameradan video akışı alır (0, yerel kamera)
cap = cv2.VideoCapture(0)

# mediapipe kütüphanesinden çizim işlevlerini içe aktarır
mpDraw = solutions.drawing_utils

# mediapipe kütüphanesinden el algılama (hands) modelini içe aktarır
mpHands = solutions.hands

# En fazla bir eli algılamak için Hands sınıfını başlatır
hands = mpHands.Hands(max_num_hands=1)

# Ses cihazlarını alır (örneğin, hoparlörler)
devices = AudioUtilities.GetSpeakers()

# Sistem ses seviyesini değiştirmek için bir arayüzü etkinleştirir
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Ses seviyesini değiştirmek için IAudioEndpointVolume arabirimini kullanır
volume = interface.QueryInterface(IAudioEndpointVolume)

#%%

# Renk kodu tanımlaması (Mavi renk)
color = (0, 255, 255)

# İlgilenilen el landmark'larının indekslerini içeren bir liste
idlist = (13, 15)

# Ölçülen mesafelerin depolanacağı bir boş liste
dislist = []

# Ses seviye oranlarının depolanacağı bir boş liste
ratio = []

# Başlangıç ses seviyesi (yüzde olarak, %50)
vol = 50
  

#%%

# Sistem ses seviyesini ayarlamak için bir fonkisyon tanımlar.
def set_system_volume(new_volume):
    
    # Ses cihazlarını alır (örneğin, hoparlörler)
    devices = AudioUtilities.GetSpeakers()
    
    # Ses seviyesini değiştirmek için bir arabirimi etkinleştirir
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
    # IAudioEndpointVolume arabirimini kullanarak ses kontrolünü sağlar
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Yeni ses seviyesini belirtilen ölçekte ayarlar (0.0 - 1.0 arası bir değer)
    volume.SetMasterVolumeLevelScalar(new_volume, None)


#%%


def draw_volume_on_image(img, volume):
    # Ses seviyesini görüntüye yazdırma işlemi
    cv2.putText(img, f"Ses Seviyesi: {volume}%", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



#%%

# Sonsuz bir döngü başlatılır, bu döngü her zaman çalışır.
while True:
    # Kameradan bir video çerçevesi okur ve çerçeveyi 'sucsess' ve 'img2' değişkenlerine atar.
    sucsess, img2 = cap.read()
    
    # Okunan çerçeve, BGR renk formatından RGB renk formatına dönüştürülür ve 'imgRGB' adlı yeni bir değişkene kaydedilir.
    #RGB formatına çevirlmesinin sebebi elleri algılayacak modelin rgb formatını destekliyor olmasıdır.
    imgRGB = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    # Elleri algılamak için mediapipe ile işlem yapar ve sonuçları 'results' adlı bir değişkene atar.
    results = hands.process(imgRGB)
        
    # Eğer birden fazla el tespit edilmişse:
    if results.multi_hand_landmarks:
        # Her el için döngü başlatılır.
        for handlms in results.multi_hand_landmarks:
            # Ellerin landmark'larını çizer ve çerçeve üzerine işler.
            mpDraw.draw_landmarks(img2, handlms, mpHands.HAND_CONNECTIONS)


#%%

            # Ellerin landmark'larını taramak için bir döngü başlatılır.
            for id, lm in enumerate(handlms.landmark):

                # Çerçevenin boyutları (yükseklik, genişlik ve kanal sayısı) alınır
                h, w, c = img2.shape


            # İşaret parmağı (4), başparmak (8), orta parmak (12) ve serçe parmağı (20) mevcutsa:
            if (
                handlms.landmark[4] and
                handlms.landmark[8] and
                handlms.landmark[12] and
                handlms.landmark[20]
            ):

                # İlgili landmark'ların ekran koordinatlarını hesapla
                
                #Baş parmak
                x1, y1 = int(handlms.landmark[4].x * w), int(handlms.landmark[4].y * h) 
                
                #İşaret parmak
                x2, y2 = int(handlms.landmark[8].x * w), int(handlms.landmark[8].y * h)
                
                #Orta parmak
                x3, y3 = int(handlms.landmark[12].x * w), int(handlms.landmark[12].y * h)
                
                #Serçe parmak
                x4, y4 = int(handlms.landmark[20].x * w), int(handlms.landmark[20].y * h)


                # İlgili noktalar arasındaki mesafeyi hesaplar
                
                #Başparmak ile işaret parmak arasındaki mesafeyi hesaplar
                distance_vol_up = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
                
                #Başparmak ile orta parmak arasındaki mesafeyi hesaplar.
                distance_vol_down = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
                
                #Başparmak ile serçe parmak arasındaki mesafeyi hesaplar.
                distance_pause = math.sqrt((x4 - x1)**2 + (y4 - y1)**2)

#%%

                #Başparmak ve serçe parmak arasındaki mesafe (distance_pause) '45' eşik değerinden küçükse:
                if distance_pause <= 45: 
            
                    # "space" tuşuna basar.
                    pg.press("space") 
                    
                    # 0.2 saniye bekler.
                    time.sleep(0.2) 
                      
                # Ses yükseltme mesafesi '30' eşik değerinden küçükse:
                elif distance_vol_up < 30: 
                    
                    # Eğer ses seviyesi '100' değerinden küçükse, 
                    if vol < 100:  
                        
                        #ses seviyesini 2 artır.
                        vol += 2  
                            
                    # Ses seviyesini oran olarak hesapla ve maksimum değeri '1.0' ile sınırla.
                    # '1.0' ile sınırlandırılmasının sebebi ses seviyesinin maksimum %100 ' e kadar arttırılabilmesidir.
                    volratio = min(1.0, vol / 100)  
                        
                    # Sistem ses seviyesini ayarlayan fonksiyona volratio değişkeni gönderilir ve ses ayarlanır.
                    set_system_volume(volratio) 
                    
                    #Ses seviyesini yazdır
                    print(vol)
                        
                
                # Ses düşürme mesafesi '30' eşik değerinden küçükse:
                elif distance_vol_down < 30: 
                    
                    # Eğer ses seviyesi '0' değerinden büyükse, 
                    if vol > 0:  
                        
                        #ses seviyesini 2 azalt.
                        vol -= 2 
                            
                    
                    # Ses seviyesini oran olarak hesapla ve minimum değeri '0.0' ile sınırla.
                    # '0.0' ile sınırlandırılmasının sebebi ses seviyesinin minimum  %0 ' a kadar azaltılabilmesidir.
                    volratio = max(0.0, vol / 100 )
                       
                    # Sistem ses seviyesini ayarlayan fonksiyona volratio değişkeni gönderilir ve ses ayarlanır.
                    set_system_volume(volratio)
                    
                    #Ses seviyesini yazdır
                    print(vol)
                    
#%%

                # İki nokta arasında bir çizgi çizer (işaret parmağından başparmağa)
                cv2.line(img2, (x1, y1), (x2, y2), (255, 255, 255), 4)  

                # İki nokta arasında bir çizgi çizer (orta parmak ile işaret parmağı arasında)
                cv2.line(img2, (x3, y3), (x1, y1), (255, 255, 255), 4) 

                # İki nokta arasında bir çizgi çizer (yüzük parmağı ile işaret parmağı arasında)
                cv2.line(img2, (x4, y4), (x1, y1), (255, 255, 255), 4)  

                # İşaret parmağı ve başparmak için dolgulu daireler çizer
                cv2.circle(img2, (x1, y1), 6, (255, 255, 0), cv2.FILLED)  # İşaret parmağı
                cv2.circle(img2, (x2, y2), 6, (255, 255, 0), cv2.FILLED)  # Başparmak

                # Orta parmak ve serçe parmağı için dolgulu daireler çizer
                cv2.circle(img2, (x3, y3), 6, (255, 255, 0), cv2.FILLED)  # Orta parmak
                cv2.circle(img2, (x4, y4), 6, (255, 255, 0), cv2.FILLED)  # Serçe parmağı


#%%
    draw_volume_on_image(img2, vol)
    
    # Resmi yatay eksende (sol-sağ) çevirerek ayna görüntüsü elde eder
    # img2 = cv2.flip(img2, 1)

    # 'img' adında bir pencere açar ve çerçeveyi bu pencerede gösterir
    cv2.imshow("img", img2)

    # Bir tuşa basılmasını bekler ve 'q' tuşuna basılırsa döngüyü sonlandırır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera kaynağını serbest bırakır
cap.release()

# Tüm penceleri kapatır ve programı sonlandırır
cv2.destroyAllWindows()

