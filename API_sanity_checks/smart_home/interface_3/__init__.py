from .add_alert import AddAlert
from .add_command import AddCommand
from .create_address import CreateAddress
from .create_device import CreateDevice
from .create_new_routine import CreateNewRoutine
from .fetch_alerts_info import FetchAlertsInfo
from .fetch_commands import FetchCommands
from .fetch_devices_info import FetchDevicesInfo
from .fetch_energy_tariffs_info import FetchEnergyTariffsInfo
from .fetch_historical_energy_consumption_by_home import FetchHistoricalEnergyConsumptionByHome
from .fetch_home_info import FetchHomeInfo
from .fetch_room_info import FetchRoomInfo
from .fetch_routine import FetchRoutine
from .fetch_user_info import FetchUserInfo
from .list_addresses import ListAddresses
from .list_children import ListChildren
from .update_alert_info import UpdateAlertInfo
from .update_device_info import UpdateDeviceInfo
from .update_room_info import UpdateRoomInfo
from .update_routine import UpdateRoutine
from .update_user_info import UpdateUserInfo


ALL_TOOLS_INTERFACE_3 = [
    AddAlert,
    AddCommand,
    CreateAddress,
    CreateDevice,
    CreateNewRoutine,
    FetchAlertsInfo,
    FetchCommands,
    FetchDevicesInfo,
    FetchEnergyTariffsInfo,
    FetchHistoricalEnergyConsumptionByHome,
    FetchHomeInfo,
    FetchRoomInfo,
    FetchRoutine,
    FetchUserInfo,
    ListAddresses,
    ListChildren,
    UpdateAlertInfo,
    UpdateDeviceInfo,
    UpdateRoomInfo,
    UpdateRoutine,
    UpdateUserInfo
]
