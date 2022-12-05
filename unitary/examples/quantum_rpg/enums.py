import enum


class HealthPoint(enum.Enum):
    """Enum representing a health point (HP).

    Each qubit in a Qaracter represents a HealthPoint.
    Measuring a HP as Healthy represents full health for that
    point, while a zero represents no health for that point
    (Hurt).
    """
    HURT = 0
    HEALTHY = 1
