# main.py

import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from flight_route_planner import FlightRoutePlanner


class FlightRouteApp:
    def __init__(self, master):
        self.master = master
        master.title("Flight Route Planner")

        # Title label
        self.title_label = tk.Label(master, text="Flight Route Planner", font=("Times New Roman", 30, "bold"), bg="lightblue")
        self.title_label.pack(pady=10)

        # Main window background color
        master.configure(bg="lightblue")

        # Input frame
        self.input_frame = tk.Frame(master, bg="lightblue", bd=5)
        self.input_frame.pack(side="top", pady=20)

        self.planner = FlightRoutePlanner()
        self.airports = list(self.planner.graph.nodes)

        # Start and end airport selection
        self.start_airport_var = tk.StringVar(master)
        self.end_airport_var = tk.StringVar(master)

        # Start airport dropdown
        tk.Label(self.input_frame, text="Select Start Airport:", font=("Times New Roman", 20), bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
        self.start_airport_menu = tk.OptionMenu(self.input_frame, self.start_airport_var, *self.airports)
        self.start_airport_menu.config(font=("Times New Roman", 20), bg="white")
        self.start_airport_menu.grid(row=0, column=1, padx=5, pady=5)

        # Destination airport dropdown
        tk.Label(self.input_frame, text="Select Destination Airport:", font=("Times New Roman", 20), bg="lightblue").grid(row=1, column=0, padx=5, pady=5)
        self.end_airport_menu = tk.OptionMenu(self.input_frame, self.end_airport_var, *self.airports)
        self.end_airport_menu.config(font=("Times New Roman", 18), bg="white")
        self.end_airport_menu.grid(row=1, column=1, padx=5, pady=5)

        # Button to find the route
        self.submit_button = tk.Button(self.input_frame, text="Find Optimal Route", font=("Times New Roman", 20), command=self.find_route)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Label to display the route
        self.result_label = tk.Label(self.input_frame, text="", wraplength=300, font=("Times New Roman", 20), bg="lightblue")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Graph frame at the bottom
        self.graph_frame = tk.Frame(master, bg="lightblue")
        self.graph_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        # Setup matplotlib figure in the graph_frame
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Draw initial graph
        self.draw_graph()

    def find_route(self):
        start = self.start_airport_var.get()
        end = self.end_airport_var.get()

        if not start or not end:
            messagebox.showerror("Input Error", "Please select both start and destination airports.")
            return

        try:
            optimal_route = self.planner.get_optimal_route(start, end)
            self.result_label.config(text="Optimal Route: " + " -> ".join(optimal_route))
            self.draw_graph(optimal_route)
        except nx.NetworkXNoPath:
            self.result_label.config(text="No route found.")
            self.draw_graph()
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")

    def draw_graph(self, optimal_route=None):
        # Clear the axes
        self.ax.clear()

        # Background transparency
        self.fig.patch.set_alpha(0.0)
        self.ax.set_facecolor('none')
        self.fig.set_size_inches(10, 8)

        # Set layout to avoid node overlap
        pos = nx.spring_layout(self.planner.graph, k=0.4, iterations=50)

        # Draw the full graph
        nx.draw(self.planner.graph, pos, ax=self.ax, with_labels=True, node_color='lightblue', node_size=700, font_size=12, font_color='darkblue')

        # Edge labels with weight
        edge_labels = nx.get_edge_attributes(self.planner.graph, 'weight')
        nx.draw_networkx_edge_labels(self.planner.graph, pos, edge_labels=edge_labels, ax=self.ax)

        # Highlight optimal route if found
        if optimal_route:
            path_edges = list(zip(optimal_route, optimal_route[1:]))
            nx.draw_networkx_edges(self.planner.graph, pos, edgelist=path_edges, ax=self.ax, edge_color='red', width=3)

        # Draw the updated canvas
        self.canvas.draw()


def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = FlightRouteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
