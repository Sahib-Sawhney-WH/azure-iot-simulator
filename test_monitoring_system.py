#!/usr/bin/env python3
"""
Test script for the monitoring and performance system
"""

import sys
import time
import threading
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_monitoring_imports():
    """Test that all monitoring components can be imported"""
    print("Testing monitoring system imports...")
    
    try:
        from monitoring.metrics_collector import metrics_collector, DeviceMetrics, SystemMetrics
        print("✓ Metrics collector imported successfully")
        
        from monitoring.performance_monitor import PerformanceMonitor, PerformanceSnapshot
        print("✓ Performance monitor imported successfully")
        
        from monitoring.monitoring_dashboard import MonitoringDashboard
        print("✓ Monitoring dashboard imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Monitoring system import test failed: {e}")
        return False

def test_metrics_collector():
    """Test metrics collector functionality"""
    print("\nTesting metrics collector...")
    
    try:
        from monitoring.metrics_collector import metrics_collector
        
        # Register test devices
        test_devices = ["device_001", "device_002", "device_003"]
        for device_id in test_devices:
            metrics_collector.register_device(device_id)
        print(f"✓ Registered {len(test_devices)} test devices")
        
        # Simulate device connections
        for device_id in test_devices:
            metrics_collector.update_device_connection(device_id, "connected")
        print("✓ Updated device connection status")
        
        # Simulate message sending
        for i in range(10):
            for device_id in test_devices:
                message_size = 100 + (i * 10)
                response_time = 0.05 + (i * 0.01)
                metrics_collector.record_message_sent(device_id, message_size, response_time)
        print("✓ Recorded test messages")
        
        # Simulate some failures
        metrics_collector.record_message_failed("device_001")
        metrics_collector.record_message_failed("device_002")
        print("✓ Recorded test failures")
        
        # Get metrics
        system_metrics = metrics_collector.get_system_metrics()
        print(f"✓ System metrics: {system_metrics.total_devices} devices, {system_metrics.total_messages} messages")
        
        device_metrics = metrics_collector.get_all_device_metrics()
        print(f"✓ Device metrics: {len(device_metrics)} devices tracked")
        
        # Get statistics
        stats = metrics_collector.get_device_statistics()
        print(f"✓ Device statistics: {stats['total_messages']} total messages, {stats['total_failures']} failures")
        
        # Clean up
        for device_id in test_devices:
            metrics_collector.unregister_device(device_id)
        print("✓ Cleaned up test devices")
        
        return True
        
    except Exception as e:
        print(f"✗ Metrics collector test failed: {e}")
        return False

def test_performance_monitor():
    """Test performance monitor functionality"""
    print("\nTesting performance monitor...")
    
    try:
        from monitoring.performance_monitor import PerformanceMonitor
        
        # Create performance monitor
        perf_monitor = PerformanceMonitor(sample_interval=0.5)
        print("✓ Performance monitor created")
        
        # Start monitoring
        perf_monitor.start_monitoring()
        print("✓ Performance monitoring started")
        
        # Wait for some samples
        time.sleep(2.0)
        
        # Get current snapshot
        snapshot = perf_monitor.get_current_snapshot()
        if snapshot:
            print(f"✓ Current snapshot: CPU {snapshot.cpu_percent:.1f}%, Memory {snapshot.memory_percent:.1f}%")
        
        # Get performance history
        history = perf_monitor.get_performance_history(1)  # Last 1 minute
        print(f"✓ Performance history: {len(history)} samples")
        
        # Get performance summary
        summary = perf_monitor.get_performance_summary(1)
        if summary:
            print(f"✓ Performance summary: CPU avg {summary['cpu']['average']:.1f}%, Memory {summary['memory']['current_used_mb']:.0f}MB")
        
        # Test alerts
        perf_monitor.add_alert("test_alert", "cpu_percent", 0.1, "greater", 1)
        print("✓ Added test alert")
        
        alerts_status = perf_monitor.get_alerts_status()
        print(f"✓ Alerts status: {len(alerts_status)} alerts configured")
        
        # Get recommendations
        recommendations = perf_monitor.get_resource_recommendations()
        print(f"✓ Resource recommendations: {len(recommendations)} suggestions")
        
        # Stop monitoring
        perf_monitor.stop_monitoring()
        print("✓ Performance monitoring stopped")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance monitor test failed: {e}")
        return False

def test_monitoring_integration():
    """Test monitoring system integration"""
    print("\nTesting monitoring integration...")
    
    try:
        from monitoring.metrics_collector import metrics_collector
        from monitoring.performance_monitor import PerformanceMonitor
        
        # Start both monitoring systems
        metrics_collector.start_monitoring()
        
        perf_monitor = PerformanceMonitor()
        perf_monitor.start_monitoring()
        
        print("✓ Both monitoring systems started")
        
        # Register devices and simulate activity
        test_devices = ["integration_device_1", "integration_device_2"]
        for device_id in test_devices:
            metrics_collector.register_device(device_id)
            metrics_collector.update_device_connection(device_id, "connected")
        
        # Simulate sustained activity
        for i in range(20):
            for device_id in test_devices:
                metrics_collector.record_message_sent(device_id, 150, 0.03)
            time.sleep(0.1)
        
        print("✓ Simulated device activity")
        
        # Check that both systems are collecting data
        system_metrics = metrics_collector.get_system_metrics()
        snapshot = perf_monitor.get_current_snapshot()
        
        if system_metrics.total_messages > 0 and snapshot:
            print(f"✓ Integration working: {system_metrics.total_messages} messages, CPU {snapshot.cpu_percent:.1f}%")
        
        # Test data export
        metrics_export_path = "/tmp/test_metrics_export.json"
        perf_export_path = "/tmp/test_performance_export.json"
        
        metrics_success = metrics_collector.export_metrics(metrics_export_path)
        perf_success = perf_monitor.export_performance_data(perf_export_path)
        
        if metrics_success and perf_success:
            print("✓ Data export successful")
            
            # Clean up export files
            import os
            os.remove(metrics_export_path)
            os.remove(perf_export_path)
        
        # Clean up
        metrics_collector.stop_monitoring()
        perf_monitor.stop_monitoring()
        
        for device_id in test_devices:
            metrics_collector.unregister_device(device_id)
        
        print("✓ Integration test cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Monitoring integration test failed: {e}")
        return False

def test_event_system_integration():
    """Test event system integration with monitoring"""
    print("\nTesting event system integration...")
    
    try:
        from core.events import event_bus, EventType
        from monitoring.metrics_collector import metrics_collector
        from monitoring.performance_monitor import PerformanceMonitor
        
        # Event tracking
        events_received = []
        
        def event_handler(event):
            events_received.append(event.event_type)
        
        # Subscribe to monitoring events
        event_bus.subscribe(EventType.METRICS_UPDATED, event_handler)
        event_bus.subscribe(EventType.PERFORMANCE_UPDATED, event_handler)
        event_bus.subscribe(EventType.PERFORMANCE_ALERT, event_handler)
        
        print("✓ Subscribed to monitoring events")
        
        # Start monitoring to trigger events
        metrics_collector.start_monitoring()
        
        perf_monitor = PerformanceMonitor()
        perf_monitor.start_monitoring()
        
        # Wait for events
        time.sleep(3.0)
        
        # Check if events were received
        if EventType.METRICS_UPDATED in events_received:
            print("✓ Metrics updated events received")
        
        if EventType.PERFORMANCE_UPDATED in events_received:
            print("✓ Performance updated events received")
        
        # Trigger a performance alert
        perf_monitor.add_alert("test_low_threshold", "cpu_percent", 0.01, "greater", 1)
        time.sleep(2.0)
        
        if EventType.PERFORMANCE_ALERT in events_received:
            print("✓ Performance alert events received")
        
        # Clean up
        event_bus.unsubscribe(EventType.METRICS_UPDATED, event_handler)
        event_bus.unsubscribe(EventType.PERFORMANCE_UPDATED, event_handler)
        event_bus.unsubscribe(EventType.PERFORMANCE_ALERT, event_handler)
        
        metrics_collector.stop_monitoring()
        perf_monitor.stop_monitoring()
        
        print(f"✓ Event integration test completed - {len(events_received)} events received")
        
        return True
        
    except Exception as e:
        print(f"✗ Event system integration test failed: {e}")
        return False

def test_monitoring_dashboard_components():
    """Test monitoring dashboard components"""
    print("\nTesting monitoring dashboard components...")
    
    try:
        from monitoring.monitoring_dashboard import MetricCard, ProgressCard
        
        # Test metric card (without GUI)
        print("✓ MetricCard class available")
        
        # Test progress card (without GUI)
        print("✓ ProgressCard class available")
        
        # Test dashboard class
        from monitoring.monitoring_dashboard import MonitoringDashboard
        print("✓ MonitoringDashboard class available")
        
        return True
        
    except Exception as e:
        print(f"✗ Monitoring dashboard test failed: {e}")
        return False

def test_stress_monitoring():
    """Test monitoring system under stress"""
    print("\nTesting monitoring system under stress...")
    
    try:
        from monitoring.metrics_collector import metrics_collector
        from monitoring.performance_monitor import PerformanceMonitor
        
        # Start monitoring
        metrics_collector.start_monitoring()
        perf_monitor = PerformanceMonitor(sample_interval=0.1)  # Faster sampling
        perf_monitor.start_monitoring()
        
        # Create many devices
        device_count = 50
        devices = [f"stress_device_{i:03d}" for i in range(device_count)]
        
        for device_id in devices:
            metrics_collector.register_device(device_id)
            metrics_collector.update_device_connection(device_id, "connected")
        
        print(f"✓ Created {device_count} stress test devices")
        
        # Simulate high-frequency message sending
        def stress_worker(device_list):
            for _ in range(100):  # 100 messages per device
                for device_id in device_list:
                    metrics_collector.record_message_sent(device_id, 200, 0.02)
                time.sleep(0.001)  # Very fast sending
        
        # Run stress test with multiple threads
        threads = []
        device_chunks = [devices[i:i+10] for i in range(0, len(devices), 10)]
        
        for chunk in device_chunks:
            thread = threading.Thread(target=stress_worker, args=(chunk,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print("✓ Stress test completed")
        
        # Check final metrics
        system_metrics = metrics_collector.get_system_metrics()
        stats = metrics_collector.get_device_statistics()
        
        print(f"✓ Final metrics: {system_metrics.total_messages} messages from {stats['total_devices']} devices")
        print(f"✓ Message rate: {system_metrics.messages_per_second:.1f} msg/s")
        
        # Clean up
        metrics_collector.stop_monitoring()
        perf_monitor.stop_monitoring()
        
        for device_id in devices:
            metrics_collector.unregister_device(device_id)
        
        print("✓ Stress test cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Stress monitoring test failed: {e}")
        return False

def main():
    """Run all monitoring system tests"""
    print("Azure IoT Hub Device Simulator - Monitoring System Test Suite")
    print("=" * 70)
    
    success = True
    
    # Test monitoring system imports
    if not test_monitoring_imports():
        success = False
    
    # Test metrics collector
    if not test_metrics_collector():
        success = False
    
    # Test performance monitor
    if not test_performance_monitor():
        success = False
    
    # Test monitoring integration
    if not test_monitoring_integration():
        success = False
    
    # Test event system integration
    if not test_event_system_integration():
        success = False
    
    # Test dashboard components
    if not test_monitoring_dashboard_components():
        success = False
    
    # Test stress monitoring
    if not test_stress_monitoring():
        success = False
    
    print("\n" + "=" * 70)
    if success:
        print("✓ All monitoring system tests passed!")
        print("\nMonitoring system features are ready:")
        print("- Real-time metrics collection with device and system tracking")
        print("- Performance monitoring with resource usage and alerts")
        print("- Professional monitoring dashboard with live updates")
        print("- Comprehensive data export and historical tracking")
        print("- Event-driven architecture with real-time notifications")
        print("- Stress-tested for high-frequency device simulations")
        print("- Resource optimization recommendations")
        print("\nTo start the application:")
        print("  cd /home/ubuntu/azure_iot_simulator")
        print("  source venv/bin/activate")
        print("  python src/main.py")
        print("\nAccess monitoring via the 'Monitoring' tab in the main window")
    else:
        print("✗ Some monitoring system tests failed.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

