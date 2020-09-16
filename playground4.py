from formify.controls import *
from formify.layout import *
import formify

table_bh = ControlTable(
	label="B(H)-Curve",
	columns=["H in A/m", "B in T"],
	column_types=[float, float],
	variable_name="bh"
)
plot = ControlMatplotlib()

def _draw_bh():
	fig = plot.fig
	fig.clf()
	ax = fig.gca()

	import numpy as np
	bh = np.array(table_bh.value).T
	ax.plot(bh[0], bh[1])

	plot.draw()

draw_bh = formify.tools.BackgroundMethod(_draw_bh)
table_bh.change.subscribe(draw_bh)

material_form = Form(Row(
	Col(
		Segment(
			h3("General Properties"),
			ControlText("Name", variable_name="name"),
			Row(
				ControlFloatMega("Conductivity in MS", variable_name="conductivity"),
				ControlFloat("Temperature in °C", variable_name="temperature"),
			),

			h3("Magnetization"),
			ConditionalForm({
				"linear": ControlFloat("Relative permeability", variable_name="mur"),
				"non-linear": Row(
					table_bh,
					plot,
				),
			}, variable_name="__flatten__"),
		)
	)
), variable_name="material")

material_form.change.subscribe(lambda : print(material_form.all_values))

import math
voltage = ControlFloat("Verkettete Spannung in V", variable_name="phase_voltage")
voltage_str = ControlFloat("Strangspannung in V")
formify.tools.Relationship(
	(voltage, lambda : voltage_str.value * math.sqrt(3)),
	(voltage_str, lambda : voltage.value / math.sqrt(3))
)

sidebar = SidebarContentView({
	"General": Row(voltage, voltage_str),
	"Material": material_form,
})

formify.MainWindow(sidebar)