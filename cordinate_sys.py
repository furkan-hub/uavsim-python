from pyproj import Transformer
import numpy as np
import copy
import math

def calculate_bearing(coord1, coord2):
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    delta_lon = lon2 - lon1

    x = math.cos(lat2) * math.sin(delta_lon)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360
    bearing = (bearing + 180) % 360

    return bearing

def haversine_distance(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]

    # Latitüd ve longitüd değerlerini radyan cinsine çevirme
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formülü
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Dünya'nın yarıçapı
    radius_of_earth = 6371  # Kilometre cinsinden

    # Uzaklık hesaplama
    distance = radius_of_earth * c
    return distance

def translate_coordinates(coord, bearing, distance):
    # Koordinatları öteleme
    lat = coord[0] 
    lon = coord[1]
    lat_rad, lon_rad = map(math.radians, [lat, lon])
    radius_of_earth = 6371
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance / radius_of_earth) +
                            math.cos(lat_rad) * math.sin(distance / radius_of_earth) * math.cos(math.radians(bearing)))

    new_lon_rad = lon_rad + math.atan2(math.sin(math.radians(bearing)) * math.sin(distance / radius_of_earth) * math.cos(lat_rad),
                                       math.cos(distance / radius_of_earth) - math.sin(lat_rad) * math.sin(new_lat_rad))

    new_lat, new_lon = math.degrees(new_lat_rad), math.degrees(new_lon_rad)
    return [new_lat, new_lon]

def cartesian_to_lat_lon(X, Y):
    """
    Kartezyen koordinatları (X, Y) kullanarak latitude ve longitude'u hesaplar.

    Args:
        X: Kartezyen koordinat sisteminde X koordinatı.
        Y: Kartezyen koordinat sisteminde Y koordinatı.

    Returns:
        Enlem ve boylam değerleri (latitude, longitude).
    """
    R = 6371000  # Dünya yarıçapı (metre)

    # Kartezyen koordinatları kullanarak latitud ve longitud'u hesapla
    distance = math.sqrt(X**2 + Y**2)
    latitude_rad = math.asin(Y / distance)
    longitude_rad = math.atan2(X, Y)

    # Radyan cinsinden değerleri dereceye çevir
    latitude = math.degrees(latitude_rad)
    longitude = math.degrees(longitude_rad)

    return latitude, longitude

def lat_lon_to_cartesian(latitude, longitude):
    """
    Latitude ve longitude'u kartezyen koordinatlara dönüştürme.

    Args:
        latitude: Enlem (derece cinsinden).
        longitude: Boylam (derece cinsinden).

    Returns:
        X ve Y kartezyen koordinatları.
    """
    R = 6371000  # Dünya yarıçapı (metre)

    # Dereceyi radyana çevir
    latitude_rad = math.radians(latitude)
    longitude_rad = math.radians(longitude)

    # Kartezyen koordinatları hesapla
    X = R * math.cos(latitude_rad) * math.cos(longitude_rad)
    Y = R * math.cos(latitude_rad) * math.sin(longitude_rad)

    return X, Y

def transform_point_2d(matrix, point):
    """
    2D öteleme matrisi ile noktayı dönüştürme.
    
    Args:
        matrix: 2D öteleme matrisi.
        point: Dönüştürülecek nokta (x, y).
    
    Returns:
        Dönüştürülmüş noktanın koordinatları (x_transformed, y_transformed).
    """
    point = np.array([point[0], point[1], 1])  # Homojen koordinat sistemine dönüştür
    transformed_point = np.dot(matrix, point)
    
    return [transformed_point[0], transformed_point[1]]

def translation_matrix_2d(dx, dy):
    """
    2D öteleme matrisi oluşturur.
    
    Args:
        dx: X ekseni boyunca öteleme miktarı.
        dy: Y ekseni boyunca öteleme miktarı.
    
    Returns:
        2D öteleme matrisi.
    """
    return np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ])

#region rotation matris
def yaw_rotation_matrix(yaw_angle):
    yaw_matrix = np.array([
        [np.cos(yaw_angle), -np.sin(yaw_angle), 0],
        [np.sin(yaw_angle), np.cos(yaw_angle), 0],
        [0, 0, 1]
    ])
    return yaw_matrix

def pitch_rotation_matrix(pitch_angle):
    pitch_matrix = np.array([
        [np.cos(pitch_angle), 0, np.sin(pitch_angle)],
        [0, 1, 0],
        [-np.sin(pitch_angle), 0, np.cos(pitch_angle)]
    ])
    return pitch_matrix

def roll_rotation_matrix(roll_angle):
    roll_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(roll_angle), -np.sin(roll_angle)],
        [0, np.sin(roll_angle), np.cos(roll_angle)]
    ])
    return roll_matrix
#endregion

def len3d(vec3):
    return np.sqrt(vec3[0]**2+vec3[1]**2+vec3[2]**2)
def subList(list1,list2):
    result=[]
    for i in range(len(list1)):
        result.append(list1[i]-list2[i])
    return result

def convert_to_0_360(angle):
    return angle % 360


class LocationConverter:
    def __init__(self) -> None:
        self.trans_GPS_to_XYZ = Transformer.from_crs(4979, 4978)
    def relativeLoc(self,loc1,loc2):
        """lat,lon,alt"""
    # lon,lat,alt -> x,y,z
        first=self.trans_GPS_to_XYZ.transform(*loc1)
        rad1=len3d(first)
    # ang1=[-30.2906140,0,-40.7991680]
        second=self.trans_GPS_to_XYZ.transform(*loc2)
        rad2=len3d(second)
        z=rad2-rad1
        locx=copy.copy(loc1)
        locy=copy.copy(loc1)
        locx[1]=loc2[1]
        locy[0]=loc2[0]
        distx=subList(self.trans_GPS_to_XYZ.transform(*locx),first)
        disty=subList(self.trans_GPS_to_XYZ.transform(*locy),first)
        distx=len3d(distx)*np.sign(loc2[1]-loc1[1])
        disty=len3d(disty)*np.sign(loc2[0]-loc1[0])
        return [distx,disty,z]