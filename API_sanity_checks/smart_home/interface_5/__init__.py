from .average_rating_device import AverageRatingDevice
from .create_alert import CreateAlert
from .create_command import CreateCommand
from .create_device import CreateDevice
from .create_energy_consumption_record import CreateEnergyConsumptionRecord
from .create_routine import CreateRoutine
from .is_expired_warranty_devices import IsExpiredWarrantyDevices
from .list_commands import ListCommands
from .list_devices import ListDevices
from .list_homes_and_rooms import ListHomesAndRooms
from .post_feedback import PostFeedback
from .retrieve_room_info import RetrieveRoomInfo
from .retrieve_device_info import RetrieveDeviceInfo
from .retrieve_energy_tariffs_details import RetrieveEnergyTariffsDetails
from .retrieve_historical_energy_consumption_by_device import RetrieveHistoricalEnergyConsumptionByDevice
from .retrieve_routine import RetrieveRoutine
from .retrieve_user_profile import RetrieveUserProfile
from .update_alert_details import UpdateAlertDetails
from .update_device_info import UpdateDeviceInfo
from .update_room_details import UpdateRoomDetails
from .update_user_profile import UpdateUserProfile


ALL_TOOLS_INTERFACE_5 = [
    AverageRatingDevice,
    CreateAlert,
    CreateCommand,
    CreateDevice,
    CreateEnergyConsumptionRecord,
    CreateRoutine,
    IsExpiredWarrantyDevices,
    ListCommands,
    ListDevices,
    ListHomesAndRooms,
    PostFeedback,
    RetrieveRoomInfo,
    RetrieveDeviceInfo,
    RetrieveEnergyTariffsDetails,
    RetrieveHistoricalEnergyConsumptionByDevice,
    RetrieveRoutine,
    RetrieveUserProfile,
    UpdateAlertDetails,
    UpdateDeviceInfo,
    UpdateRoomDetails,
    UpdateUserProfile
]
