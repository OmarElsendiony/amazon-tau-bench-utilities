from .add_command import AddCommand
from .add_device_feedback import AddDeviceFeedback
from .add_energy_consumption_record import AddEnergyConsumptionRecord
from .add_new_device import AddNewDevice
from .add_routine import AddRoutine
from .create_alert import CreateAlert
from .fetch_alert_details import FetchAlertDetails
from .fetch_devices_details import FetchDevicesDetails
from .fetch_energy_tariffs_details import FetchEnergyTariffsDetails
from .fetch_historical_energy_consumption_by_home import FetchHistoricalEnergyConsumptionByHome
from .fetch_home_details import FetchHomeDetails
from .fetch_room_details import FetchRoomDetails
from .fetch_routine import FetchRoutine
from .fetch_user_details import FetchUserDetails
from .list_alert_ids import ListAlertIds
from .list_commands import ListCommands
from .list_feedbacks import ListFeedbacks
from .mark_user_inactive import MarkUserInactive
from .update_alert import UpdateAlert
from .update_device_details import UpdateDeviceDetails
from .update_room_status import UpdateRoomStatus
from .fetch_home_by_owner_id import FetchHomeByOwnerId


ALL_TOOLS_INTERFACE_4 = [
    AddCommand,
    AddDeviceFeedback,
    AddEnergyConsumptionRecord,
    AddNewDevice,
    AddRoutine,
    CreateAlert,
    FetchAlertDetails,
    FetchDevicesDetails,
    FetchEnergyTariffsDetails,
    FetchHistoricalEnergyConsumptionByHome,
    FetchHomeDetails,
    FetchRoomDetails,
    FetchRoutine,
    FetchUserDetails,
    ListAlertIds,
    ListCommands,
    ListFeedbacks,
    MarkUserInactive,
    UpdateAlert,
    UpdateDeviceDetails,
    UpdateRoomStatus,
    FetchHomeByOwnerId
]
