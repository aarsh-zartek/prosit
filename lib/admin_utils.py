def FieldSets(**kwargs):
    """A small utility to simplify the use of fieldsets in Admin"""
    
    sections = list()
    
    for key, value in kwargs.items():
        key = None if key.lower() == "none" else key.replace("_", " ").title()
        
        sections.append((
            key, {"fields": value}
        ))

    return sections
