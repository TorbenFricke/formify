from formify.layout import *
from formify.controls import *
import formify
from helpers import ControlComboList, ControlTextList, ControlFileList


class ValueProxy:
	def __init__(self, control):
		self.control = control
		self.change = control.change
		self.variable_name = control.variable_name

	@property
	def value(self):
		return self.control.value[0]

	@value.setter
	def value(self, value):
		self.control.value = [value]

def ui():
	machine = ControlComboList(
		"Machine Type",
		items=["ESM", "PMSM"],
		variable_name="typeMachine",
	)
	machine_proxy = ValueProxy(machine)

	return Form(Col(
		ControlTextList("Model Name", variable_name="modelName"),
		ControlFileList("File Path", variable_name="path"),
		Row(
			machine,
			ConditionalForm({
				"ESM": ControlCombo(
					"Rotor Type",
					items=[(0, "Salient Pole"), (1, "Turbo")],
					variable_name="typeRotor"),
				"PMSM": ControlCombo(
					"Rotor Type",
					items=[(0, "V-PMSM"), (1, "Bar-PMSM"), (1, "Secret-PMSM")],
					variable_name="typeRotor"),
			}, condition_control=machine_proxy, variable_name="__flatten__"),
		),
		SegmentAlt(
			ConditionalForm({
				"ESM": Col(
					h4("Excitation"),
					ControlFloat("Field Winding Current in A", variable_name="Ifd")
				),
				"PMSM":Col(
					h4("Magnets"),
					ListForm(
						Form(Col(
							ControlText("Label", variable_name="label"),
							ControlFloatMilli("Width in mm", variable_name="width"),
							ControlFloatMilli("Height in mm", variable_name="height"),
							ControlFloatMilli("Temperature in °C", variable_name="temperature"),
						)),
						display_name_callback=lambda x: x["label"],
						variable_name="magnets")
				),
			}, condition_control=machine_proxy, variable_name="__flatten__"),
		),

		SegmentAlt(
			h4("Stator Current"),
			Row(
				ControlFloat("d-axis Current in A", variable_name="Id"),
				ControlFloat("q-axis Current in A", variable_name="Iq"),
			),
		),

		SegmentAlt(
			h4("Calculation Settings"),
			ControlCheckbox("Save Airgap Data", variable_name="saveAirgapData"),
			ControlCheckbox("Allow Movestep Reduction", variable_name="allowMovestepReduction"),
			ControlCheckbox("Create Fluxdensity Plot", variable_name="createFluxdensityPlot"),
			ControlCombo(
				"Calculation Routine Type",
				items=[(0, "Default"), (1, "Advanced")],
				variable_name="typeRoutine"),
			Row(
				ControlInt("Number of Movesteps", variable_name="movesteps"),
				ControlInt("Number of Skewsteps", variable_name="skewsteps"),
			)
		),
	), variable_name="singleload")