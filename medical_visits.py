"""Medical visits tracking system."""

from datetime import date
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Patient:
    """Represents a patient."""

    patient_id: int
    name: str
    date_of_birth: date
    contact_number: str


@dataclass
class MedicalVisit:
    """Represents a single medical visit."""

    visit_id: int
    patient_id: int
    visit_date: date
    doctor: str
    reason: str
    diagnosis: Optional[str] = None
    notes: Optional[str] = None


class MedicalVisitTracker:
    """Manages patients and their medical visits."""

    def __init__(self):
        self._patients: dict[int, Patient] = {}
        self._visits: dict[int, MedicalVisit] = {}
        self._next_patient_id = 1
        self._next_visit_id = 1

    # --- Patient operations ---

    def add_patient(self, name: str, date_of_birth: date, contact_number: str) -> Patient:
        """Add a new patient and return the created Patient."""
        patient = Patient(
            patient_id=self._next_patient_id,
            name=name,
            date_of_birth=date_of_birth,
            contact_number=contact_number,
        )
        self._patients[patient.patient_id] = patient
        self._next_patient_id += 1
        return patient

    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Return the patient with the given ID, or None if not found."""
        return self._patients.get(patient_id)

    def list_patients(self) -> list[Patient]:
        """Return all patients."""
        return list(self._patients.values())

    def update_patient(
        self,
        patient_id: int,
        name: Optional[str] = None,
        date_of_birth: Optional[date] = None,
        contact_number: Optional[str] = None,
    ) -> Optional[Patient]:
        """Update an existing patient's information. Returns updated patient or None."""
        patient = self._patients.get(patient_id)
        if patient is None:
            return None
        if name is not None:
            patient.name = name
        if date_of_birth is not None:
            patient.date_of_birth = date_of_birth
        if contact_number is not None:
            patient.contact_number = contact_number
        return patient

    def remove_patient(self, patient_id: int) -> bool:
        """Remove a patient and all their visits. Returns True if removed."""
        if patient_id not in self._patients:
            return False
        del self._patients[patient_id]
        visits_to_remove = [
            vid for vid, v in self._visits.items() if v.patient_id == patient_id
        ]
        for vid in visits_to_remove:
            del self._visits[vid]
        return True

    # --- Visit operations ---

    def add_visit(
        self,
        patient_id: int,
        visit_date: date,
        doctor: str,
        reason: str,
        diagnosis: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[MedicalVisit]:
        """Add a visit for a patient. Returns the visit, or None if patient not found."""
        if patient_id not in self._patients:
            return None
        visit = MedicalVisit(
            visit_id=self._next_visit_id,
            patient_id=patient_id,
            visit_date=visit_date,
            doctor=doctor,
            reason=reason,
            diagnosis=diagnosis,
            notes=notes,
        )
        self._visits[visit.visit_id] = visit
        self._next_visit_id += 1
        return visit

    def get_visit(self, visit_id: int) -> Optional[MedicalVisit]:
        """Return the visit with the given ID, or None if not found."""
        return self._visits.get(visit_id)

    def get_visits_for_patient(self, patient_id: int) -> list[MedicalVisit]:
        """Return all visits for a given patient, sorted by date."""
        visits = [v for v in self._visits.values() if v.patient_id == patient_id]
        return sorted(visits, key=lambda v: v.visit_date)

    def update_visit(
        self,
        visit_id: int,
        visit_date: Optional[date] = None,
        doctor: Optional[str] = None,
        reason: Optional[str] = None,
        diagnosis: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[MedicalVisit]:
        """Update an existing visit. Returns updated visit or None if not found."""
        visit = self._visits.get(visit_id)
        if visit is None:
            return None
        if visit_date is not None:
            visit.visit_date = visit_date
        if doctor is not None:
            visit.doctor = doctor
        if reason is not None:
            visit.reason = reason
        if diagnosis is not None:
            visit.diagnosis = diagnosis
        if notes is not None:
            visit.notes = notes
        return visit

    def remove_visit(self, visit_id: int) -> bool:
        """Remove a visit by ID. Returns True if removed."""
        if visit_id not in self._visits:
            return False
        del self._visits[visit_id]
        return True

    def list_visits(self) -> list[MedicalVisit]:
        """Return all visits, sorted by date."""
        return sorted(self._visits.values(), key=lambda v: v.visit_date)
