"""
Test suite for weekly report functionality
Tests data retrieval and report generation
"""

import pytest
from mock_data.weekly_report import (
    get_weekly_report,
    get_department_summary,
    get_quality_metrics,
    get_financial_summary,
    get_staffing_summary,
    get_highlights,
    get_recommendations,
    get_daily_metrics,
    get_trend_data,
    get_report_metrics_only,
    get_clinical_data_only,
    get_safety_compliance_only,
    WEEKLY_REPORT
)


class TestWeeklyReport:
    """Test weekly report data retrieval"""
    
    def test_get_weekly_report(self):
        """Test getting complete weekly report"""
        report = get_weekly_report()
        
        assert report is not None
        assert 'report_id' in report
        assert 'week_start' in report
        assert 'week_end' in report
        assert 'summary' in report
        assert 'daily_metrics' in report
        assert 'department_metrics' in report
        
    def test_report_structure(self):
        """Test report has all required sections"""
        report = get_weekly_report()
        
        required_sections = [
            'summary',
            'daily_metrics',
            'department_metrics',
            'quality_metrics',
            'financial_metrics',
            'staffing_metrics',
            'highlights',
            'recommendations',
            'week_over_week_change'
        ]
        
        for section in required_sections:
            assert section in report, f"Missing section: {section}"
    
    def test_summary_metrics(self):
        """Test summary metrics are present and valid"""
        report = get_weekly_report()
        summary = report['summary']
        
        assert 'total_patients' in summary
        assert 'total_admissions' in summary
        assert 'total_discharges' in summary
        assert 'average_length_of_stay_days' in summary
        assert 'bed_occupancy_rate' in summary
        
        # Validate data types
        assert isinstance(summary['total_patients'], int)
        assert isinstance(summary['bed_occupancy_rate'], (int, float))
        assert summary['bed_occupancy_rate'] >= 0
        assert summary['bed_occupancy_rate'] <= 100
    
    def test_daily_metrics(self):
        """Test daily metrics contain 7 days"""
        report = get_weekly_report()
        daily = report['daily_metrics']
        
        assert len(daily) == 7, "Should have 7 days of data"
        
        # Check each day has required fields
        for day in daily:
            assert 'date' in day
            assert 'day' in day
            assert 'patients' in day
            assert 'admissions' in day
            assert 'discharges' in day
            assert 'emergency_visits' in day
            assert 'bed_occupancy' in day


class TestDepartmentData:
    """Test department-specific data"""
    
    def test_get_department_summary(self):
        """Test getting summary for specific department"""
        # Test valid department
        cardiology = get_department_summary('Cardiology')
        assert cardiology is not None
        assert cardiology['department'] == 'Cardiology'
        assert 'patients_seen' in cardiology
        assert 'average_wait_time_minutes' in cardiology
        
        # Test case insensitive
        emergency = get_department_summary('emergency')
        assert emergency is not None
        assert emergency['department'] == 'Emergency'
        
        # Test invalid department
        invalid = get_department_summary('NonExistent')
        assert invalid == {}
    
    def test_department_metrics_structure(self):
        """Test department metrics have required fields"""
        report = get_weekly_report()
        departments = report['department_metrics']
        
        assert len(departments) > 0
        
        for dept in departments:
            assert 'department' in dept
            assert 'patients_seen' in dept
            assert 'average_wait_time_minutes' in dept
            assert 'patient_satisfaction' in dept
            assert 'staff_utilization' in dept
            assert 'trend' in dept
            
            # Validate satisfaction score
            assert 0 <= dept['patient_satisfaction'] <= 5


class TestQualityMetrics:
    """Test quality and safety metrics"""
    
    def test_get_quality_metrics(self):
        """Test quality metrics retrieval"""
        metrics = get_quality_metrics()
        
        assert metrics is not None
        assert 'patient_satisfaction_score' in metrics
        assert 'readmission_rate' in metrics
        assert 'mortality_rate' in metrics
        assert 'infection_rate' in metrics
        assert 'medication_error_rate' in metrics
        assert 'fall_rate' in metrics
        
        # Validate ranges
        assert 0 <= metrics['patient_satisfaction_score'] <= 5
        assert metrics['readmission_rate'] >= 0
        assert metrics['mortality_rate'] >= 0
    
    def test_get_safety_compliance_only(self):
        """Test safety compliance metrics"""
        safety = get_safety_compliance_only()
        
        assert 'infection_rate' in safety
        assert 'medication_error_rate' in safety
        assert 'fall_rate' in safety
        assert 'mortality_rate' in safety
        
        # All rates should be low percentages
        assert safety['infection_rate'] < 5
        assert safety['medication_error_rate'] < 5
        assert safety['fall_rate'] < 5


class TestFinancialMetrics:
    """Test financial data"""
    
    def test_get_financial_summary(self):
        """Test financial summary retrieval"""
        financial = get_financial_summary()
        
        assert financial is not None
        assert 'total_revenue' in financial
        assert 'total_expenses' in financial
        assert 'net_income' in financial
        assert 'revenue_per_patient' in financial
        assert 'cost_per_patient' in financial
        assert 'profit_margin' in financial
        
        # Validate calculations
        assert financial['net_income'] == financial['total_revenue'] - financial['total_expenses']
        assert financial['profit_margin'] >= 0
    
    def test_financial_calculations(self):
        """Test financial metric calculations are correct"""
        financial = get_financial_summary()
        
        # Net income should equal revenue minus expenses
        calculated_net = financial['total_revenue'] - financial['total_expenses']
        assert abs(financial['net_income'] - calculated_net) < 1  # Allow for rounding
        
        # Profit margin should be percentage
        assert 0 <= financial['profit_margin'] <= 100


class TestStaffingMetrics:
    """Test staffing data"""
    
    def test_get_staffing_summary(self):
        """Test staffing summary retrieval"""
        staffing = get_staffing_summary()
        
        assert staffing is not None
        assert 'total_staff' in staffing
        assert 'nurses' in staffing
        assert 'doctors' in staffing
        assert 'support_staff' in staffing
        assert 'overtime_hours' in staffing
        assert 'sick_leave_hours' in staffing
        assert 'vacancy_rate' in staffing
        assert 'turnover_rate' in staffing
    
    def test_staffing_totals(self):
        """Test staffing totals add up correctly"""
        staffing = get_staffing_summary()
        
        # Total staff should equal sum of categories
        calculated_total = (
            staffing['nurses'] + 
            staffing['doctors'] + 
            staffing['support_staff']
        )
        assert staffing['total_staff'] == calculated_total


class TestHighlightsAndRecommendations:
    """Test highlights and recommendations"""
    
    def test_get_highlights(self):
        """Test highlights retrieval"""
        highlights = get_highlights()
        
        assert isinstance(highlights, list)
        assert len(highlights) > 0
        
        for highlight in highlights:
            assert 'type' in highlight
            assert 'title' in highlight
            assert 'description' in highlight
            assert 'impact' in highlight
            assert highlight['impact'] in ['positive', 'negative']
    
    def test_get_recommendations(self):
        """Test recommendations retrieval"""
        # Get all recommendations
        all_recs = get_recommendations()
        assert isinstance(all_recs, list)
        assert len(all_recs) > 0
        
        for rec in all_recs:
            assert 'priority' in rec
            assert 'category' in rec
            assert 'recommendation' in rec
            assert 'expected_impact' in rec
            assert rec['priority'] in ['high', 'medium', 'low']
    
    def test_get_recommendations_by_priority(self):
        """Test filtering recommendations by priority"""
        high_priority = get_recommendations(priority='high')
        assert isinstance(high_priority, list)
        assert all(rec['priority'] == 'high' for rec in high_priority)
        
        medium_priority = get_recommendations(priority='medium')
        assert all(rec['priority'] == 'medium' for rec in medium_priority)


class TestDailyMetrics:
    """Test daily metrics functionality"""
    
    def test_get_daily_metrics_with_date(self):
        """Test getting metrics for specific date"""
        report = get_weekly_report()
        first_date = report['daily_metrics'][0]['date']
        
        metrics = get_daily_metrics(date=first_date)
        assert metrics is not None
        assert metrics['date'] == first_date
        assert 'patients' in metrics
    
    def test_get_daily_metrics_without_date(self):
        """Test getting daily metrics without date returns empty"""
        metrics = get_daily_metrics()
        assert metrics == {}
    
    def test_get_daily_metrics_invalid_date(self):
        """Test getting metrics for invalid date"""
        metrics = get_daily_metrics(date='2020-01-01')
        assert metrics == {}


class TestTrendData:
    """Test trend analysis"""
    
    def test_get_trend_data(self):
        """Test trend data retrieval"""
        trends = get_trend_data()
        
        assert trends is not None
        assert 'total_patients' in trends
        assert 'admissions' in trends
        assert 'discharges' in trends
        assert 'emergency_visits' in trends
        assert 'bed_occupancy' in trends
        
        # Trends should be percentage changes
        for key, value in trends.items():
            assert isinstance(value, (int, float))


class TestSpecializedReports:
    """Test specialized report functions"""
    
    def test_get_report_metrics_only(self):
        """Test getting only summary metrics"""
        metrics = get_report_metrics_only()
        
        assert metrics is not None
        assert 'total_patients' in metrics
        assert 'total_admissions' in metrics
        assert 'bed_occupancy_rate' in metrics
        
        # Should not contain other sections
        assert 'department_metrics' not in metrics
        assert 'financial_metrics' not in metrics
    
    def test_get_clinical_data_only(self):
        """Test getting only clinical data"""
        clinical = get_clinical_data_only()
        
        assert 'quality_metrics' in clinical
        assert 'department_metrics' in clinical
        
        # Should not contain financial data
        assert 'financial_metrics' not in clinical
        assert 'staffing_metrics' not in clinical
    
    def test_get_safety_compliance_only(self):
        """Test getting only safety metrics"""
        safety = get_safety_compliance_only()
        
        assert 'infection_rate' in safety
        assert 'medication_error_rate' in safety
        assert 'fall_rate' in safety
        assert 'mortality_rate' in safety
        
        # Should only contain these specific metrics
        assert len(safety) == 4


class TestDataIntegrity:
    """Test data integrity and consistency"""
    
    def test_dates_are_sequential(self):
        """Test that daily metrics dates are sequential"""
        report = get_weekly_report()
        daily = report['daily_metrics']
        
        from datetime import datetime, timedelta
        
        for i in range(len(daily) - 1):
            current_date = datetime.strptime(daily[i]['date'], '%Y-%m-%d')
            next_date = datetime.strptime(daily[i + 1]['date'], '%Y-%m-%d')
            
            # Next date should be exactly 1 day after current
            assert (next_date - current_date).days == 1
    
    def test_week_dates_match_daily_metrics(self):
        """Test that week start/end match daily metrics"""
        report = get_weekly_report()
        
        first_day = report['daily_metrics'][0]['date']
        last_day = report['daily_metrics'][-1]['date']
        
        assert report['week_start'] == first_day
        assert report['week_end'] == last_day
    
    def test_no_negative_values(self):
        """Test that counts are non-negative"""
        report = get_weekly_report()
        
        # Check summary
        for key, value in report['summary'].items():
            if isinstance(value, (int, float)):
                assert value >= 0, f"{key} should not be negative"
        
        # Check daily metrics
        for day in report['daily_metrics']:
            assert day['patients'] >= 0
            assert day['admissions'] >= 0
            assert day['discharges'] >= 0
            assert day['emergency_visits'] >= 0


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])

# Made with Bob
