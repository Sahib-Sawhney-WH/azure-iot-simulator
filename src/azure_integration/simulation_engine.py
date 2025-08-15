"""
Simulation engine for Azure IoT Hub Device Simulator
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from core.logging_config import get_logger
from core.events import EventMixin, EventType
from .device_client import VirtualDevice, DeviceConfig
from .message_generator import MessageGenerator

logger = get_logger('simulation_engine')


@dataclass
class SimulationConfig:
    """Simulation configuration"""
    interval: int = 10  # seconds between messages
    jitter: float = 0.1  # random variation (0.0 to 1.0)
    burst_mode: bool = False
    burst_count: int = 5
    burst_interval: int = 1
    max_messages: Optional[int] = None


class DeviceSimulation(EventMixin):
    """Individual device simulation"""
    
    def __init__(self, device: VirtualDevice, config: SimulationConfig):
        super().__init__()
        self.device = device
        self.config = config
        self.is_running = False
        self.message_count = 0
        self.start_time: Optional[datetime] = None
        self.message_generator = MessageGenerator()
        self._simulation_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the simulation"""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        self.device.is_simulating = True
        
        # Start simulation task
        self._simulation_task = asyncio.create_task(self._simulation_loop())
        
        self.emit_event(EventType.SIMULATION_STARTED, {
            "device_id": self.device.config.device_id
        })
        
        logger.info(f"Started simulation for device: {self.device.config.device_id}")
    
    async def stop(self):
        """Stop the simulation"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.device.is_simulating = False
        
        # Cancel simulation task
        if self._simulation_task:
            self._simulation_task.cancel()
            try:
                await self._simulation_task
            except asyncio.CancelledError:
                pass
        
        self.emit_event(EventType.SIMULATION_STOPPED, {
            "device_id": self.device.config.device_id
        })
        
        logger.info(f"Stopped simulation for device: {self.device.config.device_id}")
    
    async def _simulation_loop(self):
        """Main simulation loop"""
        try:
            while self.is_running:
                # Check message limit
                if self.config.max_messages and self.message_count >= self.config.max_messages:
                    logger.info(f"Device {self.device.config.device_id} reached message limit")
                    break
                
                # Send message(s)
                if self.config.burst_mode:
                    await self._send_burst_messages()
                else:
                    await self._send_single_message()
                
                # Calculate next interval with jitter
                base_interval = self.config.interval
                if self.config.jitter > 0:
                    jitter_amount = base_interval * self.config.jitter
                    interval = base_interval + random.uniform(-jitter_amount, jitter_amount)
                else:
                    interval = base_interval
                
                # Wait for next iteration
                await asyncio.sleep(max(0.1, interval))
        
        except asyncio.CancelledError:
            logger.debug(f"Simulation cancelled for device: {self.device.config.device_id}")
        except Exception as e:
            logger.error(f"Error in simulation loop for device {self.device.config.device_id}: {e}")
        finally:
            self.is_running = False
            self.device.is_simulating = False
    
    async def _send_single_message(self):
        """Send a single message"""
        message = self.message_generator.generate_message(self.device.config.template_name)
        if message:
            success = await self.device.send_message(message)
            if success:
                self.message_count += 1
    
    async def _send_burst_messages(self):
        """Send a burst of messages"""
        for i in range(self.config.burst_count):
            message = self.message_generator.generate_message(self.device.config.template_name)
            if message:
                success = await self.device.send_message(message)
                if success:
                    self.message_count += 1
            
            # Small delay between burst messages
            if i < self.config.burst_count - 1:
                await asyncio.sleep(self.config.burst_interval)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get simulation statistics"""
        runtime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            "device_id": self.device.config.device_id,
            "is_running": self.is_running,
            "message_count": self.message_count,
            "runtime_seconds": runtime,
            "messages_per_minute": (self.message_count / runtime * 60) if runtime > 0 else 0,
            "start_time": self.start_time.isoformat() if self.start_time else None
        }


class SimulationEngine(EventMixin):
    """Manages multiple device simulations"""
    
    def __init__(self):
        super().__init__()
        self.simulations: Dict[str, DeviceSimulation] = {}
        self.is_running = False
    
    def add_device_simulation(self, device: VirtualDevice, config: SimulationConfig):
        """Add a device simulation"""
        simulation = DeviceSimulation(device, config)
        self.simulations[device.config.device_id] = simulation
        
        logger.info(f"Added simulation for device: {device.config.device_id}")
    
    def remove_device_simulation(self, device_id: str):
        """Remove a device simulation"""
        if device_id in self.simulations:
            simulation = self.simulations[device_id]
            if simulation.is_running:
                asyncio.create_task(simulation.stop())
            
            del self.simulations[device_id]
            logger.info(f"Removed simulation for device: {device_id}")
    
    async def start_all(self):
        """Start all simulations"""
        self.is_running = True
        
        tasks = []
        for simulation in self.simulations.values():
            tasks.append(simulation.start())
        
        if tasks:
            await asyncio.gather(*tasks)
        
        self.emit_event(EventType.SIMULATION_STARTED, {
            "device_count": len(self.simulations)
        })
        
        logger.info(f"Started {len(self.simulations)} device simulations")
    
    async def stop_all(self):
        """Stop all simulations"""
        self.is_running = False
        
        tasks = []
        for simulation in self.simulations.values():
            if simulation.is_running:
                tasks.append(simulation.stop())
        
        if tasks:
            await asyncio.gather(*tasks)
        
        self.emit_event(EventType.SIMULATION_STOPPED, {
            "device_count": len(self.simulations)
        })
        
        logger.info(f"Stopped {len(self.simulations)} device simulations")
    
    async def start_device(self, device_id: str):
        """Start simulation for a specific device"""
        if device_id in self.simulations:
            await self.simulations[device_id].start()
    
    async def stop_device(self, device_id: str):
        """Stop simulation for a specific device"""
        if device_id in self.simulations:
            await self.simulations[device_id].stop()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall simulation statistics"""
        total_devices = len(self.simulations)
        running_devices = sum(1 for s in self.simulations.values() if s.is_running)
        total_messages = sum(s.message_count for s in self.simulations.values())
        
        device_stats = {}
        for device_id, simulation in self.simulations.items():
            device_stats[device_id] = simulation.get_statistics()
        
        return {
            "total_devices": total_devices,
            "running_devices": running_devices,
            "total_messages": total_messages,
            "engine_running": self.is_running,
            "device_statistics": device_stats
        }
