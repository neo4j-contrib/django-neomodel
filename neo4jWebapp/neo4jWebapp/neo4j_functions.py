from neo4j import GraphDatabase
# from Fake_gen import *


class GLOBAL_VARS:
    def __init__(self):
        self.URI = "bolt://localhost:7687"
        self.AUTH = ("neo4j", "password")


class LRU:
    def __init__(self):
        # required properties
        self.name = ""
        self.refdes = ""
        self.ports = []
        self.SOI = ""
        self.cage_code = ""
        # recommended properties
        self.manu = ""
        self.part_num = ""
        self.loc = ""
        self.weight = ""
        self.cg_xyz = []
        self.cooling = ""
        self.bonding = ""
        self.model = ""
        self.rev = ""
        self.software_rev = ""
        self.user_comment = ""
        self.photo_file_path = ""
        self.verified = False
        self.complete = False
        self.created_by = ""
        self.created_on = ""
        self.edited_by = []
        self.edited_on = []


class Port:
    def __init__(self):
        # required properties
        self.name = ""
        self.lru_refdes = ""
        self.type = ""
        self.on = False
        # required properties conditional to self.on
        self.connector = ""
        self.verified = False
        self.complete = False
        self.created_by = ""
        self.created_on = ""
        self.edited_by = []
        self.edited_on = []


class Connector:
    def __init__(self):
        self.refdes = ""
        self.partnumber = ""
        self.wires = []
        self.port_name = ""
        self.manu = ""
        self.cage_code = ""
        self.lru_refdes = ""
        self.family = ""
        self.series = ""
        self.finish = ""
        self.insert_arrangement = ""
        self.contact_type = ""
        self.keying = ""
        self.contact_size = ""
        self.hermetical_sealing = ""
        self.label = ""
        self.marking = ""
        self.user_comment = ""
        self.photo_file_path = ""
        self.verified = False
        self.complete = False
        self.created_by = ""
        self.created_on = ""
        self.edited_by = []
        self.edited_on = []


class Backshell:
    def __init__(self):
        self.part_num = ""
        self.connecter_refdes = ""
        self.cage_code = ""
        self.series = ""
        self.shell_size = ""
        self.angle = ""
        self.lock_type = ""
        self.environment = ""
        self.finish = ""
        self.wire_entry = ""
        self.user_comment = ""
        self.photo_file_path = ""
        self.verified = False
        self.complete = False
        self.created_by = ""
        self.created_on = ""
        self.edited_by = []
        self.edited_on = []


class Wire:
    def __init__(self):
        self.refdes = ""
        self.termination_refdes = []
        self.contact_id = ""
        self.contact_pn = ""
        self.conductor_contact_size = ""
        self.conductor_id = ""
        self.type = ""
        self.contact_code = ""
        self.conductor_signal_type = ""
        self.conductor_color = ""
        self.conductor_awg = ""
        self.conductor_resistance = ""
        self.shielding = ""
        self.weight = ""
        self.conductor_diameter = ""
        self.conductor_material = ""
        self.conductor_jacket = ""
        self.conductor_voltage_rating = ""
        self.conductor_temperature_rating = ""
        self.length = ""
        self.user_comment = ""
        self.photo_file_path = ""
        self.harness_refdes = ""
        self.harness_part_number = ""
        self.verified = False
        self.complete = False
        self.created_by = ""
        self.created_on = ""
        self.edited_by = []
        self.edited_on = []


class Bundle:
    def __init__(self):
        self.name = ""
        self.wires = []
        self.verified = False
        self.complete = False
        self.created_by = ""
        self.created_on = ""
        self.edited_by = []
        self.edited_on = []

# fill class with unique data from UI


def fill_lru_data(lru: LRU, in_dict: dict):
    # required lru properties
    lru.name = in_dict["LRU_Name"]
    lru.refdes = in_dict["LRU_Refdes"]
    lru.SOI = in_dict["LRU_SOI"]
    lru.cage_code = in_dict["LRU_Cage_Code"]
    for instance in in_dict["Ports"]:
        lru.ports.append(instance["Port_ID"])
    # not required properties below, need to add properties to UI/simulated inputs
    if 'Manufacturer' in in_dict:
        lru.manu = in_dict["Manufacturer"]
        lru.part_num = in_dict["Part_Number"]
        lru.loc = in_dict["Location"]
        lru.weight = in_dict["Weight"]
        lru.cg_xyz = in_dict["CG_xyz"]
        lru.cooling = in_dict["Cooling"]
        lru.bonding = in_dict["Bonding"]
        lru.model = in_dict["Model_Number"]
        lru.rev = in_dict["Revision"]
        lru.software_rev = in_dict["Software_Revision"]
        lru.user_comment = in_dict["User_Comment"]
        lru.photo_file_path = in_dict["Photo_File_Path"]
        lru.verified = in_dict["Verified"]
        lru.complete = in_dict["Complete"]
        lru.created_by = in_dict["Created_By"]
        lru.created_on = in_dict["Created_On"]
        lru.edited_by = in_dict["Edited_By"]
        lru.edited_on = in_dict["Edited_On"]

    return lru


def fill_port_data(port: Port, in_dict: dict):
    port.name = in_dict["Port_Name"]
    port.refdes = in_dict["LRU_Refdes"]
    port.type = in_dict["Port_Type"]
    port.on = in_dict["Port_On"]
    if in_dict["Port_On"] == True:
        port.connector = in_dict["Connector_Refdes"]
    if 'Verified' in in_dict:
        port.verified = in_dict["Verified"]
        port.complete = in_dict["Complete"]
        port.created_by = in_dict["Created_By"]
        port.created_on = in_dict["Created_On"]
        port.edited_by = in_dict["Edited_By"]
        port.edited_on = in_dict["Edited_On"]
    return port


def fill_connector_data(connector: Connector, in_dict: dict):
    connector.refdes = in_dict["Conn_Refdes"]
    connector.partnum = in_dict["Conn_Part_Number"]
    connector.lru_refdes = in_dict["LRU_Refdes"]
    for instance in in_dict["Wires"]:
        connector.wires.append(instance["Wire_Refdes"])
    connector.port_name = in_dict["Port_Name"]
    # need to add properties to UI/simulated inputs
    if 'Manufacturer' in in_dict:
        connector.manu = in_dict["Manufacturer"]
        connector.cage_code = ["Cage_Code"]
        connector.family = in_dict["Family"]
        connector.series = in_dict["Series"]
        connector.finish = in_dict["Finish"]
        connector.insert_arrangement = in_dict["Insert_Arrangemnt"]
        connector.contact_type = in_dict["Contact_Type"]
        connector.keying = in_dict["Keying"]
        connector.contact_size = in_dict["Contact_Size"]
        connector.hermetical_sealing = in_dict["Hermetical_Sealing"]
        connector.label = in_dict["Label"]
        connector.marking = in_dict["Marking"]
        connector.user_comment = in_dict["User_Comment"]
        connector.photo_file_path = in_dict["Photo_File_Path"]
        connector.verified = in_dict["Verified"]
        connector.complete = in_dict["Complete"]
        connector.created_by = in_dict["Created_By"]
        connector.created_on = in_dict["Created_On"]
        connector.edited_by = in_dict["Edited_By"]
        connector.edited_on = in_dict["Edited_On"]
    return connector


def fill_backshell_data(backshell, in_dict):
    if in_dict["BS_Part_Number"]:
        backshell.part_num = in_dict["BS_Part_Number"]
    if 'Cage_Code' in in_dict:
        # backshell.connecter_refdes = connector.refdes
        backshell.cage_code = in_dict["Cage_Code"]
        backshell.series = in_dict["Series"]
        backshell.shell_size = in_dict["Shell_Size"]
        backshell.angle = in_dict["Angle"]
        backshell.lock_type = in_dict["Lock_Type"]
        backshell.environment = in_dict["Environment"]
        backshell.finish = in_dict["Finish"]
        backshell.wire_entry = in_dict["Wire_Entry"]
        backshell.user_comment = in_dict["User_Comment"]
        backshell.photo_file_path = in_dict["Photo_File_Path"]
        backshell.verified = in_dict["Verified"]
        backshell.complete = in_dict["Complete"]
        backshell.created_by = in_dict["Created_By"]
        backshell.created_on = in_dict["Created_On"]
        backshell.edited_by = in_dict["Edited_By"]
        backshell.edited_on = in_dict["Edited_On"]
    return backshell


def fill_wire_data(wire: Wire, in_dict: dict):
    if in_dict["Wire_Refdes"]:
        wire.refdes = in_dict["Wire_Refdes"]
    if 'Termination_Refdes' in in_dict:
        wire.termination_refdes = in_dict["Termination_Refdes"]
        wire.contact_id = in_dict["Contact_ID"]
        wire.contact_pn = in_dict["Contact_PN"]
        wire.conductor_contact_size = in_dict["Conductor_Contact_Size"]
        wire.conductor_id = in_dict["Conductor_ID"]
        wire.type = in_dict["Wire_Type"]
        wire.contact_code = in_dict["Conductor_Code"]
        wire.conductor_signal_type = in_dict["Conductor_Signal_Type"]
        wire.conductor_color = in_dict["Conductor_Color"]
        wire.conductor_awg = in_dict["Conductor_AWG"]
        wire.conductor_resistance = in_dict["Conductor_Resistance"]
        wire.shielding = in_dict["Shielding"]
        wire.weight = in_dict["Wire_Weight"]
        wire.conductor_diameter = in_dict["Conductor_Diameter"]
        wire.conductor_material = in_dict["Conductor_Material"]
        wire.conductor_jacket = in_dict["Conductor_Jacket"]
        wire.conductor_voltage_rating = in_dict["Conductor_Voltage_Rating"]
        wire.length = in_dict["Length"]
        wire.user_comment = in_dict["User_Comment"]
        wire.photo_file_path = in_dict["Photo_File_Path"]
        wire.harness_refdes = in_dict["Harness_RefDes"]
        wire.harness_part_number = in_dict["Harness_PartNumber"]
        wire.verified = in_dict["Verified"]
        wire.complete = in_dict["Complete"]
        wire.created_by = in_dict["Created_By"]
        wire.created_on = in_dict["Created_On"]
        wire.edited_by = in_dict["Edited_By"]
        wire.edited_on = in_dict["Edited_On"]
    return wire


def fill_bundle_data(bundle, in_dict):
    bundle.name = in_dict["Bundle_Name"]
    for instance in in_dict["Wires"]:
        bundle.wires.append(instance["Wire_Refdes"])
    if 'Verified' in in_dict:
        bundle.user_comment = in_dict["User_Comment"]
        bundle.photo_file_path = in_dict["Photo_File_Path"]
        bundle.harness_refdes = in_dict["Harness_RefDes"]
        bundle.harness_part_number = in_dict["Harness_PartNumber"]
        bundle.verified = in_dict["Verified"]
        bundle.complete = in_dict["Complete"]
        bundle.created_by = in_dict["Created_By"]
        bundle.created_on = in_dict["Created_On"]
        bundle.edited_by = in_dict["Edited_By"]
        bundle.edited_on = in_dict["Edited_On"]
    return bundle


def create_neo_nodes_lru(lru, URI, AUTH):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # create lru node with its properties
            session.run(
                """CREATE (lru:LRU {Name: $name, RefDes: $refdes, Port_List: $port_list, SOI: $soi, Cage_Code: $cage_code, Manufacturer:$manufacturer, Part_Number:$part_number, Location: $location, Weight: $weight, 
                CG_XYZ: $cg_xyz, Cooling: $cooling, Bonding: $bonding, Model: $model, Revision: $revision, Software_Revision: $software_revision, User_Comment: $user_comment, Photo_File_Path: $photo_file_path, 
                Verified:$verified, Complete:$complete, Created_By:$created_by, Created_On:$created_on, Edited_By:$edited_by, Edited_On:$edited_on}) """,
                name=lru.name, refdes=lru.refdes, port_list=lru.ports, soi=lru.SOI, cage_code=lru.cage_code, manufacturer=lru.manu, part_number=lru.part_num, location=lru.loc, weight=lru.weight,
                cg_xyz=lru.cg_xyz, cooling=lru.cooling, bonding=lru.bonding, model=lru.model, revision=lru.rev, software_revision=lru.software_rev, user_comment=lru.user_comment,
                photo_file_path=lru.photo_file_path, verified=lru.verified, complete=lru.complete, created_by=lru.created_by, created_on=lru.created_on, edited_by=lru.edited_by,
                edited_on=lru.edited_on, database_="neo4j")
    return


def create_neo_nodes_port(port, URI, AUTH):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # create port node with all properties
            session.run(
                """CREATE (port:PORT {Name:$name, RefDes:$lru_refdes, Port_Type: $type, Use_Case: $use_case, Connector_RefDes: $connector_refdes, 
                Verified:$verified, Complete:$complete, Created_By:$created_by, Created_On:$created_on, Edited_By:$edited_by, Edited_On:$edited_on})""",
                name=port.name, lru_refdes=port.lru_refdes, type=port.type, use_case=port.on, connector_refdes=port.connector, verified=port.verified, complete=port.complete,
                created_by=port.created_by, created_on=port.created_on, edited_by=port.edited_by, edited_on=port.edited_on, database_="neo4j")
    return


def create_neo_nodes_connector(connector, URI, AUTH):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # create connector with all properties
            session.run(
                """CREATE (connector:CONN {RefDes:$refdes, Part_Number:$part_number, Wires:$wires, Port:$port, Manufacturer:$manu, Cage_Code:$cage_code, LRU_RefDes:$lru_refdes, Family:$family, 
                    Series:$series, Finish:$finish, Insert_Arrangement:$insert_arrangement, Contact_Type:$contact, Keying:$keying, Contact_Size:$contact_size, Hermetical_Sealing:$hseal, 
                    Label:$label, Marking:$marking, User_Comment:$user_comment, Photo_File_Path:$photo_file_path, Verified:$verified, Complete:$complete, Created_By:$created_by, 
                    Created_On:$created_on, Edited_By:$edited_by, Edited_On:$edited_on})""",
                refdes=connector.refdes, part_number=connector.partnumber, wires=connector.wires, port=connector.port_name, manu=connector.manu, cage_code=connector.cage_code, lru_refdes=connector.lru_refdes,
                family=connector.family, series=connector.series, finish=connector.finish, insert_arrangement=connector.insert_arrangement, contact=connector.contact_type, keying=connector.keying, contact_size=connector.contact_size,
                hseal=connector.hermetical_sealing, label=connector.label, marking=connector.marking, user_comment=connector.user_comment, photo_file_path=connector.photo_file_path,
                verified=connector.verified, complete=connector.complete, created_by=connector.created_by, created_on=connector.created_on, edited_by=connector.edited_by, edited_on=connector.edited_on, database_="neo4j")
    return


def create_neo_nodes_backshell(backshell, URI, AUTH):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # create backshell node with all properties
            session.run(
                """CREATE (backshell:BS {Part_Number:$part_number, Connector_RefDes:$conn_ref, Cage_Code:$cage_code, Series:$series, Shell_Size:$shell, Angle:$angle, Lock_Type:$lock, Environment:$environment, 
                Finish:$finish, Wire_Entry:$wire_entry, User_Comment:$user_comment, Photo_File_Path:$photo_file_path, Verified:$verified, Complete:$complete, Created_By:$created_by, Created_On:$created_on, 
                Edited_By:$edited_by, Edited_On:$edited_on})""",
                part_number=backshell.part_num, conn_ref=backshell.connector_refdes, cage_code=backshell.cage_code, series=backshell.series, shell=backshell.shell_size, angle=backshell.angle, lock=backshell.lock_type,
                environment=backshell.environment, finish=backshell.finish, wire_entry=backshell.wire_entry, user_comment=backshell.user_comment, photo_file_path=backshell.photo_file_path, verified=backshell.verified,
                complete=backshell.complete, created_by=backshell.created_by, created_on=backshell.created_on, edited_by=backshell.edited_by, edited_on=backshell.edited_on, database_="neo4j")
    return


def create_neo_nodes_wire(wire, URI, AUTH):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # create wires initially as nodes connected to connectors
            session.run(
                """CREATE (wire:WIRE {RefDes:$refdes, Termination_RefDes:$termination_refdes, Contact_ID:$contact_id, Contact_PN:$contact_pn, Conductor_Contact_Size:$conductor_contact_size, 
                        Conductor_ID:$conductor_id, Wire_Type:$wire_type, Contact_Code:$contact_code, Conductor_Signal_Type:$conductor_signal_type, Conductor_Color:$conductor_color, 
                        Conductor_AWG:$conductor_awg, Conductor_Resistance:$conductor_resistance, Shielding:$shielding, Wire_Weight:$wire_weight, Conductor_Diameter:$conductor_diameter, 
                        Conductor_Material:$conductor_material, Conductor_Jacket:$conductor_jacket, Conductor_Voltage_Rating:$conductor_voltage_rating, Conductor_Temp_Rating:$conductor_temp_rating, 
                        Wire_Length:$wire_length, User_Comment:$user_comment, Photo_File_Path:$photo_file_path, Harness_RefDes:$harness_refdes, Harness_Part_Number:$harness_part_number, 
                        Verified:$verified, Complete:$complete, Created_By:$created_by, Created_On:$created_on, Edited_By:$edited_by, Edited_On:$edited_on})""",
                refdes=wire.refdes, termination_refdes=wire.termination_refdes, contact_id=wire.contact_id, contact_pn=wire.contact_pn, conductor_contact_size=wire.conductor_contact_size,
                conductor_id=wire.conductor_id, wire_type=wire.type, contact_code=wire.contact_code, conductor_signal_type=wire.conductor_signal_type, conductor_color=wire.conductor_color,
                conductor_awg=wire.conductor_awg, conductor_resistance=wire.conductor_resistance, shielding=wire.shielding, wire_weight=wire.weight, conductor_diameter=wire.conductor_diameter,
                conductor_material=wire.conductor_material, conductor_jacket=wire.conductor_jacket, conductor_voltage_rating=wire.conductor_voltage_rating, conductor_temp_rating=wire.conductor_temperature_rating,
                wire_length=wire.length, user_comment=wire.user_comment, photo_file_path=wire.photo_file_path, harness_refdes=wire.harness_refdes, harness_part_number=wire.harness_part_number,
                verified=wire.verified, complete=wire.complete, created_by=wire.created_by, created_on=wire.created_on, edited_by=wire.edited_by, edited_on=wire.edited_on, database_="neo4j")
    return


def create_neo_nodes_bundle(bundle, URI, AUTH):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # create bundle nodes with all properties
            session.run(
                """CREATE (bundle:BUNDLE {Name:$name, Bundle_Wires:$wires, Verified:$verified, Complete:$complete, Created_By:$created_by, Created_On:$created_on, Edited_By:$edited_by, 
                Edited_On:$edited_on})""",
                name=bundle.name, wires=bundle.wires, verified=bundle.verified, complete=bundle.complete, created_by=bundle.created_by, created_on=bundle.created_on, edited_by=bundle.edited_by,
                edited_on=bundle.edited_on, database_="neo4j")
    return


def update_relations(new_node, node_type, URI, AUTH, driver):
    # with GraphDatabase.driver(URI, auth=AUTH) as driver:
    #     with driver.session(database="neo4j") as session:
    #         if node_type == 'LRU':
    #             #lru to port relation
    #             session.run("""
    #                 MATCH (n:LRU)
    #                 WHERE n.name = \"{}\" and n.refdes = \"{}\"
    #                 MATCH (p:PORT)
    #                 WHERE p.name = \"{}\" and p.refdes = \"{}\"
    #                 CREATE (n)-[:connected_to]->(p)""".format(new_node.name, new_node.refdes, port.name, port.lru_refdes), database_="neo4j")
    #         elif node_type == 'Port':
    #             #connector to port relation
    #             session.run("""
    #                 MATCH (p1:PORT)
    #                 WHERE p1.name = \"{}\" and p1.lru_refdes = \"{}\" and p1.connector =\"{}\"
    #                 MATCH (c:CONN)
    #                 WHERE c.port = \"{}\" and c.lru_refdes = \"{}\" and c.refdes = \"{}\"
    #                 CREATE (p1)-[:connected_to]->(c)
    #                 """.format(new_node.name, new_node.lru_refdes, new_node.connector, connector.port_name, connector.lru_refdes, connector.refdes), database_="neo4j")
    #         elif node_type == 'Conn':
    #             #backshell to connector relation
    #             session.run("""
    #                 MATCH (c1:CONN)
    #                 WHERE c1.refdes = \"{}\" and c1.lru_refdes = \"{}\"
    #                 MATCH (b:BS)
    #                 WHERE b.part_number = \"{}\" and b.conn_ref = \"{}\"
    #                 CREATE (c1)-[:connected_to]->(b)
    #                 """.format(new_node.refdes, new_node.lru_refdes, backshell.part_num, backshell.connector_refdes), database_="neo4j")
    #         elif node_type == 'Wire':
    #             #wire to connection relation
    #             session.run("""
    #                 MATCH (w:WIRE)
    #                 WHERE w.connector = \"{}\" and w.refdes = \"{}\"
    #                 MATCH (c2:CONN)
    #                 WHERE c2.refdes = \"{}\" and c2.wires = \"{}\"
    #                 """.format(new_node.termination_refdes, new_node.termination_refdes, connector.refdes, connector.wires))
    #         elif node_type == 'Bundle':
    #             #wire to bundle relation
    #             session.run("""
    #                 MATCH (c2:CONN)
    #                 WHERE c2.refdes = \"{}\" and c2.wires = \"{}\"
    #                 MATCH (w:WIRE)
    #                 WHERE w.connector = \"{}\" and w.refdes = \"{}\"
    #                 """.format(connector.refdes, connector.wires, wire.termination_refdes, wire.termination_refdes))
    #         session.close
    #     driver.close()

    return


def initNeo4jConnection(URI, AUTH):

    driver = GraphDatabase.driver(URI, auth=AUTH)
    session = driver.session(database="neo4j")

    if not driver.verify_authentication():
        return -1
    else:
        return 0


# def main():
#     if initNeo4jConnection < 0:
#         exit()

#     if False:
#         result = session.run("MATCH (n) DETACH DELETE n")
#         if result:
#             resultSummary = result.consume()
#             print("result counters:{}".format(resultSummary.counters))

#     # pull from UI dictionary make into class and fill with dictionary data
#     existing_nodes = []
#     # newItem = fake_gen()
#     newItem = []
#     for item in newItem:
#         newItemType = item["Type"]

#         if newItemType == 'LRU':
#             new_LRU = LRU()
#             new_node = fill_lru_data(new_LRU, item)
#             create_neo_nodes_lru(new_node, URI, AUTH, driver)
#         elif newItemType == 'Port':
#             new_Port = Port()
#             new_node = fill_port_data(new_Port, item)
#             create_neo_nodes_port(new_node, URI, AUTH, driver)
#         elif newItemType == 'Conn':
#             new_Conn = Connector()
#             new_node = fill_connector_data(new_Conn, item)
#             create_neo_nodes_connector(new_node, URI, AUTH, driver)
#         elif newItemType == 'Wire':
#             new_Wire = Wire()
#             new_node = fill_wire_data(new_Wire, item)
#             create_neo_nodes_wire(new_node, URI, AUTH, driver)
#         elif newItemType == 'Bundle':
#             new_Bundle = Bundle()
#             new_node = fill_bundle_data(new_Bundle, item)
#             create_neo_nodes_bundle(new_node, URI, AUTH, driver)
#         else:
#             print("unrecognized type")

#         # update_relations(new_node, newItemType, URI, AUTH, driver)

#     return 0

# if __name__ == "__main__":
#     main()
