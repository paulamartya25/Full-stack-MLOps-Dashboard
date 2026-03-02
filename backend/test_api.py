#!/usr/bin/env python
"""Comprehensive API Test Suite for Factory Dashboard"""

import sys
from main import app
from fastapi.testclient import TestClient

def main():
    client = TestClient(app)
    
    print("=" * 60)
    print("FACTORY DASHBOARD API TEST SUITE")
    print("=" * 60)
    print()
    
    # Test 1: Health Check
    print("TEST 1: Health Check")
    print("-" * 60)
    try:
        response = client.get('/health')
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 2: Get Metrics
    print("TEST 2: Get Metrics")
    print("-" * 60)
    try:
        response = client.get('/metrics')
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Factory total production: {data['factory']['total_production_count']} units")
            print(f"   Workers: {len(data['workers'])}")
            print(f"   Workstations: {len(data['workstations'])}")
            print(f"   Average utilization: {data['factory']['average_utilization']}%")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 3: Post AI Event (working)
    print("TEST 3: Post AI Event (Type: working)")
    print("-" * 60)
    try:
        event = {
            'timestamp': '2026-03-02T10:00:00Z',
            'worker_id': 1,
            'station_id': 1,
            'event_type': 'working',
            'confidence': 0.95,
            'count': 0,
            'notes': 'Worker started working'
        }
        response = client.post('/events', json=event)
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 4: Post AI Event (product_count)
    print("TEST 4: Post AI Event (Type: product_count)")
    print("-" * 60)
    try:
        event = {
            'timestamp': '2026-03-02T10:05:00Z',
            'worker_id': 1,
            'station_id': 1,
            'event_type': 'product_count',
            'confidence': 0.98,
            'count': 5,
            'notes': 'Produced 5 units'
        }
        response = client.post('/events', json=event)
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 5: Duplicate Detection
    print("TEST 5: Duplicate Detection (post same event again)")
    print("-" * 60)
    try:
        event = {
            'timestamp': '2026-03-02T10:05:00Z',
            'worker_id': 1,
            'station_id': 1,
            'event_type': 'product_count',
            'confidence': 0.98,
            'count': 5,
            'notes': 'Produced 5 units'
        }
        response = client.post('/events', json=event)
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        if result.get('success') == False and 'Duplicate' in result.get('message', ''):
            print(f"   ✅ Duplicate detection working!")
        else:
            print(f"   ⚠️ Duplicate might not be detected")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 6: Get Events
    print("TEST 6: Get Events with Filtering")
    print("-" * 60)
    try:
        response = client.get('/events')
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Total events: {data.get('total_count', 0)}")
        print(f"   Events: {len(data.get('events', []))}")
        if data.get('events'):
            print(f"   Latest event: {data['events'][-1]['event_type']}")
        
        # Filter by worker
        response = client.get('/events?worker_id=1')
        data = response.json()
        print(f"   Events for worker 1: {data.get('total_count', 0)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 7: Get Workers
    print("TEST 7: Get All Workers")
    print("-" * 60)
    try:
        response = client.get('/workers')
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        workers = data.get('workers', [])
        print(f"   Total workers: {len(workers)}")
        for i, w in enumerate(workers[:3], 1):
            print(f"   {i}. {w['name']} (Worker {w['worker_id']})")
            print(f"      Units: {w['units_produced']}, Utilization: {w['utilization']}%")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 8: Get Workstations
    print("TEST 8: Get All Workstations")
    print("-" * 60)
    try:
        response = client.get('/workstations')
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        stations = data.get('workstations', [])
        print(f"   Total workstations: {len(stations)}")
        for i, s in enumerate(stations[:3], 1):
            print(f"   {i}. {s['name']} (Station {s['station_id']})")
            print(f"      Throughput: {s['throughput_rate']} u/h, Utilization: {s['utilization']}%")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 9: Get Specific Worker
    print("TEST 9: Get Specific Worker")
    print("-" * 60)
    try:
        response = client.get('/workers/1')
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Worker: {data.get('name', 'N/A')}")
        print(f"   Shift: {data.get('shift', 'N/A')}")
        print(f"   Active time: {data.get('active_time', 0)}s")
        print(f"   Units produced: {data.get('units_produced', 0)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 10: Get Specific Workstation
    print("TEST 10: Get Specific Workstation")
    print("-" * 60)
    try:
        response = client.get('/workstations/1')
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Workstation: {data.get('name', 'N/A')}")
        print(f"   Type: {data.get('type', 'N/A')}")
        print(f"   Occupancy: {data.get('occupancy_time', 0)}s")
        print(f"   Throughput: {data.get('throughput_rate', 0)} u/h")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 11: Invalid Worker
    print("TEST 11: Edge Case - Invalid Worker ID")
    print("-" * 60)
    try:
        event = {
            'timestamp': '2026-03-02T10:10:00Z',
            'worker_id': 999,  # Invalid
            'station_id': 1,
            'event_type': 'working',
            'confidence': 0.95,
            'count': 0,
            'notes': 'Test'
        }
        response = client.post('/events', json=event)
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        if result.get('success') == False:
            print(f"   ✅ Correctly rejected invalid worker")
            print(f"   Message: {result.get('message', 'N/A')}")
        else:
            print(f"   ⚠️ Should have rejected invalid worker")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # Test 12: Invalid Station
    print("TEST 12: Edge Case - Invalid Station ID")
    print("-" * 60)
    try:
        event = {
            'timestamp': '2026-03-02T10:15:00Z',
            'worker_id': 1,
            'station_id': 999,  # Invalid
            'event_type': 'working',
            'confidence': 0.95,
            'count': 0,
            'notes': 'Test'
        }
        response = client.post('/events', json=event)
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        if result.get('success') == False:
            print(f"   ✅ Correctly rejected invalid station")
            print(f"   Message: {result.get('message', 'N/A')}")
        else:
            print(f"   ⚠️ Should have rejected invalid station")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)

if __name__ == '__main__':
    main()
