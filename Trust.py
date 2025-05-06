import pygame
import random
import math
import time
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fork Bomb Trust vs Zero Trust - Live Battle")
clock = pygame.time.Clock()

# Colors
RED = (255, 0, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Agent class
class Agent:
	def __init__(self, x, y, team):
		self.x = x
		self.y = y
		self.team = team  # 'fork' or 'zero'
		self.children = []
		self.infected = False
		self.last_spawn = time.time()
		self.authenticated = team == 'fork'

	def update(self):
		now = time.time()
		if self.infected:
			for child in self.children:
				if not child.infected:
					child.infected = True

		if now - self.last_spawn > 0.3:  # Faster spawn rate
			if self.team == 'fork':
				self.spawn_children()
			elif self.authenticated:
				self.spawn_children()
			self.last_spawn = now

	def spawn_children(self):
		if len(self.children) >= 3:
			return
		for _ in range(2):
			angle = random.uniform(0, 2 * math.pi)
			dist = random.randint(20, 50)
			new_x = self.x + math.cos(angle) * dist
			new_y = self.y + math.sin(angle) * dist
			child = None
			if self.team == 'zero':
				if random.random() < 0.8:
					child = Agent(new_x, new_y, 'zero')
					child.authenticated = True
			else:
				child = Agent(new_x, new_y, 'fork')
			if child:
				self.children.append(child)
				agents.append(child)

	def draw(self):
		color = BLACK if self.infected else RED if self.team == 'fork' else BLUE
		pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 6)
		for child in self.children:
			pygame.draw.line(screen, (150, 150, 150), (self.x, self.y), (child.x, child.y), 1)

# Setup
agents = []
fork_root = Agent(200, HEIGHT//2, 'fork')
zero_root = Agent(WIDTH - 200, HEIGHT//2, 'zero')
zero_root.authenticated = True
agents.extend([fork_root, zero_root])

# Tracking
infect_time = time.time() + 3  # Start infection earlier
infected = False
start_time = time.time()
fork_counts = []
zero_counts = []
fork_infected = []
zero_infected = []
time_series = []

# Main Loop
running = True
while running and time.time() - start_time < 15:  # Shorter simulation duration
	screen.fill(WHITE)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if not infected and time.time() > infect_time:
		fork_root.infected = True
		zero_root.infected = True
		infected = True

	for agent in agents:
		agent.update()
		agent.draw()

	# Bar graph data collection
	fork_total = sum(1 for a in agents if a.team == 'fork')
	zero_total = sum(1 for a in agents if a.team == 'zero')
	fork_inf = sum(1 for a in agents if a.team == 'fork' and a.infected)
	zero_inf = sum(1 for a in agents if a.team == 'zero' and a.infected)

	fork_counts.append(fork_total)
	zero_counts.append(zero_total)
	fork_infected.append(fork_inf)
	zero_infected.append(zero_inf)
	time_series.append(int(time.time() - start_time))

	pygame.display.flip()
	clock.tick(60)  # Higher frame rate

pygame.quit()

# Plotting final bar chart
plt.figure(figsize=(12, 6))
plt.plot(time_series, fork_counts, label='Fork Bomb - Total', color='red', linestyle='--')
plt.plot(time_series, fork_infected, label='Fork Bomb - Infected', color='darkred')
plt.plot(time_series, zero_counts, label='Zero Trust - Total', color='blue', linestyle='--')
plt.plot(time_series, zero_infected, label='Zero Trust - Infected', color='navy')
plt.axvline(x=3, color='gray', linestyle=':', label='Infection Starts')
plt.title("Fork Bomb Trust vs Zero Trust - Agent Growth & Infection")
plt.xlabel("Time (seconds)")
plt.ylabel("Number of Agents")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
