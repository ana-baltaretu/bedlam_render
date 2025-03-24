import unreal
import time

def replace_material_by_label(number, material_path):
    """
    Replaces the material of all Geometry Cache objects in the scene
    that contain '_<number>_' in their label.

    Args:
    - number (int): The number to search for in object labels.
    - material_path (str): Path to the new material in the Content Browser (e.g., "/Game/M_Green").
    """

    search_str = f"_{number}_"

    # Get all actors in the current level (works in UE 5.0.3)
    actors = unreal.EditorLevelLibrary.get_all_level_actors()

    # Load the specified material from the Content Browser
    material = unreal.EditorAssetLibrary.load_asset(material_path)

    if not material:
        unreal.log_error(f"Material not found at path: {material_path}")
        return

    # Iterate through all actors
    for actor in actors:
        actor_label = actor.get_actor_label()

        if search_str in actor_label:
            # Log the found actor
            unreal.log(f"Found matching actor: {actor_label}")

            # Check if the actor is a GeometryCacheActor
            if isinstance(actor, unreal.GeometryCacheActor):
                # Get the GeometryCacheComponent (fix for AttributeError)
                geo_cache_component = actor.get_geometry_cache_component()

                if geo_cache_component:
                    # Apply the new material to all material slots
                    for i in range(geo_cache_component.get_num_materials()):
                        geo_cache_component.set_material(i, material)
                    unreal.log(f"Replaced material for: {actor_label}")
                else:
                    unreal.log_warning(f"GeometryCacheComponent not found for {actor_label}")


# Default material
# for i in range(25, 60): # Normal weight
#     replace_material_by_label(i, "/Engine/EngineMaterials/WorldGridMaterial")


for i in range(25, 33): # Normal weight
    replace_material_by_label(i, "/Game/M_Green")

for i in range(33, 40):  # Obese
    replace_material_by_label(i, "/Game/M_Blue")

for i in range(40, 60):  # Severe Obese
    replace_material_by_label(i, "/Game/M_Red")
