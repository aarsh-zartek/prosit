import uuid

def get_diet_plan_instruction_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit('.', 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f'{instance.category}/{instance.plan_type}/{file}'
    return file_path
