import cloudinary
import cloudinary.uploader
from supabase_client import supabase

# Configura Cloudinary antes de usar
cloudinary.config(
    cloud_name="djlskhtyf",
    api_key="596625527778167",
    api_secret="zTTEjWP4apxgFF8a-kYNRTzT_XY"
)

def pits(region, traction_type, specialty, team_number, battery_number, robot_image, strategy_image, strategy_comment):
    
    robot_url = None
    strategy_url = None

    if robot_image:
        robot_url = cloudinary.uploader.upload(robot_image).get("secure_url")

    if strategy_image:
        strategy_url = cloudinary.uploader.upload(strategy_image).get("secure_url")

    data= {
        "region": region,
        "traction_type": traction_type,
        "specialty": specialty,
        "team_number": team_number,
        "battery_number": battery_number,
        "robot_image": robot_url,
        "strategy_image": strategy_url,
        "strategy_comment": strategy_comment
    }

    response = supabase.table("pits").insert(data).execute()
    return response