

i = """**Input Data:**
- `i_start_supervisor{(0), [autonomy_armed=1, mission_already_started=0, mission_number=789]}`
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=789]}`
- `i_perception_status{(2), [true]}`
- `i_aircraft_state{(3), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=120.0]}`"""

e = {
    'i_start_supervisor': [
        "(0), [autonomy_armed=true, mission_already_started=0.88, mission_name='forest']",
        "(0), [{autonomy_armed: false, mission_already_started: 44, mission_name: 'water'}]",
        "(0), [autonomy_armed:true, mission_already_started:55.8, mission_name:'volcano']"
    ]
    # Add other ports as needed
}


test_string_1 = """### Test Case 1: Mission Already Started

#### Input Data:
- `Input Data: {"i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=1, mission_number=123]}"}`

#### Expected Outputs:
- `Expected Outputs: {}`

#### State Transition Path:
- `State Transition Path: {IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

### Test Case 2: New Mission with Autonomy Armed and Perception System Healthy

#### Input Data:
- `Input Data: {"i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=456]}", "i_perception_status{(2), [true]}", "i_aircraft_state{(3), [gps_time=0, lat=0, lon=0, alt_AGL=15, alt_MSL=100, hdg_Deg=0, vel_Kts=0]}"}`

#### Expected Outputs:
- `Expected Outputs: {"o_request_perception_status{(1), [true]}", "o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}", "o_request_aircraft_state{(3), [true]}", "o_set_mission_monitor_status{(4), [1]}", "o_update_gcs{(5), ['Starting Mission in air!', 6]}", "o_start_mission{(6), [true]}"}`

#### State Transition Path:
- `State Transition Path: {IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATUS, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`

### Test Case 3: New Mission with Autonomy Not Armed

#### Input Data:
- `Input Data: {"i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=789]}"}`

#### Expected Outputs:
- `Expected Outputs: {}`

#### State Transition Path:
- `State Transition Path: {IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

These test cases cover scenarios including a mission that has already started, a new mission with all systems go, and a new mission where autonomy is not armed, demonstrating the state machine's response to various initial conditions."""


test_string_2 = """Here are three test cases based on the state machine described in the JSON format. Each test case includes input data, expected outputs, and the state transition path. These test cases are designed to cover different paths through the state machine, including handling both true and false conditions for perception system health and autonomy armed status. 

### Test Case 1: Mission Already Started

**Input Data:**
- Input Data: `{i_start_supervisor{(0), [autonomy_armed=1, mission_already_started=1, mission_number=123]}}`

**Expected Outputs:**
- No expected outputs as there are no outputs defined for transitions in this path.

**State Transition Path:**
- State Transition Path: `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

### Test Case 2: New Mission with Healthy Perception System and Autonomy Armed

**Input Data:**
- Input Data: `{i_start_supervisor{(0), [autonomy_armed=1, mission_already_started=0, mission_number=456]}, i_perception_status{(1), [true]}, i_aircraft_state{(2), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=100.0]}}`

**Expected Outputs:**
- Expected Outputs: `{o_request_perception_status{(0), [true]}, o_update_gcs{(1), ['The perceptions system is ready for operation!', 1]}, o_request_aircraft_state{(2), [true]}, o_set_mission_monitor_status{(3), [1]}, o_start_mission{(4), [true]}}`

**State Transition Path:**
- State Transition Path: `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATUS, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`

### Test Case 3: New Mission with Non-operational Perception System

**Input Data:**
- Input Data: `{i_start_supervisor{(0), [autonomy_armed=1, mission_already_started=0, mission_number=789]}, i_perception_status{(1), [false]}}`

**Expected Outputs:**
- Expected Outputs: `{o_request_perception_status{(0), [true]}, o_update_gcs{(1), ['The perceptions system is not operational!', 6]}}`

**State Transition Path:**
- State Transition Path: `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATUS}`

Note: In Test Case 3, the state machine does not proceed beyond `REQUEST_AIRCRAFT_STATUS` because the perception system is not operational, and there's no further input provided 
to continue the state transitions."""

#good
test_string_3 = """
### Test Case 1: Mission Already Started

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=1, mission_number=123]}`

#### Expected Outputs:
- No outputs as specified in the transitions.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

### Test Case 2: Mission Not Started, Autonomy Not Armed

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=456]}`

#### Expected Outputs:
- No outputs as specified in the transitions.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

### Test Case 3: Mission Not Started, Autonomy Armed, Perception System Healthy, Aircraft Above 10 AGL

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=789]}`
- `i_perception_status{(2), [true]}`
- `i_aircraft_state{(3), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=20.0, alt_MSL=500.0, hdg_Deg=180.0, vel_Kts=100.0]}`

#### Expected Outputs:
- `o_request_perception_status{(1), [true]}`
- `o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}`
- `o_request_aircraft_state{(3), [true]}`
- `o_set_mission_monitor_status{(4), [1]}`
- `o_update_gcs{(5), ['Starting Mission in air!', 6]}`
- `o_start_mission{(6), [true]}`

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`"""


test_string_4 = """### Test Case 1: Mission Already Started

#### Input Data:
- `i_start_supervisor{(0), [1, 1, 1234]}`

#### Expected Outputs:
- No outputs as per the transitions specified.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

### Test Case 2: Mission Not Started, Autonomy Not Armed

#### Input Data:
- `i_start_supervisor{(0), [0, 0, 1234]}`

#### Expected Outputs:
- No outputs as per the transitions specified.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

### Test Case 3: Mission Not Started, Autonomy Armed, Perception System Healthy, Aircraft Height Above 10 AGL

#### Input Data:
- `i_start_supervisor{(0), [1, 0, 1234]}`
- `i_perception_status{(1), [true]}`
- `i_aircraft_state{(2), [1622550000.0, 34.0219, -118.481, 20.0, 500.0, 180.0, 250.0]}`

#### Expected Outputs:
- `o_request_perception_status{(0), [true]}`
- `o_update_gcs{(1), ['The perceptions system is ready for operation!', 1]}`
- `o_request_aircraft_state{(2), [true]}`
- `o_set_mission_monitor_status{(3), [1]}`
- `o_update_gcs{(4), ['Starting Mission in air!', 6]}`
- `o_start_mission{(5), [true]}`

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`

These test cases cover various scenarios including a mission already started, autonomy not armed, and a full mission start sequence with all systems operational and the aircraft at a sufficient height."""


test_string_5 = """### Test Case 1: Mission Already Started

**Input Data:**
- `{i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=1, mission_number=123]}}`

**Expected Outputs:**
- No outputs as per the transitions specified.

**State Transition Path:**
- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

### Test Case 2: Mission Not Started, Autonomy Not Armed

**Input Data:**
- `{i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=456]}}`

**Expected Outputs:**
- No outputs as per the transitions specified.

**State Transition Path:**
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

### Test Case 3: Full Mission Start with Perception System Healthy and Aircraft Above 10 AGL

**Input Data:**
- `{i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=789]}}`
- `{i_perception_status{(2), [true]}}`
- `{i_aircraft_state{(3), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=20.0, alt_MSL=500.0, hdg_Deg=90.0, vel_Kts=100.0]}}`

**Expected Outputs:**
- `{o_request_perception_status{(1), [true]}}`
- `{o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}}`
- `{o_request_aircraft_state{(3), [true]}}`
- `{o_set_mission_monitor_status{(4), [1]}}`
- `{o_update_gcs{(5), ['Starting Mission in air!', 6]}}`
- `{o_start_mission{(6), [true]}}`

**State Transition Path:**
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`"""


test_string_6 = """Given the state machine description, here are three test cases that cover various paths through the state machine:

### Test Case 1: Mission Already Started

**Input Data:**
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=1, mission_number=123]}`

**Expected Outputs:**
- No outputs as per the transitions specified.

**State Transition Path:**
- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

This test case checks the path where a mission has already started. Since the mission has already begun, the system transitions to `RESUME_MISSION` and then back to `IDLE` without any specific outputs.

### Test Case 2: Mission Not Started, Autonomy Not Armed

**Input Data:**
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=456]}`

**Expected Outputs:**
- No outputs as per the transitions specified.

**State Transition Path:**
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

This test case verifies the scenario where a new mission is to start, but the autonomy system is not armed. The state machine transitions to `CHECK_AUTONOMY` 
and then back to `IDLE` without any actions taken.

### Test Case 3: Mission Not Started, Autonomy Armed, Perception System Healthy, Aircraft State Received

**Input Data:**
- `i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=789]}`
- `i_perception_status{(2), [true]}`
- `i_aircraft_state{(3), [gps_time=123456.78, lat=34.5678, lon=-123.4567, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=120.0]}`

**Expected Outputs:**
- `o_request_perception_status{(1), [true]}`
- `o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}`
- `o_request_aircraft_state{(3), [true]}`
- `o_set_mission_monitor_status{(4), [1]}`
- `o_update_gcs{(5), ['Starting Mission in air!', 6]}`
- `o_start_mission{(6), [true]}`

**State Transition Path:**
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`

This test case explores the scenario where a new mission is to start, the autonomy system is armed, the perception system is healthy, and the aircraft state indicates it is ready for mission start. The state machine transitions through several states, generating outputs that request perception status, confirm the perception system's readiness, request aircraft state, set mission monitor status, and finally start the mission."""


test_string_7 = """### Test Case 1

**Objective:** Test the transition from IDLE to MISSION_STATUS and then to CHECK_AUTONOMY, followed by a transition to CHECK_PERCEPTION_SYSTEM due to the autonomy system being armed, and finally moving through to START_MISSION with a healthy perception system and valid aircraft state.

**Input Data:**

- `i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=123]}`
- `i_perception_status{(2), [true]}`
- `i_aircraft_state{(3), [gps_time=123456.78, lat=34.5678, lon=-117.678, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=120.0]}`

**Expected Outputs:**

- `o_request_perception_status{(1), [true]}`
- `o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}`
- `o_request_aircraft_state{(3), [true]}`
- `o_set_mission_monitor_status{(4), [1]}`
- `o_update_gcs{(5), ['Starting Mission in air!', 6]}`
- `o_start_mission{(6), [true]}`

**State Transition Path:**

- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`

---

### Test Case 2

**Objective:** Test the scenario where the autonomy system is not armed, leading to a transition back to IDLE without proceeding to mission start.

**Input Data:**

- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=456]}`

**Expected Outputs:**

- No outputs as the system transitions back to IDLE without any action.

**State Transition Path:**

- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

---

### Test Case 3

**Objective:** Test the resumption of an already started mission, which should lead the system to transition from IDLE to MISSION_STATUS and then directly to 
RESUME_MISSION, and finally back to IDLE.

**Input Data:**

- `i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=1, mission_number=789]}`

**Expected Outputs:**

- No outputs as the system only transitions through states without generating any specific output for this scenario.

**State Transition Path:**

- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

These test cases cover various paths through the state machine, ensuring that the system behaves as expected under different conditions."""

test_String_8 = """### Test Case 1: Mission Already Started

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=1, mission_number=123]}`

#### Expected Outputs:
- No outputs as per the transitions specified.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

---

### Test Case 2: Mission Not Started, Autonomy Not Armed

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=123]}`

#### Expected Outputs:
- No outputs as per the transitions specified.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

---

### Test Case 3: Mission Not Started, Autonomy Armed, Perception System Healthy, Aircraft State Received

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=123]}`
- `i_perception_status{(2), [true]}`
- `i_aircraft_state{(3), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=100.0]}`

#### Expected Outputs:
- `o_request_perception_status{(1), [true]}`
- `o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}`
- `o_request_aircraft_state{(3), [true]}`
- `o_set_mission_monitor_status{(4), [1]}`
- `o_update_gcs{(5), ['Starting Mission in air!', 6]}`
- `o_start_mission{(6), [true]}`

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`"""

#Parser problem FIXME:
test_string_9 = """### Test Case 1: Mission Already Started

#### Input Data:
- `Input Data: {"i_start_supervisor{(1), [{'autonomy_armed': 0, 'mission_already_started': 1, 'mission_number': 42}]}"}`

#### Expected Outputs:
- `Expected Outputs: {}`

#### State Transition Path:
- `State Transition Path: {IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

### Test Case 2: Mission Not Started, Autonomy Not Armed

#### Input Data:
- `Input Data: {"i_start_supervisor{(1), [{'autonomy_armed': 0, 'mission_already_started': 0, 'mission_number': 101}]}"}`

#### Expected Outputs:
- `Expected Outputs: {}`

#### State Transition Path:
- `State Transition Path: {IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

### Test Case 3: Mission Not Started, Autonomy Armed, Perception System Healthy, Aircraft Height Above 10

#### Input Data:
- `Input Data: {"i_start_supervisor{(1), [{'autonomy_armed': 1, 'mission_already_started': 0, 'mission_number': 202}]}, "i_perception_status{(2), [true]}, "i_aircraft_state{(3), [{'gps_time': 162342.0, 'lat': 34.0219, 'lon': -118.4814, 'alt_AGL': 15.0, 'alt_MSL': 500.0, 'hdg_Deg': 90.0, 'vel_Kts': 120.0}]}"}`

#### Expected Outputs:
- `Expected Outputs: {"o_request_perception_status{(1), [true]}, "o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}, "o_request_aircraft_state{(3), [true]}, 
"o_set_mission_monitor_status{(4), [1]}, "o_update_gcs{(5), ['Starting Mission in air!', 1]}, "o_start_mission{(6), [202]}"}`

#### State Transition Path:
- `State Transition Path: {IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`"""







