def validate_row(row):
    required_filelds = ["name", "email", "phone"]

    for field in required_filelds:
        if field not in row:
            raise ValueError(f"Missing field: {field}")
        
    if not row["email"]:
        raise ValueError("Email is required")
    
    if "@" not in row["email"]:
        raise ValueError(f"Invalid email:{row["email"]}")
    
    return True