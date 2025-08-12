from .acknowledge_or_resolve_alert import AcknowledgeOrResolveAlert
from .add_command import AddCommand
from .add_device import AddDevice
from .add_feedback import AddFeedback
from .create_address import CreateAddress
from .create_emergency_alert import CreateEmergencyAlert
from .create_routine import CreateRoutine
from .get_address import GetAddress
from .get_commands import GetCommands
from .get_devices_info import GetDevicesInfo
from .get_emergency_alerts import GetEmergencyAlerts
from .get_energy_tariffs_info import GetEnergyTariffsInfo
from .get_historical_energy_consumption_by_device import GetHistoricalEnergyConsumptionByDevice
from .get_home_info import GetHomeInfo
from .get_rooms_info import GetRoomsInfo
from .get_routines import GetRoutines
from .get_user_info import GetUserInfo
from .list_children import ListChildren
from .update_device_info import UpdateDeviceInfo
from .update_home_info import UpdateHomeInfo
from .update_room_info import UpdateRoomInfo
from .update_user_info import UpdateUserInfo


ALL_TOOLS_INTERFACE_1 = [
    AcknowledgeOrResolveAlert,
    AddCommand,
    AddDevice,
    AddFeedback,
    CreateAddress,
    CreateEmergencyAlert,
    CreateRoutine,
    GetAddress,
    GetCommands,
    GetDevicesInfo,
    GetEmergencyAlerts,
    GetEnergyTariffsInfo,
    GetHistoricalEnergyConsumptionByDevice,
    GetHomeInfo,
    GetRoomsInfo,
    GetRoutines,
    GetUserInfo,
    ListChildren,
    UpdateDeviceInfo,
    UpdateHomeInfo,
    UpdateRoomInfo,
    UpdateUserInfo
]
