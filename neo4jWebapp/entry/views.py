from django.shortcuts import render
from . import forms
from django.contrib import messages
from neo4jWebapp.neo4j_functions import *


def entry(request):

    global_vars = GLOBAL_VARS()

    # status = initNeo4jConnection(global_vars.URI, global_vars.AUTH)
    # if status == -1:
    #     messages.error(
    #         request, 'You were unable to connect to the Neo4j database.')
    # elif status == 0:
    #     messages.success(request, 'You are connected to the Neo4j database!')
    return render(request, 'entry/entry.html')


def lru(request):
    if request.method == 'POST':
        LRU_Name = request.POST.get('lru_name')
        LRU_Refdes = request.POST.get('lru_refdes')
        Part_Number = request.POST.get('lru_part_num')
        LRU_SOI = request.POST.get('lru_SOI')
        LRU_Cage_Code = request.POST.get('lru_cage_code')
        Manufacturer = request.POST.get('lru_manu')
        Location = request.POST.get('lru_loc')
        Weight = request.POST.get('lru_weight')
        CG_xyz = request.POST.get('lru_cg_xyz')
        Cooling = request.POST.get('lru_cooling')
        Bonding = request.POST.get('lru_bonding')
        Model_Number = request.POST.get('lru_model')
        Revision = request.POST.get('lru_rev')
        Software_Revision = request.POST.get('lru_software_rev')
        User_Comment = request.POST.get('lru_user_comment')

        new_dict = {"node_type": "LRU",
                    "LRU_Name": LRU_Name,
                    "LRU_Refdes": LRU_Refdes,
                    "Ports": [],
                    "LRU_SOI": LRU_SOI,
                    "LRU_Cage_Code": LRU_Cage_Code,
                    "Manufacturer": Manufacturer,
                    "Part_Number": Part_Number,
                    "Location": Location,
                    "Weight": Weight,
                    "CG_xyz": CG_xyz,
                    "Cooling": Cooling,
                    "Bonding": Bonding,
                    "Model_Number": Model_Number,
                    "Revision": Revision,
                    "Software_Revision": Software_Revision,
                    "User_Comment": User_Comment,
                    "Photo_File_Path": "",
                    "Verified": False,
                    "Complete": False,
                    "Created_By": "",
                    "Created_On": "",
                    "Edited_By": "",
                    "Edited_On": ""}
        

        # new_LRU = LRU()
        global_vars = GLOBAL_VARS()
        # new_node = fill_lru_data(new_LRU, new_dict)
        # create_neo_nodes_lru(new_node, global_vars.URI, global_vars.AUTH)
        # node(new_dict, global_vars.URI, global_vars.AUTH)
        return_list = query_database(new_dict, global_vars.URI, global_vars.AUTH)
        print(return_list)
    form_lru = forms.CreateLRU()
    return render(request, 'entry/lru.html', {'form': form_lru})


def port(request):

    if request.method == "POST":
        port_reference_designator = request.POST.get(
            'port_reference_designator')
        port_part_number = request.POST.get('port_part_number')
        port_name = request.POST.get('port_name')
        port_lru_refdes = request.POST.get('port_lru_refdes')
        port_type = request.POST.get('port_type')
        port_on = request.POST.get('port_on')
        port_connector = request.POST.get('port_connector')

        new_dict = {
            "Port_Name": port_name,
            "LRU_Refdes": port_lru_refdes,
            "Port_Type": "Port",
            "Port_On": port_on,
            "Connector_Refdes": port_connector,
            "Verified": False,
            "Complete": False,
            "Created_By": "",
            "Created_On": "",
            "Edited_By": "",
            "Edited_On": "",
        }
        new_port = Port()
        global_vars = GLOBAL_VARS()
        new_node = fill_port_data(new_port, new_dict)
        create_neo_nodes_port(new_node, global_vars.URI, global_vars.AUTH)
    form_port = forms.CreatePort()
    return render(request, 'entry/port.html', {'form': form_port})


def connector(request):
    if request.method == "POST":
        conn_refdes = request.POST.get('conn_refdes')
        conn_partnumber = request.POST.get('conn_partnumber')
        conn_wires = request.POST.get('conn_wires')
        conn_port_name = request.POST.get('conn_port_name')
        conn_manu = request.POST.get('conn_manu')
        conn_cage_code = request.POST.get('conn_cage_code')
        conn_lru_refdes = request.POST.get('conn_lru_refdes')
        conn_family = request.POST.get('conn_family')
        conn_series = request.POST.get('conn_series')
        conn_finish = request.POST.get('conn_finish')
        conn_insert_arrangement = request.POST.get('conn_insert_arrangement')
        conn_contact_type = request.POST.get('conn_contact_type')
        conn_keying = request.POST.get('conn_keying')
        conn_contact_size = request.POST.get('conn_contact_size')
        conn_hermetical_sealing = request.POST.get('conn_hermetical_sealing')
        conn_label = request.POST.get('conn_label')
        conn_marking = request.POST.get('conn_marking')
        conn_user_comment = request.POST.get('conn_user_comment')
        # conn_photo_file_path = request.POST.get('conn_photo_file_path')

        new_dict = {
            "Conn_Refdes": conn_refdes,
            "Conn_Part_Number": conn_partnumber,
            "Wires": [],
            "Port_Name": conn_port_name,
            "Manufacturer": conn_manu,
            "Cage_Code": conn_cage_code,
            "LRU_Refdes": conn_lru_refdes,
            "Family": conn_family,
            "Series": conn_series,
            "Finish": conn_finish,
            "Insert_Arrangemnt": conn_insert_arrangement,
            "Contact_Type": conn_contact_type,
            "Keying": conn_keying,
            "Contact_Size": conn_contact_size,
            "Hermetical_Sealing": conn_hermetical_sealing,
            "Label": conn_label,
            "Marking": conn_marking,
            "User_Comment": conn_user_comment,
            "Photo_File_Path": "",
            "Verified": False,
            "Complete": False,
            "Created_By": "",
            "Created_On": "",
            "Edited_By": "",
            "Edited_On": "",
        }
        new_conn = Connector()
        global_vars = GLOBAL_VARS()
        new_node = fill_connector_data(new_conn, new_dict)
        create_neo_nodes_connector(new_node, global_vars.URI, global_vars.AUTH)

    form_conn = forms.CreateConn()
    return render(request, 'entry/connector.html', {'form': form_conn})


def wire(request):

    if request.method == 'POST':
        wire_refdes = request.POST.get('wire_refdes')
        wire_part_number = request.POST.get('wire_part_number')
        wire_name = request.POST.get('wire_name')
        termination_refdes = request.POST.get('termination_refdes')
        contact_id = request.POST.get('contact_id')
        contact_pn = request.POST.get('contact_pn')
        conductor_contact_size = request.POST.get('conductor_contact_size')
        conductor_id = request.POST.get('conductor_id')
        contact_code = request.POST.get('contact_code')
        conductor_signal_type = request.POST.get('conductor_signal_type')
        conductor_color = request.POST.get('conductor_color')
        conductor_awg = request.POST.get('conductor_awg')
        conductor_resistance = request.POST.get('conductor_resistance')
        shielding = request.POST.get('shielding')
        weight = request.POST.get('weight')
        conductor_diameter = request.POST.get('conductor_diameter')
        conductor_material = request.POST.get('conductor_material')
        conductor_jacket = request.POST.get('conductor_jacket')
        conductor_voltage_rating = request.POST.get('conductor_voltage_rating')
        conductor_temperature_rating = request.POST.get(
            'conductor_temperature_rating')
        length = request.POST.get('length')
        user_comment = request.POST.get('user_comment')
        photo_file_path = request.POST.get('photo_file_path')
        harness_refdes = request.POST.get('harness_refdes')
        harness_part_number = request.POST.get('harness_part_number')

        new_dict = {"Wire_Part_Number": wire_part_number,
                    "Wire_Name": wire_name,
                    "Wire_Refdes": wire_refdes,
                    "Termination_Refdes": termination_refdes,
                    "Contact_ID": contact_id,
                    "Contact_PN": contact_pn,
                    "Conductor_Contact_Size": conductor_contact_size,
                    "Conductor_ID": conductor_id,
                    "Wire_Type": "Wire",
                    "Conductor_Code": contact_code,
                    "Conductor_Signal_Type": conductor_signal_type,
                    "Conductor_Color": conductor_color,
                    "Conductor_AWG": conductor_awg,
                    "Conductor_Resistance": conductor_resistance,
                    "Shielding": shielding,
                    "Wire_Weight": weight,
                    "Conductor_Diameter": conductor_diameter,
                    "Conductor_Material": conductor_material,
                    "Conductor_Jacket": conductor_jacket,
                    "Conductor_Voltage_Rating": conductor_voltage_rating,
                    "conductor_temperature_rating": conductor_temperature_rating,
                    "Length": length,
                    "User_Comment": user_comment,
                    "Photo_File_Path": photo_file_path,
                    "Harness_RefDes": harness_refdes,
                    "Harness_PartNumber": harness_part_number,
                    "Verified": False,
                    "Complete": False,
                    "Created_By": "",
                    "Created_On": "",
                    "Edited_By": "",
                    "Edited_On": "", }
        new_wire = Wire()
        global_vars = GLOBAL_VARS()
        new_node = fill_wire_data(new_wire, new_dict)
        create_neo_nodes_wire(new_node, global_vars.URI, global_vars.AUTH)

    form_wire = forms.CreateWire()
    return render(request, 'entry/wire.html', {'form': form_wire})


def equipment(request):
    form = forms.CreateLRU()
    formwire = forms.CreateWire()
    formport = forms.CreatePort()
    return render(request, 'entry/equipment.html', { 'form' : form , 'formwire': formwire, 'formport':formport})