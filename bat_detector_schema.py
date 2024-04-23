import arcpy

# Set workspace
arcpy.env.workspace = r"C:\Users\Joe.Bullard\OneDrive - Avon Wildlife Trust\Documents\ArcGIS\Projects\Bat Detectors 2024\Bat Detectors 2024.gdb"

# Create feature class for detector locations
arcpy.management.CreateFeatureclass(
    arcpy.env.workspace,
    "locations",
    "POINT",
    spatial_reference=arcpy.SpatialReference(
        4326
    ),  # Update spatial reference as needed
)

# Create deployment table
arcpy.management.CreateTable(arcpy.env.workspace, "deployments")

# Create bat pass table - empty for now
arcpy.management.CreateTable(arcpy.env.workspace, "bat_passes")

reserve_domain_values = ["Goblin Combe (AWT)", "King's wood"]

serial_domain_values = [
    "SMU01779",
    "SMU12690",
    "SMU12567",
    "SMU01894",
    "SMU02814",
    "SMU12696",
    "SMU12541",
    "SMU02814",
]

key_domain_values = [
    "P534",
    "P539",
    "P312",
    "P682",
    "P669",
    "P364",
    "P240",
    "P359",
    "P239",
]

battery_domain_values = ["Li-ion", "AA"]

li_ion_cell_domain_values = [2, 4, 6]

card_size_domain_values = ["128GB", "256GB", "512GB"]

deployer_domain_values = ["Joe Bullard", "Jen Greenwood"]


# Add fields to the deployment table
schema_dict = {
    "locations": [
        ("location_id", "SHORT", "Location ID"),
        (
            "reserve",
            "TEXT",
            "Reserve",
            "reserve_domain",
            "Reserve_domain",
        ),
        ("compartment_id", "TEXT", "Compartment ID"),
        ("active", "SHORT", "Active"),
        ("last_deployment", "DATE", "Last deployment"),
        ("description", "TEXT", "Description"),
    ],
    "deployments": [
        ("location_guid", "GUID", "Location ID"),
        (
            "serial",
            "TEXT",
            "Serial",
            "serial_domain",
            "Serial Domain",
        ),
        (
            "key_number",
            "TEXT",
            "Key Number",
            "key_domain",
            "Key Domain",
        ),
        (
            "battery_type",
            "TEXT",
            "Battery type",
            "battery_domain",
            "Battery Domain",
        ),
        (
            "li_ion_cells",
            "SHORT",
            "Li-ion cells",
            "li_ion_cells_domain",
            "Li-ion Cells Domain",
        ),
        (
            "card_size",
            "TEXT",
            "SD Card size",
            "card_size_domain",
            "Card Size Domain",
        ),
        ("start_date", "DATE", "Start Date"),
        ("end_date", "DATE", "End Date"),
        (
            "deployed_by",
            "TEXT",
            "Deployed by",
            "deployer_domain",
            "Deployer Domain",
        ),
        ("notes", "TEXT", "Notes"),
    ],
    "bat_passes" : [
        ("deployment_guid", "GUID", "Deployment ID"),
        ("timestamp", "DATE", "Timestamp")
    ]
}


for key, value in schema_dict.items():
    layer = key

    for params in value:
        field_name = params[0]
        field_type = params[1]
        field_alias = params[2]

        arcpy.management.AddField(
            layer, field_name=field_name, field_type=field_type, field_alias=field_alias
        )
        if len(params) > 3:
            domain_name = params[3]
            domain_alias = params[4]
            domain_values = params[5]
            arcpy.management.CreateDomain(
                arcpy.env.workspace, domain_name, domain_alias, field_type, "CODED"
            )
            for value in domain_values:
                arcpy.management.AddCodedValueToDomain(
                    arcpy.env.workspace, domain_name, value, value
                )

            arcpy.management.AssignDomainToField(layer, field_name, domain_name)


arcpy.management.AddGlobalIDs("locations")
arcpy.management.AddGlobalIDs("deployments")
# Enable attachments
arcpy.management.EnableAttachments("locations")

# Set relationship class between feature class and deployment table
arcpy.management.CreateRelationshipClass(
    origin_table="locations",
    destination_table="deployments",
    out_relationship_class="detector_deployment",
    relationship_type="SIMPLE",
    forward_label="deployment date",
    backward_label="deployment location",
    cardinality="ONE_TO_MANY",
    origin_primary_key="GlobalID",
    origin_foreign_key="location_guid",
)

arcpy.management.CreateRelationshipClass(
    origin_table="deployments",
    destination_table="bat_passes",
    out_relationship_class="deployment_passes",
    relationship_type="SIMPLE",
    forward_label="bat passes",
    backward_label="deployment",
    cardinality="ONE_TO_MANY",
    origin_primary_key="GlobalID",
    origin_foreign_key="deployment_guid",
)
