from django import forms
from . import models


class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = ['title', 'body', 'slug']


class CreateConn(forms.ModelForm):
    class Meta:
        model = models.connector
        fields = [
            'conn_refdes',
            'conn_partnumber',
            'conn_wires',
            'conn_port_name',
            'conn_manu',
            'conn_cage_code',
            'conn_lru_refdes',
            'conn_family',
            'conn_series',
            'conn_finish',
            'conn_insert_arrangement',
            'conn_contact_type',
            'conn_keying',
            'conn_contact_size',
            'conn_hermetical_sealing',
            'conn_label',
            'conn_marking',
            'conn_user_comment']
            # 'conn_photo_file_path']
    conn_refdes = forms.CharField(required=False, label='conn_refdes', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_partnumber = forms.CharField(
        required=False, label='conn_partnumber', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_wires = forms.CharField(required=False, label='conn_wires', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_port_name = forms.CharField(
        required=False, label='conn_port_name', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_manu = forms.CharField(required=False, label='conn_manu', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_cage_code = forms.CharField(
        required=False, label='conn_cage_code', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_lru_refdes = forms.CharField(
        required=False, label='conn_lru_refdes', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_family = forms.CharField(required=False, label='conn_family', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_series = forms.CharField(required=False, label='conn_series', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_finish = forms.CharField(required=False, label='conn_finish', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_insert_arrangement = forms.CharField(
        required=False, label='conn_insert_arrangement', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_contact_type = forms.CharField(
        required=False, label='conn_contact_type', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_keying = forms.CharField(required=False, label='conn_keying', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_contact_size = forms.CharField(
        required=False, label='conn_contact_size', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_hermetical_sealing = forms.CharField(
        required=False, label='conn_hermetical_sealing', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conn_label = forms.CharField(required=False, label='conn_label', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_marking = forms.CharField(required=False, label='conn_marking', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conn_user_comment = forms.CharField(
        required=False, label='conn_user_comment', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    # conn_photo_file_path = forms.CharField(
    #     required=False, label='conn_photo_file_path', widget=forms.TextInput(attrs={'style': 'width: 100px'}))


class CreateLRU(forms.ModelForm):
    class Meta:
        model = models.LRU
        fields = ['lru_name',
                  'lru_refdes',
                  'lru_ports',
                  'lru_SOI',
                  'lru_cage_code',
                  'lru_manu',
                  'lru_part_num',
                  'lru_loc',
                  'lru_weight',
                  'lru_cg_xyz',
                  'lru_cooling',
                  'lru_bonding',
                  'lru_model',
                  'lru_rev',
                  'lru_software_rev',
                  'lru_user_comment']
                #   'lru_photo_file_path']
    lru_name = forms.CharField(required=False, label='lru_name:', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_refdes = forms.CharField(required=False, label='lru_refdes', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_ports = forms.CharField(required=False, label='lru_ports', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_SOI = forms.CharField(required=False, label='lru_SOI', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_cage_code = forms.CharField(
        required=False, label='lru_cage_code', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    lru_manu = forms.CharField(required=False, label='lru_manu', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_part_num = forms.CharField(
        required=False, label='lru_part_num', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    lru_loc = forms.CharField(required=False, label='lru_loc', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_weight = forms.CharField(required=False, label='lru_weight', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_cg_xyz = forms.CharField(required=False, label='lru_cg_xyz', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_cooling = forms.CharField(required=False, label='lru_cooling', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_bonding = forms.CharField(required=False, label='lru_bonding', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_model = forms.CharField(required=False, label='lru_model', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_rev = forms.CharField(required=False, label='lru_rev', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    lru_software_rev = forms.CharField(
        required=False, label='lru_software_rev', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    lru_user_comment = forms.CharField(
        required=False, label='lru_user_comment', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    # lru_photo_file_path = forms.CharField(
    #     required=False, label='lru_photo_file_path', widget=forms.TextInput(attrs={'style': 'width: 100px'}))


class CreatePort(forms.ModelForm):
    class Meta:
        model = models.port
        fields = [
            'port_reference_designator',
            'port_part_number',
            'port_name',
            'port_lru_refdes',
            'port_type',
            'port_on',
            'port_connector']
    port_reference_designator = forms.CharField(required=False, label='port_reference_designator', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    port_part_number = forms.CharField(
        required=False, label='port_part_number', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    port_name = forms.CharField(required=False, label='port_name', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    port_lru_refdes = forms.CharField(
        required=False, label='port_lru_refdes', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    port_type = forms.CharField(required=False, label='port_type', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    port_on = forms.CharField(required=False, label='port_on', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    port_connector = forms.CharField(
        required=False, label='port_connector', widget=forms.TextInput(attrs={'style': 'width: 100px'}))


class CreateWire(forms.ModelForm):
    class Meta:
        model = models.wire
        fields = ['wire_refdes',
                  'wire_part_number',
                  'wire_name',
                  'termination_refdes',
                  'contact_id',
                  'contact_pn',
                  'conductor_contact_size',
                  'conductor_id',
                  'contact_code',
                  'conductor_signal_type',
                  'conductor_color',
                  'conductor_awg',
                  'conductor_resistance',
                  'shielding',
                  'weight',
                  'conductor_diameter',
                  'conductor_material',
                  'conductor_jacket',
                  'conductor_voltage_rating',
                  'conductor_temperature_rating',
                  'length',
                  'user_comment',
                  'photo_file_path',
                  'harness_refdes',
                  'harness_part_number']

    wire_refdes = forms.CharField(required=False, label='wire_refdes', widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    wire_part_number = forms.CharField(
        required=False, label="wire_part_number", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    wire_name = forms.CharField(required=False, label="wire_name", widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    termination_refdes = forms.CharField(
        required=False, label="termination_refdes", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    contact_id = forms.CharField(required=False, label="contact_id", widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    contact_pn = forms.CharField(required=False, label="contact_pn", widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conductor_contact_size = forms.CharField(
        required=False, label="conductor_contact_size", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_id = forms.CharField(
        required=False, label="conductor_id", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    contact_code = forms.CharField(
        required=False, label="contact_code", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_signal_type = forms.CharField(
        required=False, label="conductor_signal_type", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_color = forms.CharField(
        required=False, label="conductor_color", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_awg = forms.CharField(
        required=False, label="conductor_awg", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_resistance = forms.CharField(
        required=False, label="conductor_resistance", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    shielding = forms.CharField(required=False, label="shielding", widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    weight = forms.CharField(required=False, label="weight", widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    conductor_diameter = forms.CharField(
        required=False, label="conductor_diameter", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_material = forms.CharField(
        required=False, label="conductor_material", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_jacket = forms.CharField(
        required=False, label="conductor_jacket", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_voltage_rating = forms.CharField(
        required=False, label="conductor_voltage_rating", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    conductor_temperature_rating = forms.CharField(
        required=False, label="conductor_temperature_rating", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    length = forms.CharField(required=False, label="length", widget=forms.TextInput(
        attrs={'style': 'width: 100px'}))
    user_comment = forms.CharField(
        required=False, label="user_comment", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    photo_file_path = forms.CharField(
        required=False, label="photo_file_path", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    harness_refdes = forms.CharField(
        required=False, label="harness_refdes", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    harness_part_number = forms.CharField(
        required=False, label="harness_part_number", widget=forms.TextInput(attrs={'style': 'width: 100px'}))
