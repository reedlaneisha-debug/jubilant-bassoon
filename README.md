# jubilant-bassoon

## Medical Visits Tracking System

A Python module for managing patients and their medical visit records.

### Features

- **Patient management** – add, retrieve, update, and remove patient records.
- **Visit management** – record medical visits (date, doctor, reason, diagnosis, notes) linked to patients.
- **Cascade delete** – removing a patient automatically removes all of their visits.
- **Sorted results** – visits are always returned in chronological order.

### Usage

```python
from datetime import date
from medical_visits import MedicalVisitTracker

tracker = MedicalVisitTracker()

# Add a patient
patient = tracker.add_patient(
    name="Alice Smith",
    date_of_birth=date(1985, 6, 15),
    contact_number="555-0100",
)

# Record a visit
visit = tracker.add_visit(
    patient_id=patient.patient_id,
    visit_date=date(2025, 3, 10),
    doctor="Dr. Jones",
    reason="Annual checkup",
    diagnosis="Healthy",
    notes="No issues found",
)

# Retrieve all visits for a patient
visits = tracker.get_visits_for_patient(patient.patient_id)
```

### Running the tests

```bash
python -m unittest test_medical_visits -v
```
