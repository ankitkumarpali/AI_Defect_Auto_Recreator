import streamlit as st
import json
import os
from pyvis.network import Network


# Define the path to the JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "connections.json")

# Load connections data from JSON if it exists
connections = []
col1, col2, col3 = st.columns(3)

# Display port type dropdown in the first column

with col1:
      # Custom label for the file uploader

    # File uploader without default "Drag and drop" text
    uploaded_file = st.file_uploader("Upload Show Tech") 
    if uploaded_file is not None:
        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                connections = json.load(file)
                st.success("File uploaded and loaded successfully!")


# if os.path.exists(json_path):
#     with open(json_path, "r") as file:
#         connections = json.load(file)

# Set up Pyvis network with interactive options
network = Network(height="600px", width="100%", bgcolor="white", font_color="black", directed=True)
network.barnes_hut()


if connections:
# Set the central switch name
    central_switch = connections.get("switch_name", "")

    # Add central switch with hover settings for zoom effect
    network.add_node(
        central_switch,
        label=central_switch,
        shape="box",
        color="lightblue",
        title=f"{central_switch}",  # Node title for hover display
        size=30,
        font={"size": 16, "color": "black"}
    )

    # Data for the dropdowns
    ports_data = {
        "Switchport Access Ports": connections.get("switchport_access_ports", ""),
        "Trunk Enabled Ports": connections.get("trunk_enabled_ports", ""),
    }
    port_channels = connections.get("All Port Channels", {})


    # Create columns for side-by-side dropdowns

    with col2:
        port_type = st.selectbox("Select Port Type", list(ports_data.keys()))
        st.write(f"{port_type}: {ports_data[port_type]}")

    # Display port channel dropdown in the second column
    with col3:
        selected_port_channel = st.selectbox("Select Port Channel", port_channels)
        interfaces = connections.get(selected_port_channel, [])
        if interfaces:
            st.write(f"Interfaces for {selected_port_channel}: {interfaces}")

    col3, col4, col5 = st.columns(3)
    with col3:
        macsec_interfaces=[]
        if st.button("macsec Interfaces"):
            macsec_interfaces = connections.get("macsec_interfaces", [])
    with col4:
        ospf_interfaces=[]
        if st.button("ospf interfaces"):
            ospf_interfaces = connections.get("ospf_interfaces", [])

    with col5:
        search_query = st.text_input("Please enter IP/Subnet(10.0.1.1/8)")
        highlight_interfaces = connections.get(search_query, []) if search_query else []
        if highlight_interfaces and isinstance(highlight_interfaces[0], str) and highlight_interfaces[0].startswith("Po"):
            # If it's a Port Channel, retrieve interfaces from connections based on that Port Channel name
            port_channel = highlight_interfaces[0]
            highlight_interfaces = connections.get(port_channel, [])

        

    multicast_interfaces = connections.get("multicast_interfaces", [])

    # Add each switch and all its connections to the network
    for i, conn in enumerate(connections["connections"]):
        switch = conn["switch"]
        ip = conn["interface_ip"]
        port = conn["interface_port"]
        color = conn["color"]
        # color = "red" if selected_port_channel in connections and port in connections[selected_port_channel] else conn["color"]
        version = conn.get("version", "N/A")
        vlan = conn.get("vlan", "N/A")
        vlan_type = conn.get("vlan_type", "N/A")
        neighbor_ip = conn.get("outgoing_interface_ip", "")
        outgoing_interface_port = conn["outgoing_interface_port"]
        port_l3 = conn.get("switchport_type", "")
        ospf_features = conn.get("ospf_features", "")
        bfd = conn.get("bfd_interval", "")
        multicast_enabled = conn.get("multicast_enabled", "")

        # Add each switch node with conditional hover text for details
        node_title = f"{switch} \nIP: {neighbor_ip}\nVersion: {version}\nVLAN: {vlan} ({vlan_type}) \nInterface: {outgoing_interface_port} \n{port_l3}\n"
        if ospf_features != "":
            node_title += f"{ospf_features}\n"

        if bfd:
            node_title += f"{bfd}"

        if port in multicast_interfaces:
            node_title += f"\nip pim sparse mode"

        if port in macsec_interfaces:
            node_title += f"\nmacsec network-link\nkey chain TEST_3 macsec\n key BBBB\n cryptographic-algorithm aes-256-cmac\n key-string 7 <removed>\n lifetime 15:00:00 Jul 28 2021 infinite\n key AAAA\n cryptographic-algorithm aes-256-cmac\n key-string 7 <removed>\n lifetime local 15:00:00 Mar 28 2022 duration 1800"

        if port in ports_data["Trunk Enabled Ports"]:
            node_title += f"\nswitchport mode trunk"

        

        network.add_node(
            switch,
            label=f"{switch}",
            shape="box",
            color=color,
            title=node_title,
            size=25, 
            font={"size": 16, "color": "black"}
        )
        roundness_value = 0.1 + (i * 0.05)
        
        if port in macsec_interfaces:
            edge_color = "green"
        elif port in ospf_interfaces:
            edge_color = "orange"
        elif selected_port_channel in connections and port in connections[selected_port_channel]:
            edge_color = "red"
        elif port in highlight_interfaces:
            edge_color = "blue"
        else:
            edge_color = "gray"
        

        edge_title = f"Port: {port}, IP: {ip}, VLAN: {vlan} ({vlan_type})"
        network.add_edge(
            central_switch,
            switch,
            label=f"{port}",  # Unique label to distinguish each edge
            title=edge_title,  # Edge title for hover details
            color=edge_color,
            font={"size": 6, "color": "black"},
            smooth={"type": "curvedCCW", "roundness": roundness_value}  # Adjust roundness for visual separation
        )

    # Enable smooth zoom on hover
    network.set_options("""
    {
    "nodes": {
        "scaling": {
        "min": 10,
        "max": 30
        },
        "font": {
        "size": 10,
        "face": "Helvetica"
        }
    },
    "edges": {
        "smooth": {
            "enabled": true,
        "type": "dynamic",
        "roundness": 1
        }
    },
    "interaction": {
        "hover": true,
        "zoomView": true
    },
    "physics": {
        "stabilization": false,
        "barnesHut": {
        "gravitationalConstant": -8000,
        "centralGravity": 0.3,
        "springLength": 95,
        "springConstant": 0.04
        }
    }
    }
    """)

    # Save the network with a background image
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Network Visualization</title>
    <style>
        body {{
            background-image: url('your_image_url_here');
            background-size: cover;
            margin: 0;
            padding: 0;
            height: 100%;
        }}
    </style>
</head>
<body>
    {network.generate_html()}
</body>
</html>
"""

# Save the HTML template to a file
with open("network_with_background.html", "w") as file:
    file.write(html_template)

# Display the network in Streamlit
st.components.v1.html(open("network_with_background.html", "r").read(), height=700, scrolling=True)
st.markdown(
    """
    <h4>Problem Analysis</h4>
    <div style='
        border: 2px solid red;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffe6e6;
        color: red;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
    '><ul>
        <li>High CPU utilization (98%)</li>
        <li>Packets are dropped in ASIC at IGMP ENABLE source</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)