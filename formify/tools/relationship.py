import warnings
from formify.controls._mixins import ValueMixin
from formify.controls._events import EventDispatcher

class Relationship:
	def __init__(self, *control_and_calculation, validate_every_change=True):
		"""
		Sets up a relationship between multiple controls. Whenever a child control changes, this class ensures,
		the relationship is still satisfied. If the validaiton fails, a warning is thrown. Warnings can be
		controlled using validate_every_change.

		:param control_and_calculation: A maximum of 3 tuples of (control, calculation_method). The
		calculation_method is called whenever another control changes to recalculate the value like this_
		>>> control.value = calculation_method()
		or rather
		>>> control_and_calculation[0].value = control_and_calculation[1]()
		:param validate_every_change: Validate the relationship checks out on every change event. Floats are
		 checked with a small tolerance. True by default.
		"""
		self.inputs = control_and_calculation
		self.validate_every_change = validate_every_change

		self.child_changed = EventDispatcher(self)
		self.child_changed.subscribe(self._child_changed)

		for control, method in control_and_calculation:
			# validate correct types
			assert isinstance(control, ValueMixin)
			assert callable(method)

			# set event listeners
			control.change.subscribe(lambda sender, value: self.child_changed(sender))

		if len(control_and_calculation) > 3:
			raise ValueError("Relationships between more than 3 Controls are not supported. "
			                 "To fix this, split up your relationship into multiple relationships")


	def _child_changed(self, _self, sender):
		self.ensure_relationship(sender.variable_name)

	def ensure_relationship(self, fixed_variable):
		with self.child_changed.suspend_updates():
			for control, calculate in reversed(self.inputs):
				# do not do anything with the fixed variable
				if control.variable_name == fixed_variable:
					print(fixed_variable)
					continue
				control.value = calculate()

			if self.validate_every_change:
				self.validate(fixed_variable)

	def validate(self, variable):
		def almost_equal(a, b, tolerance=1e-5):
			if type(a) == float:
				err = (abs(a) + abs(b)) / 2 * tolerance
				return a - err <= b <= a + err
			return a == b

		for control, calculate in self.inputs:
			if control.variable_name != variable:
				continue

			value = control.value
			calculated = calculate()
			if not almost_equal(value, calculated):
				warnings.warn(f"Value of {variable} does match calculated value:\n{value} != {calculated}")

			return
		warnings.warn(f"{variable} not found while validating relationship.")