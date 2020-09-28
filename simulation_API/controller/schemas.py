from typing import Optional, List, Dict, Union
from enum import Enum
from datetime import datetime

from pydantic import BaseModel
from scipy.integrate._ivp.ivp import OdeResult
from numpy import pi, linspace

"""How to add a new system to this API?

    1)  Add Simulation in simulations module and test it. 
    2)  Add the relevant simulation to Simulations dict located in __init__
        in simulations module.
    3)  Add relevant schemas and models to schemas.py
    4)  Add relevant form entries in frontend.
    4)  Add relevant plots to _plot_solution in tasks.py –do not forget to add.
        plot_query_value for each plot.
    5)  Add frontend results HTML template to show plots.
"""


###############################################################################
################### Schemas needed in main.py and tasks.py ####################
###############################################################################

###################### Available systems for simulation #######################

# NOTE: Needs update each time a new simulation is added
class SimSystem(str, Enum):
    """List of available systems for simulation.
    
    Notes
    -----
    NOTE: This list must coincide with the dictionary list `Simulations`
    defined in __init__.py in the module simulations, otherwise the system
    won't be simulated by the backend.
    """
    HO = "Harmonic-Oscillator"
    QHO = "Quantum-Harmonic-Oscillator"
    ChenLee = "Chen-Lee-Attractor"



######################## Available Integration Methods ########################

# Enum needed to verify correct values with API
# NOTE: Update this with relevant parameters
class IntegrationMethods(str, Enum):
    """List of available integration methods"""
    RK45 = "RK45"
    RK23 = "RK23"


# Needed to generate dict used to display available integration methods in frontend
# NOTE: Needs update each time a new simulation is added. Needs to coincide
# with Integration Methods
class IntegrationMethodsFrontend(str, Enum):
    RK45 = "Runge-Kutta 5(4)"
    RK23 = "Runge-Kutta 3(2)"

# Used in frontend and generated automatically from IntegrationMethodsFrontend
integration_methods = {
    member[0]: member[1].value
        for member in IntegrationMethodsFrontend._member_map_.items()
}



###################### Frontend Simulation Form schemas #######################

# NOTE Needs update each time a new simulation is added. 
# NOTE      1) create a new pydantic class similar to HOSimForm. 
# NOTE      2) add the class to the dict `SimFormDict` defined somewhere below.
class SimForm(BaseModel):
    """Base of schema used to Request a Simulation in Frontend"""
    username: Optional[str] = "Pepito"
    t0: Optional[float] = 0.0
    tf: Optional[float] = 2 * pi
    dt: Optional[float] = pi / 10
    method: Optional[IntegrationMethods] = "RK45"


class HOSimForm(SimForm):
    """Schema used to Request Harmonic Osc. Simulation in Frontend via form"""
    sim_sys: SimSystem = SimSystem.HO.value
    ini0: Optional[float] = 1.0
    ini1: Optional[float] = 0.0
    param0: Optional[float] = 1.0
    param1: Optional[float] = 1.0


class QHOSimForm(SimForm):
    """Schema used to Request Q. Harmonic Osc. Simulation in Frontend via form"""
    pass


class ChenLeeSimForm(SimForm):
    sim_sys: SimSystem = SimSystem.ChenLee.value
    ini0: Optional[float] = 10.0
    ini1: Optional[float] = 10.0
    ini2: Optional[float] = 0.0
    param0: Optional[float] = 3.0
    param1: Optional[float] = - 5.0
    param2: Optional[float] = - 1.0



############################ Simulation Parameters ############################

# NOTE Needs update each time a new system is added (add a new class).
class HOParams(BaseModel):
    """List of parameters of the Harmonic Oscillator system"""
    m: float    # Mass
    k: float    # Force constant


class QHOParams(BaseModel):
    pass


class ChenLeeParams(BaseModel):
    a: float
    b: float
    c: float


# Maps each system to its parameters (used in backend)
# NOTE Needs update each time a new system is added
SimSystem_to_SimParams = {
    SimSystem.HO.value: HOParams,
    SimSystem.QHO.value: QHOParams,
    SimSystem.ChenLee.value: ChenLeeParams,
}

# Maps systems to pydantic schemas used in route "/simulate/{sim_system}"
# NOTE Needs update each time a new system is added (add new entry in dict).
SimFormDict = {
    SimSystem.HO.value: HOSimForm,
    SimSystem.QHO.value: QHOSimForm,
    SimSystem.ChenLee.value: ChenLeeSimForm
}

# This dicts map different conventions for simulation parameter names 
# {param_name_frontend: param_name_backend}
# NOTE Needs update each time a new system is added (add new dict with params).
params_mapping_HO = {
    "param0": "m",
    "param1": "k",
}
params_mapping_QHO = {}
params_mapping_ChenLee = {
    "param0": "a",
    "param1": "b",
    "param2": "c",
}

# This dict maps each system to its parameter change-of-convention
# dictionary defined above (used in frontend simulation request)
system_to_params_dict = {
    SimSystem.HO.value: params_mapping_HO,
    SimSystem.QHO.value: params_mapping_QHO,
    SimSystem.ChenLee.value: params_mapping_ChenLee,
}



########################## Simulation Request schema ##########################

class SimRequest(BaseModel):
    """Schema needed to request harmonic oscillator simulations
    
    Most of the attributes in this pydantic class are arguments of the
    `HarmonicOsc1D.__init__` method. See `HarmonicOsc1D` documentation
    in simulation.py to understand them. 
    """
    system: SimSystem = SimSystem.HO
    t_span: List[float] = []
    t_eval: Optional[List[float]] = []
    t_steps: Optional[int] = 0
    ini_cndtn: List[float] = []
    params: Dict[str, float]
    method: Optional[IntegrationMethods] = 'RK45'
    # The backend will assign a sim_id, so it is not necessary to provide one.
    sim_id: Optional[str] = None
    # If we implement logging, user_id will be handled by backend
    user_id: Optional[int] = 0
    username: str = "Pepito Perez"



### Simulation ID response schema when simulation is requested in frontend. ###

class SimIdResponse(BaseModel):
    """Schema for the response of a simulation request via POST to route
    "/api/simulate/{sim_sys}"
    """
    sim_id : Optional[str]
    user_id : Optional[int]
    username : Optional[str]
    sim_sys : Optional[SimSystem]
    sim_status_path : Optional[str]
    sim_pickle_path : Optional[str]
    message : Optional[str]



###### Plot Query values needed to download the plots of each simulation ######

# NOTE Needs update each time a new system is added (add a new class).
class PlotQueryValues_HO(str, Enum):
    """List of plot query values needed to download the plots via get in route
    '/api/results/{sim_id}/plot?value={plot_query_value}'
    """
    coord = "coord"
    phase = "phase"


class PlotQueryValues_QHO(str, Enum):
    pass


class PlotQueryValues_ChenLee(str, Enum):
    threeD = "threeD"
    pass


# NOTE Needs update each time a new system is added (new entry w/ name of new class)
PlotQueryValues = Union[
    PlotQueryValues_HO,
    PlotQueryValues_QHO,
    PlotQueryValues_ChenLee
]



######################### Simulation Results Schemas ##########################

class SimResults(BaseModel):
    """Results of simulation as returned by scipy.integrate.solve_ivp"""
    sim_results: OdeResult



########################### Simulation Status Schema ##########################

class SimStatus(BaseModel):
    """Schema of the status of simulations

    This pydantic model is intended to store paths of results of the simulations
    algong with some metadata. This is what the API returns when someone
    requests a simulation via /api/simulate/{system}/ with method=post.
    
    Atributes
    ---------
    sim_id : int
        ID number of simulation.
    user_id : int
        User id number stored in database.
    date : datetime
        Late of request of simulation
    system : SimSystem
        Simulated system
    route_pickle : str
        Route of pickle file generated by the simulation backend.
    route_results : str
        Route of frontend showing results.
    route_plot : list
        Route of plots generated by the simulation backend.
    plot_query_values : list of strings
        Query params values of different automatically generated plots.
        These values are needed to download the plots. 
    success : bool
        Success status of simulation.
    message : str
        Additional information on status of simulation.
    """
    # User-related attributes
    sim_id: str
    user_id : int
    date: datetime

    # Simulation-related attributes
    system: SimSystem
    ini_cndtn: Optional[List[float]]
    params: Optional[Dict[str, float]]
    method: Optional[IntegrationMethods]

    # Response-related attributes
    route_pickle: Optional[str]
    route_results: Optional[str]
    route_plots: Optional[str]
    plot_query_values: Optional[List[PlotQueryValues]]
    plot_query_receipe: Optional[str] = \
        "'route_plots' + '?value=' + 'plot_query_value'"
    success : bool
    message : Optional[str]



########## Plot Captions shown in forntend, depending on the system. ##########

# NOTE Needs update each time a new system is added (add a new class).
class PlotCaptions_HO(str, Enum):
    coord = "Canoniacl Coordinates"
    phase = "Phase Space"


class PlotCaptions_QHO(str, Enum):
    pass


class PlotCaptions_ChenLee(str, Enum):
    threeD = "3D Phase Space Plot"



###############################################################################
################### Schemas needed for databse interaction ####################
###############################################################################

############################ Users ############################
class UserDBSchBase(BaseModel):
    username: Optional[str]


class UserDBSch(UserDBSchBase):
    user_id : Optional[int]
    # This is needed to include (when reading) database relations created by ORM in sqlalchemy  
    # Read more in FastAPI docs: https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode   
    class Config:
        orm_model = True


class UserDBSchCreate(BaseModel):
    # Just for now store Null hash TODO TODO TODO change when logging
    # Production username and hash_value must be mandatory
    username : str
    hash_value: Optional[str]
    pass


############################ Simulation status ############################
class SimulationDBSchBase(BaseModel):
    sim_id: Optional[str]
    user_id: Optional[int]
    date: Optional[str]
    system: Optional[str]
    method: Optional[str]
    route_pickle: Optional[str]
    route_results: Optional[str]
    route_plots: Optional[str]
    success: Optional[bool]
    message: Optional[str]


class SimulationDBSch(SimulationDBSchBase):
    # This is needed to include (when reading) database relations created by ORM in sqlalchemy  
    # Read more in FastAPI docs: https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode   
    class Config:
        orm_model = True


class SimulationDBSchCreate(SimulationDBSchBase):
    sim_id: str
    user_id: int
    date: str
    system: str
    success: bool
    

############################ Plots ############################
class PlotDBSchBase(BaseModel):
    sim_id: Optional[str]
    plot_query_value: Optional[str]


class PlotDBSch(PlotDBSchBase):
    plot_id: Optional[int]
    # This is needed to include (when reading) database relations created by ORM in sqlalchemy  
    # Read more in FastAPI docs: https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode   
    class Config:
        orm_model = True


class PlotDBSchCreate(PlotDBSchBase):
    sim_id: str
    plot_query_value: str


############################ Parameters ############################
class ParamType(str, Enum):
    ini_cndtn = "initial condition"
    param = "parameter"


class ParameterDBSchBase(BaseModel):
    sim_id: Optional[str]
    param_type: Optional[ParamType]
    param_key: Optional[str]
    ini_cndtn_id: Optional[int]
    value: Optional[float]


class ParameterDBSch(ParameterDBSchBase):
    param_id: Optional[int]
    # This is needed to include (when reading) database relations created by ORM in sqlalchemy  
    # Read more in FastAPI docs: https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode   
    class Config:
        orm_model = True


class ParameterDBSchCreate(ParameterDBSchBase):
    sim_id: str
    param_type: ParamType
    value: float




###############################################################################
################################ Some Messages ################################
###############################################################################

na_message = "Simulation of the system you requested is not available."
sim_id_not_found_message = "The simulation ID (sim_id) you provided is not " \
                           "in our database. If you are sure about the " \
                           "sim_id you provided, there was an internal " \
                           "server error, please request your simulation again."
sim_status_finished_message = "Finished. You can request via GET: download " \
                              "simulation results (pickle) in route given " \
                              "in 'route_pickle', or; download plots of " \
                              "simulation in route 'route_plots' using " \
                              "query params the ones given in " \
                              "'plot_query_values', or; see results online " \
                              "in route 'route_results'."
