"""
System Monitor Agent - Monitors system resources and health
"""

import psutil
import platform
from typing import Dict, Any
from ..core.agent import Agent, AgentResponse


class SystemMonitorAgent(Agent):
    """Agent for monitoring system resources"""
    
    def __init__(self):
        super().__init__(
            name="system_monitor",
            description="Monitors CPU, memory, disk, and network usage"
        )
        
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        """
        Execute system monitoring task
        
        Args:
            task: Task dictionary with 'action' key
            
        Returns:
            AgentResponse with system information
        """
        action = task.get("action", "full_status")
        
        try:
            if action == "full_status":
                data = self._get_full_status()
            elif action == "cpu":
                data = self._get_cpu_info()
            elif action == "memory":
                data = self._get_memory_info()
            elif action == "disk":
                data = self._get_disk_info()
            elif action == "network":
                data = self._get_network_info()
            else:
                return AgentResponse(
                    success=False,
                    data=None,
                    message=f"Unknown action: {action}",
                    agent_name=self.name
                )
                
            return AgentResponse(
                success=True,
                data=data,
                message="System monitoring completed successfully",
                agent_name=self.name
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data=None,
                message=f"Error monitoring system: {str(e)}",
                agent_name=self.name
            )
            
    def _get_full_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            },
            "cpu": self._get_cpu_info(),
            "memory": self._get_memory_info(),
            "disk": self._get_disk_info(),
            "network": self._get_network_info(),
        }
        
    def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information"""
        return {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "count_physical": psutil.cpu_count(logical=False),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }
        
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "virtual": {
                "total": mem.total,
                "available": mem.available,
                "percent": mem.percent,
                "used": mem.used,
                "free": mem.free,
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
            }
        }
        
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information"""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })
            except PermissionError:
                # Skip partitions we can't access
                continue
                
        io = psutil.disk_io_counters()
        return {
            "partitions": partitions,
            "io": {
                "read_count": io.read_count,
                "write_count": io.write_count,
                "read_bytes": io.read_bytes,
                "write_bytes": io.write_bytes,
            } if io else None
        }
        
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        io = psutil.net_io_counters()
        return {
            "bytes_sent": io.bytes_sent,
            "bytes_recv": io.bytes_recv,
            "packets_sent": io.packets_sent,
            "packets_recv": io.packets_recv,
            "errin": io.errin,
            "errout": io.errout,
            "dropin": io.dropin,
            "dropout": io.dropout,
        }
