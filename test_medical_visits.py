"""Unit tests for the medical visits tracking system."""

import unittest
from datetime import date

from medical_visits import MedicalVisit, MedicalVisitTracker, Patient


class TestPatientOperations(unittest.TestCase):
    def setUp(self):
        self.tracker = MedicalVisitTracker()

    def test_add_patient_returns_patient(self):
        patient = self.tracker.add_patient(
            name="Alice Smith",
            date_of_birth=date(1985, 6, 15),
            contact_number="555-0100",
        )
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.name, "Alice Smith")
        self.assertEqual(patient.date_of_birth, date(1985, 6, 15))
        self.assertEqual(patient.contact_number, "555-0100")
        self.assertEqual(patient.patient_id, 1)

    def test_add_multiple_patients_increments_ids(self):
        p1 = self.tracker.add_patient("Alice", date(1985, 1, 1), "555-0001")
        p2 = self.tracker.add_patient("Bob", date(1990, 2, 2), "555-0002")
        self.assertEqual(p1.patient_id, 1)
        self.assertEqual(p2.patient_id, 2)

    def test_get_patient_exists(self):
        added = self.tracker.add_patient("Alice", date(1985, 1, 1), "555-0001")
        fetched = self.tracker.get_patient(added.patient_id)
        self.assertEqual(fetched, added)

    def test_get_patient_not_found(self):
        self.assertIsNone(self.tracker.get_patient(999))

    def test_list_patients(self):
        self.tracker.add_patient("Alice", date(1985, 1, 1), "555-0001")
        self.tracker.add_patient("Bob", date(1990, 2, 2), "555-0002")
        patients = self.tracker.list_patients()
        self.assertEqual(len(patients), 2)

    def test_update_patient(self):
        patient = self.tracker.add_patient("Alice", date(1985, 1, 1), "555-0001")
        updated = self.tracker.update_patient(patient.patient_id, name="Alice Johnson")
        self.assertEqual(updated.name, "Alice Johnson")
        self.assertEqual(updated.contact_number, "555-0001")

    def test_update_patient_not_found(self):
        result = self.tracker.update_patient(999, name="Ghost")
        self.assertIsNone(result)

    def test_remove_patient(self):
        patient = self.tracker.add_patient("Alice", date(1985, 1, 1), "555-0001")
        removed = self.tracker.remove_patient(patient.patient_id)
        self.assertTrue(removed)
        self.assertIsNone(self.tracker.get_patient(patient.patient_id))

    def test_remove_patient_not_found(self):
        self.assertFalse(self.tracker.remove_patient(999))

    def test_remove_patient_also_removes_visits(self):
        patient = self.tracker.add_patient("Alice", date(1985, 1, 1), "555-0001")
        visit = self.tracker.add_visit(
            patient_id=patient.patient_id,
            visit_date=date(2025, 1, 10),
            doctor="Dr. Jones",
            reason="Checkup",
        )
        self.tracker.remove_patient(patient.patient_id)
        self.assertIsNone(self.tracker.get_visit(visit.visit_id))


class TestVisitOperations(unittest.TestCase):
    def setUp(self):
        self.tracker = MedicalVisitTracker()
        self.patient = self.tracker.add_patient(
            name="Bob Brown",
            date_of_birth=date(1978, 3, 22),
            contact_number="555-0200",
        )

    def test_add_visit_returns_visit(self):
        visit = self.tracker.add_visit(
            patient_id=self.patient.patient_id,
            visit_date=date(2025, 5, 1),
            doctor="Dr. Smith",
            reason="Annual checkup",
        )
        self.assertIsInstance(visit, MedicalVisit)
        self.assertEqual(visit.patient_id, self.patient.patient_id)
        self.assertEqual(visit.doctor, "Dr. Smith")
        self.assertEqual(visit.reason, "Annual checkup")
        self.assertIsNone(visit.diagnosis)

    def test_add_visit_with_diagnosis_and_notes(self):
        visit = self.tracker.add_visit(
            patient_id=self.patient.patient_id,
            visit_date=date(2025, 6, 15),
            doctor="Dr. Lee",
            reason="Cough",
            diagnosis="Common cold",
            notes="Rest and fluids",
        )
        self.assertEqual(visit.diagnosis, "Common cold")
        self.assertEqual(visit.notes, "Rest and fluids")

    def test_add_visit_unknown_patient(self):
        result = self.tracker.add_visit(
            patient_id=999,
            visit_date=date(2025, 1, 1),
            doctor="Dr. X",
            reason="Unknown",
        )
        self.assertIsNone(result)

    def test_get_visit(self):
        visit = self.tracker.add_visit(
            patient_id=self.patient.patient_id,
            visit_date=date(2025, 5, 1),
            doctor="Dr. Smith",
            reason="Checkup",
        )
        fetched = self.tracker.get_visit(visit.visit_id)
        self.assertEqual(fetched, visit)

    def test_get_visit_not_found(self):
        self.assertIsNone(self.tracker.get_visit(999))

    def test_get_visits_for_patient_sorted_by_date(self):
        self.tracker.add_visit(
            self.patient.patient_id, date(2025, 8, 1), "Dr. A", "Follow-up"
        )
        self.tracker.add_visit(
            self.patient.patient_id, date(2025, 3, 1), "Dr. B", "Flu"
        )
        self.tracker.add_visit(
            self.patient.patient_id, date(2025, 6, 1), "Dr. C", "Checkup"
        )
        visits = self.tracker.get_visits_for_patient(self.patient.patient_id)
        dates = [v.visit_date for v in visits]
        self.assertEqual(dates, sorted(dates))

    def test_get_visits_for_patient_empty(self):
        visits = self.tracker.get_visits_for_patient(self.patient.patient_id)
        self.assertEqual(visits, [])

    def test_get_visits_for_unknown_patient(self):
        visits = self.tracker.get_visits_for_patient(999)
        self.assertEqual(visits, [])

    def test_update_visit(self):
        visit = self.tracker.add_visit(
            self.patient.patient_id, date(2025, 5, 1), "Dr. Smith", "Checkup"
        )
        updated = self.tracker.update_visit(
            visit.visit_id, diagnosis="Healthy", notes="No issues"
        )
        self.assertEqual(updated.diagnosis, "Healthy")
        self.assertEqual(updated.notes, "No issues")
        self.assertEqual(updated.reason, "Checkup")

    def test_update_visit_not_found(self):
        result = self.tracker.update_visit(999, doctor="Dr. Ghost")
        self.assertIsNone(result)

    def test_remove_visit(self):
        visit = self.tracker.add_visit(
            self.patient.patient_id, date(2025, 5, 1), "Dr. Smith", "Checkup"
        )
        removed = self.tracker.remove_visit(visit.visit_id)
        self.assertTrue(removed)
        self.assertIsNone(self.tracker.get_visit(visit.visit_id))

    def test_remove_visit_not_found(self):
        self.assertFalse(self.tracker.remove_visit(999))

    def test_list_visits_sorted_by_date(self):
        p2 = self.tracker.add_patient("Carol", date(2000, 1, 1), "555-0300")
        self.tracker.add_visit(
            self.patient.patient_id, date(2025, 9, 1), "Dr. A", "Flu"
        )
        self.tracker.add_visit(p2.patient_id, date(2025, 4, 1), "Dr. B", "Checkup")
        self.tracker.add_visit(
            self.patient.patient_id, date(2025, 7, 1), "Dr. C", "Follow-up"
        )
        visits = self.tracker.list_visits()
        dates = [v.visit_date for v in visits]
        self.assertEqual(dates, sorted(dates))


if __name__ == "__main__":
    unittest.main()
