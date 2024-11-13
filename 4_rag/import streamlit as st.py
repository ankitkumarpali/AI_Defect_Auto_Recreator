import streamlit as st
import graphviz as gv
import os
import json

# Define the path to the JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "connections.json")

# Load connections data from JSON if it exists
if os.path.exists(json_path):
    with open(json_path, "r") as file:
        connections = json.load(file)

# Set the central switch name
central_switch = connections["switch_name"]

# Initialize a Graphviz graph with adaptive size and aspect ratio
network = gv.Digraph("Network", engine="dot", graph_attr={"size": "10,10", "ratio": "compress"})

# Customize the appearance of the central switch node with increased font and dimensions

network.node(
    central_switch,
    label=central_switch,
    shape="box",
    style="filled",
    fillcolor="lightblue",
    width="2.5",
    height="1.5",
    fontname="Helvetica",
    fontsize="18",
)

# Add connections with larger fonts and slightly larger nodes
for conn in connections["connections"]:
    switch = conn["switch"]
    ip = conn["interface_ip"]
    port = conn["interface_port"]
    color = conn["color"]
    version = conn.get("version", "N/A")
    vlan = conn.get("vlan", "N/A")
    vlan_type = conn.get("vlan_type", "N/A")

    # Customize each switch node with improved readability
    node_label =f"{switch}\n{ip}\nVersion: {version}"
    network.node(
        switch,
        label=node_label,
        shape="box",
        style="filled",
        fillcolor=color,
        width="2.2",
        height="1.3",
        fontname="Helvetica",
        fontsize="16",
    )

    # Draw an edge with IP and port label, and customize edge color and style
    edge_label = f"{port} ({ip})\nVLAN: {vlan} ({vlan_type})"
    network.edge(
        central_switch,
        switch,
        label = edge_label,
        color="gray",
        fontname="Helvetica",
        fontsize="24",
    )

# Render the resized graph in Streamlit
st.graphviz_chart(network)
