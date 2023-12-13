import matplotlib.pyplot as plt
import networkx as nx
import random

class MapColoringCSP:
    def __init__(self, regions, adjacencies, colors):
        self.regions = regions
        self.adjacencies = adjacencies
        self.colors = colors
        self.assignment = {}

    def is_valid(self, region, color):
        for neighbor in self.adjacencies.get(region, []):
            if self.assignment.get(neighbor) == color:
                return False
            
        return True

    def assign_color(self, region):
        for color in self.colors:
            if self.is_valid(region, color):
                self.assignment[region] = color
                if len(self.assignment) == len(self.regions) or self.assign_color(self.next_region()):
                    return True
                del self.assignment[region]

        return False

    def next_region(self):
        remaining = [(r, self.count_remaining_values(r)) for r in self.regions if r not in self.assignment]
        return min(remaining, key=lambda x: x[1])[0]

    def count_remaining_values(self, region):
        return sum(1 for color in self.colors if self.is_valid(region, color))

    def solve(self):
        if self.assign_color(self.regions[0]):
            return self.assignment
        
        return None

def generate_unique_random_colors(n):
    colors = set()

    while len(colors) < n:
        new_color = f'#{random.randint(0, 0xFFFFFF):06x}'
        colors.add(new_color)
    
    return list(colors)

def draw_map(regions, adjacencies, solution):
    G = nx.Graph()

    for region in regions:
        G.add_node(region)

    for region, neighbors in adjacencies.items():
        for neighbor in neighbors:
            G.add_edge(region, neighbor)

    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True, node_size=3000, node_color='white', edge_color='black', linewidths=2, font_size=15)

    for region, color in solution.items():
        nx.draw_networkx_nodes(G, layout, nodelist=[region], node_color=color)

    plt.show()

def main():
    num_regions = int(input())
    regions = input().split()
    if len(regions) != num_regions:
        print("Number of region names doesn't match the number of regions")
        return

    num_colors = int(input())
    colors = []

    colors = input().strip()
    if colors == 'random':
        colors = generate_unique_random_colors(num_colors)
    else:
        colors = colors.split()
        if len(colors) != num_colors:
            print(f"Incorrect number of colors provided")
            return                 

    adjacencies = {region: [] for region in regions}
    output_mode = ""
    keep_looping = True

    while keep_looping:
        line = input().strip()
        if line == 'text' or line == 'graph' or line == 'both':
            keep_looping = False
            output_mode = line
        else:
            region1, region2 = line.split()
            if region1 not in regions or region2 not in regions:
                print("Invalid region names")
                return
            adjacencies[region1].append(region2)
            adjacencies[region2].append(region1)
        
    csp = MapColoringCSP(regions, adjacencies, colors)
    solution = csp.solve()

    if solution:
        print("Solution found")

        if output_mode == "text" or output_mode == "both":
            color_to_group = {color: idx + 1 for idx, color in enumerate(set(solution.values()))}

            for region, color in solution.items():
                group_number = color_to_group[color]
                print(f"{region}: Color {group_number}")
        if output_mode == "graph" or output_mode == "both":
            try:
                draw_map(regions, adjacencies, solution)
            except Exception as e:
                print(f"An error occurred while drawing the map: {e}")
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
