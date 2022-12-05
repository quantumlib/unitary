from typing import Callable, Dict, List, Optional, Union
import random
from unitary import alpha
from unitary.examples.quantum_rpg import enums


class Qaracter(alpha.QuantumWorld):
    """Base class for quantum RPG characters.

  Quantum characters, or `Qaracter`s are made of
  `QuantumObject`s.  The level of a quantum character
  is equivalent to the number of `QuantumObject`s
  (not including any ancillae added for measurement post-selection).

  Qaracters have one hit point (HP) per level.  Qaracters are
  considered DOWN if they have over half their qubits measured
  as zero.  Qaracters are considered ESCAPED if they have all
  their qubits measured and at least half are measured as one.
  If neither of these is true, the Qaracter is considered to
  be ACTIVE.

  Additional HP can be added with the add_hp() function.
  Additional quantum effects can be added with the add_quantum_effects()
  function.

  Hit point values can be sampled (a random result pulled from
  the simulated distribution without measuring, which is possible
  only in simulation) with sample(hp_num, False).

  Hit point values can be measured by calling sample(hp_num, True).


  Args:
      name: name of this character as a string.
  """

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.health_status: Dict[alpha.QuantumObject, int] = {}
        self.level = 0
        self.add_hp()

    def is_npc(self) -> bool:
        """Returns Trus if a non-player or False if a player.

    Inheritors of NPCs should override this function.
    """
        return False

    def quantum_object_name(self, hp_num: int) -> str:
        """Canonical name of a QuantumObject for this Qaracter.

      Represents the n-th HP of a Qaracter.

      Args:
          hp_num: Number of the health point requested.  Health points
              start at 1 and go up to the Qaracter's level (inclusive).
      """
        return f'{self.name}_{hp_num}'

    def add_hp(self) -> alpha.QuantumObject:
        """Adds an additional Health Point (HP) to the Qaracter.

      Each HP added to the Qaracter is an additional QuantumObject
      with no effects (i.e. is a qubit with no operations).
      Adding a HP also increases the Qaracter's level.
      """
        self.level += 1
        obj = alpha.QuantumObject(self.quantum_object_name(self.level),
                                  enums.HealthPoint.HURT)
        self.add_object(obj)
        return obj

    def get_hp(self, hp_name: str) -> alpha.QuantumObject:
        """Retrieves a QuantumObject with the specified name."""
        for obj in self.objects:
            if hp_name == obj.name:
                return obj

    def active_qubits(self) -> List[str]:
        """Returns the names of all active (non-measured) quantum objects (HP)."""
        return [
            self.quantum_object_name(i)
            for i in range(1, self.level + 1)
            if self.quantum_object_name(i) not in self.health_status
        ]

    def add_quantum_effect(self, effect, quantum_name: Union[int, str]):
        """Adds a Quantum Effect to a specific quantum object."""
        if isinstance(quantum_name, int):
            quantum_name = self.quantum_object_name(quantum_name)
        hp_obj = self.get_hp(quantum_name)
        effect(hp_obj)

    @property
    def damage(self) -> int:
        """Returns the number of qubits measured to be zero."""
        return sum(status == 0 for status in self.health_status.values())

    @property
    def virtue(self) -> int:
        """Returns the number of qubits measured to be one."""
        return sum(status == 1 for status in self.health_status.values())

    def is_down(self) -> bool:
        """Returns True if over half of the HP have been measured as `HURT`."""
        return self.damage > (self.level / 2)

    def is_escaped(self) -> bool:
        """Returns True if all HP are measured and at least half are `HEALTHY`."""
        return len(
            self.health_status) == self.level and self.virtue >= (self.level / 2)

    def is_active(self) -> bool:
        """Returns True if the Qaracter is not down yet and there are HPs left to measure."""
        return not self.is_down() and len(self.health_status) < self.level

    def status_line(self) -> str:
        """Returns a one-line string summarizing the Qaracter's HP status."""
        damage = self.damage
        virtue = self.virtue
        unknown = self.level - damage - virtue
        down = ' *DOWN* ' if self.is_down() else ''
        escaped = ' *ESCAPED* ' if self.is_escaped() else ''
        return f'{self.level}QP ({virtue}|1> {damage}|0> {unknown}?){down}{escaped}'

    def sample(self, hp_name: str, save_result: bool) -> enums.HealthPoint:
        """Samples or measures a qubit representing a HP.

        Args:
            hp_name: Name of the quantum object to measure.
            save_result: If True, measures the quantum object.
                If False, sample the quantum object non-destructively.
                This takes a result from a simulated distribution without
                'measuring' the qubit.

        """
        hp_obj = self.get_hp(hp_name)
        if save_result:
            result = self.pop([hp_obj])
            self.health_status[hp_name] = result[0].value
            return result[0]
        else:
            return self.peek([hp_obj], count=1)[0][0]
