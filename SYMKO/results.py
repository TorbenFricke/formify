from formify.controls import *
from formify.layout import *
import formify
import json

def ui():
	results = {}
	def load_results(sender, value):
		nonlocal results
		try:
			with open(value) as f:
				results = json.load(f)
			combo_x.items = combo_y.items = list(results.keys())
		except Exception as e:
			pass
		else:
			draw()

	def _draw():
		fig = plot.fig
		fig.clf()
		ax = fig.gca()

		try:
			x_labels = set()
			y_labels = set()
			for job in result_form.value:
				x = results[job["x_axis"]]
				y = results[job["y_axis"]]
				x_labels.add(job["x_axis"])
				y_labels.add(job["y_axis"])
				label = job["label"]
				ax.plot(x, y, label=label)

			ax.set_xlabel(", ".join(list(x_labels)))
			ax.set_ylabel(", ".join(list(y_labels)))
			ax.legend()
		except:
			error.show()
		else:
			error.hide()
		plot.draw()
	draw = formify.tools.BackgroundMethod(_draw, lazy=True)

	plot = ControlMatplotlib()
	combo_x = ControlCombo("x-Axis Datasource", variable_name="x_axis")
	combo_y = ControlCombo("y-Axis Datasource", variable_name="y_axis")
	result_form = ListForm(
		Form(Col(
			combo_x,
			combo_y,
			ControlText("Label", variable_name="label"),
		), on_change=draw),
		display_name_callback=lambda x: f"{x['x_axis']} - {x['y_axis']}   {x['label']}",
		variable_name="plots",
	)

	error = SegmentRed(
		h5("Error while plotting..."),
	)
	error.hide()

	return Form(Col(
		ControlFile("Results File", on_change=load_results, variable_name="results_file"),
		result_form,
		error,
		plot,
	), variable_name="results")

