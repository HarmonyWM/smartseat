"""
TDD Tests for SAS Allocation Service
Derivco Graduate Programme Assessment
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.storage import Storage
from services.allocation_service import SASAllocationService


class TestSASAllocationService:
    """Test suite for allocation service - All hard constraints"""
    
    @pytest.fixture
    def setup(self):
        """Setup fresh storage and service before each test"""
        storage = Storage()
        storage.reset_allocations()
        service = SASAllocationService(storage)
        return storage, service
    
    # ============ TEST: Constraint 1 - Session Capacity (Max 20) ============
    
    def test_session_capacity_constraint(self, setup):
        """UC2: Prevent session overbooking - Max 20 participants per session"""
        storage, service = setup
        
        # Fill morning session to capacity (20 participants)
        for i in range(1, 21):
            result = service.assign_participant(
                str(i), f"Test_{i}", 'A', 'morning'
            )
            assert result['success'] is True
        
        # Try to add 21st participant - SHOULD FAIL
        result = service.assign_participant(
            '21', 'Test_21', 'A', 'morning'
        )
        assert result['success'] is False
        assert 'SESSION FULL' in result['message'] or 'capacity' in result['message'].lower()
    
    # ============ TEST: Constraint 2 - No Duplicate Assignments ============
    
    def test_no_duplicate_constraint(self, setup):
        """UC3: Prevent duplicate assignment - One session per participant"""
        storage, service = setup
        
        # First assignment - should succeed
        result1 = service.assign_participant('1', 'Employee_1', 'A', 'morning')
        assert result1['success'] is True
        
        # Second assignment for same participant - SHOULD FAIL
        result2 = service.assign_participant('1', 'Employee_1', 'A', 'afternoon')
        assert result2['success'] is False
        assert 'DUPLICATE' in result2['message'] or 'already assigned' in result2['message'].lower()
    
    # ============ TEST: Constraint 3 - Department Limits ============
    
    def test_department_limit_constraint_a(self, setup):
        """UC4: Enforce department limit - Division A max 8 per session"""
        storage, service = setup
        
        # Add 8 Division A participants to morning session
        for i in range(1, 9):
            result = service.assign_participant(str(i), f"DivA_{i}", 'A', 'morning')
            assert result['success'] is True
        
        # Try to add 9th Division A - SHOULD FAIL
        result = service.assign_participant('9', 'DivA_9', 'A', 'morning')
        assert result['success'] is False
        assert 'DEPT LIMIT' in result['message'] or 'limit' in result['message'].lower()
    
    def test_department_limit_constraint_b(self, setup):
        """UC4: Enforce department limit - Division B max 8 per session"""
        storage, service = setup
        
        for i in range(25, 33):
            result = service.assign_participant(str(i), f"DivB_{i}", 'B', 'morning')
            assert result['success'] is True
        
        result = service.assign_participant('33', 'DivB_33', 'B', 'morning')
        assert result['success'] is False
    
    def test_department_limit_constraint_c(self, setup):
        """UC4: Enforce department limit - Division C max 6 per session"""
        storage, service = setup
        
        for i in range(43, 49):
            result = service.assign_participant(str(i), f"DivC_{i}", 'C', 'morning')
            assert result['success'] is True
        
        result = service.assign_participant('49', 'DivC_49', 'C', 'morning')
        assert result['success'] is False
    
    # ============ TEST: Successful Allocation ============
    
    def test_successful_allocation(self, setup):
        """UC1: Assign participant to session successfully"""
        storage, service = setup
        
        result = service.assign_participant('1', 'John Doe', 'A', 'morning')
        assert result['success'] is True
        assert 'SUCCESS' in result['message']
        assert result['allocation']['participant_id'] == '1'
        assert result['allocation']['department'] == 'A'
    
    # ============ TEST: Available Seats Display ============
    
    def test_available_seats_display(self, setup):
        """UC5: View available seats"""
        storage, service = setup
        
        # Get initial available seats
        session = storage.get_session('morning')
        initial_available = session.available_seats
        assert initial_available == 20
        
        # Add a participant
        service.assign_participant('1', 'Test', 'A', 'morning')
        
        # Check available seats decreased
        session = storage.get_session('morning')
        assert session.available_seats == 19
    
    # ============ TEST: Invalid Participant ID ============
    
    def test_invalid_participant_id(self, setup):
        """Test error handling for non-existent participant"""
        storage, service = setup
        
        result = service.assign_participant('999', 'Invalid', 'A', 'morning')
        assert result['success'] is False
        assert 'NOT FOUND' in result['message'] or 'does not exist' in result['message']
    
    # ============ TEST: Invalid Session ============
    
    def test_invalid_session(self, setup):
        """Test error handling for non-existent session"""
        storage, service = setup
        
        result = service.assign_participant('1', 'Test', 'A', 'invalid_session')
        assert result['success'] is False
        assert 'INVALID SESSION' in result['message']
    
    # ============ TEST: Invalid Department ============
    
    def test_invalid_department(self, setup):
        """Test error handling for invalid department"""
        storage, service = setup
        
        result = service.assign_participant('1', 'Test', 'Z', 'morning')
        assert result['success'] is False
        assert 'INVALID DEPT' in result['message']
    
    # ============ TEST: Bulk Allocation ============
    
    def test_bulk_allocation(self, setup):
        """Test bulk allocation functionality"""
        storage, service = setup
        
        allocations = [
            {'participant_id': '1', 'participant_name': 'User1', 'department': 'A', 'session_id': 'morning'},
            {'participant_id': '2', 'participant_name': 'User2', 'department': 'B', 'session_id': 'morning'},
            {'participant_id': '3', 'participant_name': 'User3', 'department': 'C', 'session_id': 'morning'},
        ]
        
        result = service.bulk_allocate(allocations)
        assert result['total_success'] == 3
        assert result['total_failed'] == 0
    
    # ============ TEST: Allocation Report ============
    
    def test_allocation_report(self, setup):
        """Test allocation report generation"""
        storage, service = setup
        
        # Add some allocations
        service.assign_participant('1', 'User1', 'A', 'morning')
        service.assign_participant('25', 'User25', 'B', 'midday')
        
        report = service.get_allocation_report()
        
        assert 'summary' in report
        assert 'sessions' in report
        assert report['summary']['total_allocated'] == 2
    
    # ============ TEST: Reset Functionality ============
    
    def test_reset_allocations(self, setup):
        """Test resetting all allocations"""
        storage, service = setup
        
        service.assign_participant('1', 'User1', 'A', 'morning')
        assert len(storage.get_allocations()) == 1
        
        storage.reset_allocations()
        assert len(storage.get_allocations()) == 0
        
        # Verify session counters reset
        session = storage.get_session('morning')
        assert session.current_count == 0


class TestSASValidationService:
    """Test validation service directly"""
    
    @pytest.fixture
    def setup(self):
        storage = Storage()
        storage.reset_allocations()
        return storage
    
    def test_validation_pipeline_order(self, setup):
        """Test that validation stops at first failure"""
        from services.validation_service import SASValidationService
        
        # Invalid department should fail first (fastest check)
        is_valid, msg, _, _ = SASValidationService.validate_all_allocation(
            '1', 'Z', 'morning', setup
        )
        assert is_valid is False
        assert 'INVALID DEPT' in msg


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])