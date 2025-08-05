from faker import Faker
import random
import json
from datetime import datetime, timedelta

faker = Faker('en_US')
now = datetime.utcnow()

# Configuration: number of records to generate
N_ADDRESSES = 80
N_PARENTS = 80
N_SERVANTS = 80
N_GUESTS = 80
# Children will be generated per parent (0–5 each)
N_ROOMS = 10
N_DEVICES = 15
N_ROUTINES = 5
N_DEVICE_COMMANDS = 5
N_BULB_COMMANDS = 5
N_THERMOSTAT_COMMANDS = 5
N_CONSUMPTION = 30
N_FEEDBACKS = 10
N_ALERTS = 10
N_TARIFFS = 5

# ID counters
counters = {
    'addresses': 0,
    'users': 0,
    'homes': 0,
    'rooms': 0,
    'devices': 0,
    'consumption': 0,
    'routines': 0,
    'device_commands': 0,
    'bulb_commands': 0,
    'thermostat_commands': 0,
    'feedbacks': 0,
    'alerts': 0,
    'tariffs': 0,
}

def next_id(table):
    counters[table] += 1
    return str(counters[table])

def random_timestamp(start, end):
    """Return a random datetime between start and end."""
    return start + (end - start) * random.random()

import random

def generate_building_name():
    prefixes = [
        "Royal", "Silver", "Golden", "Green", "Sunset", "Hill", "Lake",
        "Maple", "Cedar", "Oak", "Pine", "Crystal", "River", "Spring",
        "Heritage", "Sky", "Ocean", "Sunrise", "Amber", "Willow", "Grand", "Majestic"
    ]

    suffixes = [
        "Heights", "Residency", "Tower", "Manor", "Court", "Palace",
        "Enclave", "Suites", "Gardens", "Apartments", "Plaza", "Terrace",
        "Arcade", "Complex", "Lodge", "Vista", "Hall", "Crossing", "Place", "Retreat"
    ]

    return f"{random.choice(prefixes)} {random.choice(suffixes)}"


def generate_house_number():
    return str(int(faker.building_number()))


state_area_codes = {
    "Alabama": ["205", "251", "256", "334", "938"],
    "Alaska": ["907"],
    "Arizona": ["480", "520", "602", "623", "928"],
    "Arkansas": ["479", "501", "870"],
    "California": ["209", "213", "310", "323", "408", "415", "424", "442", "530", "559", "562", "619", "626", "650", "657", "707", "714", "747", "760", "805", "818", "831", "858", "909", "916", "925", "949"],
    "Colorado": ["303", "719", "720", "970"],
    "Connecticut": ["203", "475", "860", "959"],
    "Delaware": ["302"],
    "Florida": ["239", "305", "321", "352", "386", "407", "561", "727", "754", "772", "786", "813", "850", "863", "904", "941", "954"],
    "Georgia": ["229", "404", "470", "478", "678", "706", "762", "770", "912"],
    "Hawaii": ["808"],
    "Idaho": ["208", "986"],
    "Illinois": ["217", "224", "309", "312", "331", "618", "630", "708", "773", "779", "815", "847"],
    "Indiana": ["219", "260", "317", "463", "574", "765", "812", "930"],
    "Iowa": ["319", "515", "563", "641", "712"],
    "Kansas": ["316", "620", "785", "913"],
    "Kentucky": ["270", "364", "502", "606", "859"],
    "Louisiana": ["225", "318", "337", "504", "985"],
    "Maine": ["207"],
    "Maryland": ["240", "301", "410", "443", "667"],
    "Massachusetts": ["339", "351", "413", "508", "617", "774", "781", "857", "978"],
    "Michigan": ["231", "248", "269", "313", "517", "586", "616", "734", "810", "906", "947", "989"],
    "Minnesota": ["218", "320", "507", "612", "651", "763", "952"],
    "Mississippi": ["228", "601", "662", "769"],
    "Missouri": ["314", "417", "573", "636", "660", "816"],
    "Montana": ["406"],
    "Nebraska": ["308", "402", "531"],
    "Nevada": ["702", "725", "775"],
    "New Hampshire": ["603"],
    "New Jersey": ["201", "551", "609", "640", "732", "848", "856", "862", "908", "973"],
    "New Mexico": ["505", "575"],
    "New York": ["212", "315", "332", "347", "516", "518", "585", "607", "631", "646", "680", "716", "718", "838", "845", "914", "917", "929"],
    "North Carolina": ["252", "336", "704", "743", "828", "910", "980", "984"],
    "North Dakota": ["701"],
    "Ohio": ["216", "220", "234", "283", "326", "330", "419", "440", "513", "567", "614", "740", "937"],
    "Oklahoma": ["405", "539", "580", "918"],
    "Oregon": ["458", "503", "541", "971"],
    "Pennsylvania": ["215", "223", "267", "272", "412", "445", "484", "570", "610", "717", "724", "814", "878"],
    "Rhode Island": ["401"],
    "South Carolina": ["803", "839", "843", "854", "864"],
    "South Dakota": ["605"],
    "Tennessee": ["423", "615", "629", "731", "865", "901", "931"],
    "Texas": ["210", "214", "254", "281", "325", "346", "361", "409", "430", "432", "469", "512", "682", "713", "737", "806", "817", "830", "832", "903", "915", "936", "940", "956", "972", "979"],
    "Utah": ["385", "435", "801"],
    "Vermont": ["802"],
    "Virginia": ["276", "434", "540", "571", "703", "757", "804"],
    "Washington": ["206", "253", "360", "425", "509"],
    "West Virginia": ["304", "681"],
    "Wisconsin": ["262", "274", "414", "534", "608", "715", "920"],
    "Wyoming": ["307"]
}

def generate_realistic_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "aol.com"]
    formats = [
        f"{first_name}{last_name}{random.randint(1, 999)}",
        f"{first_name[0]}{last_name}{random.randint(1, 999)}",
        f"{last_name}{random.randint(10, 9999)}",
        f"{first_name}.{last_name}",
        f"{first_name}_{last_name}{random.randint(10, 999)}"
    ]
    local_part = random.choice(formats).lower()
    domain = random.choice(domains)
    return f"{local_part}@{domain}"


def generate_state_and_phone():
    state = faker.random_element(list(state_area_codes.keys()))
    area_code = random.choice(state_area_codes[state])
    central_office_code = faker.random_int(min=200, max=999)
    subscriber_number = faker.random_int(min=1000, max=9999)
    phone_number = f"+1{area_code}{central_office_code}{subscriber_number}"  # No dashes
    return state, phone_number

# 1. Addresses
addresses = {}
for _ in range(N_ADDRESSES):
    aid = next_id('addresses')
    created = random_timestamp(now - timedelta(days=365), now - timedelta(days=30))
    updated = random_timestamp(created, now)
    addresses[aid] = {
        "address_id": aid,
        "house_number": generate_house_number(),
        "building_name": generate_building_name(),
        "street": faker.street_name(),
        "city_name": faker.city(),
        "state": faker.state(),
        "created_at": created.isoformat(),
        "updated_at": updated.isoformat(),
    }

# 2. Users (Parents, then Children, then Servants & Guests)
users = {}
parents = []
# Parents
available_address_ids = list(addresses.keys())  # track unassigned addresses
random.shuffle(available_address_ids)   
for _ in range(N_PARENTS):
    uid = next_id('users')
    dob = faker.date_of_birth(minimum_age=30, maximum_age=60)
    created = random_timestamp(now - timedelta(days=365*5), now - timedelta(days=365))
    updated = random_timestamp(created, now)
    state, phone_number = generate_state_and_phone()
    assigned_address_id = available_address_ids.pop()  # unique address
    user = {
        "user_id": uid,
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "phone_number": phone_number,
        "role": "Owner",
        "parent_id": None,
        "email": None,  # to fill after names
        "primary_address_id": assigned_address_id,
        "date_of_birth": dob.isoformat(),
        "status": "active",
        "created_at": created.isoformat(),
        "updated_at": updated.isoformat(),
    }
    user["email"] = generate_realistic_email(user["first_name"], user["last_name"])
    users[uid] = user
    parents.append((uid, dob))

    # Optional Partner
    if random.random() < 0.9:  # 90% chance of having a partner
        pid = next_id('users')
        pdob = faker.date_of_birth(minimum_age=25, maximum_age=55)
        partner_created = random_timestamp(created, now)
        partner_updated = random_timestamp(partner_created, now)
        state, partner_phone = generate_state_and_phone()
        partner = {
            "user_id": pid,
            "first_name": faker.first_name_female(),
            "last_name": user["last_name"],  # same last name
            "phone_number": partner_phone,
            "role": "Partner",
            "parent_id": None,
            "email": None,
            "primary_address_id": assigned_address_id,
            "date_of_birth": pdob.isoformat(),
            "status": "active",
            "created_at": partner_created.isoformat(),
            "updated_at": partner_updated.isoformat(),
        }
        partner["email"] = generate_realistic_email(partner["first_name"], partner["last_name"])
        users[pid] = partner

# Children
for pid, pdob in parents:
    num_children = random.randint(0, 5)
    for _ in range(num_children):
        uid = next_id('users')
        cdob = (pdob + timedelta(days=20*365))
        created = random_timestamp(now - timedelta(days=365*3), now - timedelta(days=180))
        updated = random_timestamp(created, now)
        state, phone_number = generate_state_and_phone()
        user = {
            "user_id": uid,
            "first_name": faker.first_name(),
            "last_name": users[pid]["last_name"],
            "phone_number": phone_number,
            "role": "Child",
            "parent_id": pid,
            "email": None,
            "primary_address_id": users[pid]["primary_address_id"],
            "date_of_birth": cdob.isoformat(),
            "status": "active",
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }
        user["email"] = generate_realistic_email(user["first_name"], user["last_name"])
        users[uid] = user


# 3. Homes
homes = {}
home_counter = 0

user_ids = [u for u, d in users.items() if d["role"] == "Owner"]

for owner in user_ids:
    num_homes = random.randint(1, 3)
    for i in range(num_homes):
        hid = next_id('homes')

        if i == 0:
            # Use the owner's existing primary address for their main home
            aid = users[owner]["primary_address_id"]
        else:
            # Create a new address
            aid = next_id('addresses')
            created_addr = random_timestamp(now - timedelta(days=365), now - timedelta(days=30))
            updated_addr = random_timestamp(created_addr, now)
            addresses[aid] = {
                "address_id": aid,
                "house_number": generate_house_number(),
                "building_name": generate_building_name(),
                "street": faker.street_name(),
                "city_name": faker.city(),
                "state": faker.state(),
                "created_at": created_addr.isoformat(),
                "updated_at": updated_addr.isoformat(),
            }

        created = random_timestamp(now - timedelta(days=365*3), now - timedelta(days=365))
        updated = random_timestamp(created, now)
        homes[hid] = {
            "home_id": hid,
            "owner_id": owner,
            "address_id": aid,
            "home_type": random.choice(["Home", "Apartment"]),
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }

        home_counter += 1

# Servants & Guests
for role, n in [("Servant", N_SERVANTS), ("Guest", N_GUESTS)]:
    for _ in range(n):
        uid = next_id('users')
        dob = faker.date_of_birth(minimum_age=18, maximum_age=65)
        status = random.choice(["active", "inactive"])
        created = random_timestamp(now - timedelta(days=365*2), now - timedelta(days=90))
        updated = random_timestamp(created, now)
        state, phone_number = generate_state_and_phone()
        user = {
            "user_id": uid,
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "phone_number": phone_number,
            "role": role,
            "parent_id": None,
            "email": None,
            "primary_address_id": random.choice(list(addresses.keys())),
            "date_of_birth": dob.isoformat(),
            "status": status,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }
        user["email"] = generate_realistic_email(user["first_name"], user["last_name"])
        users[uid] = user


# 4. Rooms
rooms = {}
home_rooms = {hid: [] for hid in homes}
active_user_ids = [u for u, d in users.items() if d["status"] == "active"]

for hid, home in homes.items():
    address_id = home["address_id"]
    owner_id = home["owner_id"]
    created = random_timestamp(now - timedelta(days=365*2), now - timedelta(days=180))
    updated = random_timestamp(created, now)

    # === 1. Bedrooms ===
    num_bedrooms = random.choices([1, 2, 3, 4], weights=[45, 40, 10, 5], k=1)[0]
    for i in range(num_bedrooms):
        rid = next_id('rooms')
        if i == 0:
            room_owner_id = owner_id
            status = "occupied"
        elif random.random() < 0.7:
            candidates = [
                uid for uid, u in users.items()
                if u["primary_address_id"] == address_id and u["status"] == "active"
            ]
            if candidates:
                room_owner_id = random.choice(candidates)
                status = "occupied"
            else:
                room_owner_id = None
                status = "vacant"
        else:
            room_owner_id = None
            status = "vacant"

        room = {
            "room_id": rid,
            "home_id": hid,
            "room_type": "Bedroom",
            "room_owner_id": room_owner_id,
            "status": status,
            "width_ft": round(random.uniform(10, 20), 2),
            "length_ft": round(random.uniform(10, 20), 2),
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }
        rooms[rid] = room
        home_rooms[hid].append(rid)

    # === 2. Other Room Types (append this block here) ===
    room_types_config = {
        "kitchen": (1, 2),
        "lounge": (0, 2),
        "store": (0, 1),
        "diningroom": (0, 1),
    }

    for room_type, (min_r, max_r) in room_types_config.items():
        num_rooms = random.randint(min_r, max_r)
        for _ in range(num_rooms):
            rid = next_id('rooms')
            updated = random_timestamp(created, now)

            room_owner_id = None
            status = "vacant"

            if room_type in ["kitchen", "store"]:
                servants = [
                    uid for uid, u in users.items()
                    if u["role"] == "Servant" and u["primary_address_id"] == address_id and u["status"] == "active"
                ]
                if servants:
                    room_owner_id = random.choice(servants)
                else:
                    room_owner_id = owner_id
                status = "occupied"

            elif room_type in ["lounge", "diningroom"]:
                candidates = [
                    uid for uid, u in users.items()
                    if u["primary_address_id"] == address_id and u["status"] == "active"
                ]
                if candidates:
                    room_owner_id = random.choice(candidates)
                    status = "occupied"

            room = {
                "room_id": rid,
                "home_id": hid,
                "room_type": room_type,
                "room_owner_id": room_owner_id,
                "status": status,
                "width_ft": round(random.uniform(10, 20), 2),
                "length_ft": round(random.uniform(10, 20), 2),
                "created_at": created.isoformat(),
                "updated_at": updated.isoformat(),
            }
            rooms[rid] = room
            home_rooms[hid].append(rid)



# 5. Devices + subtype tables
# Devices per room with type-specific rules
devices = {}
security_cameras = {}
smart_bulbs = {}
smart_thermostats = {}

device_id_counter = 1

def next_device_id():
    global device_id_counter
    device_id = str(device_id_counter)
    device_id_counter += 1
    return device_id

def create_device_entry(did, dtype, rid, home_id):
    installed = faker.date_between(start_date='-2y', end_date=(now - timedelta(days=16)).date())
    created = random_timestamp(now - timedelta(days=365), now - timedelta(days=90))
    updated = random_timestamp(created, now)

    last_maintainance_date = faker.date_between_dates(
        date_start=installed,
        date_end=(now - timedelta(days=7)).date()
    )

    return {
        "device_id": did,
        "device_type": dtype,
        "room_id": rid,
        "installed_on": installed.isoformat(),
        "insurance_expiry_date": (installed + timedelta(days=365)).isoformat(),
        "home_id": home_id,
        "status": random.choice(["on", "off"]),
        "width_ft": round(random.uniform(0.5, 2), 2),
        "length_ft": round(random.uniform(0.5, 2), 2),
        "price": round(random.uniform(50, 800), 2),
        "scheduled_maintainance_date": (now + timedelta(days=random.randint(30, 180))).date().isoformat(),
        "last_maintainance_date": last_maintainance_date.isoformat(),
        "daily_rated_power_consumption_kWh": round(random.uniform(0.1, 5), 2),
        "created_at": created.isoformat(),
        "updated_at": updated.isoformat(),
    }, created, updated

home_rooms_by_type = {}
for rid, rdata in rooms.items():
    home_rooms_by_type.setdefault(rdata["home_id"], {}).setdefault(rdata["room_type"].lower(), []).append(rid)

for home_id, rtypes in home_rooms_by_type.items():
    # Bulbs: 1–2 per room
    for rlist in rtypes.values():
        for rid in rlist:
            for _ in range(random.randint(1, 2)):
                did = next_device_id()
                device, created, updated = create_device_entry(did, "bulb", rid, home_id)
                devices[did] = device
                smart_bulbs[did] = {
                    "device_id": did,
                    "brightness_level": random.choice(["dim", "half", "full"]),
                    "color": random.choice(["red", "white", "yellow", "blue"]),
                    "created_at": created.isoformat(),
                    "updated_at": updated.isoformat(),
                }

    # Thermostats: 1–2 per home, placed in lounge/bedroom
    thermo_rooms = rtypes.get("lounge", []) + rtypes.get("bedroom", [])
    for rid in random.sample(thermo_rooms, min(2, len(thermo_rooms))):
        did = next_device_id()
        device, created, updated = create_device_entry(did, "thermostat", rid, home_id)
        devices[did] = device
        smart_thermostats[did] = {
            "device_id": did,
            "current_temperature": round(random.uniform(60, 75), 1),
            "lowest_rated_temperature": 60.0,
            "highest_rated_temperature": 80.0,
            "last_adjustment_time": random_timestamp(created, now).isoformat(),
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }

    # Cameras: 1–2 in lounges
    for rid in random.sample(rtypes.get("lounge", []), min(2, len(rtypes.get("lounge", [])))):
        did = next_device_id()
        device, created, updated = create_device_entry(did, "camera", rid, home_id)
        devices[did] = device
        security_cameras[did] = {
            "device_id": did,
            "resolution": random.choice(["720p", "1080p", "2k"]),
            "last_activity_timestamp": random_timestamp(created, now).isoformat(),
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }

    # Fridge & Oven: 1–2 of each per kitchen
    for rid in rtypes.get("kitchen", []):
        for dtype in ["refrigerator", "oven"]:
            for _ in range(random.randint(1, 2)):
                did = next_device_id()
                device, _, _ = create_device_entry(did, dtype, rid, home_id)
                devices[did] = device

    # Speakers & TVs: 0–3 in bedrooms/lounges
    for rid in rtypes.get("bedroom", []) + rtypes.get("lounge", []):
        for dtype in ["speaker", "tv"]:
            for _ in range(random.randint(0, 2)):
                did = next_device_id()
                device, _, _ = create_device_entry(did, dtype, rid, home_id)
                devices[did] = device


# 6. Historical energy consumption
from dateutil.relativedelta import relativedelta

# 6. Historical energy consumption (high-energy devices, last 4 months, bi-monthly)
consumption = {}

# Allowed device types
high_energy_types = {"thermostat", "refrigerator", "oven"}

# Filter devices
target_devices = {
    did: d for did, d in devices.items()
    if d["device_type"] in high_energy_types
}

# Get date window: last 4 full months including this one
end_month = now.replace(day=1)
start_month = end_month - relativedelta(months=2)

for did, device in target_devices.items():
    hid = device["home_id"]
    rid = device["room_id"]
    installed_on = datetime.fromisoformat(device["installed_on"])

    current = max(installed_on.replace(day=1), start_month)

    while current <= end_month:
        for day in [1, 15]:
            try:
                date = current.replace(day=day)
            except ValueError:
                continue  # e.g., skip invalid Feb 30

            created = random_timestamp(date, date + timedelta(days=1))
            updated = random_timestamp(created, now)

            cid = next_id('consumption')
            consumption[cid] = {
                "consumption_id": cid,
                "device_id": did,
                "home_id": hid,
                "room_id": rid,
                "date": date.date().isoformat(),
                "power_used_kWh": round(random.uniform(2, 10), 2),
                "created_at": created.isoformat(),
                "updated_at": updated.isoformat(),
            }

        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)


routines = {}
device_commands = {}
bulb_commands = {}
thermostat_commands = {}

routine_command_map = {}  # maps routine_id to list of (device_id, device_type)

import random
from datetime import datetime, timedelta

# Generate all 15-minute interval time strings (00:00 to 23:45)
time_options = [
    (datetime.strptime("00:00", "%H:%M") + timedelta(minutes=15 * i)).strftime("%H:%M")
    for i in range(96)  # 24 hours * 4 (15-min intervals)
]

for uid, user in users.items():
    address_id = user["primary_address_id"]
    home_ids = [hid for hid, h in homes.items() if h["address_id"] == address_id]
    if not home_ids:
        continue
    hid = home_ids[0]

    num_routines = random.randint(0, 2)
    for _ in range(num_routines):

        # Find all controllable devices in the same home
        eligible_devices = []
        for did, d in devices.items():
            if d["home_id"] != hid:
                continue
            room_owner = rooms[d["room_id"]]["room_owner_id"]
            if room_owner == uid or user["role"] == "Owner":
                eligible_devices.append((did, d["device_type"], d["installed_on"]))

        if not eligible_devices:
            continue

        rid = next_id("routines")

        start_action_date = faker.date_between(start_date='-15d', end_date='+30d')
        action_time = random.choice(time_options)
        created = random_timestamp(now - timedelta(days=180), now - timedelta(days=90))
        updated = random_timestamp(created, now)

        routines[rid] = {
            "routine_id": rid,
            "user_id": uid,
            "home_id": hid,
            "start_action_date": start_action_date.isoformat(),
            "action_time": action_time,
            "action_interval": random.choice(["daily", "one_time", "every_hour"]),
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }

        used_devices = set()
        for _ in range(random.randint(1, 6)):
            did, dtype, installed_on = random.choice(eligible_devices)
            if (rid, did) in used_devices:
                continue
            used_devices.add((rid, did))

            installed_date = datetime.fromisoformat(installed_on).date()
            if start_action_date < installed_date:
                routines[rid]["start_action_date"] = installed_date.isoformat()

            command_created = random_timestamp(now - timedelta(days=60), now - timedelta(days=30))
            command_updated = random_timestamp(command_created, now)

            # 1. Device command (on/off)
            if random.random() < 0.9:
                dcid = next_id("device_commands")
                device_commands[dcid] = {
                    "device_command_id": dcid,
                    "routine_id": rid,
                    "device_id": did,
                    "status": random.choice(["on", "off"]),
                    "created_at": command_created.isoformat(),
                    "updated_at": command_updated.isoformat(),
                }

            # 2. Bulb-specific commands
            if dtype == "bulb":
                if random.random() < 0.9:
                    bcid = next_id("bulb_commands")
                    bulb_commands[bcid] = {
                        "bulb_command_id": bcid,
                        "routine_id": rid,
                        "device_id": did,
                        "brightness_level": random.choice(["dim", "half", "full"]),
                        "color": random.choice(["red", "white", "yellow", "blue"]),
                        "created_at": command_created.isoformat(),
                        "updated_at": command_updated.isoformat(),
                    }

            # 3. Thermostat-specific commands
            if dtype == "thermostat":
                if random.random() < 0.8:
                    tcid = next_id("thermostat_commands")
                    thermostat_commands[tcid] = {
                        "thermostat_command_id": tcid,
                        "routine_id": rid,
                        "device_id": did,
                        "current_temperature": round(random.uniform(65, 75), 1),
                        "created_at": command_created.isoformat(),
                        "updated_at": command_updated.isoformat(),
                    }

# 11. User feedbacks
feedbacks = {}
device_usage = {}
for entry in consumption.values():
    did = entry["device_id"]
    device_usage[did] = device_usage.get(did, 0) + entry["power_used_kWh"]

# 2. Focus on high-energy devices only
eligible_devices = sorted(device_usage.items(), key=lambda x: -x[1])
eligible_devices = [did for did, _ in eligible_devices if devices[did]["device_type"] in ["thermostat", "oven", "refrigerator"]]

# 3. Create feedbacks
feedbacks = {}
for uid, udata in users.items():
    primary_home = udata["primary_address_id"]
    owned_rooms = [rid for rid, r in rooms.items() if r["room_owner_id"] == uid]
    allowed_devices = []

    for did in eligible_devices:
        dev = devices[did]
        if dev["home_id"] == primary_home or dev["room_id"] in owned_rooms:
            allowed_devices.append(did)

    sampled_devices = random.sample(allowed_devices, min(len(allowed_devices), random.randint(1, 3)))
    for did in sampled_devices:
        fid = next_id('feedbacks')
        created = now - timedelta(days=random.randint(30, 180))
        updated = created + timedelta(days=random.randint(0, 30))
        rating = random.choices([5, 4, 3, 2, 1], weights=[40, 30, 15, 10, 5])[0]
        feedbacks[fid] = {
            "user_feedback_id": fid,
            "user_id": uid,
            "device_id": did,
            "rating": rating,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }
# 12. Emergency alerts
alerts = {}
aid_counter = 1  # for unique alert IDs
alert_map = {
    "camera": ["camera_motion_detected", "camera_offline"],
    "bulb": ["bulb_malfunction"],
    "thermostat": ["thermostat_temperature_alert", "thermostat_offline"],
    "speaker": ["speaker_offline"],
    "tv": ["tv_malfunction"],
    "refrigerator": ["refrigerator_temperature_alert", "refrigerator_malfunction"],
    "oven": ["oven_overheating", "oven_malfunction"],
}

alert_severity_distribution = {
    "low": 0.3,
    "medium": 0.35,
    "high": 0.25,
    "critical": 0.1,
}

def weighted_choice(choices):
    total = sum(choices.values())
    r = random.uniform(0, total)
    upto = 0
    for key, weight in choices.items():
        if upto + weight >= r:
            return key
        upto += weight

def get_valid_user(hid, rid):
    room_owner = rooms[rid]["room_owner_id"] if rid and rid in rooms else None
    home_users = [uid for uid, u in users.items() if u["primary_address_id"] == hid]
    if room_owner:
        return room_owner
    return random.choice(home_users) if home_users else None

from datetime import datetime, timedelta
import random

alerts = {}

# Get current time reference
now = datetime.now()

# Logic helpers
def random_timestamp(start, end):
    return faker.date_time_between(start_date=start, end_date=end)

def get_valid_user_for_device(home_id, room_id=None):
    """
    Return a valid user who can acknowledge or resolve an alert.
    - Prefer room owner > home owner > any user from the same home
    """
    valid_users = []
    if room_id and room_id in rooms:
        owner = rooms[room_id].get("room_owner_id")
        if owner:
            valid_users.append(owner)

    for uid, u in users.items():
        if u.get("primary_address_id") == homes[home_id]["address_id"]:
            valid_users.append(uid)

    # Fallback to home owner
    valid_users.append(homes[home_id]["owner_id"])
    return random.choice(valid_users)

# Device-specific alert types
alert_map = {
    "camera": ["camera_motion_detected", "camera_offline"],
    "bulb": ["bulb_malfunction"],
    "thermostat": ["thermostat_temperature_alert", "thermostat_offline"],
    "speaker": ["speaker_offline"],
    "tv": ["tv_malfunction"],
    "refrigerator": ["refrigerator_temperature_alert", "refrigerator_malfunction"],
    "oven": ["oven_overheating", "oven_malfunction"],
}

# Determine how many alerts to generate (~25% of devices)
N_ALERTS = int(len(devices) * 0.25)

for _ in range(N_ALERTS):
    aid = next_id("alerts")
    did = random.choice(list(devices.keys()))
    dtype = devices[did]["device_type"]
    hid = devices[did]["home_id"]
    rid = devices[did]["room_id"]

    # Determine alert type
    alert_type = random.choice(alert_map.get(dtype, ["system_malfunction", "power_outage"]))

    # Default triggered time
    triggered = random_timestamp(now - timedelta(days=90), now)

    # Ensure triggered_at <= last_activity_timestamp for camera_motion_detected
    if dtype == "camera" and alert_type == "camera_motion_detected":
        cam = security_cameras.get(did)
        if cam and cam.get("last_activity_timestamp"):
            last_activity = datetime.fromisoformat(cam["last_activity_timestamp"])
            triggered = random_timestamp(now - timedelta(days=90), last_activity)

    # Status flow logic
    acknowledged_at = None
    acknowledged_by = None
    resolved_at = None
    resolved_by = None

    status_roll = random.random()
    if status_roll < 0.3:
        acknowledged_by = get_valid_user_for_device(hid, rid)
        acknowledged_at = random_timestamp(triggered, now)
    elif status_roll < 0.6:
        acknowledged_by = get_valid_user_for_device(hid, rid)
        acknowledged_at = random_timestamp(triggered, now)
        resolved_by = acknowledged_by if random.random() < 0.7 else get_valid_user_for_device(hid, rid)
        resolved_at = random_timestamp(acknowledged_at, now)

    alerts[aid] = {
        "home_id": hid,
        "device_id": did,
        "alert_type": alert_type,
        "severity_level": random.choice(["low", "medium", "high", "critical"]),
        "triggered_at": triggered.isoformat(),
        "acknowledged_at": acknowledged_at.isoformat() if acknowledged_at else None,
        "acknowledged_by_user": acknowledged_by,
        "resolved_at": resolved_at.isoformat() if resolved_at else None,
        "resolved_by_user": resolved_by,
        "created_at": triggered.isoformat(),
    }

# 5. Devices Updates

from datetime import datetime, timedelta
import random

# Unresolved alert types where the device must be off
UNRESOLVED_ALERT_TYPES = {
    "camera_offline", "bulb_malfunction", "thermostat_offline",
    "speaker_offline", "tv_malfunction", "refrigerator_malfunction", "oven_malfunction"
}

for aid, alert in alerts.items():
    did = alert["device_id"]
    if did not in devices:
        continue

    device = devices[did]
    resolved_at = alert.get("resolved_at")
    acknowledged_at = alert.get("acknowledged_at")
    alert_type = alert["alert_type"]

    # Parse resolved/acknowledged times
    resolved_dt = datetime.fromisoformat(resolved_at) if resolved_at else None
    acknowledged_dt = datetime.fromisoformat(acknowledged_at) if acknowledged_at else None

    # Case 1: Unresolved alert → status off, no scheduled maintenance
    if alert_type in UNRESOLVED_ALERT_TYPES and not resolved_at and not acknowledged_at:
        device["status"] = "off"
        device["scheduled_maintainance_date"] = None
        device["last_maintainance_date"] = None
        continue

    # Case 2: Resolved alert → update last_maintainance_date to be just before resolved_at
    if resolved_dt:
        maintain_date = faker.date_between_dates(
            date_start=resolved_dt.date() - timedelta(days=3),
            date_end=resolved_dt.date()
        )
        device["last_maintainance_date"] = maintain_date.isoformat()

        # Future scheduled maintenance
        device["scheduled_maintainance_date"] = (
            datetime.now().date() + timedelta(days=random.randint(30, 180))
        ).isoformat()
        continue

    # Case 3: Acknowledged but not resolved → set last_maintainance_date to before acknowledgment
    if acknowledged_dt:
        installed_date = datetime.fromisoformat(device["installed_on"]).date()
        acknowledged_date = acknowledged_dt.date()

        if installed_date < acknowledged_date:
            maintain_date = faker.date_between_dates(
                date_start=installed_date,
                date_end=acknowledged_date
            )
        else:
            # fallback: use acknowledged_date itself if installed_on is later
            maintain_date = acknowledged_date

        device["last_maintainance_date"] = maintain_date.isoformat()
        device["scheduled_maintainance_date"] = (
            datetime.now().date() + timedelta(days=random.randint(30, 180))
        ).isoformat()
        continue


    # Case 4: All other (fallback) → keep as-is


# 13. Energy tariffs
from datetime import datetime, timedelta
import random
from faker import Faker

faker = Faker()
now = datetime.now()
tariffs = {}
tariff_names = [
    "Green Saver", "Time-of-Use", "Fixed Rate", "Flexible Plan",
    "Eco Flex", "Standard Residential", "Smart Usage Plan", "Peak Saver"
]

def generate_peak_hours():
    start_hour = random.randint(15, 19)  # 15:00–19:00
    duration = random.choice([2, 3, 4])
    end_hour = start_hour + duration
    return f"{start_hour:02}:00:00", f"{end_hour:02}:00:00"

tid_counter = 1
for hid in homes.keys():
    num_tariffs = random.randint(1, 3)
    start_date = faker.date_between(start_date='-2y', end_date='-1y')
    has_active = False

    for _ in range(num_tariffs):
        eff_from = start_date
        eff_until = faker.date_between(start_date=eff_from + timedelta(days=90), end_date=eff_from + timedelta(days=365))

        # Random chance to make one tariff active
        if not has_active and random.random() < 0.7:
            eff_until = faker.date_between(start_date=now.date(), end_date=now.date() + timedelta(days=365))
            has_active = True

        peak_start, peak_end = generate_peak_hours()
        created = faker.date_time_between(start_date=eff_from - timedelta(days=60), end_date=eff_from)
        updated = faker.date_time_between(start_date=created, end_date=now)

        tariffs[str(tid_counter)] = {
            "tariff_id": str(tid_counter),
            "home_id": hid,
            "tariff_name": random.choice(tariff_names),
            "rate_per_kWh": round(random.uniform(0.1, 0.3), 2),
            "peak_hours_start": peak_start,
            "peak_hours_end": peak_end,
            "peak_rate_multiplier": round(random.uniform(1.5, 2.2), 2),
            "effective_from": eff_from.isoformat(),
            "effective_until": eff_until.isoformat(),
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }

        tid_counter += 1
        start_date = eff_until + timedelta(days=1)  # Avoid overlap

# 14. Write to JSON files
datasets = {
    'addresses.json': addresses,
    'users.json': users,
    'homes.json': homes,
    'rooms.json': rooms,
    'devices.json': devices,
    'security_cameras.json': security_cameras,
    'smart_bulbs.json': smart_bulbs,
    'smart_thermostats.json': smart_thermostats,
    'historical_energy_consumption.json': consumption,
    'automated_routines.json': routines,
    'device_commands.json': device_commands,
    'bulb_commands.json': bulb_commands,
    'thermostat_commands.json': thermostat_commands,
    'user_feedbacks.json': feedbacks,
    'emergency_alerts.json': alerts,
    'energy_tariffs.json': tariffs,
}

for filename, data in datasets.items():
    with open(filename, 'w') as f:
        json.dump({str(k): v for k, v in data.items()}, f, indent=2)

print("Seed data generation complete!")
