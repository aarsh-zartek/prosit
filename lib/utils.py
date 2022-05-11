import uuid

def get_diet_plan_instruction_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit('.', 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f'{instance.name}/instruction/{file}'
    return file_path

def get_preparation_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit('.', 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f'{instance.name}/preparation/{file}'
    return file_path

def get_user_health_image_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit('.', 1)
    file = f"{name.lower().replace(' ', '_')}_{uuid.uuid4()}.{ext}"
    file_path = f'{instance.user.uid}/health_reports/{file}'
    return file_path
