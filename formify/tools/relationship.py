import warnings
from formify.controls._value_base import ValueBase
from formify.controls._events import EventDispatcher

class Relationship:
	def __init__(self, *control_and_calculation, validate_every_change=True):
		"""
		Sets up a relationship between multiple controls. Whenever a child control changes, this class ensures,
		the relationship is still satisfied. If the validaiton fails, a warning is thrown. Warnings can be
		controlled using validate_every_change.

		Important: Make sure every calculation method is dependent on all other
		values. Otherwise, the relationship will not work! If you run into this, split the relationship
		into multiple relationships.

		:param control_and_calculation: Tuples of (control, calculation_method). The
		calculation_method is called whenever another control changes to recalculate the value like this_
		>>> control.value = calculation_method()
		or rather
		>>> control_and_calculation[0].value = control_and_calculation[1]()
		The order, in which contorls are provided matters. The first control has the highest priority and
		changes last.
		:param validate_every_change: Validate the relationship checks out on every change event. Floats are
		 checked with a small tolerance. True by default.
		"""
		self.inputs = control_and_calculation
		self.validate_every_change = validate_every_change

		self.child_changed = EventDispatcher(self)
		self.child_changed.subscribe(self._child_changed)

		for control, method in control_and_calculation:
			# validate correct types
			assert isinstance(control, ValueBase)
			assert callable(method)

			# set event listeners
			control.change.subscribe(lambda sender, value: self.child_changed(sender))


	def _child_changed(self, _self, sender):
		self.ensure_relationship(sender)

	def ensure_relationship(self, fixed_control):
		with self.child_changed.suspend_updates():
			for control, calculate in reversed(self.inputs):
				# do not do anything with the fixed variable
				if control == fixed_control:
					continue
				try:
					control.value = calculate()
				except Exception as e:
					warnings.warn(f"While calculating {control.variable_name} error occourd:\n{e}")

			if self.validate_every_change:
				self.validate(fixed_control)

	def validate(self, control:ValueBase):
		def almost_equal(a, b, tolerance=1e-5):
			if type(a) == float:
				err = (abs(a) + abs(b)) / 2 * tolerance
				return a - err <= b <= a + err
			return a == b

		for _control, calculate in self.inputs:
			if _control != control:
				continue

			value = _control.value
			try:
				calculated = calculate()
			except Exception as e:
				warnings.warn(f"Error while calculating {_control.variable_name}:\n{e}")
				return

			if not almost_equal(value, calculated):
				warnings.warn(f"Value of {control.variable_name} does match calculated value:\n{value} != {calculated}")

			return
		warnings.warn(f"{control.variable_name} not found while validating relationship.")