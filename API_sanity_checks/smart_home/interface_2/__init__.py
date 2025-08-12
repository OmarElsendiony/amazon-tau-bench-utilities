from .add_command import AddCommand
from .add_device import AddDevice
from .add_user_feedback import AddUserFeedback
from .create_address import CreateAddress
from .create_emergency_alert import CreateEmergencyAlert
from .create_routine import CreateRoutine
from .create_user import CreateUser
from .get_address_details import GetAddressDetails
from .get_alerts_by_alert_type import GetAlertsByAlertType
from .get_commands import GetCommands
from .get_devices_details import GetDevicesDetails
from .get_energy_tariffs_details import GetEnergyTariffsDetails
from .get_historical_energy_consumption_by_device import GetHistoricalEnergyConsumptionByDevice
from .get_home_details import GetHomeDetails
from .get_room_details import GetRoomDetails
from .get_routine import GetRoutine
from .get_user_details import GetUserDetails
from .list_rooms import ListRooms
from .update_alert import UpdateAlert
from .update_device_details import UpdateDeviceDetails
from .update_room_details import UpdateRoomDetails


ALL_TOOLS_INTERFACE_2 = [
    AddCommand,
    AddDevice,
    AddUserFeedback,
    CreateAddress,
    CreateEmergencyAlert,
    CreateRoutine,
    CreateUser,
    GetAddressDetails,
    GetAlertsByAlertType,
    GetCommands,
    GetDevicesDetails,
    GetEnergyTariffsDetails,
    GetHistoricalEnergyConsumptionByDevice,
    GetHomeDetails,
    GetRoomDetails,
    GetRoutine,
    GetUserDetails,
    ListRooms,
    UpdateAlert,
    UpdateDeviceDetails,
    UpdateRoomDetails
]
