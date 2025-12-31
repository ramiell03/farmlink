ROLE_PERMISSIONS = {
    "farmer":{
        "manage_account",
        "create_crop",
        "update_crop",
        "view_prices",
        "connect_with_buyers",
    },
    
    "buyer":{
        "manage_account",
        "view_products",
        "search_crops",
        "view_farmer_profiles",
        "connect_with_farmers",
        "track_orders",
    },
    
    "admin":{
        "manage_users",
        "monitor_platform",
        "generate_reports",
        "manage_market_data",
    }
}