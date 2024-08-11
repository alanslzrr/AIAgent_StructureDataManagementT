from datetime import datetime

def find_nearest_expiring_certificate(collection):
    current_date = datetime.now().date()
    
    # Pipeline for nearest expiring certificate
    nearest_expiring_pipeline = [
        {"$unwind": "$Standards"},
        {"$match": {"Standards.DueDate": {"$gt": current_date.isoformat()}}},
        {"$sort": {"Standards.DueDate": 1}},
        {"$limit": 1},
        {"$project": {
            "Certificate": "$CertNo",
            "Standard": {"$concat": ["$Standards.Description", " (ID ", "$Standards.IdInst", ")"]},
            "Expiration_date": "$Standards.DueDate",
            "Days_until_expiration": {
                "$divide": [
                    {"$subtract": [
                        {"$dateFromString": {"dateString": "$Standards.DueDate"}},
                        {"$dateFromString": {"dateString": current_date.isoformat()}}
                    ]},
                    86400000  # milliseconds in a day
                ]
            }
        }}
    ]

    # Pipeline for last expired certificate
    last_expired_pipeline = [
        {"$unwind": "$Standards"},
        {"$match": {"Standards.DueDate": {"$lt": current_date.isoformat()}}},
        {"$sort": {"Standards.DueDate": -1}},
        {"$limit": 1},
        {"$project": {
            "Certificate": "$CertNo",
            "Standard": {"$concat": ["$Standards.Description", " (ID ", "$Standards.IdInst", ")"]},
            "Expiration_date": "$Standards.DueDate",
            "Days_since_expiration": {
                "$divide": [
                    {"$subtract": [
                        {"$dateFromString": {"dateString": current_date.isoformat()}},
                        {"$dateFromString": {"dateString": "$Standards.DueDate"}}
                    ]},
                    86400000  # milliseconds in a day
                ]
            }
        }}
    ]

    nearest_expiring = list(collection.aggregate(nearest_expiring_pipeline))
    
    if nearest_expiring:
        cert_info = nearest_expiring[0]
        return {
            "Type": "Nearest Expiring",
            "Certificate": cert_info["Certificate"],
            "Standard": cert_info["Standard"],
            "Expiration date": cert_info["Expiration_date"],
            "Days until expiration": int(cert_info['Days_until_expiration'])
        }
    else:
        last_expired = list(collection.aggregate(last_expired_pipeline))
        if last_expired:
            cert_info = last_expired[0]
            return {
                "Type": "Last Expired",
                "Certificate": cert_info["Certificate"],
                "Standard": cert_info["Standard"],
                "Expiration date": cert_info["Expiration_date"],
                "Days since expiration": int(cert_info['Days_since_expiration'])
            }
        else:
            return {"Type": "No Certificates", "Status": "No certificates found in the database."}