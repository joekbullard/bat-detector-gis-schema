import arcpy
import arcpy.management

# Set workspace
arcpy.env.workspace = r"path/to/file.gdb"

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
    "location_fields": [
        ("location_id", "SHORT", "Location ID"),
        (
            "reserve",
            "TEXT",
            "Reserve",
            "reserve_domain",
            "Reserve_domain",
            reserve_domain_values,
        ),
        ("compartment_id", "TEXT", "Compartment ID"),
        ("active", "SHORT", "Active"),
        ("last_deployment", "DATE", "Last deployment"),
        ("description", "TEXT", "Description"),
    ],
    "deployment_fields": [
        ("location_guid", "GUID", "Location ID"),
        (
            "serial",
            "TEXT",
            "Serial",
            "serial_domain",
            "Serial Domain",
            serial_domain_values,
        ),
        (
            "key_number",
            "TEXT",
            "Key Number",
            "key_domain",
            "Key Domain",
            key_domain_values,
        ),
        (
            "battery_type",
            "TEXT",
            "Battery type",
            "battery_domain",
            "Battery Domain",
            battery_domain_values,
        ),
        (
            "li_ion_cells",
            "SHORT",
            "Li-ion cells",
            "li_ion_cells_domain",
            "Li-ion Cells Domain",
            li_ion_cell_domain_values,
        ),
        (
            "card_size",
            "TEXT",
            "SD Card size",
            "card_size_domain",
            "Card Size Domain",
            card_size_domain_values,
        ),
        ("start_date", "DATE", "Start Date"),
        ("end_date", "DATE", "End Date"),
        (
            "deployed_by",
            "TEXT",
            "Deployed by",
            "deployer_domain",
            "Deployer Domain",
            deployer_domain_values,
        ),
        ("notes", "TEXT", "Notes"),
    ],
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
