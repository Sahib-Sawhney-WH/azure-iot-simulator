"""Scenario manager for complex simulation scenarios"""
from typing import Dict, List, Any
from dataclasses import dataclass
from core.logging_config import get_logger

logger = get_logger('scenario_manager')

@dataclass
class SimulationScenario:
    name: str
    description: str
    devices: List[Dict[str, Any]]
    duration_minutes: int
    message_patterns: Dict[str, Any]

class ScenarioManager:
    def __init__(self):
        self.scenarios: Dict[str, SimulationScenario] = {}
        self._create_builtin_scenarios()
    
    def _create_builtin_scenarios(self):
        """Create built-in simulation scenarios"""
        # Smart building scenario
        smart_building = SimulationScenario(
            name="Smart Building",
            description="Simulate a smart building with various sensors",
            devices=[
                {"type": "temperature_sensor", "count": 10, "locations": ["floor_1", "floor_2"]},
                {"type": "motion_sensor", "count": 20, "locations": ["entrances", "corridors"]},
                {"type": "industrial_sensor", "count": 5, "locations": ["hvac_system"]}
            ],
            duration_minutes=60,
            message_patterns={"interval": 30, "jitter": 0.2}
        )
        self.scenarios["smart_building"] = smart_building
        
        # IoT Fleet scenario
        iot_fleet = SimulationScenario(
            name="IoT Fleet",
            description="Simulate a fleet of mobile IoT devices",
            devices=[
                {"type": "gps_tracker", "count": 50, "mobility": "high"},
                {"type": "temperature_sensor", "count": 50, "mobility": "high"}
            ],
            duration_minutes=120,
            message_patterns={"interval": 10, "burst_mode": True}
        )
        self.scenarios["iot_fleet"] = iot_fleet
        
        logger.info(f"Created {len(self.scenarios)} built-in scenarios")
    
    def get_scenario(self, name: str) -> SimulationScenario:
        return self.scenarios.get(name)
    
    def list_scenarios(self) -> List[str]:
        return list(self.scenarios.keys())
    
    def create_devices_from_scenario(self, scenario_name: str) -> List[Dict[str, Any]]:
        """Create device configurations from scenario"""
        scenario = self.get_scenario(scenario_name)
        if not scenario:
            return []
        
        device_configs = []
        device_counter = 1
        
        for device_spec in scenario.devices:
            device_type = device_spec["type"]
            count = device_spec["count"]
            
            for i in range(count):
                device_config = {
                    "device_id": f"{scenario_name}_{device_type}_{device_counter:03d}",
                    "device_name": f"{device_type.replace('_', ' ').title()} {device_counter}",
                    "device_type": device_type.replace('_', ' ').title(),
                    "template_name": device_type,
                    "message_interval": scenario.message_patterns.get("interval", 10),
                    "jitter_percent": int(scenario.message_patterns.get("jitter", 0.1) * 100),
                    "burst_mode": scenario.message_patterns.get("burst_mode", False),
                    "scenario": scenario_name
                }
                device_configs.append(device_config)
                device_counter += 1
        
        logger.info(f"Created {len(device_configs)} device configurations from scenario: {scenario_name}")
        return device_configs
