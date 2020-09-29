from formify.controls import *
from formify.layout import *
import formify
import json

def ui():
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

	def save():
		fn = formify.tools.save_dialog()
		with open(fn, "w+") as f:
			f.write(
				json.dumps(material_form.all_values, indent=4)
			)

	def load():
		fn = formify.tools.open_dialog()
		with open(fn) as f:
			material_form.all_values = json.loads(f.read())

	material_form = Form(Row(
		Col(
			Segment(
				h3("Material Properties"),
				ControlText("Name", variable_name="name"),
				ControlFloatMega("Conductivity in MS", variable_name="conductivity"),

				h3("Magnetization"),
				ConditionalForm({
					"linear": Row(ControlFloat("Relative permeability", variable_name="mur")),
					"non-linear": Row(
						table_bh,
						plot,
					),
				}, variable_name="__flatten__"),
				Row(
					ControlButton("Import", on_click=load),
					ControlButton("Export", on_click=save),
				),
			)
		)
	))

	return ListForm(
		material_form,
		value=[material_form.value],
		variable_name="material",
		display_name_callback=lambda x: x["name"])
