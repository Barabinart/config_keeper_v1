from netmiko import ConnectHandler
from fastapi import HTTPException
from database import new_session, ConfigurationOrm
from schemas import Authdata


# метод для сохранения конфигурации
def save_configuration(auth: Authdata):
    # создаем элемент в котором содержится необходимая информация для авторизации на устройстве
    device = {
        "device_type": auth.device_type.value,
        "host": auth.device_ip,
        "username": auth.username,
        "password": auth.password,
    }

    try:
        ssh_session = ConnectHandler(**device)
        if auth.device_type.value != "mikrotik_routeros":
            configuration = ssh_session.send_command("show running-config")
        else:
            configuration = ssh_session.send_command("export compact")
            # удаление времени снятия конфигурации у оборудования Mikrotik
            lines = configuration.split('by')
            lines = lines[1:]
            configuration = '#'+'by'.join(lines)
        ssh_session.disconnect()
    except Exception as e:
        # raise HTTPException(status_code=400, detail=f"Ошибка подключения к устройству: {str(e)}")
        return f"Ошибка подключения к устройству: {str(e)}"

    with new_session() as session:
        last_config = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == auth.device_ip).order_by(
            ConfigurationOrm.created_at.desc()).first()

        if last_config and last_config.config == configuration:
            return "Конфигурация идентична последней, сохранение не требуется"
        new_config = ConfigurationOrm(
            device_type=auth.device_type.value,
            device_ip=auth.device_ip,
            config=configuration,
        )
        session.add(new_config)
        session.commit()

    return "Конфигурация успешно сохранена"


# Метод для просмотра последней конфигурации
def get_last_configuration(device_ip):
    with new_session() as session:
        last_config = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == device_ip).order_by(
            ConfigurationOrm.created_at.desc()).first()
        print(last_config)
        if last_config:
            return last_config.config
        else:
            return "Конфигурации для данного устройства не найдено"
