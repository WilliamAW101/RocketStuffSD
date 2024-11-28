#FOUR MAIN CLASSES
#1. ENVIROMENT - weather stuff
#2. MOTOR - solid, hybrid, and liquid.
#3. ROCKET - rocket data
#4. FLIGHT - simulation

from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime

#define an enviroment object, this will store variables such as wind conditions
# and weather.
env = Environment(latitude=-81.200059, longitude=28.6024274, elevation=28)
#location is University of Central Florida

#give date of simulation, provided in a tuple
tommorow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date((tommorow.year, tommorow.month, tommorow.day, 12)) #Hour give in UTC time

#set the atmostpheric model to be used
env.set_atmospheric_model(type="Forecast", file="GFS")

env.info()

#defining motor, will need to fill in the paremeters later when I get info
#these parameters are for the Pro75M1670 motor
Pro75M1670 = SolidMotor(
    thrust_source="example.csv", #usually takes in a CSV file
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

Pro75M1670.info()

# Defining a Rocket

# To create a complete Rocket object, we need to complete some steps:

#   Define the rocket itself by passing in the rocket’s dry mass, inertia, drag coefficient and radius;

#   Add a motor;

#   Add, if desired, aerodynamic surfaces;

#   Add, if desired, parachutes;

#   Set, if desired, rail guides;

#   See results.


#creating a rocket object
sdRocket = Rocket (
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="offDragExample.csv",
    power_on_drag="onDragExample.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

#add the motor to the rocket class
sdRocket.add_motor(Pro75M1670, position=-1.25)

#REST OF THESE ARE OPTIONAL

rail_buttons = sdRocket.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

nose_cone = sdRocket.add_nose( #gives nose
    length=0.55829, kind="von karman", position=1.278
)

fin_set = sdRocket.add_trapezoidal_fins( #gives four fins
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=("airfoilExp.txt","radians"),
)

tail = sdRocket.add_tail( #gives a tail
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

#add parachute
main = sdRocket.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,      # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = sdRocket.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

sdRocket.plots.static_margin()

sdRocket.draw()

#simulation

#creating flight object
test_flight = Flight(
    rocket=sdRocket, environment=env, rail_length=5.2, inclination=85, heading=0
)


test_flight.prints.initial_conditions()
test_flight.prints.surface_wind_conditions()
test_flight.prints.launch_rail_conditions()


test_flight.prints.out_of_rail_conditions()
test_flight.prints.burn_out_conditions()
test_flight.prints.apogee_conditions()


test_flight.prints.events_registered()
test_flight.prints.impact_conditions()


test_flight.prints.maximum_values()



test_flight.plots.trajectory_3d()
test_flight.plots.linear_kinematics_data()
test_flight.plots.flight_path_angle_data()
test_flight.plots.attitude_data()
test_flight.plots.angular_kinematics_data()
test_flight.plots.aerodynamic_forces()
test_flight.plots.rail_buttons_forces()
test_flight.plots.energy_data()
test_flight.plots.fluid_mechanics_data()
test_flight.plots.stability_and_control_data()

test_flight.export_kml(
    file_name="trajectory.kml",
    extrude=True,
    altitude_mode="relative_to_ground",
)