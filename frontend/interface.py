import pygame
import random
import os

pygame.init()

WINDOW_SIZE = 800
ROAD_WIDTH = 100
VEHICLE_WIDTH = 40
VEHICLE_HEIGHT = 80
TRAFFIC_LIGHT_SIZE = 20
VEHICLE_SPACING = 90  
QUEUE_OFFSET = 300    


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)


screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Simulation d'intersection avec files d'attente")


class Box:
    def __init__(self, x, y, width, height, text, font_size=14, box_color=(0, 0, 0, 0), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)  # Définir la boîte avec ses dimensions
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size)  # Utilisation de la police Arial
        self.box_color = box_color  # Fond transparent
        self.text_color = text_color
        self.border_color = (255, 255, 204)  # Jaune pâle pour la bordure
        self.border_width = 2  # Épaisseur de la bordure

    def change_text(self,text):
        self.text = text

    def draw(self, screen):
        # Dessiner le fond transparent avec la bordure
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        
        # Créer un surface de texte
        text_surface = self.font.render(self.text, True, self.text_color)
        
        # Calculer la position du texte centré dans la boîte
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Dessiner le texte
        screen.blit(text_surface, text_rect)


class Vehicle:
    def __init__(self, direction, queue_position, vehicle_type):
        self.direction = direction
        self.queue_position = queue_position
        self.vehicle_type = vehicle_type
        
        image_path = f"/home/lucaslhm/Documents/ecole/3A/projets/PPC/Projet/frontend/img/{vehicle_type}.png"
        try:
            self.original_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.original_image, (VEHICLE_WIDTH, VEHICLE_HEIGHT))
        except:
            print(f"Image non trouvée: {image_path}")
            # Créer un rectangle de substitution si l'image n'est pas trouvée
            self.image = pygame.Surface((VEHICLE_WIDTH, VEHICLE_HEIGHT))
            self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        if direction == "north":
            self.image = pygame.transform.rotate(self.image, -90)
        elif direction == "south":
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction == "east":
            self.image = pygame.transform.rotate(self.image, 180)

    def get_position(self):

        if self.direction == "east":
            x = WINDOW_SIZE//2 + ROAD_WIDTH + (self.queue_position * VEHICLE_SPACING)
            y = (WINDOW_SIZE // 2) - ROAD_WIDTH // 2 - VEHICLE_WIDTH // 2
        elif self.direction == "west":
            x = WINDOW_SIZE//2 - ROAD_WIDTH - (self.queue_position * VEHICLE_SPACING)
            y = (WINDOW_SIZE // 2) + ROAD_WIDTH // 4 - VEHICLE_WIDTH
        elif self.direction == "north":
            x = (WINDOW_SIZE // 2) - ROAD_WIDTH // 2 - VEHICLE_WIDTH // 2
            y = WINDOW_SIZE//2 - ROAD_WIDTH - (self.queue_position * VEHICLE_SPACING)
        else:  # south
            x = (WINDOW_SIZE // 2) - VEHICLE_WIDTH // 2
            y = WINDOW_SIZE//2 + ROAD_WIDTH + (self.queue_position * VEHICLE_SPACING)
        return x, y

    def draw(self):
        x, y = self.get_position()
        screen.blit(self.image, (x, y))

class TrafficLight:
    def __init__(self, direction, position):
        self.direction = direction
        self.position = position
        self.state = 0
        self.timer = 0
    
    def define_light(self, state):
        self.state = state

    def draw(self):
        color = RED if not self.state else GREEN
        pygame.draw.circle(screen, color, self.position, TRAFFIC_LIGHT_SIZE)

class Intersection:
    def __init__(self):
        self.traffic_lights = {
            "north": TrafficLight("north", (WINDOW_SIZE//2 - ROAD_WIDTH//2, WINDOW_SIZE//2 - ROAD_WIDTH//2 - 20)),
            "south": TrafficLight("south", (WINDOW_SIZE//2 + ROAD_WIDTH//2 , WINDOW_SIZE//2 + ROAD_WIDTH//2+20)),
            "east": TrafficLight("east", (WINDOW_SIZE//2 + ROAD_WIDTH//2 + 20, WINDOW_SIZE//2 - ROAD_WIDTH//2 )),
            "west": TrafficLight("west", (WINDOW_SIZE//2 - ROAD_WIDTH//2 - 20, WINDOW_SIZE//2 + ROAD_WIDTH//2 ))
        }
        
        self.vehicle_types = ["car", "truk","scooter"]
        
        self.vehicle_queues = {
            "north": [],
            "south": [],
            "east": [],
            "west": []
        }

        largeur_box = 40
        longueur_box = 200
        self.boxs_text = {
            "north": Box(WINDOW_SIZE//2 - 250,WINDOW_SIZE//2-140 , longueur_box,largeur_box, "north"),
            "south": Box(WINDOW_SIZE//2 + 50, WINDOW_SIZE//2 +100, longueur_box, largeur_box, "south"),
            "east": Box(WINDOW_SIZE//2 +50, WINDOW_SIZE//2 - 100 , longueur_box,largeur_box, "east"),
            "west": Box(WINDOW_SIZE//2 - 250, WINDOW_SIZE//2 +60, longueur_box,largeur_box, "west")
        }

    def clear_queues(self):
        for direction in self.vehicle_queues:
            self.vehicle_queues[direction].clear()

    def define_queues(self, data):
        self.clear_queues()
        for (direction,list_vehicle) in data.items():
                for index, vehicle in enumerate(list_vehicle):
                    vehicle_type = vehicle["type"]
                    vehicle = Vehicle(direction, index, vehicle_type)
                    self.vehicle_queues[direction].append(vehicle)

    def define_trafic_lights(self, data):
        for (direction, state) in data.items():
            self.traffic_lights[direction].define_light(state)

    def define_vehicule_deleted(self, vehicle):
        if vehicle != None:
            texte = f"{vehicle["type"]} has gone to {vehicle["destination"]}"
            self.boxs_text[vehicle["source"]].change_text(texte)

    def draw(self):
        screen.fill(BLACK)
        
        pygame.draw.rect(screen, GRAY, (0, WINDOW_SIZE//2 - ROAD_WIDTH//2, WINDOW_SIZE, ROAD_WIDTH))
        pygame.draw.rect(screen, GRAY, (WINDOW_SIZE//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, WINDOW_SIZE))
        
        for i in range(0, WINDOW_SIZE, 40):
            pygame.draw.rect(screen, WHITE, (i, WINDOW_SIZE//2, 20, 2))
            pygame.draw.rect(screen, WHITE, (WINDOW_SIZE//2, i, 2, 20))
        
        for light in self.traffic_lights.values():
            light.draw()
        
        for direction in self.vehicle_queues:
            for vehicle in self.vehicle_queues[direction]:
                vehicle.draw()

        for (_,box) in self.boxs_text.items():
            box.draw(screen)
        


def main(update_function=None):
    intersection = Intersection()
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if update_function:
            new_data = update_function()
            if new_data:
                print("Mise à jour des données :", new_data)
                if new_data["vehicles"] != None:
                    intersection.define_queues(new_data["vehicles"])
                    intersection.define_vehicule_deleted(new_data["vehicle_deleted"])
                else:
                    intersection.define_trafic_lights(new_data["lights"]) 

        intersection.draw()

        pygame.display.flip()  
        clock.tick(60)  

    pygame.quit()

