from supabase_client import supabase

def match(
    team_number,
    match_number,
    regional,

    # Autonomus
    check_inicio,
    count_motiv,
    count_in_cage_auto,
    count_out_cage_auto,

    # Teleop
    count_in_cage_teleop,
    count_out_cage_teleop,
    count_rp,

    # Endgame
    check_scoring,
    count_in_cage_endgame,
    count_out_cage_endgame,
    check_full_park,
    check_partial_park,
    check_high,

    # Ratings
    robot_rating,
    comment_robot,
    driver_rating,
    comment_driver,
    general_rating,
    comment_general
):
    
    data  ={
        "team_number": team_number,
        "match_number": match_number,
        "regional": regional,

        "check_inicio": check_inicio*3,
        "count_motiv": count_motiv*2,
        "count_in_cage_auto": count_in_cage_auto*3,
        "count_out_cage_auto": count_out_cage_auto*1,

        "count_in_cage_teleop": count_in_cage_teleop*3,
        "count_out_cage_teleop": count_out_cage_teleop*1,
        "count_rp": count_rp,

        "check_scoring": check_scoring,
        "count_in_cage_endgame": count_in_cage_endgame*3,
        "count_out_cage_endgame": count_out_cage_endgame*1,
        "check_full_park": 10 if check_full_park  =="Sí" else 0,
        "check_partial_park": 5 if check_partial_park  =="Sí" else 0,
        "check_high": 10 if check_high == "Sí" else 0,

        "robot_rating": robot_rating,
        "comment_robot": comment_robot,
        "driver_rating": driver_rating,
        "comment_driver": comment_driver,
        "general_rating": general_rating,
        "comment_general": comment_general
    }

    response = supabase.table("matches").insert(data).execute()
    return response
