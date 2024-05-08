from django.db import models

# Create your models here.


class Entry(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LRU(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.TextField(default="", verbose_name="user_created")
    dates_edited = list()
    users_edited = list()
    verified = bool()
    complete = bool()
    lru_name = models.TextField(default="", verbose_name="lru_name")
    lru_refdes = models.TextField(default="", verbose_name="lru_refdes")
    lru_ports = models.TextField(default="", verbose_name="lru_ports")
    lru_SOI = models.TextField(default="", verbose_name="lru_SOI")
    lru_cage_code = models.TextField(default="", verbose_name="lru_cage_code")
    lru_manu = models.TextField(default="", verbose_name="lru_manu")
    lru_part_num = models.TextField(default="", verbose_name="lru_part_num")
    lru_loc = models.TextField(default="", verbose_name="lru_loc")
    lru_weight = models.TextField(default="", verbose_name="lru_weight")
    lru_cg_xyz = models.TextField(default="", verbose_name="lru_cg_xyz")
    lru_cooling = models.TextField(default="", verbose_name="lru_cooling")
    lru_bonding = models.TextField(default="", verbose_name="lru_bonding")
    lru_model = models.TextField(default="", verbose_name="lru_model")
    lru_rev = models.TextField(default="", verbose_name="lru_rev")
    lru_software_rev = models.TextField(
        default="", verbose_name="lru_software_rev")
    lru_user_comment = models.TextField(
        default="", verbose_name="lru_user_comment")
    lru_photo_file_path = models.TextField(
        default="", verbose_name="lru_photo_file_path")

    def __str__(self):
        return self.lru_name


class connector(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.TextField(default="", verbose_name="user_created")
    dates_edited = list()
    users_edited = list()
    verified = bool()
    complete = bool()
    conn_refdes = models.TextField(default="", verbose_name="conn_refdes")
    conn_partnumber = models.TextField(
        default="", verbose_name="conn_partnumber")
    conn_wires = models.TextField(default="", verbose_name="conn_wires")
    conn_port_name = models.TextField(
        default="", verbose_name="conn_port_name")
    conn_manu = models.TextField(default="", verbose_name="conn_manu")
    conn_cage_code = models.TextField(
        default="", verbose_name="conn_cage_code")
    conn_lru_refdes = models.TextField(
        default="", verbose_name="conn_lru_refdes")
    conn_family = models.TextField(default="", verbose_name="conn_family")
    conn_series = models.TextField(default="", verbose_name="conn_series")
    conn_finish = models.TextField(default="", verbose_name="conn_finish")
    conn_insert_arrangement = models.TextField(
        default="", verbose_name="conn_insert_arrangement")
    conn_contact_type = models.TextField(
        default="", verbose_name="conn_contact_type")
    conn_keying = models.TextField(default="", verbose_name="conn_keying")
    conn_contact_size = models.TextField(
        default="", verbose_name="conn_contact_size")
    conn_hermetical_sealing = models.TextField(
        default="", verbose_name="conn_hermetical_sealing")
    conn_label = models.TextField(default="", verbose_name="conn_label")
    conn_marking = models.TextField(default="", verbose_name="conn_marking")
    conn_user_comment = models.TextField(
        default="", verbose_name="conn_user_comment")
    conn_photo_file_path = models.TextField(
        default="", verbose_name="conn_photo_file_path")
    _type = models.TextField(default="Wire")

    def __str__(self):
        return self.connector_name


class wire(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.TextField(default="", verbose_name="user_created")
    dates_edited = list()
    users_edited = list()
    verified = bool()
    complete = bool()
    wire_refdes = models.TextField(default="", verbose_name="wire_refdes")
    wire_part_number = models.TextField(
        default="", verbose_name="wire_part_number")
    wire_name = models.TextField(default="", verbose_name="wire_name")
    termination_refdes = models.TextField(
        default="", verbose_name="wire_term_refdes")
    contact_id = models.TextField(default="", verbose_name="wire_contact_id")
    contact_pn = models.TextField(default="", verbose_name="wire_contact_pn")
    conductor_contact_size = models.TextField(
        default="", verbose_name="wire_cond_cont_size")
    conductor_id = models.TextField(default="", verbose_name="wire_cond_id")
    _type = models.TextField(default="Wire")
    contact_code = models.TextField(default="", verbose_name="wire_cont_code")
    conductor_signal_type = models.TextField(
        default="", verbose_name="wire_signal_type")
    conductor_color = models.TextField(default="", verbose_name="wire_color")
    conductor_awg = models.TextField(default="", verbose_name="wire_awg")
    conductor_resistance = models.TextField(
        default="", verbose_name="wire_resistance")
    shielding = models.TextField(default="", verbose_name="wire_shielding")
    weight = models.TextField(default="", verbose_name="wire_weight")
    conductor_diameter = models.TextField(
        default="", verbose_name="wire_diameter")
    conductor_material = models.TextField(
        default="", verbose_name="wire_material")
    conductor_jacket = models.TextField(default="", verbose_name="wire_jacket")
    conductor_voltage_rating = models.TextField(
        default="", verbose_name="wire_voltage_rating")
    conductor_temperature_rating = models.TextField(
        default="", verbose_name="wire_temp_rating")
    length = models.TextField(default="", verbose_name="wire_length")
    user_comment = models.TextField(default="", verbose_name="wire_comment")
    photo_file_path = models.TextField(
        default="", verbose_name="wire_photo_filepath")
    harness_refdes = models.TextField(
        default="", verbose_name="wire_harness_refdes")
    harness_part_number = models.TextField(
        default="", verbose_name="wire_harness_pn")

    def __str__(self):
        return self.wire_name


class port(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.TextField(default="", verbose_name="user_created")
    dates_edited = list()
    users_edited = list()
    verified = bool()
    complete = bool()
    port_reference_designator = models.TextField(
        default="", verbose_name="port_refdes")
    port_part_number = models.TextField(default="", verbose_name="port_pn")
    port_name = models.TextField(default="", verbose_name="port_name")
    port_lru_refdes = models.TextField(
        default="", verbose_name="port_lru_refdes")
    port_type = models.TextField(default="", verbose_name="port_type")
    port_on = models.TextField(default="", verbose_name="port_on")
    port_connector = models.TextField(
        default="", verbose_name="port_connector")
    _type = models.TextField(default="Port")

    def __str__(self):
        return self.port_name
