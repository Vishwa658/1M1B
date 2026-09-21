def get_authority(issue):

    issue = issue.lower()

    if "flood" in issue:

        return {

            "authority": "Greater Chennai Corporation",

            "reason": (
                "Flooding and local drainage complaints "
                "are generally civic infrastructure matters."
            ),

            "route": "Use the official GCC grievance/complaint system."
        }

    if "water" in issue or "sewer" in issue:

        return {

            "authority": (
                "Chennai Metropolitan Water Supply "
                "and Sewerage Board"
            ),

            "reason": (
                "Water supply and sewerage matters "
                "fall within CMWSSB functions."
            ),

            "route": (
                "Use the official CMWSSB complaint "
                "and grievance channels."
            )
        }

    return {

        "authority": (
            "Relevant groundwater / water-resources authority"
        ),

        "reason": (
            "Groundwater monitoring and management "
            "require technical water-resource data."
        ),

        "route": (
            "Use the appropriate official groundwater "
            "or water-resources grievance channel."
        )
    }