import pygame
import random
import os

# Initialisation de Pygame
pygame.init()

# Constantes
WINDOW_SIZE = 800
ROAD_WIDTH = 100
VEHICLE_WIDTH = 40
VEHICLE_HEIGHT = 80
TRAFFIC_LIGHT_SIZE = 20
VEHICLE_SPACING = 90  # Espace entre les véhicules
QUEUE_OFFSET = 300    # Distance depuis l'intersection où commence la file

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Création de la fenêtre
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Simulation d'intersection avec files d'attente")

class Vehicle:
    def __init__(self, direction, queue_position, vehicle_type):
        self.direction = direction
        self.queue_position = queue_position
        self.vehicle_type = vehicle_type
        
        # Charger l'image du véhicule
        image_path = f"/home/lucaslhm/Documents/ecole/3A/projets/PPC/Projet/frontend/img/{vehicle_type}.png"
        try:
            self.original_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.original_image, (VEHICLE_WIDTH, VEHICLE_HEIGHT))
        except:
            print(f"Image non trouvée: {image_path}")
            # Créer un rectangle de substitution si l'image n'est pas trouvée
            self.image = pygame.Surface((VEHICLE_WIDTH, VEHICLE_HEIGHT))
            self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Rotation de l'image selon la direction
        if direction == "north":
            self.image = pygame.transform.rotate(self.image, -90)
        elif direction == "south":
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction == "east":
            self.image = pygame.transform.rotate(self.image, 180)

    def get_position(self):
        # Calculer la position en fonction de la direction et de la position dans la file
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
        
        # Types de véhicules disponibles
        self.vehicle_types = ["car", "camion","moto"]
        
        # Initialisation des files de véhicules
        self.vehicle_queues = {
            "north": [],
            "south": [],
            "east": [],
            "west": []
        }
        

    def define_queues(self, directions, list_vehicle):
        for direction in self.vehicle_queues:
            queue_length = random.randint(3, 6)  # Nombre aléatoire de véhicules par file
            for i in range(queue_length):
                vehicle_type = random.choice(self.vehicle_types)
                vehicle = Vehicle(direction, i, vehicle_type)
                self.vehicle_queues[direction].append(vehicle)
        if direction == "north":



    def draw(self):
        # Dessiner le fond
        screen.fill(BLACK)
        
        # Dessiner les routes
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

def main():
    intersection = Intersection()
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        intersection.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()